---
tipo: reconciliacao_manifestos_hash
status: controlled_reconciliation
workorder: HC-DOC-REC-01
data: 2026-07-20
---

# Reconciliação dos manifestos de integridade dos originais 01–08

## Fontes preservadas

| Fonte | Data declarada | SHA-256 da fonte e da cópia | Papel |
|---|---|---|---|
| `MANIFESTO_DE_INTEGRIDADE_DOS_ORIGINAIS.md` | 2026-07-11 | `3b9dd19e24442dae5ef87b65761473da40907d2bb97e2615bc83740f2680a320` | manifesto histórico inicial |
| `RELATORIO_DE_INTEGRIDADE_V3.md` | 2026-07-11 | `2ab87ff4a1be56a6c70bac11539ff898c23599bfb6d8af0929f286a574c7c5cf` | relatório posterior que coincide com os bytes atuais |

As cópias byte a byte estão em `source-snapshots/`. O manifesto antigo foi preservado; não foi substituído nem editado.

## O que cada registro demonstra

O manifesto inicial, gerado por Freebuff em 2026-07-11, declara um primeiro conjunto de tamanhos e hashes. Esses bytes anteriores não estão disponíveis no corpus auditado, portanto não foi possível reconstruí-los nem provar a qual versão material correspondiam além da própria declaração do manifesto.

O relatório V3, também declarado como gerado em 2026-07-11, afirma que houve uma restauração dos originais sem frontmatter. Seus oito tamanhos e hashes conferem exatamente com os arquivos observados em 2026-07-20.

## Divergência por documento

| Doc | Tamanho/hash inicial | Tamanho/hash atual e V3 | Classificação da mudança |
|---|---|---|---|
| 1 | 25.594 / `a54bad0081bb7f7b695ba4aa7ec3caa2e0f03cb872fb09f3456ef5d3797fe3e7` | 26.494 / `98780bf11c76c747cba2f0455d0c17284cfe315b42023d93e1f14880cc9161ca` | causa material não reconstruível |
| 2 | 22.124 / `ecd0ba012dede8283c4429ce28247fb71ef42fc9a0dc3339abcbf02955ba28ad` | 23.047 / `8c6857952514caff44a8ea7371191b7339c8a78533950c1dc19a36b9efec3d59` | causa material não reconstruível |
| 3 | 8.257 / `27ceda9b80df3ce3345a4652e886cdf4d93ecb7df0c5bd1896e5ce1ff5466c87` | 8.572 / `726f1fa51be2f642e8c7b2e553f4a096e3d0e8009b93b67297013bf24285a08e` | causa material não reconstruível |
| 4 | 46.645 / `1646e7cc99d3c3d7d3d2f959c20698bdbeea2a901a6b008db4d6ba96b0c37243` | 47.777 / `7373edf6ac34c7bf3391e17dc89936afec602504946cd635ca247c062d0a2667` | causa material não reconstruível |
| 5 | 47.814 / `909714c00c994bd0de57cd23e9ab727c46b147a89ece7aa13f08e861df07de0e` | 49.463 / `d9a62922ac1274fdf07faa7796b31315ddc813212fae4427b262c951118f8268` | causa material não reconstruível |
| 6 | 45.241 / `a052e8065045d31a2213c7e1036b25c2a060d33a3dd41a25124ff76411ffa114` | 47.071 / `e44f22ddbf2dd3a6232fe1aac8c135664cd8e330e225874e676c72d44f8c09db` | causa material não reconstruível |
| 7 | 39.513 / `c219d33e8889cfd50793a481a236dfc933af1bdc2d1c4b96de221ad49b96cf3c` | 41.110 / `fec089645144b91b378ba474bcf01a0f4a1cf616150a9bd2c502fe66ad6e1738` | causa material não reconstruível |
| 8 | 25.340 / `30165fb3f01377cc41907a5c182bd6fa421822cbb098d6795dea5a438197a2d1` | 26.366 / `d4ee97eed3967887f91730fbd77790e1577fe595b7303e9f5c93597391edc6cf` | causa material não reconstruível |

## Legitimidade da alteração

O V3 declara a restauração como legítima e os bytes atuais coincidem com esse relatório. Entretanto, sem os bytes anteriores, diff ou cadeia de custódia intermediária, esta reconciliação não pode confirmar se cada alteração foi legítima, acidental ou uma combinação. A classificação probatória permanece `REQUIRES_DECISION`; isso não invalida o uso dos hashes V3 para identificar o snapshot atual.

Nenhum original 01–08 foi alterado por esta WorkOrder.
