---
tipo: documento_tecnico
titulo: "Mapeamento: Componentes vs Planos Lógicos"
tags:
  - harness
  - mapeamento
  - arquitetura
status: aprovado
data: 2026-07-15
---

# 🔄 Mapeamento: Componentes vs Planos Lógicos

> *Tratamento da diferença entre 9 componentes (especificação) e 7 planos (Doc 4) como formas distintas de organização, não como conflito arquitetural.*

---

## Contexto

A especificação recebida define **9 componentes** centrais do Harness. O Documento 4 (Arquitetura Geral) organiza o sistema em **7 planos lógicos**. Esta diferença não é um conflito — são perspectivas complementares de organização.

---

## Mapeamento

| # | Componente (Especificação) | Plano Lógico (Doc 4) | Relação |
|---|---------------------------|----------------------|---------|
| 1 | Motor de IA | Capacidades Transversais (4.7) | Adaptadores de modelo ficam nas interfaces |
| 2 | Memória Persistente | Plano Cognitivo — MEC (4.2) | Memória é a infraestrutura cognitiva |
| 3 | RAG e Recuperação | Plano Cognitivo — MEC (4.2) | RAG é mecanismo de recuperação da MEC |
| 4 | Grafo de Conhecimento | Plano Cognitivo — MEC (4.2) | Grafo registra relações entre conceitos |
| 5 | Ferramentas | Plano de Projetos e Execução (4.4) | Ferramentas são usadas na execução |
| 6 | Guardrails | Plano de Controle e Governança (4.3) | Guardrails são políticas de controle |
| 7 | Skills e Validação | Plano de Testes e Evidências (4.5) | Skills incluem validação de qualidade |
| 8 | Observabilidade | Capacidades Transversais (4.7) | Observabilidade atravessa todos os planos |
| 9 | Governador de Inferência | Plano de Controle e Governança (4.3) | Governador é componente de controle |

---

## Conclusão

**Não há conflito arquitetural.** Os 9 componentes são uma visão "por funcionalidade"; os 7 planos são uma visão "por camada de responsabilidade". Ambos são válidos e complementares.

A implementação seguirá a estrutura de **planos lógicos** (Doc 4) para organização de código, pois é mais adequada para arquitetura de software modular.
