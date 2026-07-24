---
titulo: Stack Tecnológica
status: candidate_for_review
autoriza_implementacao: false
---

# Stack Tecnológica

## Núcleo atual

| Capacidade | Tecnologia | Estado | Regra |
|---|---|---|---|
| Linguagem | Python 3.12 | DECIDIDO | núcleo e automação |
| Dependências | uv + uv.lock | DECIDIDO | instalação reproduzível |
| Contratos | Pydantic 2 | DECIDIDO | fronteiras e validação |
| Persistência | SQLite | DECIDIDO | local-first inicial |
| ORM | SQLAlchemy 2 | DECIDIDO | adapter de persistência |
| Migrações | Alembic | DECIDIDO | evolução versionada |
| Busca textual | SQLite FTS5 | DECIDIDO | primeira busca local |
| CLI | Typer | DECIDIDO | interface inicial |
| API local | FastAPI | CANDIDATO | somente atrás de ports |
| Integração agêntica | MCP | CANDIDATO | adapter, não domínio |
| Testes | pytest + Hypothesis | DECIDIDO | unitário, propriedade e adversarial |
| Lint/format | Ruff | DECIDIDO | CI bloqueante |
| Tipagem | mypy | DECIDIDO | CI bloqueante no núcleo |
| CI | GitHub Actions | DECIDIDO | evidência automatizada |
| Segurança estática | Bandit + auditoria de dependências | CANDIDATO | gate de segurança |
| Telemetria | OpenTelemetry | CANDIDATO | traces, métricas e logs correlacionados |

## Modelos e provedores

Todos os provedores são `SUBSTITUIVEIS`. O sistema deve ter:

- interface comum de geração;
- capacidades declaradas por modelo;
- timeout, retry e budget;
- registro de modelo, versão lógica, papel e custo;
- fallback controlado;
- proibição de fallback silencioso em decisões materiais.

## Frontend

`ADIADO`. Nenhum framework visual está decidido. A escolha depende de fluxos, telas, acessibilidade, distribuição e operação aprovados.

## Infraestrutura futura

- PostgreSQL: `ADIADO`, somente para concorrência ou distribuição comprovada;
- fila externa: `ADIADO`;
- Redis: `ADIADO`, não usar como solução genérica;
- containers: `CANDIDATO` para empacotamento reproduzível;
- Kubernetes: `PROIBIDO` antes de necessidade operacional demonstrada.

## Critério de adoção

Uma tecnologia nova precisa responder:

1. qual requisito resolve;
2. por que a stack atual não resolve;
3. custo cognitivo e operacional;
4. impacto de segurança;
5. estratégia de teste e rollback;
6. grau de acoplamento;
7. ADR e fase autorizada.