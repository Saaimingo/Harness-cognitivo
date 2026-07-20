---
tipo: registro_governanca_documental
status: proposed_for_internal_review
workorder: HC-DOC-REC-01
data: 2026-07-20
base_canonica: a191a37d207e47d322297f7ce84c2dd211ca02d9
---

# Registro canônico de fontes e autoridade

## Finalidade

Este registro define como determinar autoridade, estado, preservação e conflito no Harness Cognitivo. Ele governa a reconciliação documental; não altera código, não inicia fase e não transforma rascunhos em normas.

## Classes de fonte

| Classe | Autoridade e uso | Limite |
|---|---|---|
| Código e Git do Harness | Fonte do estado implementado: tree, histórico, branches, commits, tags e merges | Não prova sozinho intenção normativa nem resultado de execução |
| Commits e tags aprovados | Marcos técnicos imutáveis do snapshot aprovado | Uma tag identifica um snapshot; não torna toda descrição histórica eternamente atual |
| Originais normativos históricos 01–08 | Corpus normativo histórico fornecido por Saimon; requisitos e arquitetura de origem | Não devem ser editados silenciosamente e não provam que algo já foi implementado |
| ADRs posteriores | Evolução controlada, renomeação, expansão, rejeição ou supersessão de decisões | Devem citar fontes, escopo, decisor, data e consequência |
| Documentos operacionais versionados | Estado de fase, progresso, relatórios, índice, CI, merge e tag | São mutáveis e devem ser reconciliados com as refs/evidências atuais |
| Obsidian | Memória, projeção navegável e espaço documental | Não é código canônico; clone, cache ou nota no Vault não substitui o remoto Git |
| Relatórios forenses | Evidência derivada de um método e snapshot declarados | Não são originais normativos nem decisão soberana por si sós |
| Conversas | Fonte histórica citável quando preservada e identificada | Não são automaticamente normativas; instruções efêmeras não substituem ADR/WorkOrder |
| Declarações explícitas de Saimon | Decisão soberana dentro do escopo declarado | Para durabilidade e auditabilidade, devem ser registradas em WorkOrder, ADR ou decisão assinada |
| Testes, CI e logs | Evidência de comportamento de um SHA/ambiente identificados | Não substituem requisito, revisão independente ou autorização soberana |

## Estado implementado canônico

O estado implementado é determinado por uma ref Git identificada, seu SHA completo e o conteúdo do tree. Em 2026-07-20, antes desta reconciliação:

- `master` local e `origin/master`: `a191a37d207e47d322297f7ce84c2dd211ca02d9`;
- tag anotada `fi-2b-part1-approved`: resolve para o mesmo merge;
- branch histórica `feat/fi-2b-part1`: preservada em `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738`;
- FI-2B Parte 1: integrada e encerrada;
- FI-2B Parte 2: não iniciada e suspensa durante a reconciliação documental.

A branch `docs/hc-documentary-reconciliation` parte dessa master, mas só se torna um novo marco documental após revisão, commit, push e auditoria previstos na WorkOrder.

## Originais 01–08

Os Docs 01–08 são preservados como originais normativos históricos. Uma decisão posterior pode `RENAMED`, `EXPANDED` ou `SUPERSEDED` parte de seu conteúdo, mas deve fazê-lo por adendo, nova versão ou ADR, mantendo o original intacto e citável.

O manifesto de hashes atual identifica os bytes observados; não resolve por si só a divergência entre o manifesto inicial e o V3.

## Regras de conflito

1. Para a pergunta “o que está implementado?”, prevalecem tree/ref Git identificados e evidência do mesmo SHA.
2. Para a pergunta “qual decisão arquitetural vigora?”, prevalece a decisão soberana mais recente formalizada e aplicável, com preservação da anterior como histórico.
3. Um documento operacional factualmente incompatível com refs verificadas é marcado `CONFLICTING` e corrigido; não se altera a ref para fazê-la coincidir com o texto.
4. Similaridade conceitual não cria equivalência, herança de código ou compatibilidade.
5. Ausência de fonte não autoriza preencher lacuna por inferência. Usar `REQUIRES_DECISION` ou `NOT_FOUND`.
6. Idade não determina obsolescência. Escopo, decisão explícita, evidência e cadeia de substituição determinam o tratamento.
7. Conflito material sem decisão soberana permanece explícito; não deve ser “harmonizado” silenciosamente.
8. Toda alegação de CI, merge, PR ou tag deve citar identificador/ref verificável e o SHA auditado.

## Substituição, supersessão e preservação

- `PRESERVED`: conceito e significado continuam vigentes.
- `RENAMED`: nome mudou, com equivalência explicitamente declarada; não presumir equivalência total.
- `EXPANDED`: o conceito anterior permanece, acrescido de escopo/invariantes.
- `SUPERSEDED`: decisão posterior ocupa seu lugar para o escopo declarado; a fonte anterior continua histórica.
- `HISTORICAL_ONLY`: preservado para genealogia/evidência, sem efeito normativo atual.
- `REQUIRES_DECISION`: prova insuficiente ou escolha soberana pendente.
- `CONFLICTING`: fontes incompatíveis sem resolução válida.
- `NOT_FOUND`: conceito ou fonte não foi localizado no corpus auditado.

Nenhuma substituição permite apagar o documento anterior. A cadeia mínima é: fonte anterior, decisão nova, data, decisor, escopo, justificativa e impacto.

## Decisões históricas formalizadas nesta reconciliação

- [ADR-HIST-001 — Odysseus e SCR](../adr/history/ADR-HIST-001-odysseus-e-scr-como-origem.md)
- [ADR-HIST-002 — Hermes](../adr/history/ADR-HIST-002-hermes-como-referencia-compativel.md)
- [ADR-HIST-003 — Harness próprio](../adr/history/ADR-HIST-003-harness-proprio-e-soberano.md)
- [ADR-HIST-004 — EvoMemory](../adr/history/ADR-HIST-004-evomemory-prototipo-ancestral-da-mec.md)
- [ADR-HIST-005 — papel futuro de Odysseus e Hermes](../adr/history/ADR-HIST-005-papel-futuro-odysseus-hermes.md)

## Evidência derivada preservada

Os relatórios da [HC-DOC-ORIGIN-01](../forensics/HC-DOC-ORIGIN-01/PRESERVATION_MANIFEST.md) e o [pacote do clone divergente](../forensics/HC-DOC-REC-01/vault-clone-d11f983/README.md) são evidência derivada e não normativa.

## Alterações e aprovações

Mudança material neste registro exige revisão documental e decisão de Saimon. Este arquivo, enquanto estiver com `status: proposed_for_internal_review`, é proposta controlada e não autoriza merge, fase, migração ou implementação.
