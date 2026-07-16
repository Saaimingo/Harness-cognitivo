---
tipo: arquitetura
titulo: "Mapa Arquitetural Integrado — Harness Cognitivo"
status: ativo
data: 2026-07-15
---

# 🗺️ Mapa Arquitetural Integrado

> *Fluxo completo do Harness Cognitivo, desde a concepção até a entrega.*

---

## 1. Fluxo Integrado de 14 Passos

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USUÁRIO (Saimon)                             │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  1. CONVERSA LIVRE                                                   │
│     Usuário desenvolve ideia no chat                                 │
│     [CTP]                                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  2. PROMOÇÃO CTP                                                     │
│     Conversa → Documentação final → Aprovação → Snapshot → Pacote   │
│     [CTP]                                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  3. GOVERNANÇA DE REGRAS (GRN)                                       │
│     Identificar objetivos, processos e regras de negócio            │
│     Extrair regras do documento aprovado                            │
│     [GRN]                                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. ARQUITETURA DE DOMÍNIO                                           │
│     Arquiteto de Domínio estrutura entidades e relações             │
│     Define invariantes e transições                                  │
│     [GRN + ESQ]                                                      │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  5. PADRÕES DE ENGENHARIA (ESQ)                                      │
│     Engenheiro de Software define padrões e restrições              │
│     Estabelece identidade de código                                 │
│     [ESQ]                                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  6. PLANEJAMENTO                                                     │
│     Planejador cria plano decomposto em tarefas                     │
│     [FI-2]                                                           │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  7. AUTORIZAÇÃO (WorkOrder)                                          │
│     WorkOrders autorizam execução específica                        │
│     Autoridade registrada                                           │
│     [FI-2A]                                                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  8. EXECUÇÃO                                                         │
│     Executor implementa o trabalho                                  │
│     ExecutionRun registra tentativa                                 │
│     [FI-2B]                                                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  9. REVISÃO FUNCIONAL                                                │
│     Revisor funcional verifica se o pedido foi atendido             │
│     [FI-2B]                                                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  10. REVISÃO DE DOMÍNIO                                              │
│      Revisor de domínio verifica regras de negócio                  │
│      [FI-2B + GRN]                                                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  11. VERIFICAÇÃO DE QUALIDADE (Engenheiro de Software)               │
│      Verifica qualidade estrutural, acoplamento, duplicação         │
│      [FI-2B + ESQ]                                                   │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  12. TESTES E EVIDÊNCIAS                                             │
│      Testador produz provas objetivas                                │
│      TestRun registra execução e resultados                         │
│      [FI-2B]                                                         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  13. VERIFICAÇÃO DE SEGURANÇA (SG-0)                                 │
│      Verifica autoridade, escopo, ausência de ações destrutivas     │
│      [SG-0]                                                          │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  14. GATE DE DECISÃO                                                 │
│      GateDecision decide: advance / rework / blocked / waived        │
│      Evidências agregadas                                            │
│      [FI-2B + SG-0 + ESQ + GRN]                                     │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────────┐   ┌──────────────┐
            │   RELEASE    │   │   REWORK     │
            │   (Release)  │   │  (voltar ao  │
            │              │   │   passo 6)   │
            └──────────────┘   └──────────────┘
```

---

## 2. Três Fidelidades Obrigatórias

Nenhuma entrega poderá ser formalmente aprovada se uma dessas fidelidades estiver ausente:

| Fidelidade | Descrição | Verificação |
|------------|-----------|-------------|
| **Fidelidade à Intenção do Usuário** | A entrega faz o que o usuário pediu | Revisão funcional |
| **Fidelidade às Regras do Negócio** | A entrega respeita todas as regras | Revisão de domínio + GRN |
| **Fidelidade à Engenharia de Software** | A entrega é legível, testável, sustentável | Verificação ESQ + SG-0 |

---

## 3. Mapeamento de Eixos Transversais

### 3.1 SG-0 — Segurança Operacional

| Onde se Aplica | O que Verifica |
|----------------|----------------|
| Passo 7 (WorkOrder) | Autoridade para execução |
| Passo 8 (Execução) | Escopo de ações permitidas |
| Passo 13 (Verificação) | Ausência de ações destrutivas |
| Passo 14 (Gate) | Conformidade com política de segurança |

### 3.2 ESQ — Engenharia de Software

| Onde se Aplica | O que Verifica |
|----------------|----------------|
| Passo 5 (Padrões) | Definição de restrições técnicas |
| Passo 11 (Verificação) | Qualidade estrutural |
| Passo 14 (Gate) | Conformidade com constituição |
| Todas as fases | Testes arquiteturais |

### 3.3 GRN — Governança de Regras

| Onde se Aplica | O que Verifica |
|----------------|----------------|
| Passo 3 (Regras) | Identificação de regras |
| Passo 4 (Domínio) | Mapeamento regra → entidade |
| Passo 10 (Revisão) | Conformidade com regras |
| Passo 14 (Gate) | Bloqueio por regra violada |

### 3.4 CTP — Chat-to-Project

| Onde se Aplica | O que Happens |
|----------------|---------------|
| Passo 1-2 (Conversa → Pacote) | Promoção de conversa |
| Passo 3 (Regras) | Extração de regras do documento |
| Passo 6 (Planejamento) | Plano baseado no documento aprovado |
| Futuro: atualizações | Envio de atualizações para projeto |

---

## 4. Eixos e Fases

| Eixo | Fases de Aplicação |
|------|-------------------|
| **SG-0** | Todas (a partir de FI-2B) |
| **ESQ** | Todas que criem ou alterem código |
| **GRN** | FI-2B+ (regras), FI-5+ (contexto), FI-11+ (distribuição) |
| **CTP** | FI-6+ (interface), FI-3+ (persistência), FI-5+ (linhagem) |

---

## 5. Diagrama de Camadas

```
┌─────────────────────────────────────────────────────────┐
│                    CTP (Promoção)                        │
│              Conversa → Projeto Formal                   │
├─────────────────────────────────────────────────────────┤
│                    GRN (Regras)                          │
│         Identificação → Formalização → Fiscalização     │
├─────────────────────────────────────────────────────────┤
│                    ESQ (Qualidade)                       │
│        Padrões → Verificação → Gate Estrutural          │
├─────────────────────────────────────────────────────────┤
│                    SG-0 (Segurança)                      │
│      Autorização → Escopo → Proteção → Rollback         │
├─────────────────────────────────────────────────────────┤
│                    DOMÍNIO (FI-2A)                       │
│    Entidades → Transições → Políticas → Exceções        │
├─────────────────────────────────────────────────────────┤
│                    CONTRATOS (FI-0/1)                    │
│         Eventos → Schemas → Validação → IDs             │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Regra de Ouro

> **Nenhuma entrega poderá ser formalmente aprovada se uma das três fidelidades estiver ausente: intenção do usuário, regras do negócio, ou engenharia de software.**

---

> *Este mapa é vivo e deve ser atualizado a cada nova fase do projeto.*
