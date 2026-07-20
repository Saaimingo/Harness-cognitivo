# Evidencias reproduzidas - FI-2B Parte 1

- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`
- branch: `feat/fi-2b-part1`
- caminhos locais: sanitizados

## 01 - `pytest --collect-only -q`

- Inicio: 2026-07-18T22:40:48.9000223-03:00
- Fim: 2026-07-18T22:40:53.0404192-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/01-pytest-collect-only.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
tests/unit/domain/test_execution_run.py: 69
tests/unit/domain/test_imports.py: 17
tests/unit/domain/test_invariants.py: 9
tests/unit/domain/test_plan.py: 7
tests/unit/domain/test_policies.py: 37
tests/unit/domain/test_project.py: 31
tests/unit/domain/test_requirement.py: 5
tests/unit/domain/test_review.py: 71
tests/unit/domain/test_task.py: 28
tests/unit/domain/test_test_run.py: 93
tests/unit/domain/test_transitions.py: 56
tests/unit/domain/test_work_order.py: 14
tests/unit/test_context.py: 29
tests/unit/test_documents.py: 39
tests/unit/test_events.py: 15
tests/unit/test_logging.py: 14
```

## 02 - `pytest tests/ -ra --tb=short`

- Inicio: 2026-07-18T22:40:53.0508669-03:00
- Fim: 2026-07-18T22:40:55.9499395-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/02-pytest-tests.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
........................................................................ [ 13%]
........................................................................ [ 26%]
........................................................................ [ 40%]
........................................................................ [ 53%]
........................................................................ [ 67%]
........................................................................ [ 80%]
........................................................................ [ 94%]
..............................                                           [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\_pytest\cacheprovider.py:469
  <repo>\.venv\Lib\site-packages\_pytest\cacheprovider.py:469: PytestCacheWarning: could not create cache path <repo>\.pytest_cache\v\cache\nodeids: [WinError 5] Acesso negado: '<repo>\\.pytest_cache\\v\\cache'
    config.cache.set("cache/nodeids", sorted(self.cached_nodeids))

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
534 passed, 1 warning in 0.95s
```

## 03 - `ruff check src/ tests/`

- Inicio: 2026-07-18T22:40:55.9509396-03:00
- Fim: 2026-07-18T22:40:56.0015275-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/03-ruff-check.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
All checks passed!
```

## 04 - `ruff format --check src/ tests/`

- Inicio: 2026-07-18T22:40:56.0025276-03:00
- Fim: 2026-07-18T22:40:56.0511357-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/04-ruff-format-check.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
49 files already formatted
```

## 05 - `mypy src/harness/ --ignore-missing-imports`

- Inicio: 2026-07-18T22:40:56.0521362-03:00
- Fim: 2026-07-18T22:41:07.6753439-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/05-mypy.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
pyproject.toml: note: unused section(s): module = ['tests.*']
Success: no issues found in 31 source files
```

## 06 - `git diff --check`

- Inicio: 2026-07-18T22:41:07.6763441-03:00
- Fim: 2026-07-18T22:41:07.7295595-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/06-git-diff-check.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
(sem saida)
```

## 07 - `git status --short`

- Inicio: 2026-07-18T22:41:07.7305751-03:00
- Fim: 2026-07-18T22:41:07.7829901-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/07-git-status-short.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
(sem saida)
```

## 08 - `git rev-parse HEAD`

- Inicio: 2026-07-18T22:41:07.7840551-03:00
- Fim: 2026-07-18T22:41:07.8302047-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/08-git-rev-parse-head.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
d11f983f701936a6b3e7fde68c81fba0699f1fcd
```

## 09 - `git rev-parse origin/feat/fi-2b-part1`

- Inicio: 2026-07-18T22:41:07.8302047-03:00
- Fim: 2026-07-18T22:41:07.8749837-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/09-git-rev-parse-origin-feature.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
d11f983f701936a6b3e7fde68c81fba0699f1fcd
```

## 10 - `git log --oneline master..HEAD`

- Inicio: 2026-07-18T22:41:07.8764655-03:00
- Fim: 2026-07-18T22:41:07.9254317-03:00
- Codigo de saida: 0
- Resultado: PASS
- Log: `logs/10-git-log-master-head.log`
- audited_head: `d11f983f701936a6b3e7fde68c81fba0699f1fcd`

```text
d11f983 docs(report): FB-0004 final reconciliation — HEAD a486be6, 8 commits
a486be6 docs(report): finalize FB-0004 — HEAD 14316f6, 7 commits, 534 tests
14316f6 docs(report): FB-0004 reconcile report with real state — HEAD cd757b1, 6 commits, 13 arestas, 534 tests
cd757b1 fix(domain): FB-0003 canonical TestRun invariants — PLANNED/EXECUTING/FAILED validation, transition_to counts, adversarial tests, report reconciliation
0936955 fix(domain): harden FI-2B invariants — model_validate revalidation, adversarial tests, report update
4b04d02 fix(domain): harden FI-2B invariants on construction and deserialization
5b392e1 docs(report): record FI-2B part 1 evidence
7325efa test(domain): validate FI-2B part 1 behavior
61d58ca feat(domain): implement FI-2B execution review and test run models
```
