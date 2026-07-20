---
tipo: indice
titulo: "Índice Mestre — Harness Cognitivo"
status: ready_for_commit
data: 2026-07-15
atualizado: 2026-07-18
audited_head: d11f983f701936a6b3e7fde68c81fba0699f1fcd
---

# Índice Mestre — Harness Cognitivo

> Mapa navegacional do projeto e estado reconciliado das fases.

## Status das fases

| Fase | Nome | Estado | Referência | Tag |
|---|---|---|---|---|
| FI-0 | Fundação Inicial | Aprovada | `b3700c1` | `fi-0-approved` |
| FI-1 | Protocolo Cognitivo no Obsidian | Aprovada | `0b15b5f` | `fi-1-approved` |
| FI-2A | Domínio e Contratos Puros | Aprovada | `be1236f` | `fi-2a-approved` |
| FI-2B Parte 1 | ExecutionRun, Review e TestRun | Implementada e auditada na branch; reconciliação preparada para commit | PR #1; `audited_head=d11f983` | Não criada |
| FI-2B Parte 2 | GateDecision, Release e Incident | Não iniciada | Fora do escopo atual | — |
| FI-3 | Persistência e Recuperação | Bloqueada | Depende de autorização e das fases anteriores | — |
| FI-4 | Projeções, Busca e Orquestração | Bloqueada | Fase futura | — |
| FI-5 | Linhagem e Cápsula de Contexto | Bloqueada | Fase futura | — |
| FI-6 | CLI e Fluxo Simulado | Bloqueada | Fase futura | — |
| FI-7 | MCP e Primeiro Executor | Bloqueada | Fase futura | — |
| FI-8 | Revisão Independente e Rework | Bloqueada | Fase futura | — |
| FI-9 | Laboratório de Testes e Evidências | Bloqueada | Fase futura | — |
| FI-10 | Laboratório Web e Auditoria Visual | Bloqueada | Fase futura | — |
| FI-11 | Papéis, Moderador e Promoção | Bloqueada | Fase futura | — |
| FI-12 | Release, Operação e Incidente | Bloqueada | Fase futura | — |
| FI-13 | Evals e Evolução Opcional | Bloqueada | Fase futura | — |

## Estado da FI-2B Parte 1

- Branch: `feat/fi-2b-part1`.
- PR #1: aberta, Draft, sem merge.
- Base auditada: `master` em `be1236f`.
- `audited_head=d11f983f701936a6b3e7fde68c81fba0699f1fcd`.
- Branch auditada: 9 commits à frente e 0 atrás da base.
- Escopo implementado: ExecutionRun, Review e TestRun.
- Fora do escopo: GateDecision, Release, Incident, persistência e integrações operacionais.
- Reconciliação atual: alterações locais preparadas; nenhum commit ou push realizado.

## Evidências reproduzidas

| Validação | Resultado |
|---|---|
| Coleta | 534 testes coletados |
| Pytest | 534 passed, 1 `PytestCacheWarning` |
| Ruff check | Aprovado |
| Ruff format | 49 arquivos já formatados |
| Mypy | Sem issues em 31 arquivos |
| `git diff --check` | Código de saída 0 |
| HEAD local/remoto | Iguais em `d11f983` no baseline auditado |

O warning foi preservado e investigado como provável divergência de ACL da `.pytest_cache` entre identidades locais de execução.

## Documentos centrais

### Arquitetura

- [Mapa arquitetural](../architecture/ARCHITECTURAL_MAP.md)
- [Constituição ESQ](../architecture/ESQ_CONSTITUTION.md)
- [Plano FI-2B](../architecture/FI2B_PLAN.md)
- [Governança GRN](../architecture/GRN_BUSINESS_RULES_GOVERNANCE.md)
- [Protocolo CTP](../architecture/CTP_CHAT_TO_PROJECT.md)

### Operações

- [Guia de agentes](../operations/AGENTS.md)
- [Política SG-0](../operations/SG-0_AGENT_DESTRUCTIVE_ACTIONS_POLICY.md)
- [Checklist SG-0](../operations/SG-0_CHECKLIST.md)

### Relatórios

- [Relatório FI-0](RELATORIO_FI0.md)
- [Relatório FI-1](RELATORIO_FI1.md)
- [Consolidação FI-2A](RELATORIO_CONSOLIDACAO_FI2A.md)
- [Relatório FI-2B Parte 1](RELATORIO_FI2B_PARTE1.md)
- [Mapeamento de componentes e planos](MAPEAMENTO_COMPONENTES_PLANOS.md)
- [Classificação de lacunas](CLASSIFICACAO_LACUNAS.md)

### Evidências FI-2B Parte 1

- [`evidence/fi2b-part1/2026-07-18/`](../../evidence/fi2b-part1/2026-07-18/)

## Próxima decisão permitida

Revisar o diff e as validações desta reconciliação. O estado máximo desta WorkOrder é `READY_FOR_COMMIT`.

Não estão autorizados nesta etapa:

- commit ou push;
- atualização da descrição da PR;
- merge;
- criação de tag;
- início da FI-2B Parte 2.
