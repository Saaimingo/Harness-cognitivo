---
tipo: checklist
titulo: "SG-0 — Checklist de Segurança Operacional"
status: ativo
data: 2026-07-15
eixo: SG-0
---

# ✅ SG-0 — Checklist de Segurança Operacional

> *Verificar antes de cada operação significativa.*

---

## Pré-Execução

- [ ] Workspace identificado e documentado
- [ ] Git status verificado (`git status --porcelain`)
- [ ] Alterações pendentes resolvidas ou explicitamente ignoradas
- [ ] Comando pretendido descrito em linguagem natural
- [ ] Efeitos colaterais listados
- [ ] Classe de ação determinada (segura / verificação / destrutiva)

## Para Ações de Verificação

- [ ] Usuário informado sobre a ação
- [ ] Confirmação obtida (se aplicável)
- [ ] Backup/stash criado (se houver risco)

## Para Ações Destrutivas

- [ ] Motivo documentado
- [ ] Efeitos colaterais descritos ao usuário
- [ ] Confirmação explícita do usuário registrada
- [ ] Ponto de salvage criado (git stash, backup)
- [ ] Procedimento de rollback documentado
- [ ] Caminho alvo verificado (dentro do workspace?)

## Pós-Execução

- [ ] Exit code verificado
- [ ] Resultado esperado confirmado
- [ ] Efeitos colaterais inesperados registrados
- [ ] Rollback necessário? (sim/não)
- [ ] Log de evento registrado

## Proteção de Caminhos Críticos

- [ ] `.git/` — não modificado
- [ ] `.env` — não exposto ou modificado
- [ ] `pyproject.toml` — dependências não alteradas sem autorização
- [ ] `uv.lock` — não alterado sem necessidade
- [ ] Configurações de IDE — não modificadas

## Intenção do Usuário

- [ ] Intenção capturada antes da execução
- [ ] Não extrapolada além do solicitado
- [ ] Ambiguidades resolvidas com o usuário

---

> *Este checklist deve ser verificado antes de cada operação que altere estado.*
