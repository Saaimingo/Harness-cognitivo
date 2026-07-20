# 03 — Comparação Técnica: EvoMemory, MEC e Harness Cognitivo

## Baselines comparados

| Sistema | Snapshot | Natureza |
|---|---|---|
| EvoMemory Core | `main` `4f66ebf1278ddde68369549c29e37bb58b405f48`, tag `v0.2.0` → `ec1f54bbcbe9ddf427ea751d5ade18de43be6268`; hardening não mesclado `a1af728ae0796cf22af3c0a6858d0dc5bae7426e` | Protótipo técnico histórico |
| MEC | Doc 1 SHA-256 `98780bf11c76c747cba2f0455d0c17284cfe315b42023d93e1f14880cc9161ca`; Doc 2 `8c6857952514caff44a8ea7371191b7339c8a78533950c1dc19a36b9efec3d59` | Especificação/guia de fabricação, não implementação atual |
| Harness Cognitivo | `master` e tag `fi-2b-part1-approved` → `a191a37d207e47d322297f7ce84c2dd211ca02d9` | Implementação canônica atual até FI-2B Parte 1 |

## Comparação por dimensão

| Dimensão | EvoMemory Core | MEC especificada | Harness atual | Conclusão |
|---|---|---|---|---|
| Problema central | Memória evolutiva local para LLMs/agentes | Linhagem causal e epistêmica de ideias, fontes, ações, evidências e consequências | Ciclo governado de projetos, tarefas, execução, revisão e testes | Domínios complementares, não substitutos |
| Unidade principal | `MemoryAtom` | Objeto cognitivo + eventos imutáveis + projeções | `Project`, `Plan`, `Task`, `Requirement`, `WorkOrder`, `ExecutionRun`, `Review`, `TestRun` | Não existe mapeamento 1:1 |
| Tipos | episodic, semantic, procedural, architectural, preference, trust, strategy, code | idea, question, hypothesis, observation, evidence, decision, experiment, outcome, lesson, artifact, assumption, constraint | Tipos de domínio de projeto/review, não tipos cognitivos | Evo e MEC provavelmente representam dimensões diferentes |
| Estados | active, deprecated, contradicted, uncertain, archived | lifecycle separado de epistemic state; status de relação também separado | Máquinas de estado por entidade | MEC é semanticamente mais rigorosa que Evo neste ponto |
| Relações | replaces, replaced_by, contradicts, updates, supersedes, supports, depends_on, relates_to | 16 relações tipadas, com ator, fonte/evidência, confiança, validade e status | Ligações por IDs entre entidades; transições explícitas | Vocabulário Evo é subconjunto imperfeito da MEC |
| Persistência | SQLite, migrations, stores, índices; UoW apenas no branch 0.2.1 | Event log SQLite canônico futuro; projeções reconstruíveis; FTS5 | Nenhuma persistência de domínio | Evo prova viabilidade local, mas não cumpre todo o contrato MEC |
| Event sourcing | Event Store append-only, porém projeções/atoms também recebem atualizações | Eventos são fonte de verdade; replay e zero mutação silenciosa | Contratos de evento mínimos, sem store | Necessário redesenho, não cópia direta |
| Supersessão | Cria novo atom, relações bidirecionais, deprecia anterior e registra evento | Evento/versão preserva tudo; `supersedes` é relação com status/evidência | Task/plan podem expressar estados próprios; MEC ausente | Padrão útil como experimento, sem equivalência canônica |
| Contradição | Heurística lexical + operação explícita; reduz confiança e marca uncertain | Evidências contrárias, relação contestada, inferência nunca confirmada automaticamente | Review/TestRun registram avaliação operacional, não crença | Heurística Evo deve permanecer auxiliar/histórica |
| Recência/decay | Fórmula determinística com pesos fixos; arquiva baixo valor | Score pode combinar muitos sinais; pesos exigem dataset; sem apagamento da fonte | Não implementado | Fórmula Evo pode ser baseline de experimento, não requisito |
| Consolidação | Worker rules-based cria atom/sugestão; não supersede automaticamente | Reflexão posterior, citada, reprodutível, em quarentena quando necessário | Não implementado | Convergência no princípio “proposta, não verdade” |
| Recuperação | exact + hashed-term vector + explicit graph + fusion; `trace` e `ignored` | FTS5 primeiro; expandir linhagem, evidências, contradições e construir cápsula | Protocolo MEC navegável apenas | Evo não oferece busca semântica real nem cápsula causal completa |
| Grafo | Travessia de relações explícitas | Relações temporais/causais auditáveis; Graphiti opcional por adapter | Não implementado | Graph Evo é deliberadamente não cognitivo |
| Vetores | Feature hashing lexical em 192 dimensões | Embeddings opcionais após baseline, sem bloquear texto | Não implementado | “Vector index” do Evo não deve ser descrito como embedding semântico |
| API/cliente | FastAPI e endpoints locais | CLI, MCP e API opcional; clientes por contrato | CLI mínima/estrutura de módulos, sem MEC API | API Evo é histórica; contrato MEC deve ser novo |
| Governança | Roteador por regras e avisos de risco; sem enforcement de ações | Aprovação humana, trust, quarantine, menor privilégio | SG-0, GRN, ESQ, CTP e WorkOrder | Harness é muito mais forte em autoridade e ciclo operacional |
| Revisão independente | Não é domínio central | Obrigatória em risco relevante | `Review` e política de independência implementadas | Capacidade canônica do Harness, não do Evo |
| Evidência | source, trace e eventos; não há Evidence aggregate causal completo | Evidência é objeto; supporting/contradicting; checksum e referência | `TestRun`/evidence hashes e CI para engenharia | Integração futura precisa preservar separação cognitivo×operacional |
| Testes | Suíte Python; hardening 0.2.1 acrescenta rollback/adversarial/smoke, mas PR não mesclada | Replay, migração, propriedade, adversarial, poisoning, restore | 534 testes no baseline integrado; CI Quality success | Não somar métricas entre sistemas; testes Evo não evidenciam Harness |
| Operação | Local, mono-usuário, sem auth, sem distribuído | Local-first e modular; fases posteriores cobrem operação/incidente | Até FI-2B Parte 1; Release/Incident não implementados | Parte 2 não deve importar operação do Evo |

## Capacidades sobrepostas

1. Modelos Pydantic tipados e políticas determinísticas.
2. Origem/proveniência, confiança e relações explícitas.
3. Preservação do antecedente em supersessão e contradição.
4. SQLite local, migrations e event log.
5. Busca lexical antes de depender de embeddings.
6. Trace de recuperação e registro de razões.
7. Consolidação como sugestão, não promoção automática.
8. Separação entre modelo/cliente e memória persistente.

Essas sobreposições sustentam ancestralidade conceitual possível, mas não provam compatibilidade de código.

## Elementos potencialmente reaproveitáveis — somente como referência

| Elemento EvoMemory | Valor potencial | Condição mínima antes de considerar |
|---|---|---|
| Protocols pequenos para stores | Ajuda a separar domínio/aplicação/infra | Redesenhar nomes e operações conforme agregados MEC |
| SQLite Unit of Work do branch 0.2.1 | Demonstra rollback de operação multi-write | Auditar PR não mesclada, concorrência, migrations e event-source invariants |
| Testes de rollback/adversariais | Catálogo de falhas úteis | Reescrever contra contratos Harness/MEC; não copiar como prova |
| `trace` e `ignored` | Transparência de seleção e ancestrais excluídos | Incluir citations, lineage, epistemic warnings e budget report MEC |
| Replacement suggestion conservadora | Evita supersessão automática | Exigir ator, fonte, evidência, relação/status e decisão humana |
| Decay idempotente | Bom padrão de política pura | Remover pesos canônicos sem dataset e preservar recoverability |
| Migrations/health/schema version | Base operacional testável | Reconciliar com FI-3, backup, restore e replay obrigatório |

Nenhum item acima autoriza migração. Ação permitida futura seria escrever ADR/proposta e testes de contrato antes de qualquer implementação.

## Decisões já substituídas ou limitadas

- Odysseus como fundação do produto não é a arquitetura atual; permanece origem histórica.
- SCR como extensão leve de Odysseus não é módulo do repo atual.
- O index vetorial Evo é fallback lexical/hash, não solução semântica canônica.
- O graph Evo não é grafo cognitivo/temporal.
- Pesos de score do Evo são decisão de protótipo; MEC exige avaliação por dataset.
- FastAPI, endpoints e schema `MemoryAtom` do Evo não são contratos do Harness.
- Branch 0.2.1, PR #2 e seus 20 caminhos modificados não fazem parte de `main` do Evo.
- Workflows/payloads temporários removidos no histórico devem permanecer apenas evidência histórica.

## Riscos de duplicação

1. Implementar segundo event store no Harness sem decidir se o Evo é referência ou descarte.
2. Criar enums “memory status” que misturem lifecycle, epistemic state e thermal state.
3. Chamar hashing lexical de embeddings e medir capacidade inexistente.
4. Duplicar relação de linhagem em objetos, eventos e graph sem fonte única.
5. Misturar evidência de teste operacional com evidência cognitiva.
6. Reutilizar heurística lexical de contradição como decisão de verdade.
7. Reproduzir API FastAPI antes de estabilizar comandos/eventos/ports.
8. Contar testes Evo como cobertura da MEC/Harness.

## Lacunas da implementação atual do Harness

- Não há objetos cognitivos MEC.
- Não há lifecycle/epistemic/relation status da MEC.
- Não há event store, replay, projeções, FTS5, cápsula de contexto ou lineage service.
- Não há persistência/repositórios do domínio de projeto.
- Não há vínculo formal entre `ExecutionRun`/`Review`/`TestRun` e eventos cognitivos.
- Não há GateDecision, Release ou Incident; a Parte 2 está suspensa por esta auditoria.
- Não há política canônica sobre thermal state/recoverability/decay.
- Não há dataset de recall nem benchmark contra Hermes/Odysseus/EvoMemory.
- Não há ADR genealógico que registre o que foi herdado e o que foi recusado.

## Recomendação técnica

Tratar EvoMemory como `HISTORICAL_PROTOTYPE` congelado. Antes de FI-3 ou de qualquer MEC executável, produzir uma ADR de fronteira que: (1) fixe os agregados e as três dimensões de estado; (2) defina eventos/replay; (3) mapeie ou rejeite cada conceito Evo; (4) escolha baseline de busca; (5) estabeleça testes adversariais e de migração. Não copiar código durante a reconciliação documental.
