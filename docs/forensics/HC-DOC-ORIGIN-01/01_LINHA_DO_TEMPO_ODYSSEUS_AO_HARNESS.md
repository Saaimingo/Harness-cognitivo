# 01 — Linha do Tempo: de Odysseus ao Harness Cognitivo

## Escopo e regra de prova

Esta reconstrução separa três níveis: fato documentado, inferência por continuidade conceitual e declaração de Saimon ainda sem ponte documental. Datas de Git usam o timestamp do commit; datas de documentos usam a data declarada no próprio texto e, secundariamente, o metadado do arquivo. Antiguidade não implica obsolescência.

## Linha do tempo documentada

| Data | Marco | Evidência primária | Motivo/decisão registrada | Preservado | Transformado ou abandonado | Lacuna |
|---|---|---|---|---|---|---|
| 2026-06-16 | Pesquisa inicial no Odysseus | `Saaimingo/saimon-ai-lab`, branch `docs/odysseus-scr-foundation`, sequência `db4d106…8bbac05`; `00-visao-geral.md`; `01-auditoria-odysseus.md` | A hipótese de construir arquitetura ampla foi reduzida: Odysseus já tinha agentes, memória, RAG, ChromaDB, MCP, scheduler e integrações. Decisão: observar e não alterar seu código. | Plataforma existente como possível fundação; memória como principal lacuna. | Construção paralela ampla foi suspensa, não declarada inválida. | Não há benchmark preservado do Odysseus nem snapshot do código auditado. |
| 2026-06-16 | Nascimento do SCR | Mesmo branch; `projetos/odysseus-scr/README.md`; `02-memoria-evolutiva.md`; `03-governanca-vs-seguranca.md`; `04-origem-genealogia-e-rastreabilidade.md`; `06-roadmap-v1.md` | SCR era nome provisório de uma camada sobre Odysseus, não sistema independente: memória evolutiva, governança, segurança, classificação, genealogia e rastreabilidade. V1 deveria observar/classificar, sem apagar automaticamente. | Origem, uso, recência, relações, derivações, recuperabilidade, rastreabilidade e separação governança/segurança. | A implementação imediata foi adiada; `thermal state`, `recoverability` e `ancestor IDs` ficaram como proposta. | A expansão da sigla SCR não aparece nos arquivos auditados. |
| Após 2026-06-16, data não comprovada | Estudo do Hermes | Declaração atual de Saimon; Doc 1 MEC, linhas 809 e 872–875; Doc 2 MEC, linhas 577 e 838 | Saimon declara que Hermes foi estudado como alternativa mais próxima de suas preferências. Os documentos MEC comprovam estudo técnico e tratamento de Hermes como cliente/referência, mas não a preferência nem a data comparativa. | Acesso por contrato e independência de modelo/cliente. | Hermes deixa de ser candidato de produto e passa a referência/cliente potencial na MEC, segundo inferência. | Falta conversa, nota decisória, benchmark ou commit que registre a alternativa e o motivo da escolha. |
| 2026-06-22 | EvoMemory Core 0.1.1 e 0.2.0 | `Saaimingo/evomemory-core`, commits `a5cf3d0` e `ec1f54b`; tags anotadas `v0.1.1` e `v0.2.0`; README e `docs/architecture.md` | Protótipo local, rules-based, de memória evolutiva: `MemoryAtom`, SQLite, event store, recall, relações, contradição, supersessão, decay e consolidação conservadora. Integração com Odysseus era explicitamente fora do escopo. | Memória tipada, origem, confiança, importância, relações, rastreabilidade, retenção de antecessores e explicação do recall. | A proposta conceitual tornou-se código executável independente; `thermal state` virou `recency_score`/decay e estados operacionais, sem equivalência formal. | Nenhum arquivo do repo menciona SCR ou declara que EvoMemory é sua continuação. A ponte é inferência + declaração de Saimon. |
| 2026-06-22 | Hardening EvoMemory 0.2.1 | Branch `feature/0.2.1-hardening` em `a1af728`; PR #2 aberta e Draft; PR #3 fechada sem merge | Unit of Work SQLite para atomicidade de supersede/contradict, novos testes e smoke test. | Auditabilidade e consistência transacional. | Corrige limitação da 0.2.0, mas não entrou em `main`. | Estado é protótipo não integrado; branches temporárias e payloads removidos poluem a história. |
| 2026-07-11 | Surgimento formal da MEC | `01_ESPECIFICACAO_MESTRA_ORIGINAL.md` e `02_MANUAL_DE_FABRICACAO_ORIGINAL.md`; hashes atuais `98780bf…` e `8c68579…`; manifesto V3 | Harness é camada operacional externa e independente do modelo; MEC é o primeiro subsistema. O foco muda de memória de entradas para objetos/eventos, linhagem, evidência, tempo e consequência. | Proveniência, relações, contradições, recuperação, recência/utilidade, grafo, busca lexical primeiro e clientes por contrato. | Estados térmicos deixam de ser vocabulário canônico; entram estados de ciclo de vida, estados epistêmicos e status de relação separados. | “EvoMemory” não aparece nos documentos MEC; falta registro de derivação/renomeação e de quais partes do protótipo foram rejeitadas. |
| 2026-07-11 | Decisão por Harness próprio e expansão documental | Docs 4–8 originais, todos declarados consolidados em 11/07; `04_ARQUITETURA_GERAL_HARNESS_ORIGINAL.md`; `05_MOTOR_DE_EXECUCAO_ORIGINAL.md`; `06_PROTOCOLO_INTEGRACAO_ORIGINAL.md`; `07_MANUAL_FABRICACAO_HARNESS_ORIGINAL.md`; `08_PROMPT_MESTRE_IMPLEMENTACAO_ORIGINAL.md` | MEC é posicionada como plano cognitivo de um Harness completo que governa intenção, planejamento, execução, revisão, testes, entrega e operação. | MEC, rastreabilidade, revisão independente, autoridade humana, evidência e modelos plugáveis. | O produto deixa de ser extensão documentada de Odysseus e passa a arquitetura própria. | Não há ADR textual “rejeitar harness generalista de terceiro” nem comparação final Odysseus×Hermes×Harness. A soberania é coerente com os docs, mas o elo decisório é declaração de Saimon. |
| 2026-07-15 12:40 -03:00 | FI-0 | `Harness-cognitivo`, commit `b3700c1`; tag `fi-0-approved` | Fundação de projeto, dependências, qualidade e observabilidade. | Construção incremental e evidência. | Especificação começa a virar repositório executável. | Documentos atuais da master não registram a genealogia anterior. |
| 2026-07-15 13:15–13:35 | FI-1 | Commits `dac3509` até `0b15b5f`; tag `fi-1-approved` | Protocolo cognitivo, contratos básicos e regra Git normativo/Obsidian projeção. | Origem→antes→durante→depois, evidência e IDs. | MEC permanece documental; não há event store. | A Declarativa PDF original não está no repo/Vault auditado, apenas seu registro. |
| 2026-07-15 14:06–2026-07-16 21:22 | FI-2A | Commits `f528eda…be1236f`; tag `fi-2a-approved` | Entidades, transições e políticas puras; formalização SG-0, ESQ, GRN e CTP. | Governança, segurança e rastreabilidade transformadas em eixos explícitos. | Ênfase imediata passa do motor de memória para o domínio do ciclo de projeto. | Relação entre entidades do ciclo e futuros objetos cognitivos MEC ainda não implementada. |
| 2026-07-16 a 2026-07-20 | FI-2B Parte 1 | Branch `feat/fi-2b-part1`; commits `61d58ca…ccaa0a55`; merge `a191a37`; tag anotada `fi-2b-part1-approved` | Implementa `ExecutionRun`, `Review` e `TestRun`, políticas e testes adversariais; 534 testes; Quality de branch e master com sucesso. | Execução verificável, revisão independente, evidência e gates futuros. | Conceitos do motor completo ganham modelos de domínio, ainda sem persistência/integrações. | README, índice e relatório atuais da master ainda descrevem o estado pré-merge; isso é conflito documental, não de Git. |
| 2026-07-20 | Suspensão da Parte 2 para auditoria de origem | WorkOrder HC-DOC-ORIGIN-01 | Antes de GateDecision/Release/Incident, reconstruir a linhagem e reconciliar fontes. | Regra de não avançar sem contexto/evidência. | Planejamento existente fica suspenso, não descartado. | Decisões desta auditoria dependem de Saimon. |

## Verificação da genealogia declarada por Saimon

| Afirmação | Veredito probatório | Fundamentação |
|---|---|---|
| Odysseus seria a fundação inicial | **COMPROVADA** | O README do projeto SCR diz literalmente que a pesquisa usava Odysseus como fundação. |
| SCR buscava melhorar memória/governança | **COMPROVADA** | Vários arquivos de 16/06 descrevem memória evolutiva, genealogia, estados térmicos, recoverability e regimento interno. |
| Hermes foi alternativa mais aderente às preferências de Saimon | **DECLARAÇÃO DO PROPRIETÁRIO, NÃO CORROBORADA INTEGRALMENTE** | Hermes é referência técnica e cliente potencial nos Docs 1–2; não há documento da escolha/preferência. |
| EvoMemory foi protótipo técnico de memória evolutiva | **COMPROVADA** | README, código, tags, arquitetura e testes do repo o definem assim. |
| EvoMemory deriva diretamente do SCR | **INFERÊNCIA FORTE, NÃO PROVA DIRETA** | Continuidade temporal/conceitual existe, mas “SCR” não aparece no repo EvoMemory. |
| MEC evoluiu de EvoMemory | **INFERÊNCIA FORTE + DECLARAÇÃO DE SAIMON** | Há continuidade em tipos, relações, origem, recall, decay e SQLite; “EvoMemory” não aparece nos Docs MEC. |
| Houve decisão de não basear o produto em harness generalista de terceiros | **PARCIALMENTE CORROBORADA** | A arquitetura final é explicitamente externa, independente e própria; falta o registro da decisão comparativa. |
| Harness Cognitivo nasceu soberano e construído do zero | **PARCIALMENTE CORROBORADA** | Repositório próprio inicia em FI-0 e arquitetura declara identidade própria; “do zero” não deve significar ausência de herança conceitual ou dependências. |

## Genealogia mínima defensável

```text
Odysseus como fundação observada
  -> SCR como hipótese de extensão de memória e governança
  -> [ponte documental ausente]
  -> EvoMemory como protótipo técnico independente
  -> [ponte documental ausente]
  -> MEC como especificação causal, epistêmica e orientada a eventos
  -> Harness Cognitivo completo como arquitetura própria
  -> FI-0 / FI-1 / FI-2A / FI-2B Parte 1 implementadas
```

Essa cadeia não autoriza importar código antigo nem tratar conceitos semelhantes como equivalentes.
