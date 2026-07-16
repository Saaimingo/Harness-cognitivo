---
tipo: plano
titulo: "FI-2B — Plano Revisado: Execução, Revisão, Testes, Gates, Release, Incidentes"
status: rascunho
data: 2026-07-15
fase: FI-2B
eixo: ESQ + SG-0 + GRN + CTP
---

# 📋 FI-2B — Plano Revisado

> *Extensão do domínio com ExecutionRun, Review, TestRun, GateDecision, Release e Incident.*

---

## 1. Visão Geral

A FI-2B completa o domínio de execução e governança do Harness. Enquanto a FI-2A definiu as entidades de planejamento e autorização (Project, Task, WorkOrder, Plan, Requirement), a FI-2B define as entidades de **execução verificada** e **decisão de gate**.

### 1.1 Escopo

| Entidade | Responsabilidade |
|----------|-----------------|
| **ExecutionRun** | Tentativa concreta de cumprir uma WorkOrder |
| **Review** | Avaliação estruturada do resultado de uma ExecutionRun |
| **TestRun** | Execução de testes e registro de evidências |
| **GateDecision** | Decisão formal sobre avanço, rework ou bloqueio |
| **Release** | Versão preparada ou implantada |
| **Incident** | Falha operacional que exige investigação |

### 1.2 Relação com FI-2A

```
FI-2A: Project → Plan → Task → WorkOrder
                               ↓
FI-2B:                    ExecutionRun → Review → TestRun
                               ↓
                      GateDecision → Release / Incident
```

---

## 2. Entidade: ExecutionRun

### 2.1 Responsabilidade

Registrar cada tentativa concreta de cumprir uma WorkOrder. Uma WorkOrder pode ter múltiplas ExecutionRuns (rework).

### 2.2 Estados

```
INITIATED → RUNNING → COMPLETED / FAILED / ABANDONED
```

| Estado | Descrição |
|--------|-----------|
| `initiated` | Execução criada, aguardando início |
| `running` | Execução em andamento |
| `completed` | Execução finalizada com sucesso |
| `failed` | Execução finalizada com falha |
| `abandoned` | Execução abandonada pelo executor |

### 2.3 Invariantes

1. ExecutionRun deve estar vinculada a uma WorkOrder em estado `AUTHORIZED` ou `DISPATCHED`
2. Transição para `completed` requer changeset identificado
3. Transição para `failed` requer erro registrado
4. `started_at` deve ser preenchido ao transicionar para `running`
5. `completed_at` ou `failed_at` deve ser preenchido ao transicionar para estado final
6. Timezone obrigatório em todos os campos temporais

### 2.4 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `initiated` | `running`, `abandoned` |
| `running` | `completed`, `failed`, `abandoned` |
| `completed` | (terminal) |
| `failed` | (terminal) |
| `abandoned` | (terminal) |

### 2.5 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `InvariantViolationError` | changeset obrigatório não fornecido |
| `MissingAuthorityError` | WorkOrder não autorizada |

### 2.6 Políticas

- ExecutionRun só pode ser iniciada se WorkOrder estiver em estado executável
- ExecutionRun só pode ser completada se changeset foi identificado
- ExecutionRun só pode ser abandonada com justificativa

### 2.7 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Verificar autoridade antes de iniciar; registrar todas as ações |
| **ESQ** | changeset deve ser rastreável; código deve ser testável |
| **GRN** | Execução deve respeitar regras de negócio identificadas |
| **CTP** | ExecutionRun herda contexto do pacote de promoção via WorkOrder |

### 2.8 Testes Necessários

- Transições permitidas e rejeitadas
- Idempotência
- Imutabilidade
- Vinculação com WorkOrder
- Preenchimento de timestamps
- Timezone obrigatório

### 2.9 Riscos

- Complexidade de estado pode crescer com múltiplas tentativas
- Necessidade de rastrear qual ExecutionRun produziu qual changeset

### 2.10 Critérios de Aceite

- [ ] 100% das transições testadas
- [ ] Invariantes verificadas por testes
- [ ] Sem imports proibidos
- [ ] Timezone obrigatório em todos os campos

---

## 3. Entidade: Review

### 3.1 Responsabilidade

Avaliação estruturada do resultado de uma ExecutionRun. Suporta múltiplos tipos de revisão.

### 3.2 Tipos de Review

| Tipo | Descrição | Responsável |
|------|-----------|-------------|
| `functional` | Verifica se o pedido foi atendido | Revisor Funcional |
| `domain` | Verifica conformidade com regras de negócio | Revisor de Domínio |
| `structural` | Verifica qualidade estrutural do código | Engenheiro de Software |
| `security` | Verifica conformidade com SG-0 | Revisor de Segurança |

### 3.3 Estados

```
REQUESTED → IN_PROGRESS → APPROVED / REJECTED / CHANGE_REQUESTED
```

### 3.4 Invariantes

1. Review deve estar vinculado a uma ExecutionRun
2. Cada tipo de Review é independente (pode ser aprovado/rejeitado separadamente)
3. Transição para `approved` requer justificativa
4. Transição para `rejected` requer justificativa e lista de finding
5. Transição para `change_requested` requer descrição das mudanças necessárias

### 3.5 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `requested` | `in_progress`, `cancelled` |
| `in_progress` | `approved`, `rejected`, `change_requested` |
| `approved` | (terminal) |
| `rejected` | (terminal) |
| `change_requested` | (terminal — nova ExecutionRun necessária) |

### 3.6 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `InvariantViolationError` | justificativa obrigatória não fornecida |
| `MissingEvidenceError` | Evidência de revisão não fornecida |

### 3.7 Políticas

- Review funcional deve ser aprovado antes de GateDecision
- Review de domínio deve ser aprovado se houver regras de negócio afetadas
- Review structural deve ser aprovado se houver mudanças de código
- Review de segurança deve ser aprovado se houver ações de risco

### 3.8 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Review de segurança é obrigatório para ações de risco |
| **ESQ** | Review structural verifica conformidade com constituição |
| **GRN** | Review de domínio verifica conformidade com regras |
| **CTP** | Reviews herdam contexto do pacote de promoção |

### 3.9 Testes Necessários

- Transições por tipo de review
- Independência entre tipos
- Justificativa obrigatória
- Idempotência e imutabilidade

### 3.10 Riscos

- Múltiplos tipos de review podem criar complexidade de orquestração
- Necessidade de definir quais reviews são obrigatórios em cada contexto

### 3.11 Critérios de Aceite

- [ ] Todos os tipos de review implementados
- [ ] Transições testadas por tipo
- [ ] Independência entre tipos verificada
- [ ] Relação com SG-0, ESQ, GRN documentada

---

## 4. Entidade: TestRun

### 4.1 Responsabilidade

Registro de execução de testes e suas evidências.

### 4.2 Estados

```
PLANNED → EXECUTING → PASSED / FAILED / ERROR
```

### 4.3 Invariantes

1. TestRun deve estar vinculado a uma ExecutionRun
2. Transição para `passed` requer contagem de testes
3. Transição para `failed` requer lista de falhas
4. Transição para `error` requer mensagem de erro
5. Evidências devem ser preservadas (hashes)

### 4.4 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `planned` | `executing`, `cancelled` |
| `executing` | `passed`, `failed`, `error` |
| `passed` | (terminal) |
| `failed` | (terminal) |
| `error` | (terminal) |

### 4.5 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `MissingEvidenceError` | Evidências não fornecidas |

### 4.6 Políticas

- TestRun deve ser executado antes de GateDecision
- Resultado deve ser registrado com evidências
- Testes não devem ser enfraquecidos para obter aprovação

### 4.7 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Testes devem ser executados em ambiente seguro |
| **ESQ** | Testes arquiteturais devem ser incluídos |
| **GRN** | Testes de regra de negócio devem ser incluídos |
| **CTP** | Testes herdam contexto do pacote de promoção |

### 4.8 Testes Necessários

- Transições
- Registro de evidências
- Contagem de testes
- Idempotência e imutabilidade

### 4.9 Riscos

- Volume de evidências pode crescer rapidamente
- Necessidade de armazenamento eficiente

### 4.10 Critérios de Aceite

- [ ] Transições implementadas e testadas
- [ ] Evidências preservadas com hashes
- [ ] Relação com ExecutionRun verificada

---

## 5. Entidade: GateDecision

### 5.1 Responsabilidade

Decisão formal sobre se o trabalho pode avançar, precisa de rework, ou está bloqueado.

### 5.2 Estados do Processo (GateStatus)

```
PENDING → EVALUATING → DECIDED / CANCELLED
```

### 5.3 Tipos de Decisão (GateDecisionType)

| Decisão | Descrição |
|---------|-----------|
| `advance` | Trabalho pode avançar |
| `rework` | Trabalho precisa de retrabalho |
| `blocked` | Trabalho está bloqueado |
| `rejected` | Trabalho foi rejeitado |
| `awaiting_human` | Aguardando decisão humana |
| `waived` | Requisitos do gate foram dispensados |

### 5.4 Invariantes

1. GateDecision deve estar vinculado a uma ExecutionRun ou Task
2. Decisão requer autoridade
3. Decisão requer justificativa
4. Evidências devem ser agregadas
5. `waived` requer justificativa adicional e escopo da dispensa
6. `advance` requer que todos os reviews obrigatórios estejam aprovados

### 5.5 Transições (Processo)

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `pending` | `evaluating`, `cancelled` |
| `evaluating` | `decided`, `cancelled` |
| `decided` | (terminal) |
| `cancelled` | (terminal) |

### 5.6 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `InvariantViolationError` | Reviews obrigatórios não aprovados |
| `MissingAuthorityError` | Autoridade não fornecida |
| `MissingEvidenceError` | Evidências não agregadas |

### 5.7 Políticas

- `advance` requer: reviews obrigatórios aprovados, testes passando, evidências agregadas
- `waived` requer: autoridade, justificativa, escopo
- `rework` requer: justificativa e lista de mudanças necessárias
- `blocked` requer: justificativa e identificação do bloqueio

### 5.8 Evidências Agregadas

GateDecision deve agregar:
- ExecutionRun(s) relacionada(s)
- Review(s) com resultado
- TestRun(s) com resultado
- Evidências de conformidade SG-0
- Evidências de conformidade ESQ
- Evidências de conformidade GRN

### 5.9 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Gate verifica conformidade de segurança antes de advance |
| **ESQ** | Gate verifica qualidade estrutural antes de advance |
| **GRN** | Gate verifica conformidade com regras antes de advance |
| **CTP** | Gate herda contexto do pacote de promoção |

### 5.10 Testes Necessários

- Transições do processo
- Validação por tipo de decisão
- Agregação de evidências
- Verificação de reviews obrigatórios
- Idempotência e imutabilidade

### 5.11 Riscos

- Complexidade de agregação de evidências
- Necessidade de definir quais reviews são obrigatórios por contexto
- Overhead de verificação pode ser significativo

### 5.12 Critérios de Aceite

- [ ] Processo de gate implementado
- [ ] Todos os tipos de decisão suportados
- [ ] Agregação de evidências funcional
- [ ] Verificação de reviews obrigatórios
- [ ] Relação com SG-0, ESQ, GRN verificada

---

## 6. Entidade: Release

### 6.1 Responsabilidade

Versão preparada ou implantada do trabalho.

### 6.2 Estados

```
DRAFT → CANDIDATE → VALIDATING → APPROVED → DEPLOYING → DEPLOYED → VERIFYING → HEALTHY
                                  ↓                                    ↓
                             FAILED ←────────────────────────── DEGRADED
                                  ↓
                            ROLLING_BACK → ROLLED_BACK
                                  ↓
                            SUPERSEDED / RETIRED
```

### 6.3 Invariantes

1. Release deve ser criada a partir de uma GateDecision com `advance`
2. Transição para `deployed` requer evidência de implantação
3. Transição para `healthy` requer verificação pós-implantação
4. Transição para `failed` ou `degraded` requer evidência de falha
5. Rollback requer autoridade

### 6.4 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `draft` | `candidate`, `cancelled` |
| `candidate` | `validating`, `cancelled` |
| `validating` | `approved`, `failed` |
| `approved` | `deploying` |
| `deploying` | `deployed`, `failed` |
| `deployed` | `verifying`, `failed`, `degraded` |
| `verifying` | `healthy`, `degraded` |
| `healthy` | `superseded`, `retired` |
| `degraded` | `rolling_back`, `fixing` |
| `failed` | `rolling_back` |
| `rolling_back` | `rolled_back` |
| `rolled_back` | (terminal) |
| `superseded` | (terminal) |
| `retired` | (terminal) |

### 6.5 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `InvariantViolationError` | GateDecision não é `advance` |
| `MissingEvidenceError` | Evidência de implantação não fornecida |
| `MissingAuthorityError` | Rollback sem autoridade |

### 6.6 Políticas

- Release requer GateDecision com `advance`
- Deploy requer evidência
- Rollback requer autoridade e justificativa
- Verificação pós-implantação é obrigatória

### 6.7 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Deploy requer verificação de segurança; rollback é ação destrutiva |
| **ESQ** | Release deve passar por todos os gates de qualidade |
| **GRN** | Release deve conformar com regras de negócio |
| **CTP** | Release herda linhagem do pacote de promoção |

### 6.8 Testes Necessários

- Transições completas
- Verificação de pré-condições
- Rollback
- Idempotência e imutabilidade

### 6.9 Riscos

- Estados degradados podem ser complexos
- Necessidade de integração com infraestrutura de deploy

### 6.10 Critérios de Aceite

- [ ] Máquina de estados completa
- [ ] Verificação de pré-condições
- [ ] Rollback funcional
- [ ] Relação com SG-0 verificada

---

## 7. Entidade: Incident

### 7.1 Responsabilidade

Registro e gestão de falhas operacionais.

### 7.2 Estados

```
DETECTED → TRIAGED → INVESTIGATING → MITIGATING → CONTAINED → REPRODUCED → FIXING → VALIDATING_FIX → RESOLVED → MONITORING → CLOSED
    ↓                                                                                                              ↓
REOPENED ←────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Invariantes

1. Incident deve ter causa registrada antes de `resolved`
2. Incident deve ter ação corretiva antes de `closed`
3. Incident deve ter evidência de teste de regressão antes de `closed`
4. Transição para `reopened` requer justificativa
5. `maintenance_type` deve ser classificado

### 7.4 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `detected` | `triaged` |
| `triaged` | `investigating` |
| `investigating` | `mitigating`, `contained` |
| `mitigating` | `contained` |
| `contained` | `reproduced`, `fixing` |
| `reproduced` | `fixing` |
| `fixing` | `validating_fix` |
| `validating_fix` | `resolved`, `fixing` |
| `resolved` | `monitoring` |
| `monitoring` | `closed`, `reopened` |
| `closed` | `reopened` |
| `reopened` | `investigating` |

### 7.5 Erros

| Exceção | Quando |
|---------|--------|
| `InvalidTransitionError` | Transição inválida |
| `InvariantViolationError` | Causa ou ação corretiva não registrada |
| `MissingEvidenceError` | Evidência de regressão não fornecida |

### 7.6 Políticas

- Causa registrada antes de `resolved`
- Ação corretiva antes de `closed`
- Evidência de regressão antes de `closed`
- `incident_can_become_closed` política pura (FI-2A)

### 7.7 Relação com Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | Incident pode ser causado por violação de segurança |
| **ESQ** | Incident pode ser causado por dívida técnica |
| **GRN** | Incident pode ser causado por violação de regra |
| **CTP** | Incident pode ter origem em conversa promovida |

### 7.8 Testes Necessários

- Transições completas
- Verificação de invariantes
- Políticas de encerramento
- Classificação de manutenção
- Idempotência e imutabilidade

### 7.9 Riscos

- Número de estados pode tornar fluxo complexo
- Necessidade de integração com sistemas de monitoramento

### 7.10 Critérios de Aceite

- [ ] Máquina de estados completa
- [ ] Políticas de encerramento testadas
- [ ] Classificação de manutenção funcional
- [ ] Relação com eixos documentada

---

## 8. Avaliação: Introduções Necessárias na FI-2B

### 8.1 Tipos de Review

**Decisão:** Sim, introduzir.

| Tipo | Obrigatório Quando |
|------|-------------------|
| `functional` | Sempre |
| `domain` | Quando houver regras de negócio afetadas |
| `structural` | Quando houver mudanças de código |
| `security` | Quando houver ações de risco (SG-0) |

### 8.2 Múltiplas Decisões de Gate

**Decisão:** Sim, suportar. Um gate pode ter múltiplas decisões sequenciais (ex: avanço parcial).

### 8.3 Agregação de Evidências

**Decisão:** Sim, obrigatória. GateDecision deve agregar evidências de todas as fontes.

### 8.4 Registro de Dívida Técnica

**Decisão:** Sim, opcional. ExecutionRun pode registrar dívida técnica identificada.

### 8.5 Bloqueios por Regra de Negócio

**Decisão:** Sim, via GRN. GateDecision deve verificar conformidade com regras.

### 8.6 Bloqueios por Qualidade Estrutural

**Decisão:** Sim, via ESQ. GateDecision deve verificar qualidade estrutural.

---

## 9. Ordem de Implementação Recomendada

| Ordem | Entidade | Justificativa |
|-------|----------|---------------|
| 1 | ExecutionRun | Base para todas as outras |
| 2 | TestRun | Necessário para GateDecision |
| 3 | Review | Necessário para GateDecision |
| 4 | GateDecision | Consolida ExecutionRun + Review + TestRun |
| 5 | Release | Depende de GateDecision |
| 6 | Incident | Independente, mas integra com Release |

---

## 10. Estimativa de Testes

| Entidade | Testes Estimados |
|----------|-----------------|
| ExecutionRun | ~25 |
| Review | ~30 (4 tipos) |
| TestRun | ~20 |
| GateDecision | ~35 |
| Release | ~30 |
| Incident | ~25 |
| **Total** | **~165** |

---

## 11. Checklist de Pré-Implementação

- [ ] FI-2A aprovada e consolidada
- [ ] SG-0 documentado e integrado
- [ ] ESQ documentado e integrado
- [ ] GRN documentado e integrado
- [ ] CTP documentado e integrado
- [ ] Mapa arquitetural atualizado
- [ ] Este plano revisado aprovado

---

> *Este plano é vivo e deve ser refinado antes da implementação.*
