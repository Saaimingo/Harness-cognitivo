---
tipo: biblia_mestra
status: candidate_for_review
proprietario: Saimon
arquitetura_conceitual: Tubarao
corte_temporal: 2026-07-23T23:59:59-03:00
branch_base: master
base_sha: a191a37d207e47d322297f7ce84c2dd211ca02d9
substitui_originais: false
autoriza_implementacao: false
proxima_fase_autorizada: nenhuma
---

# Bíblia do Harness Cognitivo

> Mapa integral de construção da plataforma cognitiva agêntica soberana, desde a origem e o estado já implementado até a primeira versão completamente funcional.

## 0. Status, leitura e autoridade

Esta é uma **versão candidata para revisão**. Ela foi criada para consolidar o projeto em uma fonte única, navegável e verificável, sem apagar os documentos históricos que lhe deram origem.

Ela não:

- substitui silenciosamente os originais 01–08;
- declara a reconciliação documental concluída;
- incorpora o commit local `0a3fc196...`;
- autoriza a FI-2B Parte 2;
- transforma hipótese em requisito aprovado;
- permite merge sem auditoria e decisão soberana.

### 0.1 Marcadores usados

- **[IMPLEMENTADO]**: demonstrado por Git e evidência do mesmo estado.
- **[DECISÃO VIGENTE]**: direção ou regra já decidida por Saimon.
- **[CANDIDATO]**: consolidação proposta nesta Bíblia, aguardando revisão.
- **[FUTURO]**: capacidade planejada, ainda não implementada.
- **[HIPÓTESE]**: possibilidade sem compromisso atual.
- **[LACUNA]**: informação, ponte ou decisão ainda insuficiente.

### 0.2 Autoridade por domínio

1. **Saimon** é a autoridade soberana sobre direção, escopo, aprovação e promoção.
2. **Declarativa do Harness Cognitivo** preserva a visão fundadora, a intenção e a relação original entre humano, modelos e plataforma; ela orienta propósito, mas não prova implementação.
3. **Git, commits, tags, tree e CI** provam o estado implementado e versionado.
4. **Documentação normativa aprovada** governa requisitos, arquitetura e decisões no seu escopo.
5. **ADRs** registram decisões técnicas e suas consequências.
6. **Relatórios e evidências** provam acontecimentos e resultados, mas não são automaticamente normas futuras.
7. **Originais 01–08** são patrimônio normativo histórico e devem ser preservados.
8. **Checkpoint e input-context** preservam continuidade, mas não são canônicos automaticamente.
9. **HERMES.md** governa o comportamento operacional do Hermes no workspace local; não governa o produto.
10. **Conversas** podem conter decisões soberanas ainda não consolidadas; não devem permanecer como única fonte.

Quando duas fontes divergem, o conflito deve ser registrado. Nenhum agente pode resolvê-lo silenciosamente.

## 1. Identidade do sistema

### 1.1 Nome

**[DECISÃO VIGENTE]** `Harness Cognitivo` permanece como nome provisório do projeto e do produto até decisão específica de renomeação.

### 1.2 Natureza

**[DECISÃO VIGENTE]** O sistema completo é uma **plataforma cognitiva agêntica soberana**, comparável funcionalmente a um sistema operacional para agentes, modelos, ferramentas e projetos.

A relação entre os termos é:

- **Plataforma cognitiva agêntica soberana**: sistema completo.
- **Harness de execução**: núcleo operacional, executivo e defensivo da plataforma.
- **MEC, Memória Evolutiva Causal**: subsistema cognitivo e de memória causal.
- **LLM ou modelo**: motor intercambiável, nunca o sistema inteiro.

### 1.3 Definição consolidada

> O Harness Cognitivo é uma plataforma local-first, independente de modelos e orientada por autoridade humana, capaz de transformar intenção em projetos planejados, executados, revisados, testados, documentados, entregues, observados, reparados e evoluídos, preservando memória causal, evidência, segurança, custo, linhagem e reversibilidade.

## 2. Problema que a plataforma resolve

Ferramentas de IA atuais frequentemente:

- criam rápido, mas geram código frágil;
- alteram sem preservar contexto;
- confundem confiança com prova;
- executam e revisam o próprio trabalho;
- esquecem decisões entre sessões;
- não deixam trilha de evidência;
- aumentam escopo sem autorização;
- repetem tarefas sem perceber ausência de progresso;
- acessam ferramentas e credenciais com limites insuficientes;
- corrigem um erro provocando outro;
- dependem excessivamente de um único modelo ou provedor.

A plataforma existe para transformar capacidade de modelo em **trabalho governado, verificável e recuperável**.

## 3. Promessa central

A plataforma deve permitir que um usuário leigo, um profissional ou um desenvolvedor experiente trabalhe com agentes mantendo:

- qualidade de engenharia comparável a uma equipe sênior disciplinada;
- segurança proporcional ao risco;
- explicações compreensíveis;
- rastreabilidade de decisões;
- evidência verificável;
- capacidade de recuperar, revisar e corrigir;
- liberdade para trocar modelos e provedores;
- autoridade humana real.

Ela não promete erro zero. Ela promete reduzir improvisação indevida, limitar impacto, detectar falhas, bloquear propagação, recuperar estado e manter o humano soberano.

## 4. Escopo e fronteiras

### 4.1 Escopo conceitual fechado

**[DECISÃO VIGENTE]** O escopo conceitual está fechado com as capacidades definidas até 23 de julho de 2026.

Novas ideias devem passar por esta pergunta:

> A ideia cria uma finalidade genuinamente nova ou refina uma capacidade já existente?

- Se refina capacidade existente, entra no setor correspondente.
- Se cria finalidade genuinamente nova, exige decisão explícita de ampliação do produto.
- Se ainda não possui evidência ou maturidade, permanece como hipótese ou experimento.

### 4.2 O que não vira módulo novo agora

**Descoberta causal formal** não entra como módulo obrigatório. A causalidade já está presente na MEC por origem, relações, decisões, consequências, contradições e linhagem. Métodos formais de causal discovery poderão aprofundar a MEC quando existirem dados suficientes, diversos e bem instrumentados.

### 4.3 O que a plataforma não é

- não é somente memória;
- não é somente RAG;
- não é somente orquestrador de agentes;
- não é somente gerador de código;
- não é um modelo próprio obrigatório;
- não é ferramenta ofensiva;
- não é sistema que substitui autoridade humana;
- não é um conjunto aleatório de IAs conversando;
- não é produto que esconde custo, troca de modelo ou falha.

## 5. Princípios constitucionais

1. Saimon é a autoridade soberana.
2. Aprovação exige evidência verificável.
3. Declaração, confiança, reputação ou consenso não bastam.
4. Executor, revisor, testador e auditor possuem autoridades distintas.
5. Nenhum agente promove o próprio resultado.
6. Mudança posterior a aprovação invalida o veredito anterior.
7. Conteúdo externo é referência, nunca autoridade operacional automática.
8. Modelos e provedores são intercambiáveis.
9. Papéis vêm antes dos modelos.
10. Ausência de evidência deve ser declarada, não preenchida por narrativa plausível.
11. Fato, inferência, hipótese e ausência de evidência permanecem separados.
12. Ações devem ser explícitas, rastreáveis e reversíveis quando possível.
13. Segredos nunca entram em documentação, memória, logs ou respostas.
14. Segurança crítica não depende apenas da obediência do LLM.
15. O sistema deve falhar fechado em operações críticas.
16. Arquitetura não será distorcida para ocupar mais agentes.
17. A plataforma é construtiva e defensiva, nunca ofensiva contra terceiros.
18. Código desconhecido entra por quarentena e promoção controlada.
19. O usuário deve enxergar modelos, papéis, custos, escalonamentos e bloqueios.
20. O sistema deve saber parar quando não há progresso.

## 6. Arquitetura integral

A plataforma é composta por planos e eixos cooperantes.

### 6.1 Plano de intenção e interface

Responsável por receber e esclarecer:

- ideia;
- problema;
- objetivo;
- restrições;
- preferências;
- autoridade;
- critérios de sucesso.

Inclui chat, voz, CLI, interface visual e futuros canais remotos.

### 6.2 CTP, Chat-to-Project

Transforma conversa em trabalho formal:

```text
conversa livre
→ conceito
→ escopo
→ documentação candidata
→ aprovação humana
→ snapshot
→ pacote de promoção
→ projeto formal
```

O pacote deve preservar origem, autoria, decisões, requisitos, hashes e limites.

### 6.3 GRN, Governança de Regras de Negócio

Classifica e preserva:

- objetivos;
- processos;
- regras de negócio;
- requisitos;
- decisões;
- exceções;
- conflitos;
- vigência temporal.

As regras devem ser recuperáveis, versionadas e testáveis.

### 6.4 Arquitetura e planejamento

Converte intenção e regras em:

- arquitetura de domínio;
- entidades e relações;
- invariantes;
- contratos;
- plano;
- tarefas;
- dependências;
- caminho crítico;
- WorkOrders autorizadas.

### 6.5 Câmara de Deliberação Técnica

**[FUTURO]** Mecanismo pré-execução que reúne apenas os papéis necessários à tarefa.

Possíveis cadeiras:

- planejador;
- arquiteto de domínio;
- engenheiro de software;
- engenheiro de segurança;
- executor;
- testador;
- revisor funcional;
- revisor de domínio;
- guardião de regras;
- observador de custo e operação.

Ela não decide por votação simples. Ela resolve objeções técnicas por aderência à especificação, impacto futuro, evidência, testabilidade e reversibilidade.

Saída obrigatória:

- contrato técnico;
- abordagem escolhida;
- alternativas rejeitadas e motivos;
- componentes permitidos e proibidos;
- riscos;
- testes obrigatórios;
- evidências esperadas;
- critérios de interrupção;
- plano de rollback;
- condições de escalonamento humano.

Fluxo:

```text
sala de deliberação
→ contrato técnico e WorkOrder
→ autorização
→ execução
→ revisão
→ testes
→ evidências
→ GateDecision
```

### 6.6 Harness de execução

É o núcleo operacional que:

- recebe WorkOrder autorizada;
- escolhe executor suficiente;
- monta cápsula de contexto;
- limita ferramentas e permissões;
- executa;
- registra ações;
- preserva checkpoints;
- produz changeset;
- aciona revisão, testes e gates;
- interrompe quando necessário.

### 6.7 Roteador cognitivo adaptativo

**[FUTURO]** Seleciona papéis, modelos, ferramentas e níveis de capacidade conforme:

- risco;
- complexidade;
- contexto necessário;
- histórico de qualidade;
- custo;
- latência;
- disponibilidade;
- sensibilidade dos dados.

Regra:

> usar o executor mais simples que possua capacidade suficiente; escalar apenas diante de evidência de necessidade.

Toda troca deve ser observável:

- modelo anterior e novo;
- motivo;
- custo;
- atraso;
- falha que provocou escalonamento;
- resultado após a troca.

### 6.8 Ferramentas e integrações

A integração deve ser neutra de provedor e suportar, progressivamente:

- OpenAI;
- Anthropic;
- Google;
- OpenCode Go;
- Ollama;
- llama.cpp;
- endpoints OpenAI-compatible;
- CLIs como Codex, Claude Code, OpenCode e Hermes;
- GitHub, e-mail, calendário, mensageria e serviços empresariais.

Segredos ficam fora de Git, documentação e memória.

### 6.9 SG-0, segurança operacional

SG-0 atravessa todas as camadas:

- menor privilégio;
- autorização explícita;
- fail closed;
- escopo mínimo;
- isolamento;
- auditabilidade;
- rollback;
- interrupção;
- prevenção de exfiltração;
- proibição de ataque a terceiros.

### 6.10 Hooks ou âncoras

**[FUTURO]** Hooks são controles executáveis, não apenas instruções textuais.

Eles interceptam pontos críticos, por exemplo:

- escrita de arquivo;
- alteração de documento original;
- commit;
- push;
- troca de branch;
- instalação de dependência;
- acesso de rede;
- leitura de segredo;
- criação de skill;
- gravação em memória;
- promoção de artefato;
- avanço de fase;
- ultrapassagem de orçamento.

Um hook crítico deve estar fora da vontade decisória do modelo.

### 6.11 Loops de engenharia

A plataforma executará loops explícitos:

```text
descobrir
→ preparar
→ selecionar
→ executar
→ verificar
→ registrar
→ corrigir
→ parar
```

Cada loop deve possuir:

- objetivo;
- estado inicial;
- critério de progresso;
- orçamento;
- limite de tentativas;
- checkpoint;
- saída válida;
- condição de bloqueio;
- condição de intervenção humana.

### 6.12 Watchdog e ausência de progresso

**[FUTURO]** Supervisor passivo que não duplica trabalho enquanto o executor progride.

Monitora:

- liveness, se o agente está vivo;
- progress, se houve mudança verificável;
- compliance, se segue contrato e escopo;
- safety, se tentou ação proibida;
- cost, se custo cresce sem benefício;
- evidence, se surgiram provas novas;
- dependencies, se o caminho crítico está bloqueado.

Sinais de ausência de progresso:

- saída quase idêntica sem evidência nova;
- resposta à tarefa anterior;
- repetição de ferramenta sem mudança de estado;
- nenhuma alteração quando a tarefa exigia alteração;
- justificativa repetida;
- consumo de orçamento sem satisfação de requisito.

Ações graduais:

1. reformular instrução;
2. reconstruir cápsula de contexto;
3. abrir nova sessão;
4. trocar modelo;
5. reduzir escopo;
6. restaurar checkpoint;
7. convocar revisor;
8. bloquear e solicitar decisão.

### 6.13 Revisão, testes e evidências

A plataforma deve verificar três fidelidades:

1. intenção do usuário;
2. regras do negócio;
3. engenharia de software.

Tipos de revisão:

- funcional;
- domínio;
- estrutural;
- segurança.

Tipos de teste:

- unitário;
- integração;
- arquitetural;
- regressão;
- adversarial autorizado;
- visual;
- operacional;
- recuperação e rollback.

A evidência deve ser primária, coerente e reproduzível.

### 6.14 Gate, release e incidentes

O GateDecision avalia o resultado real após execução, revisão e testes.

Decisões possíveis incluem:

- advance;
- rework;
- blocked;
- rejected;
- awaiting_human;
- waived sob autoridade e justificativa estritas.

Release e Incident completam o ciclo operacional.

### 6.15 MEC, Memória Evolutiva Causal

A MEC preserva:

- objetos cognitivos;
- eventos;
- origem;
- estado epistêmico;
- evidência;
- decisões;
- relações tipadas;
- contradições;
- consequências;
- trajetória temporal;
- linhagem;
- contexto antes, durante e depois.

Relações exemplares:

- `derived_from`;
- `provoked_decision`;
- `resulted_in`.

Estados epistêmicos incluem:

- declarado;
- inferido;
- observado;
- confirmado;
- contestado;
- contrafactual.

A MEC consome a execução e também alimenta planejamento, revisão, roteamento e recuperação.

## 7. Fluxo completo da plataforma

### 7.1 Fluxo histórico vigente (14 passos)

O fluxo histórico do projeto, vigente e aprovado, possui 14 passos conforme documentado em [ARCHITECTURAL_MAP.md](../docs/architecture/ARCHITECTURAL_MAP.md):

```text
1. Conversa livre
2. Promoção CTP
3. Governança de Regras (GRN)
4. Arquitetura de Domínio
5. Padrões de Engenharia (ESQ)
6. Planejamento
7. Autorização (WorkOrder)
8. Execução
9. Revisão Funcional
10. Revisão de Domínio
11. Verificação de Qualidade (Engenheiro de Software)
12. Testes e Evidências
13. Verificação de Segurança (SG-0)
14. Gate de Decisão
```

Este mapa de 14 passos permanece como referência genealógica do projeto.

### 7.2 Ciclo operacional consolidado candidato (17 passos)

A sequência abaixo é denominada **ciclo operacional consolidado candidato**. Ela expande, detalha e cerca operacionalmente o fluxo histórico de 14 passos, acrescentando etapas de release, observação e recuperação que não estavam explícitas no mapa original:

**Declarações constitucionais do ciclo candidato:**
- Este ciclo candidato não é numericamente idêntico ao fluxo histórico de 14 passos.
- Reorganiza, detalha, funde e acrescenta etapas em relação ao fluxo histórico.
- É proposta candidata, não substitui o fluxo histórico e não altera automaticamente o roadmap.

```text
1. intenção e conversa livre
2. promoção CTP
3. extração e governança de regras
4. arquitetura de domínio
5. padrões de engenharia
6. deliberação técnica quando aplicável
7. planejamento e dependências
8. autorização por WorkOrder
9. roteamento e preparação da cápsula
10. execução controlada
11. revisão funcional e de domínio
12. verificação estrutural e de segurança
13. testes e evidências
14. GateDecision
15. release ou rework
16. observação operacional
17. incidente, reparo, aprendizado e evolução
```

O ciclo de 17 passos não substitui silenciosamente o fluxo histórico de 14 passos. Ele o complementa com etapas pós-GateDecision que tornam o ciclo completo observável e recuperável. A inclusão de detalhes não cria automaticamente novas fases de implementação. Ela esclarece comportamentos que serão alocados no roadmap.

### 7.3 Tabela de mapeamento entre ciclo candidato e fluxo histórico

A tabela abaixo mostra a correspondência entre as etapas do ciclo operacional consolidado candidato (17 passos) e os passos do fluxo histórico vigente (14 passos):

| Ciclo Candidato (17) | Fluxo Histórico (14) | Observação |
|----------------------|----------------------|------------|
| 1. intenção e conversa livre | 1. Conversa livre | Correspondência direta |
| 2. promoção CTP | 2. Promoção CTP | Correspondência direta |
| 3. extração e governança de regras | 3. Governança de Regras (GRN) | Correspondência direta |
| 4. arquitetura de domínio | 4. Arquitetura de Domínio | Correspondência direta |
| 5. padrões de engenharia | 5. Padrões de Engenharia (ESQ) | Correspondência direta |
| 6. deliberação técnica quando aplicável | — | Etapa adicional no candidato |
| 7. planejamento e dependências | 6. Planejamento | Correspondência |
| 8. autorização por WorkOrder | 7. Autorização (WorkOrder) | Correspondência |
| 9. roteamento e preparação da cápsula | — | Etapa adicional no candidato |
| 10. execução controlada | 8. Execução | Correspondência |
| 11. revisão funcional e de domínio | 9. Revisão Funcional + 10. Revisão de Domínio | Fusão de dois passos históricos |
| 12. verificação estrutural e de segurança | 11. Verificação de Qualidade + 13. Verificação de Segurança | Fusão de dois passos históricos (com reordenação) |
| 13. testes e evidências | 12. Testes e Evidências | Correspondência (posição alterada no candidato) |
| 14. GateDecision | 14. Gate de Decisão | Correspondência |
| 15. release ou rework | — | Extensão pós-GateDecision |
| 16. observação operacional | — | Extensão pós-GateDecision |
| 17. incidente, reparo, aprendizado e evolução | — | Extensão pós-GateDecision |

**Resumo das transformações:**
- **Etapas adicionais no candidato:** 5 (2 etapas adicionais internas — deliberação técnica e roteamento/cápsula — e 3 extensões pós-Gate)
- **Fusões no candidato:** 2 (revisão funcional+domínio, verificação estrutural+segurança)
- **Reordenação:** testes e evidências movido para após verificação (passo 13 no candidato vs. passo 12 no histórico)

## 8. Papéis e autoridades

### 8.1 Saimon

- proprietário;
- idealizador;
- autoridade soberana;
- aprovador de direção, promoção e mudanças materiais.

### 8.2 Arquiteto conceitual

- preserva intenção;
- estrutura o sistema;
- reconcilia conceitos;
- não substitui a aprovação soberana.

### 8.3 Planejador

- decompõe objetivo;
- identifica dependências;
- define caminho crítico;
- não executa sem autorização.

### 8.4 Executor

- implementa o contrato;
- registra ações e evidências;
- não revisa nem aprova o próprio trabalho.

### 8.5 Revisor

- procura falhas;
- confronta requisitos;
- não promove resultado.

### 8.6 Testador

- produz prova objetiva;
- não enfraquece teste para obter aprovação.

### 8.7 Engenheiro de segurança

- verifica limites, segredos, rede, permissões e abuso.

### 8.8 Guardião de regras

- verifica intenção, negócio, vigência e conflitos.

### 8.9 Auditor Final Independente

**Papel constitucional:** Auditor Final Independente.

**Atribuição operacional atual:** No processo operacional atual do projeto, esse papel é ocupado pelo GPT da OpenAI.

A independência arquitetural de modelos deve ser preservada: o papel é definido pela autoridade e função, não pelo modelo específico que o ocupa.

Fluxo obrigatório atual:

```text
Executor
→ Mimo, revisão interna
→ correções
→ testes
→ commit final
→ push final
→ Auditor Final Independente (GPT da OpenAI)
→ veredito
```

Separação de autoridade:

- Mimo retorna apenas `INTERNAL_REVIEW_APPROVED`.
- Antes da auditoria final, o estado máximo é `READY_FOR_FINAL_AUDIT`.
- Somente o Auditor Final Independente autorizado retorna `APPROVED`, `REJECTED` ou `BLOCKED`.
- Somente `APPROVED` permite `COMPLETED`.
- Qualquer mudança posterior invalida o veredito anterior e exige nova auditoria.

## 9. Segurança e postura defensiva

### 9.1 Missão

> Nada não autorizado entra; nenhuma informação indevida sai; o agente não ultrapassa sua cápsula; a plataforma não ataca terceiros.

### 9.2 Segurança proporcional

Uma leitura comum não exige a mesma cerimônia de uma publicação, acesso a produção ou operação financeira.

O nível de controle cresce conforme:

- impacto;
- irreversibilidade;
- privilégio;
- exposição de dados;
- alcance de rede;
- duração autônoma;
- capacidade do modelo.

### 9.3 Defesa em profundidade

```text
regra declarativa
→ hook obrigatório
→ permissão de ferramenta
→ isolamento de processo
→ política de rede
→ sistema operacional ou VM
→ credencial temporária mínima
→ monitor externo
→ interrupção automática
```

### 9.4 Ambiente vazio por padrão

Ambientes agênticos não devem receber:

- chaves permanentes;
- acesso administrativo;
- Obsidian canônico;
- escrita no GitHub sem necessidade;
- pastas pessoais;
- rede livre;
- socket do Docker;
- segredos não relacionados à missão.

### 9.5 Testes adversariais

**[FUTURO]** Permitidos somente quando:

- o ambiente pertence ao usuário ou há autorização;
- o escopo está definido;
- existe isolamento;
- terceiros não são atingidos;
- há registro e interrupção;
- o objetivo é defensivo.

## 10. Inteligência técnica externa e quarentena

### 10.1 Inteligência técnica externa

A plataforma poderá pesquisar:

- GitHub;
- documentação oficial;
- issues;
- commits;
- releases;
- testes;
- papers e referências técnicas.

Cada fonte externa recebe avaliação de:

- credibilidade;
- licença;
- manutenção;
- segurança;
- compatibilidade;
- evidência.

### 10.2 Laboratório efêmero de quarentena

Código externo desconhecido deve entrar em ambiente descartável e isolado.

### 10.3 Promoção controlada

Nenhum experimento promove a si próprio.

Promoção exige:

- origem;
- versão ou commit;
- licença;
- diff ou patch;
- dependências;
- testes;
- evidências;
- revisão;
- gate;
- rollback.

### 10.4 Registro evolutivo de confiança

A MEC registra histórico de:

- fonte;
- versão;
- risco;
- resultado de testes;
- motivo da quarentena;
- decisões;
- incidentes;
- condição de reavaliação.

Confiança é evolutiva, não permanente.

## 11. Motor de Resposta e Recuperação Operacional

**[FUTURO]** Aplicação empresarial conhecida informalmente como “domador de ticket”.

Recebe um problema e:

1. identifica sistema e componente afetado;
2. classifica urgência e impacto;
3. reproduz a falha;
4. localiza causa provável;
5. propõe solução;
6. testa regressões;
7. aplica ou prepara correção autorizada;
8. verifica restauração;
9. monitora;
10. registra dívida, evidência e consequência.

### 11.1 Reparação definitiva

Corrige causa raiz, refatora quando necessário, testa e entrega solução completa.

### 11.2 Contenção emergencial

Quando a operação precisa voltar rapidamente, aplica correção mínima:

- reversível;
- isolada;
- rastreável;
- autorizada;
- com prazo de validade;
- com risco conhecido;
- com ticket de correção definitiva.

O remendo nunca é escondido nem promovido como solução final.

## 12. Qualidade de engenharia

A identidade do código deve ser:

- legível;
- modular;
- coesa;
- testável;
- rastreável;
- sustentável;
- consistente;
- simples sem ser simplista.

Separação de camadas:

- domínio puro;
- contratos puros;
- controle orquestra;
- execução contém efeitos colaterais;
- integração adapta provedores;
- observabilidade registra;
- operação recupera e mantém.

Dívida técnica deve ser explícita e governada.

## 13. Observabilidade e experiência do usuário

O usuário deve conseguir visualizar:

- tarefa atual;
- agente e papel;
- modelo e provedor;
- motivo de troca;
- custo e tempo;
- progresso;
- dependências;
- bloqueios;
- hooks aguardando autorização;
- evidências;
- último checkpoint;
- risco e rollback.

Futuros canais remotos, como Telegram ou WhatsApp, poderão notificar e solicitar autorizações, sem substituir controles críticos.

## 14. Paralelismo multiagente

Paralelismo é definido pela arquitetura e pelo grafo de dependências, não pela quantidade de agentes disponível.

Regras:

- tarefas independentes podem executar em paralelo;
- caminho crítico recebe prioridade;
- tarefas dependentes aguardam evidência da anterior;
- agentes não editam o mesmo artefato sem coordenação;
- quantidade de agentes não justifica distorcer arquitetura;
- resultados convergem por contratos e gates.

## 15. Requisitos identificáveis

A Bíblia organiza requisitos nas famílias:

- `HC-VIS`: visão e propósito;
- `HC-ARC`: arquitetura;
- `HC-COG`: cognição e MEC;
- `HC-EXE`: execução e loops;
- `HC-GOV`: governança e autoridade;
- `HC-SEC`: segurança;
- `HC-TST`: testes e validação;
- `HC-EVD`: evidência;
- `HC-OBS`: observabilidade;
- `HC-OPS`: operação, release e incidentes;
- `HC-DOC`: documentação e memória institucional;
- `HC-PHS`: fases e roadmap.

Cada requisito futuro deve possuir:

- identificador;
- texto normativo;
- origem;
- data da decisão;
- estado;
- fase relacionada;
- evidência ou justificativa;
- conflitos conhecidos;
- documentos de implementação.

## 16. Roadmap integral

O roadmap existente FI-0 a FI-13 permanece a espinha dorsal. A descrição abaixo consolida propósito e fronteiras; não autoriza fases futuras.

### FI-0, Fundação Inicial

**Estado:** [IMPLEMENTADO] aprovado.

Entregas:

- repositório;
- ambiente Python 3.12;
- dependências e build;
- testes baseline;
- observabilidade inicial;
- governança mínima de evidência.

### FI-1, Protocolo Cognitivo

**Estado:** [IMPLEMENTADO] aprovado.

Entregas:

- contratos cognitivos;
- referências de evidência;
- tipos e vocabulário controlado;
- IDs e validações;
- separação epistêmica inicial;
- glossário e protocolo MEC.

### FI-2A, Domínio e Contratos Puros

**Estado:** [IMPLEMENTADO] aprovado.

Entregas:

- Project;
- Requirement;
- Plan;
- Task;
- WorkOrder;
- estados, invariantes e políticas;
- SG-0, ESQ, GRN e CTP formalizados.

### FI-2B Parte 1, Execução Verificada

**Estado:** [IMPLEMENTADO] aprovado.

Entregas:

- ExecutionRun;
- Review;
- TestRun;
- evidências;
- invariantes e testes adversariais;
- CI de qualidade.

### FI-2B Parte 2, Gate, Release e Incident (domínio)

**Estado:** [FUTURO] planejamento existente, implementação não autorizada.

Entregas previstas:

- modelos de domínio de GateDecision, Release e Incident;
- estados, invariantes e transições;
- políticas puras de contenção e recuperação;
- vínculo formal com evidências.

**O que FI-2B Parte 2 faz:**

- implementa os modelos de domínio;
- define estados;
- define invariantes;
- define transições;
- define políticas puras;
- abrange GateDecision, Release e Incident em nível de domínio;
- não constitui ainda implantação ou operação empresarial real.

Antes da implementação, o plano deve ser confrontado com esta Bíblia, incluindo hooks, watchdog, sala de deliberação e resposta operacional.

### FI-3, Persistência e Recuperação

**Estado:** [FUTURO].

Entregas candidatas:

- armazenamento de domínio;
- event store;
- migrações;
- backup e restore;
- replay;
- consistência;
- separação entre Git e estado operacional;
- fundação executável da MEC.

### FI-4, Busca, Projeções e Orquestração

**Estado:** [FUTURO].

Entregas candidatas:

- busca lexical inicial;
- projeções;
- consultas por linhagem;
- orquestração de tarefas;
- roteamento básico;
- métricas de custo e execução.

### FI-5, Linhagem e Cápsula de Contexto

**Estado:** [FUTURO].

Entregas candidatas:

- lineage operacional e cognitiva;
- cápsulas de contexto;
- recuperação antes/durante/depois;
- detecção de contradição;
- promoção de conversa;
- fronteira de autoridade das fontes.

### FI-6, Fluxo Simulado Completo

**Estado:** [FUTURO].

Entregas candidatas:

- ciclo ponta a ponta simulado;
- CLI ou interface controlada;
- primeiro teste humano simulado;
- gates sem executor destrutivo;
- checkpoints e rework.

### FI-7, Primeiro Executor Real

**Estado:** [FUTURO].

Entregas candidatas:

- executor de ferramentas;
- adapters de modelo;
- permissões mínimas;
- hooks essenciais;
- execução controlada;
- rollback básico;
- roteamento econômico inicial.

### FI-8, Revisão Independente e Retrabalho

**Estado:** [FUTURO].

Entregas candidatas:

- separação efetiva de autoridades;
- revisores por papel;
- ciclos de correção;
- contrato de deliberação;
- reauditoria após mudança.

### FI-9, Laboratório de Testes e Evidências

**Estado:** [FUTURO].

Entregas candidatas:

- isolamento;
- testes técnicos;
- evidências reproduzíveis;
- testes adversariais autorizados;
- promoção controlada;
- retenção e integridade de artefatos.

### FI-10, Laboratório Web e Validação Visual

**Estado:** [FUTURO].

Entregas candidatas:

- navegação controlada;
- screenshots e provas visuais;
- modelo de visão;
- diagnóstico de UI;
- detecção de links, proporções e quebras;
- isolamento de conteúdo externo.

### FI-11, Papéis, Moderação e Promoção

**Estado:** [FUTURO].

Entregas candidatas:

- papéis formalizados;
- câmara de deliberação;
- políticas de composição dinâmica;
- moderador;
- promoção entre ambientes;
- registro evolutivo de confiança;
- governança de skills.

### FI-12, Release, Operação e Incidentes (operação real)

**Estado:** [FUTURO].

**O que FI-12 faz:**

- operacionaliza os modelos de domínio definidos em FI-2B Parte 2;
- integra implantação real;
- observabilidade pós-entrega;
- rollback executável;
- resposta a incidentes;
- contenção emergencial;
- reparação definitiva;
- monitoramento contínuo;
- notificações;
- Motor de Resposta e Recuperação Operacional;
- forma inicial do "domador de ticket".

Entregas candidatas:

- pipeline de implantação com rollback automatizado;
- dashboards de observabilidade;
- fluxos de contenção e reparo;
- integração com notificações remotas;
- domador de ticket em operação real.

**Progressão de responsabilidade:** Existe progressão clara de domínio para operação real. FI-2B Parte 2 define os modelos e políticas puras; FI-12 operacionaliza esses modelos em ambiente de produção com monitoramento, resposta e reparo. Não há duplicação de finalidade.

### FI-13, Evals e Evolução (pós-V1)

**Estado:** [FUTURO] pós-V1.

**Classificação temporal:** FI-13 inicia a evolução contínua após a primeira plataforma completamente funcional (V1). Ela não bloqueia o reconhecimento da V1.

Entregas candidatas:

- evals contínuos;
- qualidade histórica por modelo e papel;
- roteamento adaptativo maduro;
- detector maduro de ausência de progresso;
- custo e desempenho;
- autodiagnóstico;
- reparo supervisionado;
- aprendizado causal baseado em dados quando houver evidência suficiente.

**Relação com V1:** A aprovação e conclusão da FI-12 encerra a construção da primeira plataforma completamente funcional. FI-13 contém capacidades que podem evoluir indefinidamente após a V1, sem impedir que a primeira plataforma seja reconhecida como concluída.

## 17. Critério da primeira plataforma completamente funcional

**Marco V1:** A aprovação e conclusão da FI-12 encerra a construção da primeira plataforma completamente funcional. O término da FI-12 representa o marco V1.

**FI-13 e além:** FI-13 inaugura a evolução contínua pós-V1 e não impede o reconhecimento da primeira plataforma como concluída. Recursos da FI-13 podem continuar evoluindo indefinidamente depois da primeira plataforma funcional.

A primeira versão é considerada funcional quando demonstrar, em um projeto real e autorizado:

1. intenção promovida para projeto formal;
2. regras extraídas e governadas;
3. arquitetura e plano rastreáveis;
4. WorkOrders autorizadas;
5. execução real em ambiente controlado;
6. papéis e modelos escolhidos por capacidade e risco;
7. hooks críticos ativos;
8. checkpoint e rollback;
9. detecção mínima de ausência de progresso;
10. revisão independente;
11. testes técnicos e, quando aplicável, visuais;
12. evidências reproduzíveis;
13. GateDecision funcional;
14. release controlado;
15. monitoramento pós-entrega;
16. incidente e recuperação demonstrados;
17. MEC persistindo origem, decisão, evidência e consequência;
18. troca de modelo sem perda de autoridade ou contexto;
19. segurança sem segredos em documentação ou logs;
20. aprovação soberana final de Saimon.

A quantidade de funcionalidades não define completude. O que define é o ciclo completo funcionar com segurança, evidência e recuperação.

## 18. Estado atual no corte de 23 de julho de 2026

### Implementado e aprovado

- FI-0;
- FI-1;
- FI-2A;
- FI-2B Parte 1;
- HEAD `a191a37d207e47d322297f7ce84c2dd211ca02d9`;
- 534 testes aprovados;
- tags de aprovação correspondentes.

### Não implementado

- FI-2B Parte 2;
- persistência;
- event store;
- MEC executável completa;
- executor real da plataforma;
- hooks de produto;
- watchdog;
- sala de deliberação;
- quarentena operacional;
- roteamento adaptativo completo;
- release e incidentes funcionais;
- integrações operacionais.

### Fechamento documental em curso

- a branch histórica docs/hc-documentary-reconciliation foi inspecionada no commit 19352a47fd6fcc66edab85a155599b6c9f6b9aca e permanece fonte proposta e forense, não cânone automático;
- a Declarativa e os originais normativos 01–08 foram recuperados, identificados por hash e confrontados com esta Bíblia e com o Histórico;
- o commit local 0a3fc1960e7afb3a60976c32c3c04f1d54c4ce3d não foi encontrado em nenhum clone ou ref acessível;
- esse commit permanece uma lacuna histórica declarada e não deve ser reconstruído por memória, inferência ou tentativa de reprodução;
- restam apenas a correção objetiva final, a revisão interna, a auditoria do SHA publicado e a decisão soberana de integração.

### Ordem vigente

```text
correção objetiva final da Bíblia e do Histórico
→ revisão interna independente
→ publicação do SHA final
→ auditoria final independente
→ decisão soberana e integração
→ retomada autorizada da FI-2B Parte 2
→ espelhamento documental no Obsidian como projeção
```

## 19. Governança de alteração desta Bíblia

Toda alteração material deve:

1. identificar origem;
2. indicar se é fato, decisão, hipótese ou implementação;
3. mapear requisitos e fases afetados;
4. registrar conflitos;
5. preservar texto anterior no Git;
6. receber revisão independente;
7. ser publicada em SHA identificável;
8. receber auditoria final quando alterar estado canônico;
9. depender de aprovação soberana de Saimon.

Ideias novas não entram apenas porque são interessantes. Elas precisam de classificação, encaixe e consequência.

## 20. Decisões fechadas

- MEC é subsistema, não o Harness inteiro.
- O sistema completo é uma plataforma cognitiva agêntica soberana.
- O harness de execução é o núcleo operacional.
- Modelos e provedores são intercambiáveis.
- Segurança é transversal e proporcional.
- A plataforma é defensiva e construtiva.
- Hooks refinam setores existentes.
- Watchdog refina execução e observabilidade.
- Sala de deliberação reúne papéis necessários e não decide por maioria simples.
- Papéis vêm antes dos modelos.
- Descoberta causal formal não é módulo obrigatório atual.
- Bíblia precede FI-2B Parte 2.
- O commit local 0a3fc1960e7afb3a60976c32c3c04f1d54c4ce3d está indisponível nas fontes acessíveis, permanece lacuna histórica declarada e não será reconstruído, simulado ou tratado como conteúdo conhecido.
- O executor não aprova o próprio trabalho.

## 21. Pendências antes do merge e backlog não bloqueante

### 21.1 Pendências obrigatórias antes do merge

1. concluir este patch objetivo de estado e rastreabilidade;
2. obter revisão interna independente sobre o diff final;
3. publicar o SHA final da branch;
4. realizar auditoria final independente sobre o SHA publicado;
5. obter decisão soberana expressa para integração.

### 21.2 Backlog não bloqueante

Os itens abaixo pertencem às fases em que forem necessários e não bloqueiam o fechamento desta Bíblia nem, por si só, a FI-2B Parte 2:

- numeração completa dos requisitos por família;
- detalhamento de subfases futuras;
- catálogo operacional de hooks;
- contrato executável do watchdog;
- critérios operacionais da Câmara de Deliberação;
- política detalhada de retenção de evidências;
- arquitetura operacional de integrações e segredos;
- critérios de produto público ou comercial.

Um item do backlog somente se torna bloqueador quando a fase autorizada depender materialmente dele.

## 22. Fontes e rastreabilidade

- Declarativa do Harness Cognitivo, PDF recuperado e identificado pelo SHA-256 a3c4e62883b0240b756acc0f010a6d73f171571788d127a632232225a16fc825;
- originais normativos 01–08, recuperados e verificados individualmente por SHA-256;
- branch histórica docs/hc-documentary-reconciliation no commit 19352a47fd6fcc66edab85a155599b6c9f6b9aca, tratada como proposta e evidência histórica;
- [Histórico evidencial](history/00_HISTORICO_EVIDENCIAL_DO_PROJETO.md)
- [Mapa arquitetural](architecture/ARCHITECTURAL_MAP.md)
- [Plano FI-2B](architecture/FI2B_PLAN.md)
- [MEC Protocol](MEC_PROTOCOL.md)
- [Glossário](GLOSSARY.md)
- [Constituição ESQ](architecture/ESQ_CONSTITUTION.md)
- [Governança GRN](architecture/GRN_BUSINESS_RULES_GOVERNANCE.md)
- [CTP](architecture/CTP_CHAT_TO_PROJECT.md)
- [Política SG-0](operations/SG-0_AGENT_DESTRUCTIVE_ACTIONS_POLICY.md)
- [Relatório FI-2B Parte 1](reports/RELATORIO_FI2B_PARTE1.md)
- PR #1 e commits citados no histórico.

## 23. Gate desta versão candidata

Esta Bíblia só poderá ser tratada como canônica depois de:

- revisão de conteúdo por Saimon;
- confronto concluído com a Declarativa e os originais 01–08;
- reconciliação concluída com os documentos acessíveis da branch histórica;
- correção final de links, estados e rastreabilidade;
- revisão interna independente;
- publicação de SHA final;
- auditoria final independente;
- veredito `APPROVED`;
- decisão soberana expressa de Saimon;
- merge e tag conforme governança.
