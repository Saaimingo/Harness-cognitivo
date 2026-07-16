---
tipo: glossario
titulo: "Glossário — Harness Cognitivo"
status: ativo
data: 2026-07-15
---

# 📖 Glossário — Harness Cognitivo

> *Termos unificados do projeto. Todo documento normativo deve usar estes termos.*

---

## Conceitos Fundamentais

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Harness** | Camada operacional externa que transforma modelos de IA intercambiáveis em sistemas persistente, verificável, seguro e eficiente | Doc 0 (Declarativa) |
| **MEC** | Memória Evolutiva Causal — infraestrutura cognitiva persistente do Harness | Doc 1 |
| **Modelo de IA** | Motor cognitivo que produz interpretação, raciocínio e linguagem | Doc 0 |
| **SG-0** | Eixo transversal de Segurança Operacional e Ações Destrutivas | ESQ-0 |
| **ESQ** | Eixo transversal de Engenharia de Software e Qualidade Estrutural | ESQ-0 |
| **GRN** | Eixo transversal de Governança de Regras de Negócio | GRN-0 |
| **CTP** | Chat-to-Project — Promoção de Conversa para Projeto | CTP-0 |

---

## Papéis

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Saimon** | Proprietário e autoridade final do projeto | Doc 0 |
| **Tubarão** | Arquiteto conceitual; transforma ideias em especificações | Doc 0 |
| **Freebuff** | Executor de engenharia; implementa, testa, produz evidências | Doc 0 |
| **Validador** | Papel separado do executor; confirma resultados independentemente | Doc 7 |

---

## Componentes do Sistema

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Motor de IA** | Adaptadores para modelos de linguagem (OpenAI, Claude, etc.) | Especificação |
| **Memória Persistente** | Armazenamento de longo prazo: fatos, decisões, preferências | Doc 1 |
| **RAG** | Retrieval-Augmented Generation — recuperação inteligente de informações | Especificação |
| **Grafo de Conhecimento** | Estrutura que registra relações entre conceitos | Especificação |
| **Ferramentas** | Capacidade de executar ações externas (código, web, arquivos) | Especificação |
| **Guardrails** | Mecanismos de segurança e limites | Especificação |
| **Skills** | Capacidades reutilizáveis e procedimentos consolidados | Especificação |
| **Observabilidade** | Registro completo de decisões e processos | Especificação |
| **Governador** | Componente que decide como tarefas devem ser executadas | Especificação |

---

## Objetos Funcionais

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Projeto** | Unidade persistente no ciclo de vida, iniciada por intenção aprovada | Doc 4 |
| **Requisito** | Comportamento, restrição ou qualidade verificável | Doc 5 |
| **Plano** | Versão aprovada da decomposição do trabalho | Doc 5 |
| **Tarefa** | Unidade planejada com dependências e critério de aceite | Doc 5 |
| **WorkOrder** | Autorização estruturada para tentativa delimitada de execução | Doc 5 |
| **ExecutionRun** | Tentativa concreta de cumprir WorkOrder | Doc 5 |
| **Changeset** | Conjunto identificável de alterações | Doc 5 |
| **Release** | Versão preparada ou implantada | Doc 5 |
| **Incidente** | Falha operacional que exige investigação | Doc 5 |

---

## Epistemologia (Estados de Conhecimento)

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **Fato** | Informação declarada como verdadeira pelo proprietário | Doc 6 |
| **Hipótese** | Proposta ainda não verificada | Doc 6 |
| **Inferência** | Conclusão derivada de outros dados | Doc 6 |
| **Decisão** | Escolha registrada com justificativa | Doc 6 |
| **Evidência** | Artefato que sustenta uma afirmação (screenshot, teste, log) | Doc 6 |
| **Interpretação** | Análise subjetiva de evidência | Doc 6 |

---

## Níveis de Confiança

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **owner_declared** | Declarado pelo proprietário (Saimon) | Doc 6 |
| **verified** | Confirmado por teste ou verificação independente | Doc 6 |
| **inferred** | Derivado de outros dados; pode estar incorreto | Doc 6 |
| **observed** | Observado diretamente em logs ou métricas | Doc 6 |
| **unverified** | Ainda não verificado | Doc 6 |
| **unknown** | Sem informação suficiente para classificar | Doc 6 |

---

## Processo

| Termo | Definição | Fonte |
|-------|-----------|-------|
| **REALIZAR** | Implementar apenas o essencial (MVP) | Regras de Execução |
| **TESTAR** | Verificar se funciona com evidências reais | Regras de Execução |
| **APROVAR** | Validar se atende ao objetivo com critérios objetivos | Regras de Execução |
| **REGISTRAR** | Documentar o que foi feito e preparar próxima iteração | Regras de Execução |

---

## Regras de Escrita

| Regra | Descrição |
|-------|-----------|
| **Separação epistêmica** | `object_type` = natureza do objeto; `trust_level` = nível de confiança |
| **Proposta não é fato** | Saídas de modelo entram com proveniência e confiança |
| **Evidência não é interpretação** | Screenshots/logs são evidências; conclusões são objetos separados |
| **Causalidade explícita** | Correlação ≠ causalidade; protocolo distingue as duas |

---

> *Este glossário é vivo e deve ser atualizado a cada novo termo introduzido no projeto.*
