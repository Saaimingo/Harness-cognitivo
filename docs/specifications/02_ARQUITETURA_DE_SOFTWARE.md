---
titulo: Arquitetura de Software
status: candidate_for_review
autoriza_implementacao: false
---

# Arquitetura de Software

## Estilo arquitetural

`DECIDIDO`: monólito modular com Ports and Adapters.

O sistema deve crescer por módulos coesos, não por serviços distribuídos prematuros. Distribuição exige ADR, carga medida, boundary estável e plano operacional.

## Camadas

- **Domínio:** entidades, value objects, estados, invariantes e políticas puras.
- **Aplicação:** casos de uso, coordenação, autorização, transações e emissão de eventos.
- **Ports:** interfaces para persistência, LLMs, ferramentas, segredos, relógio, IDs e mensageria.
- **Adapters:** SQLite, filesystem, Git, MCP, APIs, provedores e interfaces.
- **Delivery:** CLI, API local e futura interface visual.

## Módulos candidatos

- projects;
- planning;
- requirements;
- workorders;
- execution;
- reviews;
- testing;
- evidence;
- gate;
- release;
- incidents;
- memory/MEC;
- retrieval;
- model-routing;
- tools;
- security;
- observability;
- operations.

## Regras de dependência

- domínio não depende de framework;
- módulo não acessa tabela de outro módulo diretamente;
- comunicação entre módulos usa contratos de aplicação ou eventos tipados;
- adapters podem depender do domínio, nunca o contrário;
- provedores externos são sempre substituíveis;
- operações remotas precisam de policy check e audit record.

## Estado e transições

Estados críticos devem ser enums fechados e transições devem passar por funções ou serviços de domínio. Atualização direta de status é proibida.

## Eventos

Eventos representam fatos ocorridos, não ordens. Devem conter ID, tipo, versão, timestamp, causation ID, correlation ID, actor, authority e referência de evidência.

## Concorrência

O padrão inicial é execução serial ou concorrência limitada com budgets e locks explícitos. Paralelismo de agentes só é permitido quando não há sobreposição de autoridade ou escrita.

## Falhas

- falhas de domínio são tipadas;
- falhas de infraestrutura são traduzidas em boundaries;
- retry exige idempotência e política;
- nenhuma exceção pode ser convertida silenciosamente em sucesso;
- estados intermediários devem ser recuperáveis.

## Evolução

Novos módulos entram somente quando há boundary real. Duplicação deliberada temporária pode existir durante migração, mas deve ter ticket, prazo e critério de remoção.