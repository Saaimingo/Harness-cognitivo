---
tipo: indice
titulo: "Índice Mestre — Harness Cognitivo"
status: documentary_reconciliation_in_progress
data: 2026-07-15
atualizado: 2026-07-20
base_canonica: a191a37d207e47d322297f7ce84c2dd211ca02d9
workorder_atual: HC-DOC-REC-01
---

# Índice Mestre — Harness Cognitivo

> Mapa navegacional do estado implementado, das normas preservadas e da reconciliação documental em andamento.

## Status das fases

| Fase | Nome | Estado | Referência | Tag |
|---|---|---|---|---|
| FI-0 | Fundação Inicial | Aprovada | `b3700c1` | `fi-0-approved` |
| FI-1 | Protocolo Cognitivo no Obsidian | Aprovada | `0b15b5f` | `fi-1-approved` |
| FI-2A | Domínio e Contratos Puros | Aprovada | `be1236f` | `fi-2a-approved` |
| FI-2B Parte 1 | ExecutionRun, Review e TestRun | Integrada e encerrada | merge `a191a37d207e47d322297f7ce84c2dd211ca02d9` | `fi-2b-part1-approved` |
| FI-2B Parte 2 | GateDecision, Release e Incident | Não iniciada; suspensa | Fora do escopo da reconciliação documental | — |
| FI-3+ | Fases futuras | Não iniciadas/bloqueadas | Dependem de decisão soberana e fases anteriores | — |

## Estado canônico da FI-2B Parte 1

- Branch histórica preservada: `feat/fi-2b-part1` em `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738`.
- PR #1: fechada por merge commit, sem squash e sem rebase.
- Merge na master: `a191a37d207e47d322297f7ce84c2dd211ca02d9`.
- Quality da feature: execução `29747690315`, conclusão `success`.
- Quality da master: execução `29751012597`, conclusão `success`.
- Tag anotada publicada: `fi-2b-part1-approved`, resolvendo ao merge.
- Testes: 534 aprovados; 1 `PytestCacheWarning` local ambiental preservado.
- Estado formal: `FI-2B_PART1_CLOSED`.

## Reconciliação documental atual

| Item | Estado |
|---|---|
| WorkOrder | `HC-DOC-REC-01` |
| Branch de trabalho | `docs/hc-documentary-reconciliation` |
| Base | master canônica `a191a37d…` |
| Escopo | preservação, reconciliação documental e rascunhos controlados |
| Implementação FI-2B Parte 2 | não iniciada |
| Bíblia | rascunho não canônico |
| Próximo gate | revisão interna Mimo, verificações, commit/push e auditoria final |

Esta reconciliação não altera os originais normativos 01–08, código Python, testes, dependências ou fase.

## Governança e autoridade

- [Registro canônico de fontes e autoridade](../governance/00_REGISTRO_CANONICO_DE_FONTES_E_AUTORIDADE.md)
- [Matriz de reconciliação conceitual](../reconciliation/01_MATRIZ_DE_RECONCILIACAO_CONCEITUAL.md)
- [ADRs históricos](../adr/history/)
- [Status da WorkOrder HC-DOC-REC-01](HC_DOC_REC_01_STATUS.md)

## Arquitetura

- [Mapa arquitetural](../architecture/ARCHITECTURAL_MAP.md)
- [Constituição ESQ](../architecture/ESQ_CONSTITUTION.md)
- [Plano FI-2B](../architecture/FI2B_PLAN.md)
- [Governança GRN](../architecture/GRN_BUSINESS_RULES_GOVERNANCE.md)
- [Protocolo CTP](../architecture/CTP_CHAT_TO_PROJECT.md)

## Operações

- [Guia de agentes](../operations/AGENTS.md)
- [Política SG-0](../operations/SG-0_AGENT_DESTRUCTIVE_ACTIONS_POLICY.md)
- [Checklist SG-0](../operations/SG-0_CHECKLIST.md)

## Relatórios

- [Relatório FI-0](RELATORIO_FI0.md)
- [Relatório FI-1](RELATORIO_FI1.md)
- [Consolidação FI-2A](RELATORIO_CONSOLIDACAO_FI2A.md)
- [Relatório FI-2B Parte 1](RELATORIO_FI2B_PARTE1.md)
- [Mapeamento de componentes e planos](MAPEAMENTO_COMPONENTES_PLANOS.md)
- [Classificação de lacunas](CLASSIFICACAO_LACUNAS.md)

## Evidências e forense

- [Evidências FI-2B Parte 1](../../evidence/fi2b-part1/2026-07-18/)
- [Manifesto de preservação HC-DOC-ORIGIN-01](../forensics/HC-DOC-ORIGIN-01/PRESERVATION_MANIFEST.md)
- [Clone divergente do Vault](../forensics/HC-DOC-REC-01/vault-clone-d11f983/README.md)
- [Reconciliação dos manifestos de hashes](../forensics/HC-DOC-REC-01/hash-manifests/01_RECONCILIACAO_DOS_MANIFESTOS.md)
- [Manifesto atual dos originais 01–08](../forensics/HC-DOC-REC-01/hash-manifests/02_MANIFESTO_CANONICO_ATUAL.md)

## Rascunhos

- [Bíblia do Harness Cognitivo — rascunho inicial não canônico](../drafts/00_BIBLIA_DO_HARNESS_COGNITIVO_DRAFT.md)

## Estado permitido

Antes da auditoria documental final, o teto permanece `READY_FOR_FINAL_DOCUMENTARY_AUDIT`. FI-2B Parte 2 não pode ser iniciada por esta WorkOrder.
