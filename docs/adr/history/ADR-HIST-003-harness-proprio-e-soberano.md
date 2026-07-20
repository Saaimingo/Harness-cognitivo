---
tipo: adr_historico
status: accepted_retrospective
decisor: Saimon
formalizado_em: 2026-07-20
efeito_retroativo: false
---

# ADR-HIST-003 — Rejeição de harnesses generalistas como base definitiva

## Decisão declarada por Saimon

Harnesses generalistas de terceiros não serão a base definitiva do produto. O Harness Cognitivo é uma implementação própria e soberana, com contratos, governança e evolução controlados pelo projeto.

“Próprio” e “soberano” descrevem autoridade arquitetural e implementação canônica. Não significam ausência de referências, ideias herdadas ou dependências de software declaradas.

## Apoio documental

- Os documentos históricos 04–08 descrevem arquitetura própria, externa e independente de um modelo específico.
- O repositório `Saaimingo/Harness-cognitivo`, iniciado na FI-0 e integrado até a FI-2B Parte 1, materializa uma implementação própria.
- A [situação documental](../../forensics/HC-DOC-ORIGIN-01/05_RELATORIO_DE_SITUACAO_DOCUMENTAL.md) registra a soberania como parcialmente corroborada antes desta decisão formal.

## Lacunas históricas

- Não existia ADR contemporâneo com a comparação final Odysseus × Hermes × Harness próprio.
- Não foi preservada uma matriz de critérios que explique cada alternativa rejeitada.

## Consequência arquitetural

- código e Git do Harness definem o estado implementado;
- referências externas não substituem requisitos, ADRs ou evidências do projeto;
- adoção de padrão externo exige decisão explícita, contrato e testes próprios.

## Preservado

- problemas, padrões e aprendizados tecnicamente avaliados em Odysseus, Hermes, SCR e EvoMemory;
- modelos plugáveis e acesso por contrato;
- rastreabilidade e autoridade humana.

## Abandonado ou rejeitado

- dependência arquitetural obrigatória de um harness generalista;
- importação automática de código, schemas, estados ou políticas históricas;
- equivalência entre similaridade conceitual e compatibilidade técnica.

## Regra temporal

Formalizado em 2026-07-20. O ADR não reescreve a intenção de experimentos anteriores nem altera a proveniência de suas evidências.
