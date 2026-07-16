---
tipo: politica
titulo: "SG-0 — Política de Ações Destrutivas de Agentes"
status: ativo
data: 2026-07-15
eixo: SG-0
---

# 🛡️ SG-0 — Política de Ações Destrutivas de Agentes

> *Nenhuma ação destrutiva deve ocorrer sem autorização explícita e verificável.*

---

## 1. Princípios Fundamentais

| Princípio | Descrição |
|-----------|-----------|
| **Fail Closed** | Na dúvida, bloquear. Nunca permitir por padrão. |
| **Menor Privilégio** | Cada ação deve usar o mínimo de permissão necessário. |
| **Separação Leitura/Escrita** | Operações de leitura e escrita devem ser conceitualmente distintas. |
| **Autorização Explícita** | Toda ação destrutiva requer confirmação registrada. |
| **Escopo de Arquivos** | Operações devem respeitar limites de diretório definidos. |
| **Proteção de Caminhos Críticos** | `.git/`, configurações de sistema, e dados persistentes são protegidos. |
| **Nenhuma Ação Destrutiva Implícita** | Nunca inferir que destruição é aceitável. |
| **Registro** | Toda ação e seu efeito devem ser rastreáveis. |
| **Rollback** | Quando tecnicamente possível, manter capacidade de reversão. |
| **Capacidade de Interrupção** | Processos devem ser interrompíveis. |

---

## 2. Classificação de Ações

### 2.1 Ações Seguras (sem confirmação)

- Leitura de arquivos dentro do workspace
- Criação de novos arquivos
- Execução de testes
- Execução de lint e formatação
- Consulta a Git (status, log, diff)

### 2.2 Ações que Requerem Verificação

- Modificação de arquivos existentes
- Execução de comandos que alteram estado (npm install, pip install)
- Criação de branches
- Merge de branches

### 2.3 Ações Destrutivas (requerem confirmação explícita)

- Exclusão de arquivos (`rm`, `del`)
- Sobrescrita perigosa de arquivos de configuração
- Reset de estado Git (`git reset --hard`, `git clean`)
- Limpeza de diretórios (`rm -rf`, `rmdir /s`)
- Alteração fora do workspace definido
- `git push` para branches protegidos
- Alteração de credenciais ou secrets
- Execução de scripts que modificam ambientes de produção

---

## 3. Regras Operacionais

### 3.1 Verificação de Git Limpo

Antes de qualquer operação que altere estado significativo:

```
git status --porcelain
```

Se houver alterações pendentes, **não prosseguir** sem autorização explícita.

### 3.2 Preferência por Ambientes Descartáveis

Quando houver risco de alteração irreversível:

1. Preferir `git worktree` ou `git stash`
2. Preferir clone temporário para testes destrutivos
3. Nunca executar ações destrutivas no diretório de trabalho principal sem necessidade comprovada

### 3.3 Extração de Intenção do Usuário

- **Proibido** extrapolar a intenção do usuário além do que foi explicitamente solicitado
- Em caso de ambiguidade, **perguntar** antes de agir
- Registrar a intenção do usuário antes de executar ações de risco

### 3.4 Confirmação Adicional

Para ações na categoria 2.3, o agente deve:

1. Descrever a ação pretendida
2. Listar os efeitos colaterais esperados
3. Confirmar com o usuário antes de executar
4. Registrar a confirmação no log de eventos

---

## 4. Escopo de Proteção

### 4.1 Caminhos Críticos (nunca modificar sem autoridade máxima)

- `.git/`
- `.env`, `.env.*`
- `pyproject.toml` (dependências)
- `uv.lock`
- `.python-version`
- Configurações de IDE (`.vscode/`, `.idea/`)

### 4.2 Workspace Definido

Todas as operações devem ocorrer dentro do diretório do projeto. Operações fora do workspace requerem:

- Motivo documentado
- Autorização do usuário
- Registro de caminho alvo

---

## 5. Registro de Comandos

Todo comando executado deve ser registrado com:

| Campo | Descrição |
|-------|-----------|
| `timestamp` | Data/hora da execução |
| `command` | Comando exato executado |
| `working_dir` | Diretório de trabalho |
| `exit_code` | Código de retorno |
| `stdout_preview` | Primeiras 500 chars de saída |
| `stderr_preview` | Primeiras 500 chars de erro |
| `destructive` | Se a ação é classificada como destrutiva |
| `authorized_by` | Quem autorizou (se aplicável) |

---

## 6. Rollback

Quando tecnicamente possível:

- Antes de operações destrutivas, criar ponto de salvage (`git stash`, backup de arquivo)
- Documentar o procedimento de reversão
- Verificar se o rollback foi bem-sucedido após execução

---

## 7. Interrupção

- Processos longos devem ser interrompíveis
- O usuário deve poder cancelar a qualquer momento
- Estado parcial deve ser registrado ao interromper

---

## 8. Escopo de Aplicação

Este documento se aplica a:

1. **Desenvolvimento do Harness** — todas as fases de implementação
2. **Execuções futuras do Harness** — quando o sistema estiver operacional

---

## 9. Relação com Outros Eixos

| Eixo | Relação |
|------|---------|
| **ESQ** | SG-0 complementa a qualidade estrutural com segurança operacional |
| **GRN** | SG-0 protege regras de negócio contra alteração não autorizada |
| **CTP** | SG-0 protege o pacote de promoção e seus artefatos |

---

> *Este documento é vivo e deve ser revisado a cada nova fase do projeto.*
