---
tipo: arquitetura
titulo: "CTP — Chat-to-Project (Promoção de Conversa para Projeto)"
status: ativo
data: 2026-07-15
eixo: CTP
---

# 💬 CTP — Chat-to-Project

> *"Permitir que uma conversa madura de concepção seja transformada diretamente em entrada formal para o Harness."*

---

## 1. Objetivo

Eliminar a necessidade de:
- Exportação manual de conversas
- Cópia e colagem de contexto
- Reexplicação do que já foi decidido
- Perda de contexto entre chat e projeto

---

## 2. Fluxo Conceitual

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  CONVERSA    │ →  │  DOCUMENTAÇÃO │ →  │  APROVAÇÃO   │
│  LIVRE       │    │  FINAL        │    │  EXPLÍCITA   │
└──────────────┘    └──────────────┘    └──────────────┘
                                              │
                                              ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  CRIAÇÃO     │ ←  │  PACOTE DE   │ ←  │  SNAPSHOT    │
│  DO PROJETO  │    │  PROMOÇÃO    │    │  DA CONVERSA │
└──────────────┘    └──────────────┘    └──────────────┘
       │
       ▼
┌──────────────┐
│  PLANEJAMENTO│
│  PELOS       │
│  AGENTES     │
└──────────────┘
```

---

## 3. Princípios Fundamentais

### 3.1 Fonte Normativa

> **A documentação final aprovada é a fonte normativa principal.**

- Não a conversa inteira
- Não trechos exploratórios
- A documentação que o usuário aprovou explicitamente

### 3.2 Linhagem

A conversa completa permanece vinculada como:
- **Origem** — de onde veio a ideia
- **Contexto** — o que foi considerado
- **Histórico** — como evoluiu
- **Justificativa** — por que decisões foram tomadas
- **Evidência de intenção** — prova do que o usuário queria
- **Material para resolução de ambiguidades** — quando algo não está claro

### 3.3 Precedência

Quando houver conflito:
1. Documentação final aprovada **prevalece** sobre trechos exploratórios
2. Alterações posteriores devem gerar nova versão, adendo ou solicitação formal
3. Histórico original **não deve ser apagado**

### 3.4 Continuidade

> A continuidade pertence aos dados, ao documento, à conversa e à linhagem — **não à identidade do modelo**.

- Não pressupor que o mesmo modelo do chat precise executar o projeto
- Modelo é apenas metadado
- Dados são o que importa

---

## 4. ProjectPromotionPackage

### 4.1 Campos

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `package_id` | str | ✅ | ID único (formato: `pkg_xxx`) |
| `title` | str | ✅ | Título do projeto promovido |
| `approved_document` | str | ✅ | Documento principal aprovado (conteúdo) |
| `conversation_snapshot` | str | ✅ | Snapshot completo da conversa |
| `attachments` | list[dict] | ❌ | Anexos adicionais |
| `version` | int | ✅ | Versão do pacote |
| `promotion_date` | datetime | ✅ | Data da promoção |
| `responsible_user` | str | ✅ | Usuário responsável pela promoção |
| `participating_models` | list[str] | ❌ | Modelos participantes (apenas metadado) |
| `integrity_hashes` | dict[str, str] | ✅ | Hashes de integridade dos artefatos |
| `known_pending_items` | list[str] | ❌ | Pendências conhecidas |
| `initial_instructions` | str | ❌ | Instruções iniciais para o projeto |
| `initial_permissions` | list[str] | ❌ | Permissões iniciais |
| `created_project_id` | str \| None | ❌ | ID do projeto criado (preenchido após criação) |

### 4.2 Integridade

Cada artefato do pacote deve ter hash SHA-256 registrado:

```python
integrity_hashes = {
    "approved_document": "sha256:abc123...",
    "conversation_snapshot": "sha256:def456...",
}
```

---

## 5. Processo de Promoção

### 5.1 Pré-Condições

1. Conversa atingiu maturidade suficiente
2. Documentação final foi gerada no chat
3. Usuário aprovou explicitamente a documentação

### 5.2 Execução

1. **Snapshot** — capturar estado final da conversa
2. **Empacotamento** — criar ProjectPromotionPackage
3. **Validação** — verificar integridade e completude
4. **Registro** — armazenar pacote com hashes
5. **Criação** — criar projeto no Harness a partir do pacote
6. **Vinculação** — associar conversa ao projeto criado

### 5.3 Pós-Condições

- Projeto criado com status `CAPTURED`
- Conversa vinculada como origem
- Documentação aprovada como fonte normativa
- Pendências registradas

---

## 6. Capacidades Futuras

### 6.1 Criar Projeto a Partir da Conversa

```
conversa madura → aprovação → promoção → projeto criado
```

### 6.2 Enviar Atualização da Conversa para Projeto Existente

```
conversa com mudanças → análise de impacto → solicitação de mudança
```

### 6.3 Transformar Atualização em Solicitação de Mudança

```
atualização detectada → classificação → change request criada
```

### 6.4 Analisar Impacto Antes de Incorporar Mudança

```
change request → análise de impacto → aprovação/rejeição → incorporação
```

---

## 7. Integração com Eixos

### 7.1 CTP → FI-3 (Persistência)

- Pacotes de promoção devem ser persistidos
- Snapshots devem ser armazenados
- Hashes devem ser verificáveis

### 7.2 CTP → FI-5 (Contexto e Linhagem)

- Conversa original deve ser recuperável
- Linhagem deve ser rastreável
- Contexto deve ser reconstruível

### 7.3 CTP → FI-6 (CLI ou Interface)

- Interface de promoção deve existir
- Workflow de aprovação deve ser suportado
- Status de promoção deve ser visível

### 7.4 CTP → FI-11 (Distribuição aos Agentes)

- Documentação aprovada deve ser distribuída
- Regras extraídas devem ser incluídas
- Contexto deve ser formatado para agentes

### 7.5 CTP → GRN

- Regras de negócio devem ser extraídas do documento aprovado
- Objetivos e processos devem ser identificados
- Catálogo inicial deve ser gerado

---

## 8. Segurança (SG-0)

| Regra | Descrição |
|-------|-----------|
| **Integridade** | Hashes verificados antes de uso |
| **Imutabilidade** | Conversas originais não modificáveis |
| **Auditoria** | Promoções registradas com timestamp e autor |
| **Permissões** | Acesso controlado a pacotes de promoção |

---

## 9. Qualidade (ESQ)

| Regra | Descrição |
|-------|-----------|
| **Schema** | ProjectPromotionPackage é Pydantic BaseModel |
| **Validação** | Campos obrigatórios verificados |
| **Testes** | Criação e validação de pacotes testados |
| **Documentação** | Cada campo documentado |

---

## 10. Exemplo Conceitual

```python
package = ProjectPromotionPackage(
    package_id="pkg_conversa001",
    title="Sistema de Gestão de Estoque",
    approved_document="# Especificação...\n\n## Requisitos...",
    conversation_snapshot="Usuário: Quero um sistema...\nAI: Entendi...",
    version=1,
    promotion_date=datetime.now(timezone.utc),
    responsible_user="saimon",
    participating_models=["mimo-v2.5"],
    integrity_hashes={
        "approved_document": "sha256:abc123...",
        "conversation_snapshot": "sha256:def456...",
    },
    known_pending_items=["Definir tecnologia de frontend"],
)
```

---

## 11. Relação com Outros Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | CTP protege integridade e imutabilidade dos artefatos |
| **ESQ** | CTP define padrões para o pacote de promoção |
| **GRN** | CTP extrai regras do documento aprovado |

---

> *Este documento é vivo e deve ser refinado a cada nova fase do projeto.*
