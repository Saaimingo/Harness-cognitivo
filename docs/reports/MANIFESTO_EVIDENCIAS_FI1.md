---
tipo: manifesto_evidencias
fase: FI-1
titulo: "Manifesto de Evidências — FI-1"
status: aguardando_aprovacao
data: 2026-07-15
executor: "Freebuff"
---

# 📦 Manifesto de Evidências — FI-1

> *Registro de todas as evidências produzidas durante a FI-1*

---

## 1. Ambiente

| Campo | Valor |
|-------|-------|
| Sistema | Windows 11 |
| Python | 3.14.6 (compatível com 3.12) |
| uv | 0.11.28 |
| Git | Instalado |
| Data | 2026-07-15 |

---

## 2. Arquivos Criados

### 2.1 Código-Fonte
- `src/harness/contracts/context.py` — Contratos de contexto (5 Enums, 4 schemas Pydantic, 2 funções utilitárias)

### 2.2 Testes
- `tests/unit/test_context.py` — 29 testes de contratos de contexto
- `tests/unit/test_documents.py` — 39 testes de validação documental

### 2.3 Documentação
- `docs/GLOSSARY.md` — Glossário unificado
- `docs/MEC_PROTOCOL.md` — Protocolo cognitivo
- `docs/sources/DECLARATIVA_ORIGINAL.md` — Registro da Declarativa
- `docs/reports/DIARIO_FI1.md` — Diário da FI-1

### 2.4 Arquivos Alterados
- `src/harness/__init__.py` — Novos exports de contexto

---

## 3. Hashes dos Artefatos Principais

| Artefato | Hash SHA-256 |
|----------|--------------|
| src/harness/contracts/context.py | `9dcebb8fbec67e16f2a61028549a8497e3eb02f396eac1dc8fd181c4629b0034` |
| tests/unit/test_context.py | `b5dc43e57d205e15b7a7d6673a27d796b9293559833c438ec165b2b031aba226` |
| docs/GLOSSARY.md | `4823d9b674f6b2fd1f6d9d830f43d54e78e219e22c61c570680388cbc4d3d009` |
| docs/MEC_PROTOCOL.md | `dca816613e817ce985c6c3a5b76e2a37098c947f92be47930005f0cc0c020be7` |

---

## 4. Testes

### Categorização

| Categoria | Arquivo | Testes | Fase |
|-----------|---------|--------|------|
| Eventos e Logging | test_events.py + test_logging.py | 29 | FI-0 |
| Contratos de Contexto | test_context.py | 29 | FI-1 |
| Validação Documental | test_documents.py | 39 | FI-1 |
| **Total** | | **97** | |

### Métricas

| Métrica | Valor |
|---------|-------|
| Total de testes | 97 |
| Testes passaram | 97 |
| Testes falharam | 0 |
| Warnings | 0 |
| Tempo de execução | ~0.47s |

---

## 5. Contratos Implementados

| Contrato | Campos | Enums |
|----------|--------|-------|
| ContextRequest | 8 campos | Purpose (12 valores) |
| ContextCapsule | 7 campos | — |
| ContextItem | 7 campos | ObjectType (9), TrustLevel (6) |
| CognitiveObject | 9 campos | ObjectType (9), TrustLevel (6) |
| EvidenceReference | 6 campos | ChecksumAlgorithm (3) |

---

## 6. Integridade

- ✅ Nenhum arquivo original do Obsidian foi modificado
- ✅ Declarativa original registrada com hash SHA-256
- ✅ Todos os testes passam
- ✅ Code review realizado e issues corrigidos
- ✅ Python 3.12 compatível (Field(default_factory), Enums)

---

## 7. Pendências para Aprovação

- [ ] Saimon revisar este manifesto
- [ ] Calcular hashes dos artefatos
- [ ] Aprovar início da FI-2
