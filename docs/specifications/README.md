---
titulo: Índice das Especificações Técnicas
status: candidate_for_review
autoriza_implementacao: false
proxima_fase_autorizada: nenhuma
---

# Especificações Técnicas do Harness Cognitivo

Esta pasta é a fonte normativa candidata para decisões de produto, arquitetura, stack, segurança, dados, integrações, testes, observabilidade, frontend, operação e requisitos não funcionais.

## Regra de precedência

1. Decisões soberanas explícitas de Saimon.
2. Bíblia do Harness Cognitivo, quando aprovada.
3. Especificações desta pasta, dentro de seu escopo.
4. ADRs aprovados.
5. Plano da fase autorizada.
6. Código e evidências do HEAD auditado.

Em caso de conflito, o agente deve parar, registrar o conflito e solicitar decisão. Não pode escolher silenciosamente a interpretação mais conveniente.

## Leitura obrigatória para agentes

Antes de planejar ou implementar qualquer fase, o executor deve ler:

- `00_ESPECIFICACAO_TECNICA_MESTRA.md`;
- a especificação da área afetada;
- os ADRs relacionados;
- o plano da fase autorizada;
- as políticas de segurança e governança aplicáveis.

A ausência dessa leitura bloqueia planejamento, alteração de código, commit e push.

## Documentos

- [00 — Especificação Técnica Mestra](00_ESPECIFICACAO_TECNICA_MESTRA.md)
- [01 — Especificação de Produto](01_ESPECIFICACAO_DE_PRODUTO.md)
- [02 — Arquitetura de Software](02_ARQUITETURA_DE_SOFTWARE.md)
- [03 — Stack Tecnológica](03_STACK_TECNOLOGICA.md)
- [04 — Dados e Persistência](04_DADOS_E_PERSISTENCIA.md)
- [05 — APIs e Integrações](05_APIS_E_INTEGRACOES.md)
- [06 — Segurança e Modelo de Ameaças](06_SEGURANCA_E_MODELO_DE_AMEACAS.md)
- [07 — Observabilidade e Auditoria](07_OBSERVABILIDADE_E_AUDITORIA.md)
- [08 — Testes e Qualidade](08_TESTES_E_QUALIDADE.md)
- [09 — Deployment e Operação](09_DEPLOYMENT_E_OPERACAO.md)
- [10 — Frontend e Experiência](10_FRONTEND_E_EXPERIENCIA.md)
- [11 — Requisitos Não Funcionais](11_REQUISITOS_NAO_FUNCIONAIS.md)

## Estados permitidos para decisões

- `DECIDIDO`: obrigatório no escopo atual.
- `CANDIDATO`: preferência atual, ainda exige validação.
- `ADIADO`: decisão reservada para fase futura.
- `SUBSTITUIVEL`: deve permanecer atrás de contrato ou adapter.
- `PROIBIDO`: incompatível com a arquitetura ou governança atual.

Nenhum agente pode promover `CANDIDATO`, `ADIADO` ou `SUBSTITUIVEL` para `DECIDIDO` sem autorização e ADR.