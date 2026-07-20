# 04 — Conflitos, Duplicações e Lacunas

## Conflitos materiais

| ID | Fontes | Conflito observado | Classificação | Impacto | Tratamento recomendado — não aplicado |
|---|---|---|---|---|---|
| C-01 | `MANIFESTO_DE_INTEGRIDADE_DOS_ORIGINAIS.md` vs arquivos atuais e `RELATORIO_DE_INTEGRIDADE_V3.md` | O manifesto inicial registra tamanhos/hashes antigos (`a54bad…`, `ecd0ba…` etc.); os oito arquivos atuais conferem exatamente com os hashes/tamanhos do relatório V3 (`98780b…`, `8c6857…` etc.). | Manifesto inicial `CONFLICTING`; V3 `IMPLEMENTATION_EVIDENCE` para o snapshot atual | Alegação de imutabilidade fica ambígua sem cadeia de versões | Preservar ambos; criar manifesto versionado que explique a restauração e a supersessão, sem reescrever originais |
| C-02 | Git refs/tags vs `README.md`, `docs/reports/INDICE_MESTRE.md`, `RELATORIO_FI2B_PARTE1.md` na `master` atual | Git prova merge `a191a37`, tag e 10 commits da branch; documentos versionados ainda dizem PR aberta/Draft, 9 commits, nenhum merge/tag e estado `READY_FOR_REVIEW/COMMIT`. | Docs atuais `CONFLICTING`; refs/commit/tag `CANONICAL_CURRENT` | Usuário pode tomar decisão operacional com estado obsoleto apesar de estar no repo canônico | WorkOrder documental separada para reconciliar estado pós-merge; não alterar nesta auditoria |
| C-03 | Vault pós-merge vs docs da master | `Progresso FI-2B` e `Governança e Rastreabilidade` registram corretamente merge/tag/CI, mas são projeções; o nível normativo que elas citam está desatualizado textualmente. | Vault `DERIVED_PROJECTION`; Git metadata `CANONICAL_CURRENT` | Fonte secundária está factualmente melhor que parte da documentação primária | Registrar que “repo canônico” significa estado Git/código; cada documento ainda pode conflitar |
| C-04 | `docs/sources/DECLARATIVA_ORIGINAL.md` e relatórios FI-0 | O PDF “Declarativa Harness Cognitivo.pdf” é referido por caminho pessoal fora do repo/Vault, mas nenhum PDF foi encontrado no inventário acessível. | `UNKNOWN_REQUIRES_SAIMON` | Origem conceitual não é independentemente reprodutível; caminho expõe ambiente local | Saimon deve fornecer o artefato autorizado ou hash/fonte estável; depois higienizar referências por WorkOrder |
| C-05 | Declaração de Saimon vs corpus | “Hermes foi alternativa preferida” não possui nota/commit/conversa no corpus. Docs MEC só provam estudo e referência. | `UNRESOLVED_HYPOTHESIS` | Genealogia pode apresentar inferência como fato | Registrar decisão retrospectiva de Saimon e, se existir, anexar conversa/data/benchmark |
| C-06 | Declaração de Saimon vs repos | SCR→EvoMemory→MEC tem continuidade temporal e conceitual, mas EvoMemory não contém “SCR” e os Docs MEC não contêm “EvoMemory”. | `UNRESOLVED_HYPOTHESIS` | Não se sabe o que foi herdado deliberadamente ou recriado independentemente | Criar ADR genealógico com mapa aceita/rejeita/transforma por conceito |
| C-07 | SCR, EvoMemory, MEC | Estados térmicos, status operacionais Evo e estados lifecycle/epistemic MEC são três taxonomias diferentes. | `CONFLICTING` se tratadas como aliases | Pode gerar estado impossível e lógica de decay misturada a verdade/validade | Manter dimensões separadas até decisão de domínio |
| C-08 | Git fonte atual vs SQLite futuro | FI-1 diz Git normativo; Doc 1 prevê event log SQLite como fonte do domínio cognitivo após implementação e Obsidian como projeção. | `UNRESOLVED_HYPOTHESIS`, não conflito temporal imediato | A transição de autoridade pode criar dupla verdade | Definir gate e plano de migração de fonte da verdade antes de FI-3 |
| C-09 | Decisão “repo fora do OneDrive” no diário vs Vault atual | O Vault contém um clone completo `Projetos/harness-cognitivo`, inclusive `.git`, `.venv`, caches e fonte. | `CONFLICTING` operacional | Confusão entre repo canônico e projeção; OneDrive/cache/ACL; enorme ruído forense | Saimon decide se clone permanece, vira snapshot identificado ou é removido em WorkOrder própria; nenhuma movimentação agora |
| C-10 | “MEC” | Corpus define MEC como “Memória Evolutiva Causal”; a expressão “Motor Evolutivo Cognitivo” não ocorre. | `UNKNOWN_REQUIRES_SAIMON` para o termo alternativo | Expansão errada mudaria escopo | Fixar glossário; não usar “motor evolutivo cognitivo” como sinônimo sem autorização |
| C-11 | Diário do Vault | Entradas pós-merge foram adicionadas depois de um marcador “Última atualização” e de texto “novas entradas acima/abaixo”, criando ordem editorial ambígua. | `CONFLICTING` leve | Timeline humana pode ser lida fora de ordem | Reestruturar diário por ordem cronológica em reconciliação, preservando texto histórico |
| C-12 | EvoMemory `main` vs branch 0.2.1/PR #2 | Arquitetura 0.2.0 documenta não atomicidade; branch 0.2.1 a corrige, mas segue não mesclada. | `HISTORICAL_PROTOTYPE` com variantes | Citar 0.2.1 como estado atual de `main` seria falso | Sempre indicar ref; decidir se arquiva/fecha o protótipo em outra missão |
| C-13 | Clone `Projetos/harness-cognitivo` dentro do Vault vs GitHub | O clone local está em `d11f983`, anterior à reconciliação/merge; `docs/reports/INDICE_MESTRE.md` já está modificado no working tree e há `nul` não rastreado. O README desse clone tem 0 bytes. | `DERIVED_PROJECTION` divergente | Não pode ser usado como checkout atual nem como espelho limpo da master | Preservar como observado e decidir destino em WorkOrder específica; não resetar/corrigir automaticamente |

## Duplicações e projeções

| Grupo | Exemplares | Natureza | Risco |
|---|---|---|---|
| Originais 01–08 e derivados | `Originais/01…08`; oito notas homônimas em `Memória/Fontes Base` | Originais preservados + projeções com frontmatter/links | Edição da derivada pode parecer alteração normativa; hashes históricos divergem |
| Documentos repo e notas do projeto | `Projetos/harness-cognitivo/docs/*` vs `Projetos/Harness Cognitivo/*` | Clone Git + projeção Obsidian administrativa | Estados podem divergir, como ocorreu após merge |
| Relatório FI-2B | repo `docs/reports/...` e Vault `Projetos/Harness Cognitivo/relatorios/...` | Evidência versionada + cópia/projeção | Ambas podem parecer atuais com conteúdos diferentes |
| Harness repo dentro e fora do Vault | clone no Vault, mirror temporário de auditoria e repositório remoto | Implementação/projeção/cópia de custódia | Hash/branch não identificados pelo caminho sozinho |
| EvoMemory branches de teste | nove branches `test/tree-api-do-not-use*` quase idênticas a main | Projeções experimentais | Aumentam superfície histórica sem valor de produto aparente |
| Eterno-FC | oficial, laboratório, cópia antiga e `.next`/`node_modules` | Outro projeto e artefatos derivados | Termos genéricos como “replay”, “segurança”, “MEC” ou “SCR” geram falsos positivos |

## Lacunas documentais da genealogia

1. Expansão da sigla SCR.
2. Conversa/nota que iniciou SCR antes ou em 16/06.
3. Registro de avaliação do Hermes e critérios de preferência.
4. Registro explícito que liga SCR ao repositório EvoMemory.
5. Registro explícito que liga EvoMemory aos Docs MEC.
6. ADR que formaliza a recusa de harness generalista de terceiro.
7. Definição precisa de “soberano” e “construído do zero”.
8. Proveniência completa da Declarativa PDF e do perfil funcional original.
9. Significado/fonte de SaimonOS.
10. Classificação formal de Tubarão/Contramedida na arquitetura atual.

## Lacunas técnicas do estado canônico

- MEC é especificada, mas ainda não implementada como domínio/persistência.
- Event store, replay, projections, FTS5, lineage e context capsule inexistem.
- GateDecision, Release e Incident não existem; FI-2B Parte 2 está suspensa.
- Falta contrato entre evidência cognitiva e `TestRun`/`Review`/`ExecutionRun`.
- Falta política de thermal state/recoverability/decay.
- Falta benchmark reproduzível contra EvoMemory, Odysseus, Hermes ou alternativas.
- Falta estratégia de importação: a regra atual corretamente proíbe migração automática.
- Falta política de retenção para logs/evidências e para artefatos gerados dentro do Vault.

## Limitações da auditoria

- Duas árvores `.pytest_cache` negaram leitura à identidade padrão usada na busca textual. A enumeração forense final, somente leitura e autorizada, conseguiu cobri-las; o manifesto final registra zero erros. Nenhuma ACL foi alterada.
- Arquivos removidos de Git foram examinados por histórico, mas conteúdos binários/payloads temporários não foram executados.
- Busca “semântica” foi feita por famílias conceituais, leitura de contexto, links e equivalências; não foi usado modelo de embeddings sobre o Vault.
- Conversas não materializadas no Vault/repositórios não puderam ser auditadas.
- Issues/PRs foram lidas pela fonte remota; mirrors Git preservam refs e commits, não todos os metadados sociais.

## Questões reservadas a Saimon

1. A genealogia SCR→EvoMemory→MEC deve ser declarada oficialmente mesmo sem ponte contemporânea?
2. Qual artefato comprova a etapa Hermes?
3. Os estados térmicos pertencem à MEC futura?
4. EvoMemory deve ser arquivado como protótipo ancestral, mantido como laboratório ou apenas referenciado?
5. O clone dentro do Vault é intencional?
6. Qual fonte contém SaimonOS?
7. É autorizado reconciliar a documentação pós-merge da master em WorkOrder posterior?
