# Harness Cognitivo

Camada operacional para transformar modelos de IA intercambiáveis em sistemas persistentes, verificáveis, seguros e rastreáveis.

> Um modelo não é um sistema. O modelo é o motor; o Harness fornece contratos, memória, governança, execução, validação e observabilidade.

## Estado atual

| Marco | Estado | Referência |
|---|---|---|
| FI-0 | Aprovada | tag `fi-0-approved` → `b3700c1` |
| FI-1 | Aprovada | tag `fi-1-approved` → `0b15b5f` |
| FI-2A | Aprovada | tag `fi-2a-approved` → `be1236f` |
| FI-2B Parte 1 | Integrada e encerrada | merge `a191a37d207e47d322297f7ce84c2dd211ca02d9`; tag `fi-2b-part1-approved` |
| FI-2B Parte 2 | Não iniciada; suspensa durante a reconciliação documental | GateDecision, Release e Incident não implementados |

A PR #1 foi fechada por merge commit. A branch histórica `feat/fi-2b-part1` permanece preservada em `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738`. A auditoria/reconciliação documental `HC-DOC-REC-01` está em andamento na branch `docs/hc-documentary-reconciliation`; ela não autoriza implementação da Parte 2 nem avanço de fase.

## O que existe hoje

- Contratos cognitivos e referências de evidência.
- Entidades de domínio para Project, Plan, Task, Requirement e WorkOrder.
- Entidades da FI-2B Parte 1: ExecutionRun, Review e TestRun.
- Enums, transições, políticas puras e erros de domínio.
- Logging estruturado e CLI inicial.
- Documentação de SG-0, ESQ, GRN e CTP.
- Suíte com 534 testes aprovada na integração da FI-2B Parte 1.

Ainda não existem entidades GateDecision, Release e Incident, persistência, event store, executor real, RAG, grafo de conhecimento ou integrações operacionais.

## Evidência da FI-2B Parte 1

| Evidência | Resultado |
|---|---|
| HEAD aprovado da feature | `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738` |
| Merge na master | `a191a37d207e47d322297f7ce84c2dd211ca02d9` |
| Quality da feature | execução `29747690315`, `success` |
| Quality da master | execução `29751012597`, `success` |
| Pytest | 534 passed; 1 `PytestCacheWarning` local ambiental preservado |
| Tag | `fi-2b-part1-approved` → merge `a191a37d…` |

O warning local não ocorreu como falha do CI e não foi ocultado. Ele foi atribuído à permissão da `.pytest_cache` no ambiente local auditado.

## Requisitos

- Python 3.12
- [uv](https://docs.astral.sh/uv/)

## Instalação reproduzível

```bash
uv sync --frozen --all-extras
```

O `uv.lock` é a fonte das versões congeladas. A instalação deve falhar se o lock estiver incompatível com o projeto.

## Validações

```bash
uv run pytest --collect-only -q
uv run pytest tests/ -ra --tb=short
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/harness/ --ignore-missing-imports
git diff --check
```

## Estrutura

```text
src/harness/             código-fonte
tests/unit/              testes unitários
docs/architecture/       arquitetura e planos
docs/operations/         governança operacional
docs/governance/         autoridade documental
docs/adr/history/        decisões históricas formalizadas
docs/forensics/          evidências derivadas preservadas
docs/reconciliation/     matrizes de reconciliação
docs/drafts/             rascunhos não canônicos
docs/reports/            relatórios e índice mestre
evidence/                evidências sanitizadas
```

## Governança

- O tree/ref Git identifica o estado implementado; o Obsidian é memória e projeção, não código canônico.
- Os originais 01–08 são patrimônio normativo histórico e não devem ser alterados silenciosamente.
- Executor e revisor devem ser autoridades diferentes.
- Ações destrutivas exigem autorização explícita e rastreabilidade.
- Mudança posterior a uma auditoria exige nova auditoria do novo SHA.
- Merge, tags e avanço de fase dependem de autorização expressa de Saimon.

## Navegação

- [Índice mestre](docs/reports/INDICE_MESTRE.md)
- [Status HC-DOC-REC-01](docs/reports/HC_DOC_REC_01_STATUS.md)
- [Registro de fontes e autoridade](docs/governance/00_REGISTRO_CANONICO_DE_FONTES_E_AUTORIDADE.md)
- [ADRs históricos](docs/adr/history/)
- [Relatórios forenses preservados](docs/forensics/HC-DOC-ORIGIN-01/PRESERVATION_MANIFEST.md)
- [Matriz de reconciliação](docs/reconciliation/01_MATRIZ_DE_RECONCILIACAO_CONCEITUAL.md)
- [Bíblia — rascunho não canônico](docs/drafts/00_BIBLIA_DO_HARNESS_COGNITIVO_DRAFT.md)
- [Plano da FI-2B](docs/architecture/FI2B_PLAN.md)
- [Relatório da FI-2B Parte 1](docs/reports/RELATORIO_FI2B_PARTE1.md)
- [PR #1](https://github.com/Saaimingo/Harness-cognitivo/pull/1)
