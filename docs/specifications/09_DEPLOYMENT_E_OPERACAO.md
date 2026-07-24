---
titulo: Deployment e Operação
status: candidate_for_review
autoriza_implementacao: false
---

# Deployment e Operação

## Estado atual

Deployment público e operação contínua ainda não estão autorizados. Esta especificação define pré-condições para as fases futuras, especialmente FI-12.

## Princípios

- ambientes separados;
- infraestrutura reproduzível;
- configuração fora do código;
- segredos fora do Git;
- promoção por artefato imutável;
- health checks reais;
- rollback testado;
- observabilidade antes de exposição;
- menor privilégio para processos e contas.

## Ambientes candidatos

- local de desenvolvimento;
- teste/integração;
- staging controlado;
- produção.

Dados reais não devem ser copiados para ambientes inferiores sem sanitização.

## Pipeline futuro

```text
commit auditável
→ CI de qualidade e segurança
→ artefato identificado por checksum
→ staging
→ smoke tests
→ autorização de release
→ produção gradual
→ observação
→ rollback ou confirmação
```

## Controles operacionais

- backups e restore testado;
- rotação e revogação de segredos;
- logs e alertas sanitizados;
- limites de CPU, memória, disco, rede e custo;
- runbooks;
- inventário de dependências e versões;
- janela de manutenção;
- procedimento de incidente;
- domador de ticket com autoridade limitada.

## Containers

Containers são `CANDIDATO` para empacotamento, não requisito constitucional. Kubernetes é proibido antes de necessidade demonstrada.

## Incidentes

Todo incidente deve ter severidade, impacto, detecção, contenção, recuperação, causa, evidência, ações corretivas e aprendizado causal. Correção emergencial não encerra o incidente sem reparo definitivo ou risco aceito formalmente.