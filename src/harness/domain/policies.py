"""
Políticas puras de domínio do Harness Cognitivo — FI-2.

Regras que dependem de múltiplas entidades são implementadas como
políticas puras, sem banco, filesystem, rede ou estado global.

Políticas recebem objetos relacionados como parâmetros e retornam
o resultado da validação.
"""

from __future__ import annotations

from dataclasses import dataclass

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
            reason="Projeto requer pelo menos um plano aprovado para entrar em 'ready'",
        )
    if not has_approved_requirements:
        return PolicyResult(
            allowed=False,
            reason="Projeto requer pelo menos um requisito aprovado para entrar em 'ready'",
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
            reason="Projeto possui gate bloqueador; não pode entrar em 'release_ready'",
        )
    if pending_human_approvals > 0:
        return PolicyResult(
            allowed=False,
            reason=f"Projeto possui {pending_human_approvals} aprovação(ões) humana(s) pendente(s)",
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
            allowed=False, reason="Task requer changeset identificado para ser aceita"
        )
    if not review_approved:
        return PolicyResult(
            allowed=False, reason="Task requer revisão aprovada para ser aceita"
        )
    if not tests_passed:
        return PolicyResult(
            allowed=False, reason="Task requer testes passando para ser aceita"
        )
    if not has_evidence:
        return PolicyResult(
            allowed=False, reason="Task requer evidências preservadas para ser aceita"
        )
    if not no_blockers:
        return PolicyResult(
            allowed=False, reason="Task possui bloqueadores; não pode ser aceita"
        )
    if rework_count >= rework_limit:
        return PolicyResult(
            allowed=False,
            reason=f"Limite de rework atingido ({rework_count}/{rework_limit})",
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
            allowed=False, reason="Gate requer critérios definidos para avanço"
        )
    if not has_evidence:
        return PolicyResult(allowed=False, reason="Gate requer evidências para avanço")
    if not has_authority:
        return PolicyResult(allowed=False, reason="Gate requer autoridade para avanço")
    if not tests_passed:
        return PolicyResult(
            allowed=False, reason="Gate requer testes passando para avanço"
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
            allowed=False, reason="Gate waiver requer autoridade identificável"
        )
    if not has_justification:
        return PolicyResult(allowed=False, reason="Gate waiver requer justificativa")
    if not has_scope:
        return PolicyResult(allowed=False, reason="Gate waiver requer escopo definido")
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: ExecutionRun → start
# =============================================================================


def execution_run_can_start(
    work_order_is_executable: bool,
    has_executor: bool,
    no_active_execution: bool,
) -> PolicyResult:
    """
    Política para início de ExecutionRun.

    Uma ExecutionRun só pode ser iniciada se:
    - A WorkOrder está em estado executável (AUTHORIZED ou DISPATCHED)
    - Existe executor identificado
    - Não há outra execução ativa para a mesma WorkOrder
    """
    if not work_order_is_executable:
        return PolicyResult(
            allowed=False,
            reason="WorkOrder não está em estado executável (AUTHORIZED ou DISPATCHED)",
        )
    if not has_executor:
        return PolicyResult(
            allowed=False,
            reason="ExecutionRun requer executor identificado",
        )
    if not no_active_execution:
        return PolicyResult(
            allowed=False,
            reason="Já existe uma execução ativa para esta WorkOrder",
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Review independence
# =============================================================================


def review_requires_independence(
    reviewer: str | None,
    executor: str | None,
) -> PolicyResult:
    """
    Política de independência de revisão.

    O reviewer e o executor não podem ser a mesma autoridade
    quando ambas as identidades estão disponíveis.
    """
    if reviewer is not None and executor is not None and reviewer == executor:
        return PolicyResult(
            allowed=False,
            reason="Reviewer e executor não podem ser a mesma autoridade",
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: Review → approved (três fidelidades)
# =============================================================================


def review_can_be_approved(
    has_justification: bool,
    has_reviewer: bool,
    has_no_blocker_findings: bool,
) -> PolicyResult:
    """
    Política para aprovação de Review.

    Uma Review só pode ser aprovada se:
    - Justificativa fornecida
    - Reviewer identificado
    - Sem achados bloqueadores
    """
    if not has_justification:
        return PolicyResult(
            allowed=False,
            reason="Review requer justificativa para aprovação",
        )
    if not has_reviewer:
        return PolicyResult(
            allowed=False,
            reason="Review requer reviewer identificado para aprovação",
        )
    if not has_no_blocker_findings:
        return PolicyResult(
            allowed=False,
            reason="Review possui achados bloqueadores; não pode ser aprovada",
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: TestRun completion
# =============================================================================


def test_run_can_complete_as_passed(
    has_total_tests: bool,
    has_evidence: bool,
) -> PolicyResult:
    """
    Política para conclusão de TestRun como passed.

    Um TestRun só pode ser marcado como passed se:
    - Total de testes informado
    - Evidências preservadas
    """
    if not has_total_tests:
        return PolicyResult(
            allowed=False,
            reason="TestRun requer total_tests para ser marcado como passed",
        )
    if not has_evidence:
        return PolicyResult(
            allowed=False,
            reason="TestRun requer evidências para ser marcado como passed",
        )
    return PolicyResult(allowed=True)


# =============================================================================
# POLÍTICA: TestRun failure vs error distinction
# =============================================================================


def test_run_failure_vs_error(
    is_test_failure: bool,
    is_infra_error: bool,
) -> PolicyResult:
    """
    Política de distinção entre falha de teste e erro de infraestrutura.

    failed = teste executou e falhou (resultado inesperado)
    error = erro operacional ou técnico (infraestrutura, timeout, etc.)

    Não pode ser ambos ao mesmo tempo.
    """
    if is_test_failure and is_infra_error:
        return PolicyResult(
            allowed=False,
            reason="TestRun não pode ser simultaneamente failed e error",
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
            allowed=False, reason="Incident requer causa registrada para encerramento"
        )
    if not has_corrective_action:
        return PolicyResult(
            allowed=False, reason="Incident requer ação corretiva para encerramento"
        )
    if not has_regression_evidence:
        return PolicyResult(
            allowed=False,
            reason="Incident requer evidência de teste de regressão para encerramento",
        )
    return PolicyResult(allowed=True)
