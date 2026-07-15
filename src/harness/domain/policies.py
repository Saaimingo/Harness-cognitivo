"""
Políticas puras de domínio do Harness Cognitivo — FI-2.

Regras que dependem de múltiplas entidades são implementadas como
políticas puras, sem banco, filesystem, rede ou estado global.

Políticas recebem objetos relacionados como parâmetros e retornam
o resultado da validação.
"""

from __future__ import annotations

from dataclasses import dataclass

from harness.domain.errors import InvariantViolationError


# =============================================================================
# RESULTADO DA POLÍTICA
# =============================================================================

@dataclass(frozen=True)
class PolicyResult:
    """Resultado de uma política de domínio."""
    allowed: bool
    reason: str = ""


# =============================================================================
# POLÍTICA: Project → ready
# =============================================================================

def project_can_become_ready(
    has_approved_plan: bool,
    has_approved_requirements: bool,
) -> PolicyResult:
    """
    Política para entrada de Project em 'ready'.

    Um projeto só pode ficar 'ready' se tiver:
    - Pelo menos um plano aprovado
    - Pelo menos um requisito aprovado
    """
    if not has_approved_plan:
        return PolicyResult(
            allowed=False,
            reason="Projeto requer pelo menos um plano aprovado para entrar em 'ready'"
        )
    if not has_approved_requirements:
        return PolicyResult(
            allowed=False,
            reason="Projeto requer pelo menos um requisito aprovado para entrar em 'ready'"
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Project → release_ready
# =============================================================================

def project_can_become_release_ready(
    has_blocking_gate: bool,
    pending_human_approvals: int,
) -> PolicyResult:
    """
    Política para entrada de Project em 'release_ready'.

    Um projeto só pode ficar 'release_ready' se:
    - Nenhum gate estiver bloqueador
    - Nenhuma aprovação humana pendente
    """
    if has_blocking_gate:
        return PolicyResult(
            allowed=False,
            reason="Projeto possui gate bloqueador; não pode entrar em 'release_ready'"
        )
    if pending_human_approvals > 0:
        return PolicyResult(
            allowed=False,
            reason=f"Projeto possui {pending_human_approvals} aprovação(ões) humana(s) pendente(s)"
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Task → accepted
# =============================================================================

def task_can_become_accepted(
    has_changeset: bool,
    review_approved: bool,
    tests_passed: bool,
    has_evidence: bool,
    no_blockers: bool,
    rework_count: int,
    rework_limit: int,
) -> PolicyResult:
    """
    Política para entrada de Task em 'accepted'.

    Uma tarefa só pode ser aceita se:
    - Possui changeset identificado
    - Revisão aprovada
    - Testes passaram
    - Evidências preservadas
    - Sem bloqueadores
    - Limite de rework não atingido
    """
    if not has_changeset:
        return PolicyResult(
            allowed=False,
            reason="Task requer changeset identificado para ser aceita"
        )
    if not review_approved:
        return PolicyResult(
            allowed=False,
            reason="Task requer revisão aprovada para ser aceita"
        )
    if not tests_passed:
        return PolicyResult(
            allowed=False,
            reason="Task requer testes passando para ser aceita"
        )
    if not has_evidence:
        return PolicyResult(
            allowed=False,
            reason="Task requer evidências preservadas para ser aceita"
        )
    if not no_blockers:
        return PolicyResult(
            allowed=False,
            reason="Task possui bloqueadores; não pode ser aceita"
        )
    if rework_count >= rework_limit:
        return PolicyResult(
            allowed=False,
            reason=f"Limite de rework atingido ({rework_count}/{rework_limit})"
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Gate → advance
# =============================================================================

def gate_can_advance(
    has_criteria: bool,
    has_evidence: bool,
    has_authority: bool,
    tests_passed: bool,
) -> PolicyResult:
    """
    Política para decisão de Gate = 'advance'.

    Um gate só pode avançar se:
    - Critérios foram definidos
    - Evidências foram fornecidas
    - Autoridade está presente
    - Testes passaram
    """
    if not has_criteria:
        return PolicyResult(
            allowed=False,
            reason="Gate requer critérios definidos para avanço"
        )
    if not has_evidence:
        return PolicyResult(
            allowed=False,
            reason="Gate requer evidências para avanço"
        )
    if not has_authority:
        return PolicyResult(
            allowed=False,
            reason="Gate requer autoridade para avanço"
        )
    if not tests_passed:
        return PolicyResult(
            allowed=False,
            reason="Gate requer testes passando para avanço"
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Gate → waived
# =============================================================================

def gate_can_be_waived(
    has_authority: bool,
    has_justification: bool,
    has_scope: bool,
) -> PolicyResult:
    """
    Política para decisão de Gate = 'waived'.

    Um gate só pode ser dispensado se:
    - Autoridade identificável presente
    - Justificativa documentada
    - Escopo da dispensa definido
    """
    if not has_authority:
        return PolicyResult(
            allowed=False,
            reason="Gate waiver requer autoridade identificável"
        )
    if not has_justification:
        return PolicyResult(
            allowed=False,
            reason="Gate waiver requer justificativa"
        )
    if not has_scope:
        return PolicyResult(
            allowed=False,
            reason="Gate waiver requer escopo definido"
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Incident → closed
# =============================================================================

def incident_can_become_closed(
    has_cause: bool,
    has_corrective_action: bool,
    has_regression_evidence: bool,
) -> PolicyResult:
    """
    Política para entrada de Incident em 'closed'.

    Um incidente só pode ser encerrado se:
    - Causa registrada
    - Ação corretiva implementada
    - Evidência ou referência de teste de regressão
    """
    if not has_cause:
        return PolicyResult(
            allowed=False,
            reason="Incident requer causa registrada para encerramento"
        )
    if not has_corrective_action:
        return PolicyResult(
            allowed=False,
            reason="Incident requer ação corretiva para encerramento"
        )
    if not has_regression_evidence:
        return PolicyResult(
            allowed=False,
            reason="Incident requer evidência de teste de regressão para encerramento"
        )
    return PolicyResult(allowed=True)
