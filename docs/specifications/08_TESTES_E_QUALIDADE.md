---
titulo: Testes e Qualidade
status: candidate_for_review
autoriza_implementacao: false
---

# Testes e Qualidade

## Estratégia

Qualidade é verificada em camadas:

1. testes unitários de domínio;
2. testes de propriedades e invariantes;
3. contract tests de ports e adapters;
4. integração com infraestrutura real controlada;
5. testes adversariais e de segurança;
6. testes de recuperação e rollback;
7. testes de fluxo ponta a ponta;
8. evidência visual quando houver interface.

## Ferramentas decididas

- pytest;
- Hypothesis;
- Ruff check e format check;
- mypy no núcleo;
- `git diff --check`;
- GitHub Actions.

Ferramentas de segurança e cobertura permanecem candidatas até ADR e baseline.

## Regras

- teste não pode ser enfraquecido para obter aprovação;
- bug corrigido exige teste de regressão;
- mocks não substituem teste de integração quando o risco está no adapter;
- testes devem ser determinísticos ou declarar fonte de variabilidade;
- flaky test é defeito, não ruído aceitável;
- cobertura numérica não substitui cobertura de risco;
- cada requisito deve apontar para evidência ou justificativa de não aplicabilidade.

## Gates mínimos

Antes de `READY_FOR_FINAL_AUDIT`:

- suíte aplicável aprovada;
- lint e tipagem aprovados;
- diff limpo;
- escopo conferido;
- segurança aplicável validada;
- evidências preservadas;
- parecer interno válido sobre o diff final.

## Interface visual futura

Quando houver frontend, incluir:

- testes de acessibilidade;
- responsividade;
- estados vazios, erro e carregamento;
- navegação por teclado;
- snapshots ou comparação visual com tolerância definida;
- captura automática de telas críticas;
- detecção de links quebrados, overflow e proporções inválidas.