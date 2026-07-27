---
titulo: Índice de ADRs
status: candidate_for_review
autoriza_implementacao: false
---

# Architecture Decision Records

ADRs registram decisões técnicas materiais, contexto, alternativas, consequências e condições de revisão.

## Regra

Uma decisão de stack, boundary, persistência, segurança, integração, deploy ou interface que altere custo, risco ou acoplamento exige ADR antes da implementação.

## Estados

- `proposed`
- `accepted`
- `superseded`
- `deprecated`
- `rejected`

Somente autoridade autorizada promove um ADR para `accepted`.

## Modelo mínimo

```text
Título
Status
Data
Decisores
Contexto
Decisão
Alternativas
Consequências positivas
Consequências negativas
Riscos e controles
Critério de revisão
Referências
```

## ADRs desta série

- [ADR-0002 — Governança das Especificações Técnicas](ADR-0002-GOVERNANCA-DAS-ESPECIFICACOES-TECNICAS.md)

ADRs históricos existentes fora desta pasta devem ser reconciliados no índice antes de qualquer renumeração.