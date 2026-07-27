---
titulo: APIs e Integrações
status: candidate_for_review
autoriza_implementacao: false
---

# APIs e Integrações

## Regra fundamental

Contratos são definidos antes dos transportes. CLI, MCP, HTTP, filas e SDKs são adapters substituíveis.

## Interfaces iniciais

- CLI local para operação humana;
- application services internos;
- API local candidata para inspeção e automação controlada;
- MCP candidato para exposição limitada de ferramentas e contexto.

## Contratos

Toda operação deve declarar:

- identidade e versão;
- entrada validada;
- saída tipada;
- autoridade exigida;
- idempotência;
- timeout;
- efeitos colaterais;
- erros possíveis;
- evidências produzidas;
- política de retry e rollback.

## Segurança de integração

- deny by default;
- allowlist de hosts, comandos e recursos;
- autenticação e autorização separadas;
- tokens obtidos por secret provider;
- redaction antes de logs;
- rate limiting quando houver exposição de rede;
- proteção contra SSRF, path traversal, command injection e prompt injection;
- conteúdo externo classificado como não confiável até validação.

## Ferramentas

Ferramentas devem declarar capacidade, risco, escopo, modo de leitura/escrita, reversibilidade e necessidade de aprovação. O executor recebe apenas as ferramentas compatíveis com o estado do workflow.

Com `CHANGES_REQUIRED`, ferramentas de commit e push devem ser removidas ou bloqueadas por policy gate.

## Versionamento

- contratos públicos usam versionamento explícito;
- breaking changes exigem migração e ADR;
- respostas devem incluir correlation ID;
- adapters devem possuir contract tests.

## Integrações externas futuras

GitHub, e-mail, calendário, mensageria, navegadores, provedores LLM e serviços de deploy entram apenas por adapters dedicados, cada um com threat model, budgets, logs sanitizados e procedimento de revogação.