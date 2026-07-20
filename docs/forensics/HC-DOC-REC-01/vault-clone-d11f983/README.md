---
tipo: pacote_forense_clone_divergente
status: preserved_read_only_export
workorder: HC-DOC-REC-01
observado_em: 2026-07-20
base_canonica_comparada: a191a37d207e47d322297f7ce84c2dd211ca02d9
---

# Pacote do clone divergente do Vault

## Regra de custódia

Este pacote foi produzido somente por leitura e exportação. O clone observado dentro do Vault não recebeu `reset`, `clean`, `pull`, `merge`, `rebase`, checkout, correção ou escrita. Depois da exportação, o estado foi lido novamente e permaneceu igual ao estado inicial descrito abaixo.

## Estado observado

| Campo | Valor |
|---|---|
| Branch | `feat/fi-2b-part1` |
| HEAD completo | `d11f983f701936a6b3e7fde68c81fba0699f1fcd` |
| Upstream | `origin/feat/fi-2b-part1` |
| Divergência da upstream | `+0 -0` |
| Arquivos staged | nenhum |
| Arquivo modificado | `docs/reports/INDICE_MESTRE.md` |
| Arquivo não rastreado | `nul` |

Saída estrutural preservada de `git status --porcelain=v2 --branch --untracked-files=all`:

```text
# branch.oid d11f983f701936a6b3e7fde68c81fba0699f1fcd
# branch.head feat/fi-2b-part1
# branch.upstream origin/feat/fi-2b-part1
# branch.ab +0 -0
1 .M N... 100644 100644 100644 3b4eaaa58592d736680c29a885ef867cc9fb4142 3b4eaaa58592d736680c29a885ef867cc9fb4142 docs/reports/INDICE_MESTRE.md
? nul
```

## Inventário dos arquivos divergentes

| Estado | Caminho no clone | Bytes | SHA-256 | Cópia neste pacote |
|---|---|---:|---|---|
| modificado | `docs/reports/INDICE_MESTRE.md` | 1.887 | `2bbf0053a279fc70ee9c2820d19946a1c68dc818bd0bc5d1645072af67f4c296` | `snapshots/working-tree/INDICE_MESTRE.md` |
| não rastreado | `nul` | 46 | `c2d0e87c31a3e90b8a697321a1b91146c3ecd5a6179bb2a65e1a6c8cf437a016` | `snapshots/untracked/untracked_nul.bin` |

O arquivo reservado do Windows `nul` foi copiado com o nome seguro `untracked_nul.bin`. O nome mudou apenas no pacote; tamanho, bytes e SHA-256 foram preservados.

## Diffs e hashes do pacote

| Artefato | Conteúdo | Bytes do arquivo | SHA-256 do arquivo |
|---|---|---:|---|
| `working-tree.patch.zip` | ZIP contendo `working-tree.patch`, a saída completa de `git diff --no-ext-diff --binary` contra `d11f983…` | 2.172 | `d1b95ae2e0e9543f9b8b0c16041369bb729df926f1af2db8ea65da1872e58542` |
| `cached.patch` | `git diff --cached --no-ext-diff --binary`; vazio porque não havia stage | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `conceptual-vs-canonical-master.patch.zip` | ZIP da comparação mecânica do índice divergente com o índice da master canônica no início desta WorkOrder | 2.797 | `f6da6710f9d460b6d24e41c5915652ac14dc8198d22bb1308760aca3eaeecf04` |

Verificação interna dos ZIPs:

| Entrada preservada | Bytes | SHA-256 da entrada |
|---|---:|---|
| `working-tree.patch` | 4.707 | `f24ae87461a60c0fbc4bd115eb3858dfd45de96f31d4877cb9c6f4fbe34f0676` |
| `conceptual-vs-canonical-master.patch` | 6.175 | `b3f2cbf88c4a455967bacc2a7cc36568b99aa5fa0a9382998a525d925ac71470` |

Nenhum patch binário adicional foi necessário: o arquivo modificado rastreado é texto. A cópia binária integral do arquivo não rastreado está em `snapshots/untracked/`.

## Comparação contra `d11f983…`

O `working-tree.patch` preservado dentro de `working-tree.patch.zip` mostra que apenas o índice rastreado diverge do HEAD. A mudança substitui o estado pré-merge por fatos pós-integração, incluindo merge `a191a37d…`, CI da master e tag `fi-2b-part1-approved`. O arquivo `nul` não existe no tree de `d11f983…`.

## Comparação conceitual contra a master canônica

No início de `HC-DOC-REC-01`, a master canônica estava em `a191a37d207e47d322297f7ce84c2dd211ca02d9`; o blob de seu índice era `d5a4c252507c2581cf8af54597d75288451403eb`. A master continha um índice operacional ainda pré-merge. A cópia divergente possuía fatos pós-merge mais recentes, mas também:

- estava em um checkout antigo e sujo;
- removia parte da navegação histórica;
- não tinha commit, revisão ou autoridade canônica;
- incluía um arquivo não rastreado de origem não determinada.

Conclusão: o conteúdo divergente é evidência/projeção útil, não deve ser adotado por cópia automática. Os fatos válidos são reconciliados na branch documental canônica, com preservação separada deste snapshot.

## Decisão pendente

O destino do clone dentro do Vault exige decisão expressa de Saimon. Este pacote não autoriza removê-lo, atualizá-lo ou convertê-lo em espelho.
