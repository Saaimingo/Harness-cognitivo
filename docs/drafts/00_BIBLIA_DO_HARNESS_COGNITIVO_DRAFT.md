---
tipo: rascunho_estrutura_biblia
status: draft_non_canonical
workorder: HC-DOC-REC-01
data: 2026-07-20
substitui_originais: false
---

# Bíblia do Harness Cognitivo — rascunho inicial não canônico

> Este arquivo é somente estrutura de trabalho. Não substitui os originais 01–08, não declara consolidação concluída e não autoriza implementação. Toda seção incompleta contém marcador explícito.

## Como ler este rascunho

Cada afirmação futura deverá ser marcada como:

- **História** — o que uma fonte ou experimento registrou em seu contexto;
- **Decisão vigente** — decisão formal aplicável hoje;
- **Hipótese** — proposta ainda sem decisão/evidência suficiente;
- **Implementação** — comportamento demonstrado por tree/ref e evidência do mesmo SHA.

Fonte de autoridade: [Registro canônico de fontes e autoridade](../governance/00_REGISTRO_CANONICO_DE_FONTES_E_AUTORIDADE.md).

## 1. Identidade, propósito e soberania

- **História:** Odysseus foi a primeira base considerada; SCR propôs uma camada de memória e governança.
- **Decisão vigente:** o Harness é próprio, soberano e independente de harness/modelo externo obrigatório.
- **PENDENTE:** incorporar definição operacional aprovada de “soberano”, sem apagar a herança conceitual.

Fontes: ADR-HIST-001, ADR-HIST-003, Docs históricos 04–08.

## 2. Genealogia e fronteiras

### 2.1 Odysseus e SCR

- **História:** origem documentada em 2026-06-16.
- **Decisão vigente:** referência histórica, sem dependência obrigatória.
- **PENDENTE:** significado da sigla SCR.

### 2.2 Hermes

- **História:** referência técnica nos Docs 01–02 e preferência retrospectiva declarada por Saimon.
- **Decisão vigente:** fonte de estudo, sem dependência obrigatória.
- **PENDENTE:** localizar nota/benchmark contemporâneo, se existir.

### 2.3 EvoMemory e MEC

- **História:** EvoMemory é protótipo técnico ancestral da MEC.
- **Decisão vigente:** não é implementação canônica nem fonte automática de código/schema.
- **PENDENTE:** mapa detalhado aceita/rejeita/transforma antes da FI-3/MEC executável.

Fontes: [relatórios forenses](../forensics/HC-DOC-ORIGIN-01/PRESERVATION_MANIFEST.md) e ADRs históricos 001–005.

## 3. Princípios constitucionais

### 3.1 SG-0

- **Decisão vigente:** menor privilégio, autorização explícita, fail closed e rastreabilidade de ações destrutivas.
- **PENDENTE:** exemplos normativos consolidados por classe de risco.

### 3.2 ESQ

- **Decisão vigente:** contratos explícitos, separação de camadas, testes e evidência reproduzível.
- **PENDENTE:** critérios de exceção e dívida técnica.

### 3.3 GRN

- **Decisão vigente:** regras de negócio como políticas verificáveis e rastreáveis.
- **PENDENTE:** ligação formal completa SCR → GRN além do ADR histórico.

### 3.4 CTP

- **Decisão vigente:** conversa pode originar trabalho, mas promoção exige contexto, decisão e rastreabilidade.
- **PENDENTE:** pipeline implementável e fronteira com memória cognitiva.

## 4. Arquitetura vigente

- **Implementação:** FI-0, FI-1, FI-2A e FI-2B Parte 1 integradas.
- **Implementação:** entidades atuais incluem Project, Requirement, Plan, Task, WorkOrder, ExecutionRun, Review e TestRun.
- **Decisão vigente:** Git/código identificam o estado implementado.
- **PENDENTE:** mapa atualizado do tree após esta reconciliação documental.

## 5. MEC — Memória Evolutiva Causal

- **História/norma:** Docs 01–03 especificam objetos, eventos, relações, estados epistêmicos, busca e projeções.
- **Implementação:** MEC executável, event store, replay, FTS5, lineage e cápsula de contexto ainda não existem no Harness atual.
- **PENDENTE:** limites entre tipos cognitivos, lifecycle, epistemic state e thermal state.
- **PENDENTE:** contrato entre evidência cognitiva e evidência operacional.

## 6. Ciclo de projeto, execução e evidência

- **Implementação:** ExecutionRun, Review e TestRun existem desde FI-2B Parte 1.
- **Decisão vigente:** revisão independente e evidência precedem promoção.
- **PENDENTE:** GateDecision, Release e Incident; FI-2B Parte 2 não iniciada.

## 7. Persistência, projeções e recuperação

- **História:** EvoMemory demonstra SQLite/event log como protótipo.
- **Decisão vigente:** não copiar contratos Evo; projetar contra MEC/Harness.
- **PENDENTE:** autoridade futura do event store, migração, backup, restore, replay e transição em relação ao Git.

## 8. Agentes, modelos e clientes

- **Decisão vigente:** modelos e clientes são intercambiáveis por contratos e não são fonte de verdade automática.
- **PENDENTE:** adapters, autoridade por papel e limites de execução real.

## 9. Segurança, governança e operação

- **Decisão vigente:** SG-0, ESQ, GRN e CTP são eixos transversais.
- **PENDENTE:** Release/Incident e integrações operacionais.

## 10. Evidência, revisão e aprovação soberana

- **Decisão vigente:** testes/CI provam um snapshot; revisor independente e Saimon mantêm papéis distintos.
- **PENDENTE:** taxonomia única de evidência e política de retenção.

## 11. Matriz de preservação e supersessão

Referência inicial: [Matriz de reconciliação conceitual](../reconciliation/01_MATRIZ_DE_RECONCILIACAO_CONCEITUAL.md).

- **PENDENTE:** converter somente decisões aprovadas em texto normativo consolidado.
- **PENDENTE:** manter anexos com conflitos e fontes substituídas.

## 12. Apêndices planejados

1. Inventário dos originais 01–08 e hashes.
2. Genealogia documentada e lacunas.
3. ADRs e cadeia de supersessão.
4. Glossário controlado.
5. Mapa de implementação por commit/tag.
6. Riscos, hipóteses e decisões soberanas pendentes.

## Gate para qualquer versão canônica futura

Este rascunho só poderá evoluir para candidato canônico após:

- revisão interna independente;
- resolução explícita ou preservação formal de cada conflito material;
- validação de links, fontes e hashes;
- comparação com os originais 01–08 sem alteração silenciosa;
- auditoria final do SHA publicado;
- decisão soberana expressa de Saimon.
