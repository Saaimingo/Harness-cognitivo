---
tipo: historico_evidencial
status: candidate_for_review
proprietario: Saimon
corte_temporal: 2026-07-23T23:59:59-03:00
branch_base: master
base_sha: a191a37d207e47d322297f7ce84c2dd211ca02d9
substitui_fontes: false
autoriza_implementacao: false
---

# Histórico Evidencial do Harness Cognitivo

> Reconstrução cronológica do projeto desde sua origem documentada até o corte de 23 de julho de 2026. Este documento organiza evidências, declarações soberanas e lacunas. Ele não apaga fontes anteriores, não transforma inferência em fato e não autoriza a FI-2B Parte 2.

## 1. Finalidade

Este histórico existe para que uma pessoa ou agente que não viveu as conversas consiga compreender:

1. de onde o projeto veio;
2. por que cada mudança ocorreu;
3. quais partes foram realmente implementadas;
4. quais decisões são vigentes;
5. quais conceitos surgiram depois do último commit canônico;
6. o que continua pendente;
7. onde cada afirmação pode ser verificada.

Ele resolve um problema identificado durante os testes com agentes externos: documentos corretos, mas produzidos em momentos e contextos diferentes, estavam sendo lidos como se possuíssem a mesma finalidade e a mesma autoridade.

## 2. Regra de prova

Cada marco recebe uma classe de evidência:

- **GIT**: commit, tag, branch, PR, tree ou CI reproduzível.
- **DOC**: documento preservado, relatório, ADR, manifesto ou especificação identificável.
- **OWNER**: declaração soberana de Saimon, ainda que a conversa original não esteja versionada no Git.
- **INFERENCE**: continuidade conceitual forte, mas sem ponte documental direta.
- **GAP**: ausência de evidência suficiente.

Uma classe não substitui outra. O Git prova o estado versionado. Documentos normativos governam requisitos e decisões no seu escopo. Declarações de Saimon governam direção e intenção, mas devem ser consolidadas para se tornarem consumíveis por agentes futuros.

## 3. Linha do tempo consolidada

### 3.1 16 de junho de 2026: estudo do Odysseus

**Classe:** GIT + DOC.

O projeto começou estudando o Odysseus como possível fundação. A investigação identificou que ele já possuía agentes, memória, RAG, banco vetorial, integrações e scheduler. Isso reduziu a necessidade de construir imediatamente uma arquitetura paralela ampla.

**Decisão da época:** observar a base e não alterar seu código antes de entender o problema real.

**O que foi preservado:**

- ideia de harness como camada coordenadora;
- agentes especializados;
- memória e recuperação de contexto;
- integrações por ferramentas;
- necessidade de governança acima do modelo.

**Lacunas:**

- não existe snapshot reproduzível do Odysseus auditado naquele dia;
- não existe benchmark preservado que permita repetir a comparação.

**Evidência histórica:** repositório `Saaimingo/saimon-ai-lab`, branch `docs/odysseus-scr-foundation`, conforme relatório forense `HC-DOC-ORIGIN-01`.

### 3.2 16 de junho de 2026: nascimento do SCR

**Classe:** GIT + DOC.

O SCR surgiu como uma camada proposta sobre o Odysseus, com foco em memória evolutiva, governança, segurança, genealogia e rastreabilidade. Ele não era, naquele momento, um sistema independente.

**Características registradas:**

- origem de informações;
- uso e recência;
- relações e derivações;
- recuperabilidade;
- separação entre governança e segurança;
- regra inicial de observar e classificar antes de apagar.

**Transformação posterior:** parte desses princípios reapareceu no EvoMemory, na MEC e nos eixos SG-0, GRN e CTP.

**GAP:** a expansão original da sigla SCR não foi encontrada nas fontes auditadas.

### 3.3 Depois de 16 de junho: estudo do Hermes

**Classe:** OWNER + DOC parcial.

Saimon declara ter estudado o Hermes como alternativa mais compatível com seu estilo de trabalho. Os documentos históricos da MEC comprovam que Hermes foi analisado como referência e possível cliente do Harness, mas não preservam a conversa comparativa nem a data exata da preferência.

**Decisão vigente:** Hermes é referência e executor possível, não base normativa nem dependência arquitetural obrigatória.

### 3.4 22 de junho de 2026: EvoMemory Core

**Classe:** GIT + DOC.

O repositório `Saaimingo/evomemory-core` materializou um protótipo de memória evolutiva local e baseada em regras.

**Capacidades demonstradas:**

- `MemoryAtom`;
- SQLite;
- event store;
- recall;
- relações;
- contradição;
- supersessão;
- decay;
- consolidação conservadora;
- rastreabilidade transacional.

**Versões verificadas:**

- `v0.1.1`, commit `a5cf3d0`;
- `v0.2.0`, commit `ec1f54b`;
- hardening `0.2.1` em branch não integrada, commit `a1af728`.

**Decisão vigente:** EvoMemory é ancestral técnico e fonte de aprendizado, não implementação canônica da MEC nem fonte automática de código ou schema.

**INFERENCE:** a continuidade SCR → EvoMemory é conceitualmente forte, mas a ponte textual direta não foi encontrada.

### 3.5 11 de julho de 2026: formalização da MEC

**Classe:** DOC + OWNER.

Foram produzidos os documentos históricos numerados, começando pela Especificação Mestra da Memória Evolutiva Causal e pelo Manual de Fabricação.

A mudança central foi sair de uma memória de entradas isoladas para uma infraestrutura de objetos e eventos capaz de preservar:

- origem;
- contexto antes, durante e depois;
- decisões;
- evidências;
- relações;
- contradições;
- consequências;
- linhagem;
- motivo pelo qual o sistema sabe algo.

A MEC foi posicionada como subsistema cognitivo. Ela nunca representou sozinha o Harness completo.

**GAP histórico:** os documentos MEC não registraram explicitamente a transição nominal e técnica EvoMemory → MEC.

### 3.6 11 de julho de 2026: expansão para o Harness completo

**Classe:** DOC + OWNER.

Os documentos 04 a 08 expandiram o projeto para um Harness completo, governando:

- intenção;
- planejamento;
- arquitetura;
- execução;
- revisão independente;
- testes reais;
- evidências;
- entrega;
- operação;
- memória causal;
- autoridade humana;
- modelos plugáveis.

**Decisão:** o produto deixou de ser uma simples extensão de um harness generalista e passou a possuir arquitetura própria e soberana.

**Definição que emergiu:** o modelo é o motor. O Harness é o sistema operacional, executivo e defensivo ao redor dele.

### 3.7 15 de julho de 2026, 12:40 -03:00: FI-0

**Classe:** GIT.

Commit: `b3700c1976c2468c0ad69ba7db4b6ec62bdd8aea`.
Tag: `fi-0-approved`.

A FI-0 estabeleceu a fundação do repositório:

- Python 3.12;
- empacotamento e dependências;
- qualidade inicial;
- testes baseline;
- logging e observabilidade básica;
- estrutura para evolução incremental.

Commit documental de fechamento: `d0f6451e1daf0dea0430e0baed1898014d599c22`.

**Estado:** aprovada.

### 3.8 15 de julho de 2026, 13:15 a 13:35: FI-1

**Classe:** GIT + DOC.

Commit principal: `dac3509ee7063cb6605963a08626ed622b2e8892`.
Tag aprovada: `fi-1-approved`, referência consolidada `0b15b5f`.

A FI-1 implementou o protocolo cognitivo inicial:

- `ContextRequest`;
- `ContextCapsule`;
- `ContextItem`;
- `CognitiveObject`;
- `EvidenceReference` com checksum;
- vocabulários controlados;
- validação de IDs;
- separação entre `object_type` e `trust_level`;
- glossário;
- protocolo MEC documentado.

Commits de fechamento e reconciliação: `85307929...` e `f70bd3fe...`.

**Estado:** aprovada.

### 3.9 15 a 16 de julho de 2026: FI-2A

**Classe:** GIT + DOC.

Commits principais:

- `f528edaaba2b1464dbb1ad1904ad7eb524953657`;
- `0ff954efd84c6898a52532accc264008681fbc70`;
- `eadf4c89cb2ba5bb80234261be682ef488fe9bb0`;
- `9d99834640e6d35192f7624b7f51f2102e644e49`;
- `79bce9c3b83454d9c188a61e3e8d21c382a97750`;
- fechamento `be1236ff7885b950cfdd7cdac50c3f9531be48f9`.

Tag: `fi-2a-approved`.

A FI-2A implementou:

- `Project`;
- `Requirement`;
- `Plan`;
- `Task`;
- `WorkOrder`;
- estados, transições e políticas puras;
- erros de domínio;
- testes arquiteturais e de invariantes.

Também formalizou quatro eixos transversais:

- SG-0, segurança operacional;
- ESQ, engenharia de software e qualidade estrutural;
- GRN, governança de regras de negócio;
- CTP, promoção de conversa para projeto.

**Estado:** aprovada.

### 3.10 16 a 20 de julho de 2026: FI-2B Parte 1

**Classe:** GIT + CI + DOC.

Branch: `feat/fi-2b-part1`.

Commits relevantes:

- `61d58caa48403d771f9436c2ea3c6741dd748628`;
- `7325efafd3bfde09045da771b10f0c153b31915d`;
- `5b392e1735298bc95636a7eadbe15e57d9c81f41`;
- `4b04d0255f5f9fb5d2667bc6d15dec9c4df05b72`;
- `093695540c0f637cca5040f1d0b054bfdad65f5c`;
- HEAD final `ccaa0a55aaa78a08d8f4588e8ec3a5669f84b738`.

Merge: `a191a37d207e47d322297f7ce84c2dd211ca02d9`.
Tag: `fi-2b-part1-approved`.
PR: `#1`.

Implementado:

- `ExecutionRun`;
- `Review`;
- `TestRun`;
- transições explícitas;
- invariantes de construção, desserialização e mudança de estado;
- testes adversariais;
- evidências reconciliadas;
- workflow remoto de qualidade.

Validação:

- 534 testes aprovados;
- Ruff aprovado;
- Ruff format aprovado em 49 arquivos;
- Mypy sem erros em 31 arquivos;
- `git diff --check` limpo;
- workflow da feature `29747690315`, sucesso;
- workflow da master `29751012597`, sucesso.

**Fora do escopo:** `GateDecision`, `Release`, `Incident`, persistência, event store, executor real, integrações e FI-3.

**Estado:** integrada e aprovada.

### 3.11 20 de julho de 2026: suspensão da FI-2B Parte 2

**Classe:** OWNER + DOC.

Antes de continuar para `GateDecision`, `Release` e `Incident`, Saimon determinou uma auditoria de origem e uma reconciliação documental. A implementação da Parte 2 foi suspensa, não cancelada.

**Regra vigente:** não iniciar FI-2B Parte 2 antes do fechamento conceitual e da Bíblia.

### 3.12 20 de julho de 2026: auditoria forense de origem

**Classe:** DOC + GIT.

WorkOrder: `HC-DOC-ORIGIN-01`.

Resultados registrados:

- 42.705 arquivos inventariados;
- 1.387 Markdown;
- zero erros de inventário;
- Odysseus → SCR comprovado;
- EvoMemory comprovado como protótipo;
- SCR → EvoMemory → MEC classificado como continuidade forte, mas com pontes documentais ausentes;
- implementação atual reconhecida como própria e soberana;
- divergências entre Git, Obsidian e documentos antigos identificadas.

### 3.13 20 de julho de 2026: reconciliação documental

**Classe:** GIT + DOC.

Branch: `docs/hc-documentary-reconciliation`.
Commit remoto: `19352a47fd6fcc66edab85a155599b6c9f6b9aca`.
Mensagem: `docs: reconcile canonical Harness documentation`.

A reconciliação adicionou, entre outros:

- registro de fontes e autoridade;
- ADRs históricos;
- materiais forenses preservados;
- matriz de reconciliação;
- rascunho inicial não canônico da Bíblia;
- correção do estado pós-merge da FI-2B Parte 1.

A auditoria final rejeitou esse pacote por duas classes de problema:

1. pilares futuros ainda ausentes;
2. estados administrativos desatualizados.

### 3.14 20 a 22 de julho de 2026: correção local bloqueada

**Classe:** OWNER + DOC de continuidade; GIT não disponível neste clone.

Commit local no ambiente anterior: `0a3fc1960e7afb3a60976c32c3c04f1d54c4ce3d`.
Parent: `19352a47fd6fcc66edab85a155599b6c9f6b9aca`.

A correção foi revisada internamente, mas o push foi bloqueado pelo ambiente.

**Estado exato:**

- o commit não está na `master`;
- não está no clone atual;
- não deve ser recriado, alterado, amendado, rebaseado ou resetado;
- a ação futura definida é push normal no ambiente original, seguido de auditoria documental final.

### 3.15 22 de julho de 2026: Hermes como executor contextualizado

**Classe:** OWNER + evidência operacional local, ainda não versionada.

Foi preparado o workspace local:

`C:\Users\saimi\Projects\harness-hermes-work`

O Hermes foi conectado ao OpenCode Go e configurado como executor contextualizado, não autoridade do projeto.

Configuração validada:

- modelo principal inicialmente `qwen3.7-plus`;
- modelos auxiliares para visão, compressão e extração;
- aprovações manuais;
- escrita de memória e skills sob aprovação;
- delegação limitada;
- memória persistente em `MEMORY.md`;
- perfil persistente em `USER.md`;
- `HERMES.md` local para limites operacionais.

O repositório permaneceu sem alterações rastreadas; apenas `HERMES.md` e `input-context/` ficaram não rastreados.

### 3.16 22 e 23 de julho de 2026: falha documental revelada por testes com agentes

**Classe:** OWNER + observação operacional.

Qwen e MiMo receberam missões de leitura documental. Os testes revelaram:

- confusão entre FI-2B Parte 1 e reconciliação documental;
- reabertura de decisões já fechadas;
- classificação errada de fontes auxiliares como canônicas;
- inferência indevida sobre documentos ausentes;
- dificuldade para entender relações que estavam claras apenas para quem viveu o projeto.

**Conclusão:** o problema não era apenas capacidade do modelo. O pacote documental exigia uma camada explícita de cronologia, autoridade, estado e precedência.

### 3.17 23 de julho de 2026: evolução conceitual para plataforma

**Classe:** OWNER, ainda aguardando consolidação formal.

Saimon fechou a natureza atual do produto:

- `Harness Cognitivo` permanece como nome provisório;
- o sistema completo é uma plataforma cognitiva agêntica soberana;
- o harness de execução é seu núcleo operacional;
- a MEC é o subsistema cognitivo e de memória causal;
- modelos, provedores, ferramentas e clientes são intercambiáveis.

Novos conceitos foram classificados como refinamentos de setores existentes, não produtos paralelos:

- hooks ou âncoras executáveis;
- detector de repetição e ausência de progresso;
- watchdog passivo;
- roteamento cognitivo adaptativo;
- observabilidade de troca de modelos e custo;
- sala de deliberação técnica por papéis;
- inteligência técnica externa;
- laboratório efêmero de quarentena;
- promoção controlada;
- registro evolutivo de confiança;
- testes visuais;
- autodiagnóstico e reparo supervisionado;
- resposta a tickets e incidentes empresariais;
- contenção emergencial reversível;
- supervisão remota futura.

**Exclusão de novo escopo:** descoberta causal formal não vira módulo obrigatório agora. A causalidade já é propriedade da MEC e pode ser aprofundada quando existirem dados suficientes.

### 3.18 23 de julho de 2026: decisão de produzir a Bíblia diretamente

**Classe:** OWNER.

Saimon determinou que a consolidação não deve depender de agentes externos tentando remontar a história por fragmentos. O arquiteto conceitual que acompanhou o projeto deve produzir:

1. este histórico evidencial;
2. a Bíblia de construção de ponta a ponta;
3. uma branch documental revisável no GitHub;
4. posteriormente, espelhamento no Obsidian.

**Razão:** reduzir trabalho circular, impedir interpretações livres e dar a qualquer agente futuro uma fonte organizada e versionada.

## 4. Estado atual no corte

### Implementação canônica

- branch: `master`;
- HEAD: `a191a37d207e47d322297f7ce84c2dd211ca02d9`;
- FI-0 aprovada;
- FI-1 aprovada;
- FI-2A aprovada;
- FI-2B Parte 1 aprovada;
- 534 testes aprovados na integração;
- FI-2B Parte 2 não iniciada.

### Documentação em reconciliação

- branch remota conhecida: `docs/hc-documentary-reconciliation`;
- commit remoto: `19352a47...`;
- correção local anterior: `0a3fc196...`, ainda não publicada;
- auditoria documental final pendente.

### Estado conceitual

- escopo conceitual fechado com as capacidades definidas até 23 de julho de 2026;
- novas ideias devem, por padrão, refinar setores existentes;
- somente uma finalidade genuinamente nova pode ampliar o produto;
- Bíblia precede retomada da implementação.

## 5. Ordem de continuidade

1. revisar este histórico e a Bíblia candidata;
2. publicar ambos em branch documental, sem merge automático;
3. confrontar com fontes históricas 01–08 e com a reconciliação pendente;
4. corrigir conflitos sem apagar evidência;
5. realizar revisão independente;
6. publicar SHA final de auditoria;
7. obter decisão soberana de Saimon;
8. integrar documentação aprovada;
9. espelhar no Obsidian;
10. somente então retomar a FI-2B Parte 2.

## 6. Regras permanentes derivadas da história

1. Ausência de evidência não pode ser preenchida por narrativa plausível.
2. Documento histórico não deve ser apagado porque ficou desatualizado.
3. Estado implementado e intenção normativa são autoridades complementares.
4. Agente novo deve receber cronologia e mapa de autoridade antes de interpretar o projeto.
5. Implementação não avança enquanto o contrato documental essencial estiver contraditório.
6. Segurança, qualidade, governança, evidência e memória são transversais.
7. O modelo nunca é soberano.
8. Saimon mantém a decisão final sobre direção, aprovação e promoção.

## 7. Fontes principais

- commits e tags do repositório `Saaimingo/Harness-cognitivo`;
- PR #1;
- `docs/architecture/ARCHITECTURAL_MAP.md`;
- `docs/architecture/FI2B_PLAN.md`;
- `docs/MEC_PROTOCOL.md`;
- documentos SG-0, ESQ, GRN e CTP;
- relatórios FI-0, FI-1, FI-2A e FI-2B Parte 1;
- evidências `evidence/fi2b-part1/`;
- commit documental `19352a47...`;
- relatório forense `HC-DOC-ORIGIN-01`;
- checkpoint mestre de continuidade;
- declarações soberanas de Saimon consolidadas até 23 de julho de 2026.

## 8. Limites deste documento

- Não substitui os originais 01–08.
- Não declara o commit local `0a3fc196...` publicado.
- Não declara a reconciliação documental aprovada.
- Não autoriza FI-2B Parte 2.
- Não prova conversas que ainda não foram versionadas.
- Deve ser atualizado quando novas evidências primárias forem incorporadas.
