---
tipo: constituição
titulo: "ESQ — Constituição de Engenharia de Software"
status: ativo
data: 2026-07-15
eixo: ESQ
---

# 🔧 ESQ — Constituição de Engenharia de Software

> *"Funcionar não é suficiente. O código também deve ser legível, coeso, testável, rastreável, sustentável e compatível com a arquitetura."*

---

## 1. Identidade de Código do Harness

O código do Harness Cognitivo possui identidade própria. Ele deve ser:

| Característica | Descrição |
|----------------|-----------|
| **Legível** | Qualquer pessoa familiarizada com Python deve entender o fluxo |
| **Coeso** | Cada módulo faz uma coisa e faz bem |
| **Testável** | Lógica de negócio isolada de infraestrutura |
| **Rastreável** | Decisões documentadas, origem rastreável |
| **Sustentável** | Modificações futuras não devem exigir remendos |
| **Consistente** | Padrões seguidos uniformemente |

---

## 2. Padrões de Organização

### 2.1 Estrutura de Pacotes

```
src/harness/
├── domain/          # Entidades, regras, invariantes (PURO)
├── contracts/       # Schemas, eventos, interfaces
├── control/         # Orquestração e governança (FI-4+)
├── execution/       # Motor de execução (FI-2B+)
├── testing/         # Geração e avaliação de testes (FI-2+)
├── delivery/        # Release e implantação (FI-2B+)
├── projects/        # Gestão de projetos (FI-3+)
├── agents/          # Agentes e papéis (FI-11+)
├── cognition/       # RAG, grafo, memória (FI-5+)
├── integrations/    # Adaptadores externos (FI-7+)
├── interfaces/      # CLI, API, web (FI-6+)
├── observability/   # Logging, métricas, tracing (FI-0+)
└── operations/      # Operações e manutenção (FI-10+)
```

### 2.2 Separación por Camada

| Camada | Dependências Permitidas |
|--------|------------------------|
| **domain/** | Nenhuma (apenas pydantic para modelagem) |
| **contracts/** | Nenhuma (apenas pydantic para modelagem) |
| **control/** | domain, contracts |
| **execution/** | domain, contracts, control |
| **testing/** | domain, contracts |
| **delivery/** | domain, contracts, control, execution |
| **observability/** | Nenhuma (infraestrutura pura) |

---

## 3. Convenções de Nomes

### 3.1 Módulos

- `snake_case` para arquivos e funções
- `PascalCase` para classes e enums
- `UPPER_SNAKE_CASE` para constantes

### 3.2 Variáveis e Funções

- Variáveis: `snake_case` descritivo
- Funções de transição: `transition_to_<estado>()`
- Funções de verificação: `can_<ação>()` ou `is_<estado>()`
- Políticas: `<entidade>_can_<ação>()`

### 3.3 Enums

- Nome do enum em `PascalCase` singular
- Valores em `snake_case`
- Documentar semântica no docstring

### 3.4 Exceções

- Sufixo `Error` para todas as exceções de domínio
- Herdar de `DomainError` (base)
- Incluir `entity`, `state` ou contexto relevante

---

## 4. Contratos Explícitos

### 4.1 Tipos de Contrato

| Tipo | Localização | Exemplo |
|------|-------------|---------|
| **Entidade** | `domain/` | Project, Task, WorkOrder |
| **Schema** | `contracts/` | ContextRequest, EvidenceReference |
| **Evento** | `contracts/events.py` | Event, TaskCreated |
| **Política** | `domain/policies.py` | project_can_become_ready |
| **Transição** | `domain/transitions.py` | PROJECT_TRANSITIONS |

### 4.2 Regras de Contrato

1. Todo contrato deve ser `BaseModel` (Pydantic)
2. Campos mutáveis devem usar `Field(default_factory=...)`
3. IDs devem seguir o padrão `prefixo_alfanumérico`
4. Campos temporais devem exigir timezone
5. Enums devem ter valores `str` para serialização

---

## 5. Separação de Responsabilidades

| Responsabilidade | Quem | Onde |
|------------------|------|------|
| Definir regras de negócio | Domínio | `domain/` |
| Definir schemas | Contratos | `contracts/` |
| Orquestrar fluxo | Controle | `control/` |
| Executar trabalho | Execução | `execution/` |
| Gerar evidências | Testes | `testing/` |
| Registrar observabilidade | Observabilidade | `observability/` |

---

## 6. Tratamento de Erros

### 6.1 Princípios

1. **Exceções específicas** — nunca `ValueError` genérico para erros de domínio
2. **Contexto rico** — exceção deve conter entity, state, allowed, details
3. **Hierarquia clara** — `DomainError` como base, especializações abaixo
4. **Idiomatico** — usar `raise` com contexto, não返回 None

### 6.2 Hierarquia de Exceções

```
DomainError (base)
├── InvalidTransitionError
├── InvariantViolationError
├── ReworkLimitExceededError
├── MissingAuthorityError
├── MissingEvidenceError
├── TimezoneRequiredError
└── DuplicateTransitionError
```

---

## 7. Imutabilidade

### 7.1 Regra

> Entidades de domínio são imutáveis. Transições retornam nova instância.

### 7.2 Implementação

```python
# Correto
new_entity = entity.transition_to(target)
# entity permanece inalterado

# Incorreto
entity.status = target  # MUTAÇÃO — proibido
```

### 7.3 Onde Aplicar

- Entidades de domínio (Project, Task, WorkOrder, etc.)
- Schemas de contrato (Event, ContextCapsule, etc.)
- Resultados de políticas (PolicyResult é frozen)

---

## 8. Controle de Efeitos Colaterais

### 8.1 Princípio

> Domínio não pode ter efeitos colaterais. Infraestrutura pode.

### 8.2 Separação

| Camada | Efeitos Colaterais |
|--------|-------------------|
| `domain/` | Nenhum (puro) |
| `contracts/` | Nenhum (puro) |
| `control/` | Orquestração (chama infraestrutura) |
| `execution/` | Execução de código, rede, filesystem |
| `observability/` | Escrita de logs |

---

## 9. Comentários e Docstrings

### 9.1 Princípio Fundamental

- **Código** explica O QUE faz
- **Comentários** explicam POR QUE a decisão existe, quais invariantes devem ser preservadas, e onde há risco futuro

### 9.2 Quando Comentar

| Situação | Comentário |
|----------|------------|
| Decisão arquitetural não óbvia | ✅ Sim |
| Invariante que deve ser preservado | ✅ Sim |
| Risco futuro conhecido | ✅ Sim |
| Referência a especificação/fonte | ✅ Sim |
| O que o código faz (já óbvio) | ❌ Não |
| Código autoexplicativo | ❌ Não |
| Documentação excessiva | ❌ Não |

### 9.3 Formato

```python
# Decisão: Por que este valor é 5 e não outro?
# Invariante: Este campo NUNCA deve ser None após transição para AUTHORIZED.
# Risco: Se este enum for expandido, verificar TODAS as tabelas de transição.
```

---

## 10. Pontos Sensíveis

### 10.1 Áreas Críticas

| Área | Risco | Proteção |
|------|-------|----------|
| Tabelas de transição | Inconsistência | Testes de completude |
| Políticas | Lógica incorreta | Testes parametrizados |
| Validação de IDs | Formato inválido | Reutilização de FI-1 |
| Timezone | Dados inconsistentes | Validadores obrigatórios |
| Imutabilidade | Estado corrompido | Testes de idempotência |

---

## 11. ADRs (Architecture Decision Records)

### 11.1 Quando Criar ADR

- Decisão que afeta mais de um módulo
- Decisão que não pode ser revertida facilmente
- Decisão que conflita com padrão anterior
- Decisão que introduz nova dependência

### 11.2 Formato

```
# ADR-XXXX: Título

## Status
Aceito / Rejeitado / Deprecado

## Contexto
O que está acontecendo que força esta decisão?

## Decisão
O que foi decidido?

## Consequências
O que fica mais fácil? O que fica mais difícil?
```

---

## 12. Controle de Dívida Técnica

### 12.1 Classificação

| Tipo | Descrição | Ação |
|------|-----------|------|
| **Crítica** | Impede funcionalidade ou segurança | Corrigir imediatamente |
| **Maior** | Degrada manutenibilidade | Corrigir na próxima fase |
| **Menor** | Inconveniência cosmética | Registrar e priorizar |
| **Consciente** | Escolhida intencionalmente (ex: MVP) | Documentar e planejar correção |

### 12.2 Registro

Toda dívida técnica deve ser registrada com:
- Localização (arquivo + linha)
- Tipo
- Justificativa
- Fase planejada para correção

---

## 13. Testes Arquiteturais

### 13.1 O que Testar

| Teste | O que Valida |
|-------|-------------|
| `test_imports.py` | Ausência de dependências proibidas |
| `test_domain_files_count.py` | Contagem correta de módulos |
| `test_pydantic_is_present.py` | Dependência de modelagem disponível |
| `test_all_enum_values_in_table.py` | Completude das tabelas de transição |

### 13.2 Regra

> Testes arquiteturais não devem ser enfraquecidos para obter aprovação.

---

## 14. Dependências Proibidas no Domínio

| Categoria | Dependências Proibidas |
|-----------|----------------------|
| **Banco** | sqlalchemy, sqlite, alembic, peewee, tortoise, orm, django |
| **Rede** | requests, httpx, aiohttp, urllib3 |
| **IA** | openai, anthropic, google.generativeai, cohere |
| **MCP** | mcp |
| **Web** | fastapi, uvicorn, flask |
| **Sistema** | os.path, shutil, asyncio, threading, subprocess, socket |

---

## 15. Gate de Qualidade Estrutural

Antes de qualquer aprovação de fase, verificar:

- [ ] Todos os testes passando
- [ ] Zero warnings
- [ ] Sem imports proibidos no domínio
- [ ] Completude das tabelas de transição
- [ ] Imutabilidade preservada
- [ ] Timezone obrigatório em todos os campos temporais
- [ ] Comentários apenas onde necessários
- [ ] Sem código morto relevante
- [ ] Sem duplicação de regra de negócio
- [ ] ADRs criados para decisões significativas

---

## 16. Papel Futuro: Engenheiro de Software

| Responsabilidade | Momento |
|------------------|---------|
| Avaliar impacto arquitetural | Antes da implementação |
| Definir restrições técnicas | Durante o planejamento |
| Revisar resultado | Após a implementação |
| Verificar sistema como um todo | Não apenas o diff |
| Detectar acoplamento, duplicação, remendos | Sempre |
| Gate próprio ou participação obrigatória | No gate final |

---

## 17. Relação com Outros Eixos

| Eixo | Relação |
|------|---------|
| **SG-0** | ESQ complementa segurança com qualidade estrutural |
| **GRN** | ESQ garante que regras de negócio são implementadas com qualidade |
| **CTP** | ESQ define padrões para código gerado a partir de promoções |

---

> *Esta constituição é viva e deve ser revisada a cada fase significativa do projeto.*
