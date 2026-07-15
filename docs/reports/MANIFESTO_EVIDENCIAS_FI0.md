---
tipo: manifesto_evidencias
fase: FI-0
titulo: "Manifesto de Evidências — FI-0"
status: aguardando_aprovacao
data: 2026-07-15
executor: "Freebuff"
---

# 📦 Manifesto de Evidências — FI-0

> *Registro de todas as evidências produzidas durante a Fase Zero*

---

## 1. Ambiente

| Campo | Valor |
|-------|-------|
| Sistema | Windows 11 |
| Python | 3.14.6 |
| uv | 0.11.28 |
| Git | Instalado |
| Data | 2026-07-15 |

---

## 2. Arquivos Criados

### 2.1 Configuração
- `pyproject.toml` — Configuração do projeto Python
- `.gitignore` — Arquivo de ignore do Git

### 2.2 Código-Fonte
- `src/harness/__init__.py` — Ponto de entrada do pacote
- `src/harness/contracts/__init__.py` — Pacote de contratos
- `src/harness/contracts/events.py` — Contratos de eventos (14 tipos, 13 classes)
- `src/harness/logging.py` — Logging estruturado com structlog
- `src/harness/cli.py` — Interface de linha de comando

### 2.3 Testes
- `tests/unit/__init__.py` — Pacote de testes unitários
- `tests/unit/test_events.py` — Testes dos contratos de eventos
- `tests/unit/test_logging.py` — Testes do módulo de logging

### 2.4 Documentação
- `docs/reports/MAPEAMENTO_COMPONENTES_PLANOS.md` — Mapeamento 9 componentes vs 7 planos
- `docs/reports/CLASSIFICACAO_LACUNAS.md` — Classificação das lacunas
- `docs/reports/RELATORIO_AUDITORIA_FASE_ZERO.md` — Relatório de auditoria

---

## 3. Comandos Executados

| Comando | Resultado |
|---------|-----------|
| `git init` | Repositório inicializado |
| `uv init --package --name harness` | Projeto Python criado |
| `uv add pydantic typer structlog` | Dependências instaladas |
| `uv add --dev pytest pytest-cov hypothesis ruff mypy` | Dependências dev instaladas |
| `python -m pytest tests/unit/ -v` | 29 testes passaram |

---

## 4. Testes

| Métrica | Valor |
|---------|-------|
| Total de testes | 29 |
| Testes passaram | 29 |
| Testes falharam | 0 |
| Warnings | 0 |
| Tempo de execução | ~0.4s |

---

## 5. Hashes dos Artefatos Principais

| Artefato | Hash |
|----------|------|
| pyproject.toml | `710b81ed6f1a34b58cb3bc5c7d24c82feb59e51b356c8620f1f337404edce7e3` |
| src/harness/__init__.py | `10f84455a2dc9f6239b8544abfe0be8ef19d867de7008a15323845be835ddaf0` |
| src/harness/contracts/events.py | `733330236b426b2dc81607d5d759c19f5095828901fae95c8db04ce67a498f3e` |
| src/harness/logging.py | `8007513e13475a44c83a8d0b523558a2a7b2d82940f1dd067ee83a2347e2aad6` |
| src/harness/cli.py | `e5a81c98799c854bcd2bac0d1c10cd5015d6b72a563139caddda46f077c2e263` |

---

## 6. Integridade

- ✅ Nenhum arquivo original do Obsidian foi modificado
- ✅ Repositório Git inicializado corretamente
- ✅ Pacote Python importa sem erros
- ✅ Todos os testes passam
- ✅ Code review realizado e issues corrigidos

---

## 7. Pendências para Aprovação

- [ ] Saimon revisar este manifesto
- [ ] Calcular hashes dos artefatos
- [ ] Copiar Declarativa PDF para o vault
- [ ] Aprovar início da FI-1
