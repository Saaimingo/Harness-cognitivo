---
titulo: Frontend e Experiência
status: candidate_for_review
autoriza_implementacao: false
---

# Frontend e Experiência

## Estado

A stack visual está `ADIADA`. O MVP atual usa CLI, MCP, Markdown e API local candidata. Nenhum agente pode escolher React, Next.js, Vue, desktop ou mobile sem requisitos e ADR.

## Objetivo futuro

Oferecer uma interface compreensível para um usuário não técnico controlar projetos, autorizações, agentes, custos, evidências, memória, incidentes e recuperação sem perder soberania.

## Fluxos que devem existir antes da escolha da stack

- criar e promover projeto;
- revisar requisitos e regras;
- aprovar ou negar WorkOrders;
- acompanhar execução e agentes;
- consultar evidências;
- comparar pareceres;
- observar custo e progresso;
- recuperar contexto;
- controlar integrações, permissões e segredos por referência;
- responder a alertas e incidentes.

## Requisitos de experiência

- linguagem simples e adequada à leitura por voz;
- informação crítica não depende apenas de cor;
- estados e autoridade sempre visíveis;
- confirmação forte para ação destrutiva;
- histórico e origem acessíveis;
- estados vazios, carregamento, erro e recuperação definidos;
- acessibilidade por teclado e leitor de tela;
- responsividade somente quando o canal exigir;
- nenhuma ação automática escondida.

## Critérios para escolher tecnologia

1. canais exigidos: web, desktop, mobile ou híbrido;
2. operação local e offline;
3. segurança do runtime;
4. integração com Python sem acoplamento indevido;
5. acessibilidade;
6. distribuição e atualização;
7. testes visuais e de ponta a ponta;
8. custo de manutenção.

## Contrato com backend

A interface consome application APIs versionadas. Não acessa banco diretamente, não contém regra de domínio e não recebe segredos permanentes. Toda ação material retorna correlation ID, estado e evidência.