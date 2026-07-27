---
titulo: Requisitos Não Funcionais
status: candidate_for_review
autoriza_implementacao: false
---

# Requisitos Não Funcionais

## Segurança

- negar por padrão;
- menor privilégio;
- nenhuma credencial no Git, memória ou logs;
- ações materiais autorizadas e auditáveis;
- dependências verificadas e atualizáveis;
- incidentes detectáveis, contíveis e recuperáveis.

## Confiabilidade

- operações materiais idempotentes quando aplicável;
- falhas explícitas, tipadas e rastreáveis;
- estados intermediários recuperáveis;
- backup e restore testados;
- nenhuma promoção com evidência incompleta.

## Desempenho

Metas numéricas serão definidas por benchmark de fase. Até lá:

- evitar chamadas LLM em caminhos determinísticos críticos;
- budgets de tempo, tokens e custo;
- paginação e limites para consultas;
- índices justificados por métricas;
- nenhuma otimização sem perfil.

## Portabilidade

- núcleo executável em ambiente local suportado;
- caminhos e filesystem tratados de forma multiplataforma;
- providers atrás de adapters;
- configuração documentada e reproduzível;
- lockfile como fonte de versões.

## Manutenibilidade

- tipagem no núcleo;
- módulos com responsabilidade clara;
- dependências direcionadas para dentro;
- ADR para decisões materiais;
- documentação e testes atualizados junto da mudança;
- complexidade e duplicação monitoradas.

## Auditabilidade

- correlation e causation IDs;
- autor, autoridade, modelo, ferramenta e resultado registrados;
- evidências associadas ao SHA;
- redaction verificável;
- histórico não reescrito silenciosamente.

## Usabilidade e acessibilidade

- linguagem simples;
- compatibilidade com consumo por áudio;
- estados, riscos e próximas ações claros;
- acessibilidade visual e por teclado quando houver interface;
- confirmações proporcionais ao risco.

## Escalabilidade

Escalar primeiro por simplicidade, profiling e limites. Distribuição, filas externas, banco remoto e microsserviços exigem necessidade medida, ADR, threat model e plano operacional.

## Critérios de aceite

Cada fase deve transformar requisitos aplicáveis em métricas, testes ou evidências. Requisito sem método de verificação não está pronto para implementação.