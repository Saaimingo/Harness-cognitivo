---
tipo: governança
titulo: "GRN — Governança de Regras de Negócio"
status: ativo
data: 2026-07-15
eixo: GRN
---

# 📋 GRN — Governança de Regras de Negócio

> *"O Harness deve conseguir identificar, formalizar, preservar, recuperar, versionar e fiscalizar as regras específicas de cada projeto."*

---

## 1. Objetivo

Garantir que o Harness possa:
- Identificar regras explícitas e implícitas
- Formalizar cada regra com metadados completos
- Preservar regras ao longo do tempo
- Recuperar regras por contexto
- Versionar alterações em regras
- Fiscalizar conformidade antes de gates e releases

---

## 2. Taxonomia de Conceitos

### 2.1 Distinguir Claramente

| Conceito | Definição | Exemplo |
|----------|-----------|---------|
| **Objetivo de Negócio** | Resultado desejado pelo negócio | "Lançar o produto no mercado X" |
| **Processo de Negócio** | Sequência de atividades que entrega valor | "Onboarding de novo cliente" |
| **Regra de Negócio** | Restrição ou política que governa comportamento | "Cliente deve ter CPF válido" |
| **Requisito** | Comportamento, restrição ou qualidade verificável | "Sistema deve responder em < 2s" |
| **Decisão Técnica** | Escolha de implementação | "Usar PostgreSQL como banco" |
| **Diretriz de Engenharia** | Padrão ou convenção técnica | "Todo código deve ter testes" |
| **Regra de Interface** | Restrição de UX/UI | "Botão de confirmação deve ser vermelho" |

### 2.2 Hierarquia

```
Objetivo de Negócio
  └── Processo de Negócio
        └── Regra de Negócio
              └── Requisito
                    └── Decisão Técnica
                          └── Código + Testes
```

---

## 3. Modelo Conceitual de Regra de Negócio

### 3.1 Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `rule_id` | str | ID estável (formato: `rul_xxx`) |
| `name` | str | Nome curto e descritivo |
| `description` | str | Descrição completa da regra |
| `origin` | str | De onde a regra veio (usuário, documento, lei) |
| `justification` | str | Por que esta regra existe |
| `scope` | str | Onde a regra se aplica |
| `actors` | list[str] | Quem é afetado pela regra |
| `affected_entities` | list[str] | Entidades do sistema afetadas |
| `conditions` | list[str] | Conções que ativam a regra |
| `expected_result` | str | O que deve acontecer quando a regra é atendida |
| `exceptions` | list[str] | Exceções conhecidas |
| `priority` | str | criticidade: critical, high, medium, low |
| `valid_from` | datetime | Data de vigência início |
| `valid_until` | datetime \| None | Data de vigência fim (None = indefinido) |
| `version` | int | Versão da regra |
| `responsible_authority` | str | Quem é responsável pela regra |
| `status` | str | active, deprecated, superseded |

### 3.2 Campos Opcionais (rastreabilidade)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `related_requirements` | list[str] | IDs de requisitos relacionados |
| `related_code` | list[str] | Caminhos de arquivos de código |
| `related_tests` | list[str] | Caminhos de arquivos de teste |
| `related_evidence` | list[str] | IDs de evidências |
| `change_history` | list[dict] | Histórico de alterações |

---

## 4. Regras de Governo

### 4.1 Identificação

- Toda regra deve ter um ID estável
- Regras implícitas devem ser tornadas explícitas
- Regras devem ser classificadas por tipo e prioridade

### 4.2 Preservação

- Regras aprovadas não podem ser alteradas silenciosamente
- Alterações requerem nova versão
- Versão anterior deve ser preservada

### 4.3 Recuperação

- Regras devem ser recuperáveis por: projeto, entidade, requisito, código, teste
- Cápsula de contexto deve incluir regras aplicáveis

### 4.4 Versionamento

- Cada alteração gera nova versão
- Histórico completo preservado
- Regras deprecadas mantidas para referência

### 4.5 Fiscalização

- Gates devem verificar conformidade com regras aplicáveis
- Alterações silenciosas são impedidas
- Conflitos entre regras devem ser detectados

---

## 5. Papéis Futuros

### 5.1 Analista de Negócio

| Responsabilidade | Descrição |
|------------------|-----------|
| Identificar regras | Descobrir regras explícitas e implícitas |
| Documentar regras | Formalizar com modelo completo |
| Validar com usuário | Confirmar interpretação |

### 5.2 Arquiteto de Domínio

| Responsabilidade | Descrição |
|------------------|-----------|
| Estruturar domínio | Mapear entidades e relações |
| Definir invariantes | Identificar regras que não podem ser violadas |
| Validar coerência | Garantir que regras são internamente consistentes |

### 5.3 Guardião de Regras de Negócio

| Responsabilidade | Descrição |
|------------------|-----------|
| Manter catálogo | Garantir que todas as regras estão registradas |
| Detectar conflitos | Identificar regras que se contradizem |
| Controlar versões | Gerenciar alterações em regras |
| Analisar impacto | Avaliar efeito de mudanças |
| Verificar conformidade | Checar antes de gates e releases |

---

## 6. Integração com Domínio

### 6.1 Regras → Entidades

Cada regra de negócio deve ser rastreável até:
- Entidades do domínio afetadas
- Políticas que a implementam
- Estados onde ela se aplica

### 6.2 Regras → Código

Cada regra deve ser rastreável até:
- Funções/métodos que a implementam
- Enums que a definem
- Exceções que a protegem

### 6.3 Regras → Testes

Cada regra deve ser rastreável até:
- Testes que a validam
- Testes que verificam exceções
- Testes de invariantes

---

## 7. Cápsula de Contexto e Regras

Quando um agente recebe contexto para executar uma tarefa, a cápsula deve incluir:

1. **Regras aplicáveis** à tarefa atual
2. **Invariantes** que devem ser preservados
3. **Exceções** conhecidas
4. **Conflitos** pendentes de resolução

---

## 8. Detecção de Conflitos

### 8.1 Tipos de Conflito

| Tipo | Descrição | Ação |
|------|-----------|------|
| **Direto** | Duas regras se contradizem | Escalar para resolução |
| **Temporal** | Regras com períodos sobrepostos | Verificar precedência |
| **Escopo** | Regras com escopos sobrepostos | Definir prioridade |
| **Prioridade** | Regras de mesma prioridade conflitantes | Escalar para resolução |

### 8.2 Processo de Resolução

1. Identificar conflito
2. Registrar ambas as regras
3. Escalar para autoridade competente
4. Registrar decisão e justificativa
5. Atualizar regras conforme necessário

---

## 9. Estado de uma Regra

```
draft → active → deprecated
                    ↓
              superseded (por nova versão)
```

### 9.1 Transições

| Estado Atual | Próximos Válidos |
|--------------|------------------|
| `draft` | `active`, `deprecated` |
| `active` | `deprecated`, `superseded` |
| `deprecated` | (terminal) |
| `superseded` | (terminal) |

---

## 10. Escopo de Implementação Futura

### FI-2B (parcial)
- Definir contratos de regras de negócio
- Integrar com GateDecision (verificação de conformidade)

### FI-3+
- Catálogo persistente de regras
- Versionamento completo
- Detecção automática de conflitos

### FI-5+
- Inserção de regras aplicáveis na cápsula de contexto
- Recuperação por contexto

### FI-11+
- Distribuição de regras aos agentes
- Verificação automática antes de execução

---

## 11. Relação com Outros Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | GRN protege regras contra alteração não autorizada |
| **ESQ** | GRN garante que regras são implementadas com qualidade |
| **CTP** | GRN extrai regras do documento de promoção |

---

> *Este documento é vivo e deve ser refinado a cada nova fase do projeto.*
