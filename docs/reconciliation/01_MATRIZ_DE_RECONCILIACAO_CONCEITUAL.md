---
tipo: matriz_reconciliacao_conceitual
status: proposed_for_internal_review
workorder: HC-DOC-REC-01
data: 2026-07-20
---

# Matriz de reconciliação conceitual

## Regra

As conclusões abaixo consideram fontes, decisões formais e implementação. Nenhuma classificação decorre somente da idade. “Preservado” não significa implementado; “histórico” não significa irrelevante.

| Conceito | Origem principal | Situação atual | Conclusão | Fundamentação/limite |
|---|---|---|---|---|
| Odysseus como base do produto | pesquisa de 2026-06-16 | referência histórica, sem integração | `SUPERSEDED` | substituído pela decisão de Harness próprio; padrões ainda podem ser estudados |
| SCR | camada proposta sobre Odysseus | origem de problemas de memória/governança | `HISTORICAL_ONLY` | não existe módulo SCR atual; expansão da sigla não foi encontrada |
| memória evolutiva | SCR/EvoMemory | MEC especificada, ainda não implementada | `EXPANDED` | MEC acrescenta causalidade, epistemologia, eventos e evidência |
| “Memória Evolutiva” → “Memória Evolutiva Causal” | corpus histórico | nome MEC vigente | `RENAMED` | rename parcial com expansão; não implica equivalência de schemas |
| estados térmicos | SCR | sem dimensão canônica atual | `REQUIRES_DECISION` | não equivalem a status Evo nem lifecycle/epistemic MEC |
| recoverability | SCR | reconstrução/reativação parcialmente especificada | `REQUIRES_DECISION` | falta contrato e métrica antes de persistência |
| ancestor IDs/genealogia | SCR | linhagem/proveniência MEC/CTP | `EXPANDED` | conceito preservado e ampliado; serviço ainda ausente |
| regimento interno | SCR | GRN | `RENAMED` | equivalência transformada registrada; GRN possui escopo mais formal |
| segurança reforçada | SCR | SG-0 | `EXPANDED` | autoridade e ação destrutiva formalizadas; não substitui segurança de infraestrutura |
| RAG/ChromaDB como stack obrigatório | Odysseus | FTS5 primeiro, adapters futuros | `SUPERSEDED` | dependência do stack externo não vigora |
| grafo/mapa mental | SCR/EvoMemory | relações tipadas e grafo futuro | `REQUIRES_DECISION` | graph do protótipo não satisfaz automaticamente MEC |
| EvoMemory | repo `evomemory-core` | protótipo técnico ancestral | `HISTORICAL_ONLY` | fonte de padrões, não implementação canônica atual |
| `MemoryAtom` | EvoMemory | nenhum aggregate MEC implementado | `HISTORICAL_ONLY` | não há mapeamento 1:1; schema não será importado automaticamente |
| tipos de memória Evo | EvoMemory | tipos cognitivos MEC distintos | `CONFLICTING` | fundi-los criaria taxonomia ambígua |
| status Evo | EvoMemory | lifecycle e epistemic state MEC separados | `CONFLICTING` | dimensões não são aliases |
| supersessão/contradição | EvoMemory/MEC | padrões especificados; domínio cognitivo ausente | `EXPANDED` | MEC exige ator, evidência, validade e eventos/replay |
| pesos fixos de decay | EvoMemory | nenhum baseline aprovado | `HISTORICAL_ONLY` | só experimento; MEC exige dataset antes de pesos canônicos |
| SQLite/event store Evo | EvoMemory | persistência MEC futura | `HISTORICAL_ONLY` | mesma tecnologia possível, contratos distintos; FI-3 decidirá |
| Hermes como referência | Docs 01–02 e declaração de Saimon | referência técnica futura | `PRESERVED` | preferência histórica é retrospectiva; sem dependência obrigatória |
| Harness próprio e soberano | Docs 04–08, repo atual, ADR | decisão vigente | `PRESERVED` | soberania de autoridade/implementação, não ausência de herança conceitual |
| modelos/clientes plugáveis | Odysseus/MEC/Harness | decisão arquitetural vigente | `PRESERVED` | runtime multi-modelo ainda não implementado |
| revisão independente | Docs 04–08 | `Review` e política implementadas | `PRESERVED` | CI não substitui revisor independente |
| evidência antes da aprovação | MEC/Harness | `TestRun`, evidence e CI | `EXPANDED` | evidência operacional existe; contrato cognitivo ainda pendente |
| SG-0 | FI-2A | governança vigente | `PRESERVED` | cobre autoridade/ações destrutivas; aplicação continua por risco |
| ESQ | FI-2A | constituição vigente | `PRESERVED` | origem tardia, sem ancestral nominal no SCR |
| GRN | SCR/FI-2A | governança vigente | `EXPANDED` | formaliza políticas e conformidade de domínio |
| CTP | arquitetura Harness | norma vigente, pipeline futuro | `PRESERVED` | mantém conversa como fonte potencial, não normativa automática |
| Git como fonte do estado implementado | FI-1 | vigente | `PRESERVED` | event store futuro exigirá decisão explícita de autoridade |
| Obsidian como memória/projeção, não código canônico | Docs MEC, FI-1 e projeções do Vault | regra de autoridade vigente | `PRESERVED` | o tree/ref Git identifica o estado implementado, mesmo quando o Vault contém um clone |
| clone do Harness dentro do Vault | projeção divergente | preservado sem correção | `CONFLICTING` | checkout velho/sujo; destino exige decisão soberana |
| manifesto inicial de hashes | 2026-07-11 | evidência histórica divergente | `HISTORICAL_ONLY` | bytes antigos não foram reconstruídos; não representa snapshot atual |
| relatório V3 de integridade | 2026-07-11 | coincide com bytes atuais | `PRESERVED` | evidencia o snapshot atual, sem provar sozinho a transição anterior |
| SaimonOS | termo da auditoria | nenhuma fonte localizada | `NOT_FOUND` | Saimon deve indicar fonte/alias se o conceito for relevante |
| Tubarão/Contramedida como entidade de domínio | Declarativa/projeções | papel conceitual, não entidade implementada | `REQUIRES_DECISION` | falta classificação formal na genealogia técnica |
| Declarativa PDF original | referências FI-0/Vault | artefato não localizado | `NOT_FOUND` | requer fonte estável ou hash fornecido por Saimon |
| GateDecision, Release e Incident | plano FI-2B | Parte 2 não iniciada | `REQUIRES_DECISION` | implementação suspensa até decisão posterior; não criada nesta WorkOrder |

## Decisões ainda reservadas a Saimon

1. Significado formal da sigla SCR.
2. Retorno ou rejeição definitiva dos estados térmicos.
3. Contrato de recoverability e fronteira com lifecycle/epistemic state.
4. Destino do clone divergente no Vault.
5. Fonte e papel de SaimonOS.
6. Classificação de Tubarão/Contramedida.
7. Proveniência estável da Declarativa original.
