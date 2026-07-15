---
tipo: diario
titulo: "Diário do Projeto — FI-1"
status: ativo
data: 2026-07-15
---

# 📔 Diário do Projeto — FI-1

---

## 2026-07-15 — Início da FI-1

**Evento:** Autorização condicional da FI-1

**Correções obrigatórias incorporadas:**
1. Escopo: contratos executáveis Pydantic + testes (não serviços)
2. Python 3.12 compatível
3. Field(default_factory) para mutáveis
4. Enum/Literal para vocabulário controlado
5. Separação object_type vs trust_level
6. Contrato EvidenceReference
7. Validação de formato para IDs
8. Regra de fonte da verdade documentada
9. Declarativa original registrada
10. EventLogger fora do escopo
11. DIARIO_FI1.md separado
12. Testes de documentos via manifesto

**Arquivos criados:**
- `src/harness/contracts/context.py` — Schemas de contexto
- `tests/unit/test_context.py` — 29 novos testes
- `docs/GLOSSARY.md` — Glossário unificado
- `docs/MEC_PROTOCOL.md` — Protocolo cognitivo
- `docs/sources/DECLARATIVA_ORIGINAL.md` — Registro da Declarativa
- `docs/reports/DIARIO_FI1.md` — Este diário

**Métricas:**
- 58 testes passando (29 da FI-0 + 29 novos)
- Zero warnings
- 5 Enums definidos
- 4 schemas Pydantic criados
- Função de validação de IDs
- Função de detecção de duplicatas

**Pendências para continuação:**
- Atualizar __init__.py com novos exports
- Criar manifesto de evidências FI-1
- Gerar relatório final FI-1

---

> *Este diário é vivo e deve ser atualizado a cada marco da FI-1.*
