# Harness Cognitivo

Camada operacional para transformar modelos de IA intercambiáveis em sistemas persistentes, verificáveis, seguros e rastreáveis.

> Um modelo não é um sistema. O modelo é o motor; o Harness fornece contratos, memória, governança, execução, validação e observabilidade.

## Estado atual

| Marco | Estado | Referência |
|---|---|---|
| FI-0 | Aprovada | tag `fi-0-approved` → `b3700c1` |
| FI-1 | Aprovada | tag `fi-1-approved` → `0b15b5f` |
| FI-2A | Aprovada | tag `fi-2a-approved` → `be1236f` |
| FI-2B Parte 1 | Implementada e auditada na branch; reconciliação preparada para commit | PR #1, `audited_head=d11f983f701936a6b3e7fde68c81fba0699f1fcd` |
| FI-2B Parte 2 | Não iniciada | GateDecision, Release e Incident permanecem fora do escopo |

A PR #1 permanece Draft, sem merge e sem tag de aprovação da FI-2B Parte 1. A preparação desta reconciliação não autoriza integração nem avanço de fase.

## O que existe hoje

- Contratos cognitivos e referências de evidência.
- Entidades de domínio para Project, Plan, Task, Requirement e WorkOrder.
- Entidades da FI-2B Parte 1: ExecutionRun, Review e TestRun.
- Enums, transições, políticas puras e erros de domínio.
- Logging estruturado e CLI inicial.
- Documentação de SG-0, ESQ, GRN e CTP.
- Suíte unitária com 534 testes coletados.
- Especificações técnicas candidatas para produto, arquitetura, stack, dados, integrações, segurança, observabilidade, testes, operação, frontend e requisitos não funcionais.

Ainda não existem GateDecision, Release, Incident, persistência, event store, executor real, RAG, grafo de conhecimento ou integrações operacionais.

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

Na reprodução de 2026-07-18 sobre o HEAD auditado:

- 534 testes coletados;
- 534 testes aprovados;
- 1 `PytestCacheWarning` ambiental, preservado nas evidências;
- Ruff check aprovado;
- Ruff format: 49 arquivos já formatados;
- Mypy sem issues em 31 arquivos;
- `git diff --check` com código de saída 0.

## Estrutura

```text
src/harness/             código-fonte
tests/unit/              testes unitários
docs/architecture/       arquitetura e planos
docs/specifications/     especificações técnicas normativas candidatas
docs/adr/                registros de decisões arquiteturais
docs/operations/         governança operacional
docs/reports/            relatórios e índice mestre
evidence/                evidências sanitizadas
```

## Governança

- O repositório Git é a fonte normativa; o Obsidian é uma projeção de navegação e trabalho.
- Executor e revisor devem ser autoridades diferentes.
- Ações destrutivas exigem autorização explícita e rastreabilidade.
- Alterações após uma auditoria invalidam o veredito anterior e exigem nova auditoria do novo HEAD.
- Merge, tags e avanço de fase dependem de autorização explícita de Saimon.
- Agentes devem ler a Especificação Técnica Mestra, a spec da área e os ADRs relacionados antes de planejar ou implementar.
- Lacunas materiais de especificação devem bloquear a execução com `SPECIFICATION_GAP_REQUIRES_DECISION`.

## Navegação

- [Especificações técnicas](docs/specifications/README.md)
- [Especificação Técnica Mestra](docs/specifications/00_ESPECIFICACAO_TECNICA_MESTRA.md)
- [ADRs](docs/adr/README.md)
- [Índice mestre](docs/reports/INDICE_MESTRE.md)
- [Plano da FI-2B](docs/architecture/FI2B_PLAN.md)
- [Relatório da FI-2B Parte 1](docs/reports/RELATORIO_FI2B_PARTE1.md)
- [Constituição ESQ](docs/architecture/ESQ_CONSTITUTION.md)
- [Política SG-0](docs/operations/SG-0_AGENT_DESTRUCTIVE_ACTIONS_POLICY.md)
- [PR #1](https://github.com/Saaimingo/Harness-cognitivo/pull/1)
