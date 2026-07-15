---
tipo: protocolo
titulo: "Protocolo Cognitivo — MEC"
status: ativo
data: 2026-07-15
---

# 🔗 Protocolo Cognitivo — MEC

> *Validação da linguagem cognitiva com cadeias reais de navegação*

---

## 1. Objetivo

Validar que a linguagem da MEC funciona como documento navegável, com links, IDs, evidências referenciadas e inferências marcadas — sem depender de banco, API ou modelo de IA.

---

## 2. Regra de Fonte da Verdade

| Nível | Fonte | Descrição |
|-------|-------|-----------|
| **Normativo** | Repositório Git | Documentos aprovados e versionados são a fonte da especificação |
| **Navegação** | Obsidian Vault | Projeção para navegação e trabalho; não é fonte primária |
| **Operacional (futuro)** | Event Store | Definida nas fases de persistência (FI-3+) |

**Regra:** Nenhum documento Obsidian é tratado como autoridade. O commit aprovado no Git é a fonte normativa.

---

## 3. Cadeia de Navegação

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   ORIGEM    │ →  │   ANTES     │ →  │  DURANTE    │ →  │   DEPOIS    │
│             │    │             │    │             │    │             │
│ Fonte PDF   │    │ Contexto    │    │ Execução    │    │ Resultado   │
│ Hash SHA    │    │ Requisitos  │    │ Evidências  │    │ Aprendizado │
│ Decisões    │    │ Plano       │    │ Changeset   │    │ Release     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 3.1 ORIGEM
- Documento fonte (PDF, arquivo original)
- Hash SHA-256 para integridade
- Data de captura e autor

### 3.2 ANTES
- Contexto recuperado da MEC
- Requisitos aprovados
- Decisões arquiteturais
- Plano versionado

### 3.3 DURANTE
- WorkOrder autorizada
- Execução controlada
- Evidências coletadas
- Changeset produzido

### 3.4 DEPOIS
- Resultado verificado
- Aprendizado registrado
- Contribuição cognitiva proposta
- Release identificada

---

## 4. Separação Epistêmica

| Conceito | Campo | Descrição |
|----------|-------|-----------|
| **Natureza** | `object_type` | O que o objeto É (fact, hypothesis, inference, decision) |
| **Confiabilidade** | `trust_level` | QUÃO confiável é (owner_declared, verified, inferred, unknown) |

**Nunca confundir:** Um objeto pode ser um `fact` com `trust_level=unverified` (é declarado como fato, mas ainda não verificado).

---

## 5. Evidências

Toda afirmação relevante deve referenciar evidências:

```python
EvidenceReference(
    evidence_id="evd_teste123",
    source_description="Teste unitário que valida schema",
    checksum="abc123def456",
    algorithm=ChecksumAlgorithm.SHA256,
    location="tests/unit/test_context.py",
)
```

**Regras:**
- Evidências são imutáveis após vinculadas a gate
- Checksum verifica integridade
- Localização permite reprodutibilidade

---

## 6. IDs

Formato aceito: `prefixo_alfanumérico` (ex: `prj_abc123`, `tsk_def456`)

**Validações:**
- Deve conter pelo menos um underscore
- Prefixo em minúsculas
- Sem caracteres especiais (apenas alfanuméricos e underscore)

---

## 7. Links entre Documentos

| Documento | Tipo | Status |
|-----------|------|--------|
| Doc 0 (Declarativa) | Fonte conceitual | Referenciado, não copiado |
| Doc 1 (Especificação Mestra) | Normativo | Versão de trabalho no vault |
| Doc 4 (Arquitetura Geral) | Normativo | Versão de trabalho no vault |
| Doc 5 (Motor de Execução) | Normativo | Versão de trabalho no vault |
| Doc 6 (Protocolo de Integração) | Normativo | Versão de trabalho no vault |
| Doc 7 (Manual Fabricação) | Normativo | Versão de trabalho no vault |
| Doc 8 (Prompt Mestre) | Normativo | Versão de trabalho no vault |
| GLOSSARY.md | Referência | Projeto |
| Este protocolo | Referência | Projeto |

---

## 8. Status desta Validação

| Critério | Status |
|----------|--------|
| Linguagem definida | ✅ |
| Enums definidos | ✅ |
| Schemas Pydantic criados | ✅ |
| Validação de IDs implementada | ✅ |
| Testes passando (58/58) | ✅ |
| Glossário consistente | ✅ |
| Regra de fonte documentada | ✅ |

---

> *Este protocolo é vivo e será refinado conforme o projeto evolui.*
