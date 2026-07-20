---
tipo: relatorio_fase
fase: FI-2B-Parte1
titulo: "Relatório da FI-2B Parte 1 — ExecutionRun, Review e TestRun"
status: ready_for_review
executor_original: Freebuff
reconciliacao: Codex
data: 2026-07-17
reconciliado_em: 2026-07-18
branch: feat/fi-2b-part1
base_head: be1236ff7885b950cfdd7cdac50c3f9531be48f9
audited_head: d11f983f701936a6b3e7fde68c81fba0699f1fcd
---

# Relatório da FI-2B Parte 1

## 1. Estado deste documento

Este relatório reconcilia o código, a PR #1, o histórico Git e as evidências reproduzidas da FI-2B Parte 1.

- Branch auditada: `feat/fi-2b-part1`.
- Base auditada: `master` em `be1236ff7885b950cfdd7cdac50c3f9531be48f9`.
- `audited_head=d11f983f701936a6b3e7fde68c81fba0699f1fcd`.
- PR #1: aberta, Draft, sem merge.
- Commits no baseline auditado: 9 à frente da base, 0 atrás.
- Estado desta reconciliação: `READY_FOR_REVIEW`, pendente de nova auditoria independente.

O `audited_head` identifica o baseline anterior a esta reconciliação. Este documento não tenta registrar o hash do commit que futuramente possa contê-lo, evitando autorreferência e commits documentais sucessivos apenas para atualizar o próprio hash.

Nenhum merge, tag, release ou avanço para FI-2B Parte 2 é autorizado por este relatório.

## 2. Resumo do escopo implementado

A FI-2B Parte 1 adiciona três entidades de domínio para representar execução verificada:

| Entidade | Responsabilidade | Estados |
|---|---|---|
| ExecutionRun | Tentativa concreta de cumprir uma WorkOrder | initiated, running, completed, failed, abandoned |
| Review | Avaliação estruturada de uma ExecutionRun | requested, in_progress, approved, rejected, change_requested |
| TestRun | Execução verificável de testes e evidências | planned, executing, passed, failed, error |

Também foram adicionados ou ampliados:

- enums de execução, revisão e testes;
- tabelas explícitas de transição;
- políticas puras de domínio;
- invariantes de construção, desserialização e transição;
- testes de regressão e tentativas adversariais;
- rastreabilidade documental da FI-2B Parte 1.

## 3. Fora do escopo

Continuam ausentes e não foram iniciados nesta parte:

- GateDecision;
- Release;
- Incident;
- persistência e repositórios;
- event store;
- executor real de ferramentas;
- integrações externas;
- avanço para FI-3 ou FI-2B Parte 2.

## 4. Entidades e invariantes

### 4.1 ExecutionRun

Principais invariantes:

1. vinculada a uma WorkOrder;
2. estados não iniciais exigem timestamps coerentes;
3. `completed` exige changeset;
4. `failed` exige erro registrado;
5. `abandoned` exige justificativa;
6. campos temporais exigem timezone;
7. construção e desserialização não podem materializar estados impossíveis.

Transições reais: 5 arestas.

```text
initiated -> running
initiated -> abandoned
running -> completed
running -> failed
running -> abandoned
```

### 4.2 Review

Tipos suportados:

- functional;
- domain;
- structural;
- security.

Principais invariantes:

1. vinculada a uma ExecutionRun;
2. decisões terminais exigem revisor e justificativa;
3. aprovação não aceita `blocking_findings`;
4. `change_requested` exige mudanças solicitadas;
5. reviewer e executor devem ser autoridades diferentes;
6. construção e desserialização preservam as invariantes.

Transições reais: 4 arestas.

```text
requested -> in_progress
in_progress -> approved
in_progress -> rejected
in_progress -> change_requested
```

### 4.3 TestRun

Principais invariantes:

1. `planned` não aceita resultados conclusivos;
2. `executing` exige `started_at` e não aceita conclusão antecipada;
3. contagens não podem ser negativas;
4. `passed_tests + failed_tests == total_tests` quando aplicável;
5. `passed` exige total positivo, todas as aprovações, zero falhas e evidências;
6. `failed` exige ao menos uma falha e detalhes;
7. `error` exige mensagem e não aceita contagens de resultado;
8. estados terminais exigem timestamps coerentes;
9. `failed` e `error` permanecem semanticamente distintos.

Transições reais: 4 arestas.

```text
planned -> executing
executing -> passed
executing -> failed
executing -> error
```

## 5. Alterações da PR no baseline auditado

| Métrica | Valor |
|---|---:|
| Arquivos alterados | 12 |
| Inserções | 4.865 |
| Exclusões | 5 |
| Commits à frente de `master` | 9 |
| Commits atrás de `master` | 0 |

Arquivos do baseline da PR:

- `docs/reports/RELATORIO_FI2B_PARTE1.md`;
- `src/harness/domain/enums.py`;
- `src/harness/domain/execution_run.py`;
- `src/harness/domain/policies.py`;
- `src/harness/domain/review.py`;
- `src/harness/domain/test_run.py`;
- `src/harness/domain/transitions.py`;
- `tests/unit/domain/test_execution_run.py`;
- `tests/unit/domain/test_imports.py`;
- `tests/unit/domain/test_policies.py`;
- `tests/unit/domain/test_review.py`;
- `tests/unit/domain/test_test_run.py`.

As alterações da presente reconciliação documental são tratadas separadamente no diff local e não são retroativamente atribuídas ao baseline `d11f983`.

## 6. Histórico da branch auditada

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

Os hashes acima descrevem o baseline auditado. Nenhum hash de commit futuro desta reconciliação é antecipado neste documento.

## 7. Evidências reproduzidas

### 7.1 Ambiente

- Python 3.12.13.
- uv 0.11.29.
- Dependências restauradas pelo `uv.lock` com `uv sync --frozen --all-extras`.
- Checkout isolado de `feat/fi-2b-part1`.
- HEAD local e remoto iguais em `d11f983f701936a6b3e7fde68c81fba0699f1fcd` durante a reprodução do baseline.

### 7.2 Resultados e códigos de saída

| Comando | Código | Resultado |
|---|---:|---|
| `pytest --collect-only -q` | 0 | 534 testes coletados |
| `pytest tests/ -ra --tb=short` | 0 | 534 passed, 1 `PytestCacheWarning` |
| `ruff check src/ tests/` | 0 | All checks passed |
| `ruff format --check src/ tests/` | 0 | 49 arquivos já formatados |
| `mypy src/harness/ --ignore-missing-imports` | 0 | Sem issues em 31 arquivos; nota sobre seção `tests.*` não usada |
| `git diff --check` | 0 | Sem saída |
| `git status --short` | 0 | Sem saída no baseline |
| `git rev-parse HEAD` | 0 | `d11f983f701936a6b3e7fde68c81fba0699f1fcd` |
| `git rev-parse origin/feat/fi-2b-part1` | 0 | `d11f983f701936a6b3e7fde68c81fba0699f1fcd` |
| `git log --oneline master..HEAD` | 0 | 9 commits |

As saídas completas e sanitizadas estão em:

- `evidence/fi2b-part1/2026-07-18/baseline/EVIDENCIAS_FI2B_PARTE1.md`;
- `evidence/fi2b-part1/2026-07-18/baseline/evidence-manifest.json`;
- `evidence/fi2b-part1/2026-07-18/baseline/logs/`.

## 8. Investigação do `PytestCacheWarning`

O warning não foi ocultado nem suprimido.

### Sintoma

O Pytest não conseguiu atualizar `<repo>/.pytest_cache/v/cache/nodeids` por permissão negada. A suíte terminou com código 0 e `534 passed, 1 warning`.

### Causa provável

A `.pytest_cache` pertence à identidade isolada da primeira tentativa e possui ACL mais restrita que o diretório raiz do checkout. A identidade usada na reprodução autorizada conseguiu ler e executar o projeto, mas não modificar o cache pertencente à outra identidade.

Isso caracteriza uma divergência de permissões do ambiente local, não uma falha dos testes ou do domínio.

### Correções propostas — não aplicadas

1. recriar o cache em checkout limpo sob a mesma identidade que executará o Pytest;
2. ajustar a ACL da `.pytest_cache` de forma controlada;
3. validar no runner Linux efêmero do CI, onde workspace e cache pertencem à mesma identidade.

Não foram alterados testes, plugin de cache ou configuração do Pytest. Remoção/recriação do cache e mudança de ACL permanecem dependentes de autorização específica.

Detalhes: `evidence/fi2b-part1/2026-07-18/WARNING_INVESTIGATION.md`.

## 9. Marcos históricos

As tags existentes resolvem para:

| Marco | Commit | Tag |
|---|---|---|
| FI-0 | `b3700c1` | `fi-0-approved` |
| FI-1 | `0b15b5f` | `fi-1-approved` |
| FI-2A | `be1236f` | `fi-2a-approved` |

Não existe tag de aprovação da FI-2B Parte 1.

## 10. Governança da reconciliação

- A FB-0004 recebeu veredito anterior sobre `d11f983`.
- Esta reconciliação altera documentação, workflow e evidências; portanto, um futuro commit/push produzirá novo HEAD e invalidará o uso do veredito anterior para o novo estado.
- A descrição da PR não foi alterada nesta WorkOrder.
- O Obsidian não foi alterado nesta WorkOrder.
- Nenhuma mudança foi realizada em domínio, testes, dependências, `pyproject.toml` ou `uv.lock`.
- A `master` não foi alterada.

## 11. Estado permitido

Após a preparação do diff e a reprodução das validações sobre todas as mudanças locais, o estado máximo permitido é:

`READY_FOR_REVIEW`

Continuam fora da autorização:

- commit;
- push;
- alteração da descrição da PR;
- merge;
- tag;
- release;
- deployment;
- FI-2B Parte 2.

## 12. Apêndice histórico e arquitetural preservado

Este apêndice restaura informações técnicas válidas que constavam do relatório anterior. Ele complementa o estado reconciliado acima e não substitui os números, referências Git ou resultados atuais. Métricas históricas de HEAD, commits e testes não são repetidas aqui.

### A. Políticas de domínio

Os nomes abaixo correspondem às funções existentes no baseline auditado.

| Política | Função | Entidades às quais se aplica |
|---|---|---|
| `execution_run_can_start` | Exige WorkOrder executável, executor identificado e ausência de outra execução ativa | ExecutionRun e WorkOrder |
| `review_requires_independence` | Impede que reviewer e executor sejam a mesma autoridade quando ambos são conhecidos | Review e a ExecutionRun revisada |
| `review_can_be_approved` | Exige justificativa, reviewer identificado e ausência de achados bloqueadores | Review |
| `test_run_can_complete_as_passed` | Exige total de testes e evidências preservadas para conclusão como `passed` | TestRun |
| `test_run_failure_vs_error` | Impede classificar simultaneamente o resultado como falha de teste e erro de infraestrutura | TestRun |

O relatório histórico usava alguns nomes descritivos que não correspondem a funções autônomas no baseline atual:

- `execution_run_can_initiate` corresponde à política existente `execution_run_can_start`;
- `execution_run_can_complete` e `execution_run_can_abandon` descreviam regras que hoje são invariantes e validações de transição da própria `ExecutionRun`, não funções separadas em `policies.py`;
- `review_approved_requires_no_blockers` está representada pela política existente `review_can_be_approved` e pelas invariantes de `Review`.

Essa distinção preserva a intenção registrada sem apresentar nomes históricos como APIs atuais.

### B. Inventário de implementação

Arquivos criados pela implementação da FI-2B Parte 1:

| Arquivo | Responsabilidade |
|---|---|
| `src/harness/domain/execution_run.py` | Modelar tentativas auditáveis de execução de uma WorkOrder e suas transições |
| `src/harness/domain/review.py` | Modelar avaliações estruturadas, tipos de review, achados e independência de autoridade |
| `src/harness/domain/test_run.py` | Modelar execuções de testes, contagens, evidências e distinção entre `failed` e `error` |
| `tests/unit/domain/test_execution_run.py` | Verificar estados, invariantes e transições de ExecutionRun |
| `tests/unit/domain/test_review.py` | Verificar estados, decisões, achados e independência de Review |
| `tests/unit/domain/test_test_run.py` | Verificar estados, contagens, evidências e resultados de TestRun |

Arquivos alterados pela implementação:

| Arquivo | Responsabilidade da alteração |
|---|---|
| `src/harness/domain/enums.py` | Acrescentar estados e tipos usados por ExecutionRun, Review e TestRun |
| `src/harness/domain/policies.py` | Acrescentar políticas puras aplicáveis à execução, revisão e testes |
| `src/harness/domain/transitions.py` | Registrar as tabelas explícitas de transição das três entidades |
| `tests/unit/domain/test_imports.py` | Incluir os novos módulos na verificação de importação |
| `tests/unit/domain/test_policies.py` | Cobrir as novas políticas de domínio |

### C. Decisões arquiteturais

| Decisão preservada | Justificativa registrada |
|---|---|
| ExecutionRun registra a execução, mas não executa ferramentas | Separar o modelo de domínio do executor externo e de infraestrutura |
| Review não modifica o objeto revisado | Manter a avaliação como registro independente e evitar mutação do resultado avaliado |
| Review possui tipos `functional`, `domain`, `structural` e `security` | Representar fidelidades distintas de avaliação sem misturá-las em um único resultado implícito |
| Reviewer e executor devem ser independentes | Evitar conflito de interesse por meio de política e invariantes explícitas |
| TestRun distingue `failed` de `error` | Separar falha de asserção de erro operacional ou de infraestrutura |
| Campos temporais são timezone-aware | Evitar ambiguidade temporal e preservar rastreabilidade |
| Transições retornam nova instância | Preservar imutabilidade convencional e revalidar invariantes a cada mudança de estado |

A alternativa explicitamente rejeitada no histórico foi mascarar a coleta do Pytest por configuração global em `conftest.py`. Os aliases nos testes foram preferidos porque atuam na causa do conflito de nomes e não reduzem silenciosamente a superfície coletada. A marcação `__test__ = False` também não foi adotada como mecanismo de ocultação.

### D. Aplicação dos eixos de governança

| Eixo | Relação válida com a FI-2B Parte 1 |
|---|---|
| SG-0 | A política de início verifica condição executável e autoridade do executor; timestamps exigem timezone; `ReviewType.SECURITY` permite registrar revisão de segurança. O baseline não torna toda security review obrigatória automaticamente. |
| ESQ | ExecutionRun preserva `changeset_id`; TestRun preserva `evidence_hashes`; reviews estruturais e testes separados sustentam verificabilidade e qualidade estrutural. |
| GRN | `ReviewType.DOMAIN` e `referenced_rules` permitem relacionar uma avaliação às regras de negócio; invariantes e políticas mantêm decisões de domínio explícitas. |
| CTP | A rastreabilidade é indireta pela cadeia de identificadores WorkOrder -> ExecutionRun -> Review/TestRun. O baseline não copia nem materializa um pacote de promoção dentro dessas entidades. |

### E. Correção histórica dos warnings de coleta

O warning histórico era um `PytestCollectionWarning`: imports com os nomes `TestRun` e `TestRunStatus` em módulos de teste podiam ser interpretados pelo Pytest como classes coletáveis por começarem com `Test`.

A correção adotada usou aliases explícitos nos módulos de teste, por exemplo:

```python
from harness.domain.test_run import TestRun as DomainTestRun
from harness.domain.enums import TestRunStatus as DomainTestRunStatus
```

Foram preservadas as seguintes decisões:

- não usar `conftest.py` com `collect_ignore`, pois isso poderia ocultar módulos ou reduzir silenciosamente a coleta futura;
- não inserir `__test__ = False` no domínio como ocultação artificial;
- manter os testes coletáveis e resolver o conflito no ponto de importação por aliases.

Esse warning histórico de descoberta de classes é diferente do warning atual. A evidência reconciliada registra um `PytestCacheWarning`, causado pela impossibilidade de atualizar `.pytest_cache` no ambiente Windows por permissão negada. O warning atual não foi suprimido e não representa regressão da correção por aliases.

### F. Riscos residuais

| Risco ainda aplicável | Situação e tratamento |
|---|---|
| Imutabilidade convencional | Os modelos não usam congelamento estrutural; a disciplina depende das transições que retornam novas instâncias e da revalidação por Pydantic |
| Crescimento dos arquivos de evidência | Logs e relatórios podem aumentar o repositório; requer política futura de retenção sem remover a rastreabilidade atual |
| Ausência de CI remoto | O workflow foi preparado, mas não haverá execução remota até o primeiro push autorizado |
| Integração com infraestrutura | Persistência, executor de ferramentas e integrações continuam fora desta parte e permanecem risco para fases posteriores |
| Cache local do Pytest | A ACL da `.pytest_cache` continua produzindo `PytestCacheWarning`; qualquer correção de permissão permanece separada e dependente de autorização |
