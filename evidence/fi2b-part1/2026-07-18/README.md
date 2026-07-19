# Evidências da FI-2B Parte 1 — 2026-07-18

Este diretório preserva evidências da reprodução controlada da FI-2B Parte 1.

## Baseline

- Branch: `feat/fi-2b-part1`
- `audited_head=d11f983f701936a6b3e7fde68c81fba0699f1fcd`
- Python 3.12.13
- Dependências restauradas a partir de `uv.lock` com modo congelado

## Conteúdo

- `baseline/EVIDENCIAS_FI2B_PARTE1.md`: relatório com saídas integrais.
- `baseline/evidence-manifest.json`: comando, horários, código de saída, resultado, log e HEAD.
- `baseline/logs/`: dez saídas brutas, com caminhos pessoais sanitizados.
- `WARNING_INVESTIGATION.md`: investigação somente de leitura do `PytestCacheWarning`.

## Sanitização

Somente caminhos pessoais e locais foram substituídos por marcadores como `<repo>` e `<user-home>`. Comandos, horários, resultados, mensagens funcionais, códigos de saída e o HEAD auditado foram preservados.

O warning do Pytest não foi ocultado, suprimido ou removido.
