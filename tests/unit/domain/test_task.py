"""
Testes parametrizados para a entidade Task — FI-2A.
Cobre: transições, rework limit, idempotência, imutabilidade, timezone.
"""

from datetime import datetime

import pytest

from harness.domain.enums import TaskStatus
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
    ReworkLimitExceededError,
)
from harness.domain.task import Task
from harness.domain.transitions import TASK_TERMINAL


def make_task(status: TaskStatus = TaskStatus.PROPOSED, rework_limit: int = 5) -> Task:
    """Helper para criar Task com estado específico."""
    return Task(
        task_id="tsk_test123",
        project_id="prj_test123",
        plan_id="pln_test123",
        title="Tarefa Teste",
        status=status,
        rework_limit=rework_limit,
    )


# =============================================================================
# TRANSIÇÕES PERMITIDAS (não-terminais)
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (TaskStatus.PROPOSED, TaskStatus.PLANNED),
        (TaskStatus.PLANNED, TaskStatus.ELIGIBLE),
        (TaskStatus.ELIGIBLE, TaskStatus.ASSIGNED),
        (TaskStatus.ASSIGNED, TaskStatus.RUNNING),
        (TaskStatus.RUNNING, TaskStatus.SUBMITTED),
        (TaskStatus.SUBMITTED, TaskStatus.IN_REVIEW),
        (TaskStatus.IN_REVIEW, TaskStatus.IN_VALIDATION),
        (TaskStatus.IN_VALIDATION, TaskStatus.REWORK),
        (TaskStatus.REWORK, TaskStatus.RUNNING),
        (TaskStatus.PLANNED, TaskStatus.BLOCKED),
        (TaskStatus.BLOCKED, TaskStatus.ELIGIBLE),
    ],
)
def test_task_valid_transitions(current: TaskStatus, target: TaskStatus):
    """Transições válidas não-terminais devem ser aceitas sem autoridade."""
    task = make_task(status=current)
    new_task = task.transition_to(target)
    assert new_task.status == target


# =============================================================================
# TRANSIÇÃO PARA ESTADO TERMINAL (com autoridade)
# =============================================================================


def test_task_terminal_transition_with_authority():
    """Transição para ACCEPTED (terminal) requer autoridade."""
    task = make_task(status=TaskStatus.IN_VALIDATION)
    new_task = task.transition_to(TaskStatus.ACCEPTED, authority="test")
    assert new_task.status == TaskStatus.ACCEPTED


def test_task_terminal_transition_without_authority_rejected():
    """Transição para ACCEPTED sem autoridade é rejeitada."""
    task = make_task(status=TaskStatus.IN_VALIDATION)
    with pytest.raises(InvariantViolationError):
        task.transition_to(TaskStatus.ACCEPTED)


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (TaskStatus.PROPOSED, TaskStatus.RUNNING),
        (TaskStatus.PROPOSED, TaskStatus.ACCEPTED),
        (TaskStatus.RUNNING, TaskStatus.ACCEPTED),
        (TaskStatus.ACCEPTED, TaskStatus.RUNNING),
        (TaskStatus.CANCELLED, TaskStatus.RUNNING),
    ],
)
def test_task_invalid_transitions_rejected(current: TaskStatus, target: TaskStatus):
    """Transições inválidas devem ser rejeitadas."""
    task = make_task(status=current)
    with pytest.raises(InvalidTransitionError):
        task.transition_to(target)


# =============================================================================
# REWORK LIMIT
# =============================================================================


def test_task_rework_increment():
    """Transição para REWORK incrementa rework_count."""
    task = make_task(status=TaskStatus.IN_VALIDATION, rework_limit=5)
    new_task = task.transition_to(TaskStatus.REWORK)
    assert new_task.rework_count == 1


def test_task_rework_limit_not_exceeded():
    """Task pode fazer rework até o limite."""
    task = make_task(status=TaskStatus.IN_VALIDATION, rework_limit=3)
    # 1º rework
    t1 = task.transition_to(TaskStatus.REWORK)
    assert t1.rework_count == 1
    # Voltar para IN_VALIDATION via ciclo completo
    t2 = t1.transition_to(TaskStatus.RUNNING)
    t3 = t2.transition_to(TaskStatus.SUBMITTED)
    t4 = t3.transition_to(TaskStatus.IN_REVIEW)
    t5 = t4.transition_to(TaskStatus.IN_VALIDATION)
    # 2º rework
    t6 = t5.transition_to(TaskStatus.REWORK)
    assert t6.rework_count == 2


def test_task_rework_limit_exceeded():
    """Task excede limite de rework e lança exceção."""
    task = make_task(status=TaskStatus.IN_VALIDATION, rework_limit=2)
    t1 = task.transition_to(TaskStatus.REWORK)  # 1º
    t2 = t1.transition_to(TaskStatus.RUNNING)
    t3 = t2.transition_to(TaskStatus.SUBMITTED)
    t4 = t3.transition_to(TaskStatus.IN_REVIEW)
    t5 = t4.transition_to(TaskStatus.IN_VALIDATION)
    with pytest.raises(ReworkLimitExceededError):
        t5.transition_to(TaskStatus.REWORK)  # 2º - excede limite


def test_task_rework_exhausted_property():
    """Propriedade rework_exhausted retorna True quando limite atingido."""
    task = make_task(status=TaskStatus.REWORK, rework_limit=1)
    task_with_count = task.model_copy(update={"rework_count": 1})
    assert task_with_count.rework_exhausted


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================


def test_task_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    task = make_task(status=TaskStatus.PROPOSED)
    result = task.transition_to(TaskStatus.PROPOSED)
    assert result is task


# =============================================================================
# IMUTABILIDADE
# =============================================================================


def test_task_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    task = make_task(status=TaskStatus.PROPOSED)
    original_status = task.status
    _ = task.transition_to(TaskStatus.PLANNED)
    assert task.status == original_status


# =============================================================================
# TIMEZONE
# =============================================================================


def test_task_rejects_naive_datetime():
    """Task rejeita datetime sem timezone."""
    with pytest.raises(ValueError, match="timezone"):
        Task(
            task_id="tsk_test123",
            project_id="prj_test123",
            plan_id="pln_test123",
            title="Teste",
            created_at=datetime(2026, 1, 1),
        )


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(TASK_TERMINAL))
def test_task_terminal_states(terminal_status: TaskStatus):
    """Tarefas em estados terminais são marcadas como is_terminal."""
    task = make_task(status=terminal_status)
    assert task.is_terminal
