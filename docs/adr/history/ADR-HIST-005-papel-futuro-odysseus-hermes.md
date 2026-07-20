---
tipo: adr_historico
status: accepted
decisor: Saimon
formalizado_em: 2026-07-20
efeito_retroativo: false
---

# ADR-HIST-005 — Papel futuro de Odysseus e Hermes

## Decisão declarada por Saimon

Odysseus e Hermes permanecem referências técnicas, fontes de estudo e possíveis origens de padrões. Nenhum deles é dependência arquitetural obrigatória do Harness Cognitivo.

## Apoio documental

- A [linha do tempo](../../forensics/HC-DOC-ORIGIN-01/01_LINHA_DO_TEMPO_ODYSSEUS_AO_HARNESS.md) registra Odysseus como primeira fundação observada e Hermes como referência posterior.
- Os Docs históricos 01–02 tratam clientes/modelos por contrato e citam Hermes.
- A arquitetura atual declara o Harness externo e independente do modelo.

## Lacunas históricas

- Não existem benchmarks reproduzíveis atuais entre Harness, Odysseus e Hermes.
- Não há catálogo aprovado de padrões candidatos a reaproveitamento.
- Licenças, versões e compatibilidade técnica devem ser verificadas no momento de qualquer estudo futuro.

## Consequência arquitetural

- referências externas entram por avaliação controlada;
- nenhum padrão externo se torna requisito sem ADR, fonte, versão e testes;
- adapters futuros devem preservar a neutralidade do núcleo;
- ausência ou mudança de Odysseus/Hermes não pode impedir o funcionamento canônico.

## Preservado

- observação comparativa de capacidades;
- memória e interação como eixos de estudo;
- modelos/clientes intercambiáveis por contratos.

## Abandonado ou proibido por padrão

- acoplamento obrigatório;
- cópia não auditada de código ou configuração;
- uso de comportamento externo como fonte de verdade do domínio.

## Regra temporal

Formalizado em 2026-07-20, sem efeito retroativo sobre avaliações, evidências ou decisões anteriores.
