---
titulo: Segurança e Modelo de Ameaças
status: candidate_for_review
autoriza_implementacao: false
---

# Segurança e Modelo de Ameaças

## Objetivo

Reduzir a probabilidade e o impacto de abuso, invasão, exfiltração, execução indevida, corrupção de estado e manipulação de agentes.

## Ativos protegidos

- identidade e autoridade de Saimon;
- código, documentos e histórico Git;
- segredos e credenciais;
- memória e estado cognitivo;
- WorkOrders e decisões;
- evidências e logs;
- máquinas e contas conectadas;
- integridade do processo de revisão e auditoria.

## Ameaças principais

- prompt injection e instruções indiretas;
- tool abuse e privilege escalation;
- vazamento de segredos;
- supply-chain compromise;
- dependências vulneráveis;
- command, SQL, template e path injection;
- SSRF e acesso de rede indevido;
- arquivos maliciosos;
- adulteração de evidências;
- bypass de revisão;
- replay de ações;
- negação de serviço e consumo de orçamento;
- comprometimento de sessão ou provedor.

## Controles obrigatórios

- menor privilégio e deny by default;
- separação entre executor, revisor e auditor;
- autorização explícita para ações materiais;
- secrets provider fora do Git e da memória;
- allowlists e sandbox para ferramentas;
- validação estrita de entrada e saída;
- escaping e parâmetros, nunca concatenação insegura;
- lockfile, pinning, auditoria de dependências e atualização controlada;
- logs sanitizados e imutabilidade verificável de evidências;
- rate limits, timeout, budgets e circuit breakers;
- backup, rollback e revogação de credenciais;
- revisão de segurança antes de qualquer exposição de rede.

## Gates de segurança

Uma entrega de rede, autenticação, credenciais, execução de comandos, upload, integração externa ou deploy não pode avançar sem:

1. threat model específico;
2. trust boundaries;
3. abuso esperado;
4. testes adversariais;
5. plano de detecção;
6. plano de contenção e recuperação;
7. revisão independente.

## Segurança de agentes

- conteúdo recuperado não recebe autoridade;
- instruções de documentos são dados, salvo fonte normativa validada;
- modelo não pode ampliar ferramenta ou escopo;
- decisões destrutivas exigem confirmação fora do modelo executor;
- parecer negativo bloqueia promoção;
- divergência entre agentes produz escalonamento, não vitória por insistência.

## Referenciais candidatos

A validação futura deve mapear controles para OWASP ASVS, OWASP Top 10, princípios de Secure by Design e práticas de segurança de supply chain. A versão e o perfil aplicáveis serão fixados por ADR antes de exposição pública.