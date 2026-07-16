---
tipo: adr
titulo: "ADR-002: Migração de (str, Enum) para StrEnum"
status: aceito
data: 2026-07-15
eixo: ESQ
---

# ADR-002: Migração de (str, Enum) para StrEnum

## Status

Aceito

## Contexto

O padrão `(str, Enum)` para enums de string foi o padrão original do projeto (FI-0/1/2A). O ruff identificou 24 violações UP042, indicando que `StrEnum` (Python 3.11+) é o padrão moderno e preferido.

## Decisão

Migrar todos os enums de string de `(str, Enum)` para `StrEnum`.

**Arquivos afetados:**
- `src/harness/contracts/context.py` — Purpose, ObjectType, TrustLevel, ChecksumAlgorithm
- `src/harness/contracts/events.py` — EventType
- `src/harness/domain/enums.py` — 10 enums (ProjectStatus, TaskStatus, etc.)
- `src/harness/domain/plan.py` — PlanStatus
- `src/harness/domain/requirement.py` — RequirementStatus, RequirementPriority

## Justificativa

- `StrEnum` é a forma canônica em Python 3.11+
- Elimina violação UP042 do ruff
- StrEnum é subclasse de `(str, Enum)`, garantindo compatibilidade
- Pydantic suporta StrEnum nativamente

## Consequências

### Mais fácil
- Código mais idiomático e moderno
- Zero violações de lint para padrão de enum
- Compatível com serialização Pydantic

### Mais difícil
- Nada significativo — comportamento externo é idêntico

## Referências

- Python 3.11+ StrEnum documentation
- Pydantic StrEnum support
- pyproject.toml: `requires-python = ">=3.12"`
