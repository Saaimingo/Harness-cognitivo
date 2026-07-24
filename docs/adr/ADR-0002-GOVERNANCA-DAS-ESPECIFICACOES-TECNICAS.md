---
titulo: ADR-0002 — Governança das Especificações Técnicas
status: proposed
data: 2026-07-24
autoriza_implementacao: false
---

# ADR-0002 — Governança das Especificações Técnicas

## Contexto

O Harness Cognitivo possui visão, contratos, roadmap, documentos de governança e implementação parcial, mas decisões de stack e operação estavam distribuídas. Isso permite que agentes preencham lacunas por preferência própria, criando retrabalho, risco e divergência.

## Decisão proposta

Criar `docs/specifications/` como camada normativa candidata entre a Bíblia e os planos de implementação.

A ordem de trabalho passa a ser:

```text
Bíblia e decisões soberanas
→ especificação técnica mestra
→ especificações por área
→ ADRs
→ plano da fase
→ WorkOrder
→ implementação
→ revisão, testes e auditoria
```

Agentes devem ler as especificações aplicáveis antes de planejar ou executar. Lacunas materiais produzem `SPECIFICATION_GAP_REQUIRES_DECISION`.

## Consequências positivas

- menos improvisação;
- stack e boundaries explícitos;
- segurança definida antes da exposição;
- decisões substituíveis sem contaminar o domínio;
- revisão e auditoria com critérios objetivos;
- onboarding mais rápido de executores.

## Consequências negativas

- maior esforço documental inicial;
- necessidade de manutenção e reconciliação;
- risco de especificação excessiva ou obsoleta.

## Controles

- classificar decisões como DECIDIDO, CANDIDATO, ADIADO, SUBSTITUIVEL ou PROIBIDO;
- evitar versões e ferramentas futuras sem necessidade;
- exigir ADR para decisões materiais;
- revisar a spec junto de mudanças de arquitetura;
- specs candidatas não autorizam implementação.

## Alternativas rejeitadas

- deixar escolhas para cada executor;
- colocar todos os detalhes mutáveis dentro da Bíblia;
- decidir toda a stack até FI-12 antecipadamente;
- corrigir arquitetura somente após o código existir.

## Critério de aceitação

Este ADR só se torna `accepted` após revisão soberana, reconciliação com documentos existentes, revisão interna independente e auditoria final do SHA publicado.