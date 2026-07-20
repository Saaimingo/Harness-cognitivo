---
tipo: adr_historico
status: accepted_retrospective
decisor: Saimon
formalizado_em: 2026-07-20
efeito_retroativo: false
---

# ADR-HIST-001 — Odysseus como primeira base considerada e SCR como melhoria de memória

## Decisão declarada por Saimon

Odysseus foi a primeira base técnica considerada para o projeto. O SCR surgiu como proposta de camada sobre Odysseus para melhorar memória evolutiva, governança, segurança, genealogia e rastreabilidade, sem alterar imediatamente o código da base observada.

## Apoio documental

- [Linha do tempo forense](../../forensics/HC-DOC-ORIGIN-01/01_LINHA_DO_TEMPO_ODYSSEUS_AO_HARNESS.md): branch histórica `docs/odysseus-scr-foundation`, auditoria de 2026-06-16 e arquivos `projetos/odysseus-scr/`.
- [Matriz de herança](../../forensics/HC-DOC-ORIGIN-01/02_MATRIZ_DE_HERANCA_CONCEITUAL.md): continuidade de origem, genealogia, recoverability e separação governança/segurança.

## Lacunas históricas

- A expansão da sigla SCR não foi encontrada.
- A conversa ou nota que antecedeu a documentação de 2026-06-16 não está preservada.
- Não há benchmark reproduzível nem snapshot do código Odysseus auditado naquele momento.

## Consequência arquitetural

Odysseus e SCR são origem histórica e fonte de problemas/ideias, não dependência arquitetural nem módulo do Harness atual. Nenhum código ou contrato atual é derivado automaticamente dessa origem.

## Preservado

- memória com origem, recência, relações e recuperabilidade;
- genealogia/rastreabilidade;
- separação entre governança e segurança;
- postura inicial de observar e classificar sem apagar automaticamente.

## Abandonado ou substituído

- Odysseus como fundação obrigatória do produto;
- SCR como extensão operacional obrigatória de Odysseus;
- adoção automática de RAG, ChromaDB ou do stack observado.

## Regra temporal

Esta formalização retrospectiva registra a decisão soberana em 2026-07-20. Ela não altera datas, commits, evidências nem o grau de prova dos registros históricos anteriores.
