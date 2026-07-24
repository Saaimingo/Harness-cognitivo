---
titulo: Dados e Persistência
status: candidate_for_review
autoriza_implementacao: false
---

# Dados e Persistência

## Princípios

- local-first;
- schema versionado;
- integridade antes de conveniência;
- dados derivados sempre regeneráveis;
- origem, causalidade e autoridade preservadas;
- segredos nunca armazenados como conteúdo cognitivo.

## Armazenamento inicial

`DECIDIDO`: SQLite com SQLAlchemy 2 e Alembic.

Requisitos:

- foreign keys habilitadas;
- transações explícitas;
- WAL avaliado por benchmark e segurança;
- timestamps UTC;
- IDs estáveis e não semânticos;
- migrações forward e rollback quando tecnicamente seguro;
- backup antes de migração destrutiva;
- checksum para artefatos e snapshots relevantes.

## Categorias de dados

- estado operacional;
- memória cognitiva e relações causais;
- eventos e transições;
- evidências e manifests;
- configurações não secretas;
- telemetria sanitizada;
- índices derivados.

Cada registro material deve possuir, quando aplicável: `id`, `created_at`, `updated_at`, `version`, `actor`, `authority_ref`, `source_ref`, `causation_id`, `correlation_id` e estado epistêmico.

## Busca

- FTS5 para busca textual inicial;
- embeddings e vector store permanecem `ADIADOS` até corpus, recall e custo serem medidos;
- grafo de conhecimento permanece atrás de port;
- índices são projeções, não fonte primária.

## Retenção e exclusão

Toda classe de dado precisa de política de retenção. Exclusão material requer autoridade, impacto, backup aplicável e audit record. Logs não podem reter segredos ou conteúdo sensível sem necessidade.

## Backup e recuperação

- backup verificável e restaurável;
- teste periódico de restore;
- snapshots associados a versão do schema;
- Recovery Point Objective e Recovery Time Objective definidos por fase;
- corrupção deve produzir estado bloqueado, nunca recuperação silenciosa.

## Evolução futura

PostgreSQL somente mediante ADR que demonstre concorrência, distribuição ou volume incompatíveis com SQLite. A migração deve preservar contratos de domínio e evidência.