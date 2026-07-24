---
titulo: Observabilidade e Auditoria
status: candidate_for_review
autoriza_implementacao: false
---

# Observabilidade e Auditoria

## Objetivo

Permitir entender o que aconteceu, por que aconteceu, quem autorizou, qual modelo e ferramenta atuaram, quanto custou e como reproduzir o resultado.

## Sinais obrigatórios

- logs estruturados;
- métricas operacionais;
- traces correlacionados;
- eventos de domínio;
- evidências e manifests;
- estado do workflow;
- custo, latência, retries e uso por modelo.

## Campos mínimos

`timestamp`, `level`, `event_type`, `correlation_id`, `causation_id`, `project_id`, `workorder_id`, `actor`, `role`, `model`, `provider`, `tool`, `authority_ref`, `result`, `duration_ms`, `cost_estimate`, `evidence_ref`.

## Regras

- nenhum segredo ou conteúdo sensível desnecessário em logs;
- eventos materiais não podem ser apagados pelo executor;
- logs não substituem evidência de teste;
- observabilidade não pode alterar semântica do domínio;
- falhas de telemetria não podem ser escondidas;
- mudanças posteriores ao SHA auditado invalidam o parecer anterior.

## Evidências

Cada gate deve apontar para artefatos reproduzíveis: comandos, saídas, versões, ambiente, checksums, arquivos, screenshots quando aplicável e limitações conhecidas.

## Métricas candidatas

- taxa de sucesso por tipo de tarefa;
- rework por causa;
- violações de escopo bloqueadas;
- tempo por etapa;
- custo por etapa e por entrega;
- chamadas e falhas de ferramentas;
- divergência entre executor e revisor;
- tempo de recuperação;
- incidentes por categoria.

## Auditoria

Auditoria final ocorre somente sobre SHA publicado e imutável. O auditor deve receber requisitos, diff, evidências, parecer interno e estado remoto. Consenso sem prova não produz aprovação.