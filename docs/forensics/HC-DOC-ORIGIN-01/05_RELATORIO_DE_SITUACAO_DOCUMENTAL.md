# 05 — Relatório de Situação Documental

## Resultado executivo

A genealogia central é **plausível e parcialmente comprovada**, mas não pode ser canonizada integralmente ainda. Há prova direta de Odysseus→SCR, do protótipo EvoMemory, da especificação MEC e da implementação própria Harness. Faltam pontes contemporâneas SCR→EvoMemory, EvoMemory→MEC e o registro comparativo que levou de Hermes/terceiros ao Harness próprio.

O estado implementado canônico permanece `Saaimingo/Harness-cognitivo`, `master` `a191a37d207e47d322297f7ce84c2dd211ca02d9`, tag `fi-2b-part1-approved`. Nenhuma fonte histórica foi usada para alterar escopo ou código.

## Custódia e método

- Vault: `C:/Users/saimi/OneDrive/Documents/Obsidian Vault`, acesso somente leitura.
- GitHub: leitura pelo conector GitHub e mirrors bare temporários fora dos repositórios de origem.
- Repositórios principais: `Saaimingo/saimon-ai-lab`, `Saaimingo/evomemory-core`, `Saaimingo/Harness-cognitivo`.
- Busca: nomes exatos, famílias regex, contexto de linhas, títulos, frontmatter, tags, WikiLinks, backlinks e vizinhança conceitual.
- “Busca semântica”: leitura por equivalência de conceitos (por exemplo, thermal state↔recência/decay; regimento interno↔GRN), sem embeddings sobre o Vault.
- Git: todas as refs disponíveis nos mirrors, commits, tags, trees e arquivos removidos; issues/PRs relevantes consultados remotamente.
- Saída: somente esta pasta de auditoria; nenhum arquivo do Vault ou dos repos de origem foi escrito.
- Custódia auxiliar: os mirrors e o gerador do manifesto permanecem em `tmp/hc-doc-origin-01` para reprodutibilidade; sua exclusão destrutiva exige autorização específica e não foi executada.

## Cobertura do Vault

| Métrica | Resultado |
|---|---:|
| Arquivos enumerados | 42.705 |
| Markdown | 1.387 |
| Erros no manifesto final | 0; duas subárvores `.pytest_cache` negaram a busca padrão, mas foram cobertas na enumeração forense somente leitura autorizada |
| PDFs autorais encontrados no Vault enumerado | 0 |
| Canvas encontrados no recorte autoral | 0 |
| Manifesto per-file | `00_MANIFESTO_FORENSE_DO_VAULT.md` |

Cada linha do manifesto registra caminho relativo, título, extensão, bytes, timestamps UTC, SHA-256, frontmatter, tags, links, backlinks, anexos, projeto provável e relevância. Datas de arquivo são indícios do filesystem/OneDrive, não prova autoral. A enumeração final cobriu as duas subárvores de cache por leitura autorizada sem alterar ACL. Dois arquivos reais chamados `nul` exigiram leitura por caminho estendido do Windows e foram hasheados sem renomeação.

O volume é dominado por artefatos não autorais: `.venv`, `.git`, caches, `.next`, dependências e três projeções do Eterno-FC. O corpus útil do Harness concentra-se em `Memória/Fontes Base`, `Memória/Fontes Base/Originais`, `Projetos/Harness Cognitivo` e no clone `Projetos/harness-cognitivo`.

## Resultado da busca integral no Vault

| Conceito | Arquivos fora do Eterno-FC | Leitura |
|---|---:|---|
| Odysseus | 3 | Referências técnicas nos Docs MEC 1–2 e derivada |
| SCR como sigla isolada | 0 | Ocorrências anteriores por substring eram falsos positivos |
| Hermes | 4 | Referência/cliente nos Docs MEC 1–2 e derivadas |
| EvoMemory | 0 | A origem está no GitHub, não no Vault |
| MEC como sigla | 32 | Núcleo conceitual amplamente documentado |
| Harness Cognitivo | 48 | Arquitetura, operação e projeções atuais |
| SaimonOS | 0 | Fonte não encontrada |
| Tubarão | 7 | Perfil, Declarativa, papéis e glossários |
| Contramedida | 2 | Perfil/Manifesto; papel conceitual |
| memória evolutiva | 16 | Docs MEC, derivados e registros |
| memória causal (frase exata) | 0 | O corpus usa “Memória Evolutiva Causal” |
| memória persistente | 12 | Especificação, arquitetura e registros operacionais |
| memória do dia | 0 | Não encontrada |
| thermal state | 0 | Só aparece no repo histórico SCR, não no Vault |
| recoverability | 0 | Só aparece no repo histórico SCR |
| genealogia | 0 | O Vault usa principalmente “linhagem” |
| linhagem | 18 | MEC, arquitetura e CTP |
| ancestral/ancestor | 3 | Cápsula/contexto e pacote de merge |
| origem | 31 | Fontes, PIC, MEC e rastreabilidade |
| derivação | 2 | Presente, mas menos frequente que relações concretas |
| rastreabilidade | 20 | Princípio transversal |
| grafo | 19 | Especificação e arquitetura futura |
| RAG | 8 | Referência tecnológica, sem implementação atual |
| banco vetorial | 5 | Futuro/opcional |
| governança | 33 | GRN e documentos transversais |
| regimento interno | 0 | O termo aparece no repo SCR, não no Vault |
| segurança | 39 | SG-0, arquitetura e execução |
| guardrails | 5 | Declarativa/glossário |
| evidência | 53 | Conceito dominante de auditoria/qualidade |
| auditoria | 21 | Relatórios e governança |
| revisão independente | 11 | Docs 4–8 e planejamento |
| agentes | 25 | Arquitetura, papéis e integração |
| modelos | 21 | Plugabilidade e separação de autoridade |
| execução | 53 | Motor, FI-2B e documentação operacional |
| contexto antes/durante/depois | 11 | Cadeia cognitiva e de execução |

O resultado semântico mais importante é a equivalência transformada “genealogia”→“linhagem” e “regimento interno”→“GRN”. Ausência literal não significa ausência do conceito; já ausência de EvoMemory/SCR/SaimonOS impede afirmar que o Vault contém essas pontes.

## Situação dos repositórios

### `Saaimingo/saimon-ai-lab`

- Branch `main` contém apenas README mínimo.
- Branch `docs/odysseus-scr-foundation` em `8bbac05f4045c0f57d24b9875dc7f45be0d71043` contém 15 commits de 16/06/2026.
- Sem tags.
- Prova direta: Odysseus como fundação observada; SCR como extensão; memória evolutiva, estados térmicos, recoverability, ancestor IDs, genealogia e separação governança/segurança.
- Classificação: `HISTORICAL_ORIGIN`.

### `Saaimingo/evomemory-core`

- `main` `4f66ebf1278ddde68369549c29e37bb58b405f48`.
- Tags: `v0.1.1` → `a5cf3d0…`; `v0.2.0` → `ec1f54b…`.
- Branch `feature/0.2.1-hardening` `a1af728…`; PR #2 aberta/Draft, não mesclada.
- PR #3 fechada, não mesclada; workflows/payloads temporários foram removidos no histórico.
- Nove branches `test/tree-api-do-not-use*`, quase todas apontando para main.
- Issue #1 acompanha hardening 0.2.1.
- Classificação: `HISTORICAL_PROTOTYPE`; branch 0.2.1 é variante não integrada.

### `Saaimingo/Harness-cognitivo`

- `master` `a191a37d207e47d322297f7ce84c2dd211ca02d9`.
- Feature preservada `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738`.
- Tag anotada `fi-2b-part1-approved` resolve ao merge `a191a37…`.
- PR #1 fechada por merge; refs Git são evidência primária.
- Implementação atual: domínio puro até FI-2B Parte 1; MEC executável/persistência ainda não existem.
- Classificação: código/refs `CANONICAL_CURRENT`; testes/CI/evidence `IMPLEMENTATION_EVIDENCE`; README/índice/relatório pré-merge `CONFLICTING`.

### Outros repositórios de Saimon

| Repositório | Resultado da triagem | Classificação |
|---|---|---|
| `Eterno-FC` | Simulador de futebol; termos genéricos causam falsos positivos, sem linhagem técnica do Harness | `UNRELATED` |
| `jose`, `jose_base` | Vazios ou sem conteúdo relacionado observado | `UNRELATED` |
| `Matrix` | Repositório privado/minimal observado, sem evidência relacionada no material acessível | `UNKNOWN_REQUIRES_SAIMON` |

## Classificação das fontes relevantes

| Fonte | Categoria | Fundamentação |
|---|---|---|
| Git refs, código e tags de `Harness-cognitivo` no snapshot `a191a37` | `CANONICAL_CURRENT` | Estado implementado provisoriamente declarado canônico e verificado |
| Testes, workflow Quality e evidence versionada do Harness | `IMPLEMENTATION_EVIDENCE` | Demonstram comportamento/integração, não substituem requisitos |
| Docs de arquitetura do Harness já aprovados no Git | `CANONICAL_CURRENT` para o escopo que não conflita com refs | Normas versionadas atuais, sujeitas a inconsistências factuais identificadas |
| README, índice e relatório FI-2B pré-merge na master | `CONFLICTING` | Contradizem merge/tag/CI atuais |
| Todo `saimon-ai-lab/projetos/odysseus-scr/` | `HISTORICAL_ORIGIN` | Origem documentada da hipótese Odysseus+SCR |
| Decisão de usar Odysseus como fundação do produto final | `SUPERSEDED_DECISION` | Era a hipótese de 16/06; a arquitetura e implementação atuais são próprias |
| `evomemory-core` main/tags/código | `HISTORICAL_PROTOTYPE` | Protótipo real, não componente canônico atual |
| Evo branch 0.2.1, PR #2 e testes novos | `HISTORICAL_PROTOTYPE` | Hardening não mesclado |
| Oito branches Evo `test/tree-api-do-not-use-2…9` apontando a `main` | `DUPLICATE` | Refs redundantes sem conteúdo distinto no snapshot |
| Evo workflows/payloads removidos | `HISTORICAL_PROTOTYPE` | Artefatos temporários preservados só pelo Git |
| Docs originais 01–08 no Vault | `HISTORICAL_ORIGIN` | Fontes conceituais/normativas preservadas, mas não alteram automaticamente o escopo atual |
| Oito notas derivadas em `Memória/Fontes Base` | `DERIVED_PROJECTION` | Projeções declaradas dos originais |
| `MANIFESTO_DE_INTEGRIDADE_DOS_ORIGINAIS.md` inicial | `CONFLICTING` | Hashes/tamanhos anteriores não correspondem aos bytes atuais |
| `RELATORIO_DE_INTEGRIDADE_V3.md` | `IMPLEMENTATION_EVIDENCE` | Hashes/tamanhos conferem com os oito arquivos atuais |
| Notas `Progresso`, `Governança`, `Índice`, diário e pacotes no Vault | `DERIVED_PROJECTION` | Navegação/estado administrativo; não são Git canônico |
| Declaração Saimon sobre Hermes e pontes genealógicas | `UNRESOLVED_HYPOTHESIS` até registro formal | Autoridade do proprietário é válida, mas a missão pede correlação documental |
| Declarativa PDF ausente | `UNKNOWN_REQUIRES_SAIMON` | Há registro/caminho, não artefato auditável |
| Clone `Projetos/harness-cognitivo` no Vault | `DERIVED_PROJECTION` + `IMPLEMENTATION_EVIDENCE` | Cópia local com Git/venv/caches; não confundir com remoto |
| `.venv`, caches, `.next`, dependências, binários gerados | `UNRELATED` | Artefatos runtime/build, inventariados por completude |
| Eterno-FC e suas três árvores | `UNRELATED` | Projeto distinto |

## Situação canônica recomendada para reconciliação

```text
1. Git commit/ref/tag do Harness = estado implementado atual
2. Documentos versionados no mesmo repo = normas, salvo conflito factual explícito
3. Evidências/CI = prova do snapshot indicado
4. Originais 01–08 = patrimônio conceitual e requisitos históricos a reconciliar
5. Obsidian = projeção/navegação
6. saimon-ai-lab e evomemory-core = origem/protótipo, sem migração automática
7. Declarações de Saimon = autoridade soberana, mas devem ganhar registro de decisão para completar a linhagem
```

## Plano recomendado de reconciliação documental

1. Saimon decide/assina a genealogia mínima e responde às lacunas Hermes, SCR, EvoMemory, SaimonOS e Tubarão.
2. Criar um ADR genealógico versionado no Harness, sem incorporar código antigo.
3. Reconciliar README, índice e relatório FI-2B com merge/tag/CI atuais em WorkOrder separada.
4. Criar manifesto de origem versionado para Docs 01–08, explicando a sequência dos dois conjuntos de hashes sem editar os originais.
5. Registrar a Declarativa por hash/localização estável ou declarar formalmente sua indisponibilidade.
6. Definir política para clone/ambientes/caches dentro do Vault.
7. Produzir um mapa de decisão EvoMemory: `preservar`, `transformar`, `rejeitar`, `avaliar depois`, conceito por conceito.
8. Só então revisar o pacote FI-2B Parte 2. GateDecision/Release/Incident não dependem de copiar EvoMemory, mas sua rastreabilidade deve citar esta reconciliação.

## Ações que exigem autorização expressa de Saimon

- Canonizar a genealogia ou preencher retrospectivamente decisões ausentes.
- Declarar qualquer fonte superseded/obsoleta em sentido normativo.
- Alterar o Vault ou docs do repo.
- Mover/remover o clone, `.venv`, caches ou duplicatas.
- Incorporar a Declarativa ou outras conversas/fontes externas.
- Migrar/reutilizar código EvoMemory.
- Retomar FI-2B Parte 2.
- Excluir os artefatos temporários de auditoria depois que Saimon decidir que a reprodução não é mais necessária.

## Riscos residuais

1. A identidade padrão não lê duas subárvores `.pytest_cache`; a cobertura final exigiu contexto de leitura autorizado. A ACL permanece inalterada e pode afetar futuras reproduções comuns.
2. Metadados OneDrive não substituem data autoral/commit.
3. Documentos da master podem induzir estado operacional errado até reconciliação.
4. Originais têm duas gerações de hashes registradas; usar o manifesto inicial como atual é incorreto.
5. Ausência de conversa materializada impede provar preferências/decisões históricas.
6. Similaridade conceitual pode ser confundida com compatibilidade técnica.
7. O volume de artefatos derivados torna buscas ingênuas propensas a falsos positivos.
8. O clone do Harness dentro do Vault está em `d11f983`, com índice modificado e `nul` não rastreado; não é espelho limpo da master atual.

## Estado

`READY_FOR_DOCUMENTARY_RECONCILIATION`

Este estado não autoriza editar fontes, migrar código, retomar FI-2B Parte 2, criar branch/commit/push/PR/tag ou escrever a Bíblia definitiva.
