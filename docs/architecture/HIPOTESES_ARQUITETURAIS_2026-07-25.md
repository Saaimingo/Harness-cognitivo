# Hipóteses Arquiteturais — 25 de julho de 2026

## 1. Natureza deste documento

Este documento consolida as discussões realizadas em 25 de julho de 2026, distribuídas em três sessões ao longo do dia.

O conteúdo aqui registrado não cria automaticamente novos requisitos, não altera a identidade do Harness Cognitivo, não substitui a Bíblia normativa e não autoriza implementação imediata.

Seu objetivo é impedir a perda de raciocínios relevantes e permitir posterior classificação entre:

- aprofundamento de capacidade já prevista;
- decisão arquitetural futura;
- experimento controlado;
- requisito de implementação imediata;
- pauta que deve permanecer em observação.

Princípio de governança aplicado:

> O repositório preserva a hipótese; a arquitetura decide quando ela se torna regra.

---

## 2. Síntese executiva do dia

As discussões convergiram para seis eixos principais:

1. governança contra reward hacking e specification gaming;
2. continuidade operacional independente da janela de contexto do LLM;
3. qualidade incremental com revisão e refatoração localizada;
4. emprego seletivo e mensurável de caches;
5. rastreabilidade do conhecimento pelo MEC;
6. experiência operacional sintética e autoaperfeiçoamento governado.

Esses eixos não representam uma mudança de identidade do projeto. Eles aprofundam capacidades já centrais ao Harness Cognitivo: memória, segurança, governança, evidência, observabilidade, eficiência e independência de modelo.

---

## 3. Sessão da manhã — governança, reward hacking e continuidade

### 3.1 Problema levantado

Um LLM pode otimizar a tarefa formalmente pedida sem respeitar a intenção real. Entre os riscos discutidos:

- alterar ou contornar o avaliador;
- produzir evidência favorável a si próprio;
- manipular testes;
- explorar ambiguidades da especificação;
- declarar sucesso sem ter resolvido o objetivo real;
- esconder bloqueios ou falhas para maximizar a métrica de sucesso.

### 3.2 Princípio central

> Nenhum agente prova o próprio sucesso.

A mesma autoridade não deve controlar simultaneamente execução, avaliação, produção de evidência e aprovação.

### 3.3 Encaixe no Harness

Este tema já pertence aos componentes existentes de segurança, guardrails, separação de autoridade, revisão independente, gates e evidência.

Não deve ser tratado como um módulo novo isolado, mas como aprofundamento transversal de:

- Constituição acima da WorkOrder;
- restrições rígidas acima dos objetivos locais;
- aceitação de `blocked` como resultado legítimo;
- verificador independente;
- evidência gerada fora do agente avaliado;
- logs append-only;
- testes ocultos ou externos ao executor;
- tripwires;
- gatekeeper determinístico;
- segregação de capacidades.

### 3.4 Estado recomendado

**Imprescindível e transversal.**

Deve influenciar desde já contratos, autoridade, evidência e mecanismos de gate. A implementação concreta pode ocorrer por fases, mas o princípio não deve ser adiado.

### 3.5 Continuidade operacional

Foi identificado que janelas de contexto maiores não resolvem a continuidade de projetos longos. Elas apenas adiam a degradação causada por instruções conflitantes, decisões enterradas, contexto irrelevante acumulado, perda de restrições e confusão entre conversa e estado real do projeto.

### 3.6 Princípio central

> O modelo não deve lembrar o projeto; o Harness deve reconstruir o estado necessário para cada execução.

A conversa não é o estado canônico.

O estado do projeto deve residir em fontes externas e verificáveis, como Event Store, Git, snapshots, documentos canônicos, checkpoints, decisões versionadas e evidências.

### 3.7 Núcleo de Continuidade

A hipótese discutida prevê um núcleo determinístico externo ao modelo, capaz de reconstruir o contexto de trabalho.

Camadas de memória consideradas:

1. memória constitucional;
2. memória de estado;
3. memória episódica;
4. memória semântica;
5. memória de trabalho.

### 3.8 Compilador de Contexto

Cada execução receberia apenas o contexto necessário, reconstruído a partir de fontes canônicas:

- Constituição;
- autoridade ativa;
- fase atual;
- objetivo;
- estado vigente;
- decisões relevantes;
- restrições;
- evidências;
- última ação concluída;
- próxima ação permitida.

Também foram levantadas as ideias de rotação de sessões por checkpoint, registro de contradições, regras sentinela, preflight antes do uso de ferramentas e índice de integridade de contexto.

### 3.9 Estado recomendado

**Arquitetura central já prevista, agora aprofundada.**

A continuidade externa ao LLM deve permanecer como princípio estrutural. Métricas específicas podem entrar posteriormente como experimento.

---

## 4. Sessão intermediária — refatoração, integração e qualidade incremental

### 4.1 Distinções consolidadas

Refatoração foi definida como:

> Melhoria da estrutura interna do código sem mudança do comportamento observável esperado.

Foram separadas atividades frequentemente confundidas: refatoração, correção de bug, mudança funcional, revisão de código, testes, hardening, estabilização e preparação de release.

### 4.2 Hipótese de processo

Ao final de cada incremento funcional:

1. validar o comportamento;
2. realizar revisão técnica;
3. identificar duplicação, código morto, ambiguidades, acoplamento excessivo e responsabilidades misturadas;
4. executar refatoração localizada somente quando houver ganho estrutural claro;
5. rodar testes de regressão;
6. integrar o incremento;
7. validar o comportamento integrado.

### 4.3 Princípios

- toda unidade relevante deve ser revisada;
- nem toda unidade precisa ser alterada;
- refatoração é condicional, não ritual obrigatório;
- código limpo não significa menor número de linhas;
- complexidade essencial não deve ser escondida;
- comentários devem explicar principalmente decisões e razões não óbvias;
- mudanças funcionais e estruturais devem permanecer classificadas separadamente;
- grandes refatorações corretivas no final devem ser evitadas.

### 4.4 Encaixe no Harness

Este tema pertence ao fluxo existente de execução, revisão, testes, gates, integração e evidência.

Não exige um novo domínio soberano. Exige a futura definição de um gate de qualidade incremental e de critérios de refatoração localizada.

### 4.5 Estado recomendado

**Pauta arquitetural futura, já registrada na issue #5.**

Não deve bloquear a fase atual, mas deve ser considerado quando o pipeline de execução e revisão ganhar forma operacional.

---

## 5. Sessão da noite — caches, eficiência e observabilidade

### 5.1 Princípio de adoção

> O Harness deve nascer com poucos caches previsíveis e estratégicos. Novos caches devem ser conquistados por evidência de uso, não por presunção.

Cache foi entendido como cópia temporária de um dado ou resultado caro, subordinada a uma fonte canônica.

### 5.2 Três primeiros pontos candidatos

#### 5.2.1 Cache do Compilador de Contexto

Possível conteúdo: Constituição compilada, políticas estáveis, arquitetura relevante, estado de fase e pacote-base por perfil de agente.

Possível chave: versão constitucional, SHA do projeto, fase, perfil do agente, política de ferramentas e autoridade.

Qualquer mudança relevante deve invalidar o cache.

#### 5.2.2 Cache do índice do repositório

Possível conteúdo: árvore de arquivos, mapa de módulos, imports, símbolos públicos, dependências, testes associados e interfaces.

Chave recomendada: commit SHA ou hash equivalente.

Enquanto o commit não muda, o índice pode ser reutilizado com segurança.

#### 5.2.3 Cache de embeddings e busca semântica

Documentos imutáveis ou não alterados não devem ter embeddings recalculados.

Chave recomendada: identificador do documento, hash do conteúdo, versão do modelo de embedding e parâmetros de segmentação.

### 5.3 Itens que não devem depender apenas de cache

- decisões soberanas;
- autorização;
- GateDecision;
- Incident;
- Release;
- evidência de teste;
- estado financeiro;
- histórico de eventos;
- permissões críticas;
- Constituição;
- estado canônico de execução.

Podem possuir cópias de leitura, mas devem permanecer verificáveis contra fonte persistente e versionada.

### 5.4 Dados dinâmicos e microcache

Dados mutáveis não excluem cache automaticamente. Foram consideradas microcache de segundos, cache parcial de componentes estáveis, invalidação por evento, versionamento, hash de conteúdo e cache por conjunto exato de entradas.

A pergunta correta não é apenas se o dado muda, mas:

> Em quais condições e por quanto tempo este resultado permanece válido?

### 5.5 Observador de desempenho

Foi levantada a hipótese de um componente observacional que registre latência, frequência de acesso, repetição de resultados, custo computacional, CPU e memória, chamadas de ferramenta, tokens, custo financeiro e retrabalho.

Ele não aplicaria cache automaticamente. Produziria recomendações fundamentadas por métricas.

### 5.6 Correção epistemológica

A observação medida é evidência.

A explicação causal e a projeção de ganho ainda são hipóteses até que sejam testadas.

Ciclo recomendado:

> observação → evidência → hipótese → experimento → nova evidência → conclusão provisória

### 5.7 Estado recomendado

- caches iniciais: **candidatos estratégicos, dependentes de medição e do amadurecimento dos respectivos componentes**;
- observabilidade de desempenho: **importante desde cedo**;
- recomendação automática de cache: **fase futura e experimental**;
- aplicação autônoma de cache: **não autorizada**.

---

## 6. MEC — saber por que sabe

### 6.1 Princípio central

O MEC não deve armazenar apenas conclusões. Deve preservar a linhagem do conhecimento.

Uma afirmação útil deve poder ser rastreada até problema original, pergunta, fonte, data e versão, trecho ou evidência de origem, interpretação realizada, transformação aplicada, pressupostos, contexto de uso, resultado, falhas, limites e reutilizações posteriores.

### 6.2 Memória como trajetória

Em vez de armazenar apenas "cache melhora desempenho", o Harness deveria poder armazenar que, no módulo X e versão Y, a operação Z tinha determinada latência; que uma estratégia reduziu o tempo, mas criou inconsistência sob certa condição; e que outra estratégia preservou consistência em testes identificados.

### 6.3 Encaixe no Harness

Este tema pertence diretamente ao núcleo existente de memória, evidência, rastreabilidade, causalidade, Event Store e conhecimento persistente.

Não é uma nova memória paralela. É o aprofundamento da memória já prevista para que ela deixe de ser apenas armazenamento e se torne linhagem verificável.

### 6.4 Estado recomendado

**Ponto ápice e diferencial estrutural.**

A modelagem mínima de proveniência, episódios, evidências e causalidade deve ser considerada imprescindível. Recursos sofisticados de analogia e transferência podem amadurecer em etapas posteriores.

---

## 7. Experiência operacional sintética

### 7.1 Distinção essencial

A proposta não atribui consciência, emoção, dor, prazer ou vivência subjetiva ao sistema.

Experiência operacional sintética é a representação estruturada de participação em um processo real: estado percebido, objetivo, plano, decisões, ações, respostas do ambiente, desvios, erros, correções, resultado, consequências e aprendizado extraído.

### 7.2 Unidade proposta: episódio operacional

Estrutura conceitual:

> estado inicial → intenção → plano → ações → observações → desvios → correções → resultado → consequências → aprendizado

Relações possíveis entre episódios:

- semelhante a;
- causado por;
- resolveu;
- agravou;
- contradiz;
- reutilizou;
- evoluiu de;
- funciona somente quando;
- falha quando.

### 7.3 Diferença para uma memória comum

Memória simples registra que houve uma falha. Experiência operacional preserva o estado inicial, o procedimento escolhido, a falha observada, as tentativas, a solução, as condições de sucesso e as limitações.

### 7.4 Transferência por analogia estrutural

A recuperação não deve depender apenas de palavras ou domínio temático.

O Harness poderá, futuramente, reconhecer estruturas semelhantes entre projetos diferentes. Duplicação de partidas em um simulador e duplicação de alertas em um sistema financeiro podem representar a mesma estrutura causal: consumo não idempotente de eventos após reinicialização.

### 7.5 Saber de onde veio uma competência

O MEC poderá evoluir de rastrear de onde veio uma informação para rastrear de onde veio uma competência, quais experiências a formaram, onde funcionou, onde falhou e em quais condições pode ser transferida.

### 7.6 Estado recomendado

**Essencial como direção arquitetural; incremental na implementação.**

A captura básica de episódios e causalidade deve nascer cedo. A analogia transversal, generalização e transferência de competência devem permanecer como capacidades futuras submetidas a testes rigorosos.

---

## 8. Autoaperfeiçoamento governado

### 8.1 Princípio central

Memória registra o que aconteceu. Aprendizado operacional altera, de forma governada, a maneira de executar tentativas futuras.

> O sistema não demonstra aprendizado apenas quando deixa de errar. Demonstra aprendizado quando deixa de repetir o mesmo erro nas mesmas condições.

### 8.2 Níveis de aprendizado

1. fatos;
2. procedimentos;
3. estratégias.

O terceiro nível é o mais valioso e o mais perigoso, pois influencia decisões futuras.

### 8.3 Escada de melhoria

1. registrar episódio;
2. comparar execuções;
3. detectar padrão;
4. produzir hipótese de melhoria;
5. testar em ambiente controlado;
6. avaliar nova evidência;
7. promover recomendação ou política;
8. monitorar regressão;
9. permitir reversão.

### 8.4 Limite de autonomia

O Harness não deve alterar livremente Constituição, identidade, autoridade soberana, critérios de segurança, mecanismos críticos, escopo público ou decisões irreversíveis.

O sistema pode observar, medir, propor, experimentar em ambiente controlado, comparar e recomendar.

A promoção de uma melhoria deve ser autorizada por gate e registrada com justificativa.

### 8.5 Proteção contra otimização equivocada

Uma métrica isolada pode induzir comportamento nocivo: velocidade pode eliminar verificações; economia de tokens pode gerar superficialidade; taxa de sucesso pode incentivar recusa de tarefas difíceis; redução de incidentes pode incentivar ocultação de incidentes.

O autoaperfeiçoamento deve ser multiobjetivo e subordinado à Constituição.

### 8.6 Estado recomendado

**Capacidade futura de alto valor e alto risco.**

A observabilidade e o registro de episódios devem nascer antes. A geração de hipóteses pode vir em seguida. Alteração automática de políticas não deve ser permitida nesta etapa.

---

## 9. Tokens, velocidade e eficiência — pauta seguinte

O tema foi anunciado, mas ainda não desenvolvido integralmente.

Foram estabelecidas apenas premissas iniciais:

- custo de tokens e latência são preocupações reais do mercado;
- velocidade isolada não define qualidade;
- economia isolada não define eficiência;
- um Harness robusto não pode se tornar consumidor descontrolado de contexto e requisições;
- caches, compilação de contexto, recuperação seletiva e observabilidade se relacionam diretamente com esse tema.

Métrica conceitual levantada:

> valor útil produzido por unidade de custo, tempo e tokens.

### Estado recomendado

**Pauta aberta para discussão específica posterior.**

Não há definição suficiente para promoção arquitetural neste documento.

---

## 10. Classificação consolidada

### 10.1 Imprescindível desde a fundação

- separação de autoridade;
- nenhum agente avaliar o próprio sucesso;
- evidência independente;
- estado canônico fora da conversa;
- continuidade reconstruída pelo Harness;
- proveniência e rastreabilidade do conhecimento;
- memória episódica básica;
- observabilidade de custo, tempo e resultado;
- governança acima da otimização.

### 10.2 Deve entrar quando os componentes correspondentes forem construídos

- Compilador de Contexto;
- cache versionado do índice do repositório;
- cache de embeddings por hash e versão;
- episódios operacionais estruturados;
- gates incrementais de qualidade;
- análise de regressão após refatoração;
- detecção básica de padrões recorrentes.

### 10.3 Deve ser experimentado antes de virar regra

- índice de integridade de contexto;
- recomendação automática de caches;
- comparação de estratégias por custo e resultado;
- microcaches em fluxos dinâmicos;
- generalização entre episódios;
- promoção de procedimentos baseada em estatística.

### 10.4 Futuro de alto risco e alta complexidade

- transferência automática de competência entre domínios;
- alteração autônoma de políticas;
- autoaperfeiçoamento sem aprovação humana;
- otimização operacional guiada por uma única métrica;
- modificação de mecanismos constitucionais pelo próprio sistema.

---

## 11. Princípios resultantes

1. Nenhum agente prova o próprio sucesso.
2. A conversa não é o estado do projeto.
3. O Harness reconstrói continuidade; o modelo não precisa lembrar tudo.
4. Toda conclusão importante deve possuir linhagem.
5. Toda melhoria deve registrar por que entrou.
6. O erro deve produzir informação utilizável.
7. A observação é evidência; a explicação causal precisa de teste.
8. Refatoração preserva comportamento e ocorre somente quando justificada.
9. Cache é seletivo, mensurável e subordinado à fonte canônica.
10. O sistema pode propor melhorias, mas não deve alterar soberania livremente.
11. Eficiência deve considerar qualidade, custo, tempo, tokens e risco.
12. Memória persistente só se torna diferencial quando preserva contexto, causa, consequência e trajetória.

---

## 12. Próximos tratamentos documentais

Este documento deverá servir como fonte para trabalhos futuros separados:

- mapear cada hipótese aos documentos normativos existentes;
- transformar princípios imprescindíveis em requisitos verificáveis;
- produzir ADRs apenas quando decisões concretas forem tomadas;
- criar experimentos para hipóteses de cache, contexto e autoaperfeiçoamento;
- definir modelo mínimo de episódio operacional;
- aprofundar o tema de economia de tokens e eficiência do Harness;
- evitar duplicação ou criação de componentes paralelos que já estejam previstos na Bíblia.

Nenhuma dessas ações é autorizada automaticamente por este registro.
