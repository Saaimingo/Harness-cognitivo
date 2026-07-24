---
titulo: Especificação Técnica Mestra do Harness Cognitivo
status: candidate_for_review
versao: 0.1.0
autoriza_implementacao: false
proxima_fase_autorizada: nenhuma
---

# Especificação Técnica Mestra

## 1. Finalidade

Converter a visão, a Bíblia, os contratos e o roadmap do Harness Cognitivo em regras técnicas verificáveis para produto, arquitetura, stack, segurança, dados, integrações, testes, observabilidade e operação.

Esta especificação não autoriza implementação. Ela reduz improvisação, impede escolhas silenciosas por agentes e fornece material, ferramentas e limites antes da execução.

## 2. Princípios obrigatórios

- local-first e modelo-independente;
- monólito modular antes de distribuição;
- domínio puro antes de adapters;
- contratos antes de provedores;
- evidência antes de aprovação;
- segurança, observabilidade e recuperação como requisitos transversais;
- menor privilégio e negação por padrão;
- ações externas e destrutivas sempre autorizadas e auditáveis;
- qualquer mudança após auditoria invalida o veredito anterior;
- componentes substituíveis não podem contaminar o domínio.

## 3. Arquitetura de referência

```text
Interação
  CLI / MCP / API local / futura interface visual
        ↓
Aplicação
  casos de uso, coordenação, WorkOrders, políticas
        ↓
Domínio
  entidades, estados, invariantes, decisões puras
        ↓
Ports
  persistência, modelos, ferramentas, eventos, segredos
        ↓
Adapters
  SQLite, provedores LLM, Git, filesystem, APIs externas
        ↓
Evidência e Observabilidade
  logs estruturados, traces, métricas, artefatos, auditoria
```

Dependências apontam para dentro. O domínio não importa FastAPI, SQLAlchemy, SDKs de provedores, GitHub, OpenAI, Hermes ou infraestrutura.

## 4. Decisões consolidadas

| Área | Estado | Decisão |
|---|---|---|
| Linguagem do núcleo | DECIDIDO | Python 3.12 |
| Arquitetura | DECIDIDO | monólito modular, Ports and Adapters |
| Modelagem | DECIDIDO | Pydantic 2 nos contratos de fronteira; dataclasses ou modelos puros no domínio conforme ADR |
| Ambiente e lock | DECIDIDO | uv e `uv.lock` |
| Persistência inicial | DECIDIDO | SQLite, SQLAlchemy 2 e Alembic |
| Busca textual inicial | DECIDIDO | SQLite FTS5 |
| CLI | DECIDIDO | Typer |
| API local | CANDIDATO | FastAPI atrás de application ports |
| MCP | CANDIDATO | adapter de integração, nunca dependência do domínio |
| Testes | DECIDIDO | pytest, Hypothesis e testes adversariais |
| Qualidade | DECIDIDO | Ruff, mypy e validação de diff |
| CI | DECIDIDO | GitHub Actions |
| Frontend visual | ADIADO | somente após requisitos de experiência aprovados |
| Banco distribuído | ADIADO | PostgreSQL apenas por necessidade comprovada |
| Microsserviços | PROIBIDO no MVP | somente mediante ADR e evidência operacional |
| Provedor LLM | SUBSTITUIVEL | roteado por adapter e políticas observáveis |

## 5. Entregáveis obrigatórios antes de implementar uma área

1. requisitos e critérios de aceitação;
2. limites do domínio e contratos;
3. ameaças e controles;
4. decisão de stack classificada;
5. ADR para decisão material;
6. plano de testes e evidências;
7. plano de observabilidade e recuperação;
8. WorkOrder autorizada.

## 6. Regras para agentes

Um executor não pode:

- escolher framework ou provedor material sem especificação ou ADR;
- substituir tecnologia decidida porque conhece outra melhor;
- iniciar frontend, deploy, rede ou banco distribuído sem fase autorizada;
- reduzir validações para concluir mais rápido;
- ultrapassar `INTERNAL_REVIEW_CHANGES_REQUIRED`;
- declarar `APPROVED` ou `COMPLETED`.

Quando uma decisão estiver ausente, o resultado correto é `SPECIFICATION_GAP_REQUIRES_DECISION`.

## 7. Critério de conformidade

Uma entrega é tecnicamente conforme quando:

- satisfaz requisitos funcionais e não funcionais aplicáveis;
- respeita dependências e boundaries;
- possui testes objetivos e evidências reproduzíveis;
- não amplia superfície de ataque sem controle;
- registra decisões materiais;
- mantém rollback ou caminho de recuperação;
- foi revisada por autoridade independente;
- foi auditada no SHA publicado.

## 8. Documentos subordinados

As especificações 01 a 11 detalham esta norma. ADRs aprovados podem especializar decisões, mas não contrariar princípios constitucionais sem decisão soberana explícita.