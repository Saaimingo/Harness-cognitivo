---
tipo: adr_historico
status: accepted_retrospective_with_boundary
decisor: Saimon
formalizado_em: 2026-07-20
efeito_retroativo: false
---

# ADR-HIST-004 — EvoMemory como protótipo técnico e ancestral da MEC

## Decisão declarada por Saimon

EvoMemory é classificado como protótipo técnico e ancestral conceitual da Memória Evolutiva Causal (MEC). Não é a implementação canônica atual da MEC nem componente do Harness Cognitivo.

## Apoio documental

- O repositório `evomemory-core` demonstra um protótipo local com `MemoryAtom`, SQLite, event store, relações, recall, contradição, supersessão, decay e consolidação conservadora.
- A [comparação técnica](../../forensics/HC-DOC-ORIGIN-01/03_COMPARACAO_EVOMEMORY_MEC_HARNESS.md) mostra sobreposições e diferenças estruturais entre EvoMemory, a MEC especificada e o Harness implementado.
- A [linha do tempo](../../forensics/HC-DOC-ORIGIN-01/01_LINHA_DO_TEMPO_ODYSSEUS_AO_HARNESS.md) demonstra continuidade temporal e conceitual.

## Lacunas históricas

- O repo EvoMemory não menciona SCR.
- Os documentos MEC não mencionam EvoMemory.
- Não existe mapeamento contemporâneo aceita/rejeita/transforma por conceito.

## Consequência arquitetural

EvoMemory pode ser estudado como experimento e fonte de padrões/testes, mas qualquer reaproveitamento exige ADR específico, redesenho contra contratos MEC/Harness e validação adversarial. Não há autorização de migração nesta decisão.

## Preservado

- memória tipada e local-first;
- origem, confiança, importância e relações explícitas;
- retenção de antecessores e explicação do recall;
- padrões experimentais de Unit of Work, rollback e idempotência.

## Abandonado ou não canônico

- `MemoryAtom` como aggregate obrigatório;
- taxonomias Evo como enums MEC;
- hashing lexical chamado de busca semântica;
- FastAPI/endpoints e schemas Evo como contratos atuais;
- pesos fixos de decay sem dataset;
- branch 0.2.1 não mesclada como estado de `main`.

## Regra temporal

Formalizado em 2026-07-20. A classificação de ancestralidade não cria prova contemporânea onde a ponte documental estava ausente e não altera refs ou evidências históricas.
