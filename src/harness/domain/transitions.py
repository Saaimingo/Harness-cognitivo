"""
Tabelas de transição do domínio Harness Cognitivo — FI-2.

Cada máquina de estado é definida por uma tabela explícita.
Evita grandes blocos de condicionais espalhados entre entidades.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from harness.domain.enums import (
    ExecutionRunStatus,
    GateStatus,
    ProjectStatus,
    ReviewStatus,
    TaskStatus,
    TestRunStatus,
    WorkOrderStatus,
)

if TYPE_CHECKING:
    from enum import StrEnum

# =============================================================================
# PROJETO — 19 estados (Doc 5, §6)
# =============================================================================

PROJECT_INITIAL = ProjectStatus.CAPTURED
PROJECT_TERMINAL: frozenset[ProjectStatus] = frozenset(
    {
        ProjectStatus.ARCHIVED,
        ProjectStatus.ABANDONED,
    }
)

PROJECT_TRANSITIONS: dict[ProjectStatus, frozenset[ProjectStatus]] = {
    ProjectStatus.CAPTURED: frozenset(
        {
            ProjectStatus.TRIAGE,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.TRIAGE: frozenset(
        {
            ProjectStatus.DISCOVERY,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.DISCOVERY: frozenset(
        {
            ProjectStatus.SPECIFIED,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.SPECIFIED: frozenset(
        {
            ProjectStatus.ARCHITECTED,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.ARCHITECTED: frozenset(
        {
            ProjectStatus.PLANNED,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.PLANNED: frozenset(
        {
            ProjectStatus.READY,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.READY: frozenset(
        {
            ProjectStatus.EXECUTING,
            ProjectStatus.SUSPENDED,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.EXECUTING: frozenset(
        {
            ProjectStatus.REVIEWING,
            ProjectStatus.REWORK_REQUIRED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.REVIEWING: frozenset(
        {
            ProjectStatus.VALIDATING,
            ProjectStatus.REWORK_REQUIRED,
            ProjectStatus.AWAITING_APPROVAL,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.VALIDATING: frozenset(
        {
            ProjectStatus.RELEASE_READY,
            ProjectStatus.REWORK_REQUIRED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.REWORK_REQUIRED: frozenset(
        {
            ProjectStatus.PLANNED,
            ProjectStatus.EXECUTING,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.AWAITING_APPROVAL: frozenset(
        {
            ProjectStatus.RELEASE_READY,
            ProjectStatus.REWORK_REQUIRED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.RELEASE_READY: frozenset(
        {
            ProjectStatus.RELEASED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.RELEASED: frozenset(
        {
            ProjectStatus.MONITORED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.MONITORED: frozenset(
        {
            ProjectStatus.MAINTENANCE,
            ProjectStatus.ARCHIVED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.MAINTENANCE: frozenset(
        {
            ProjectStatus.PLANNED,
            ProjectStatus.RELEASED,
            ProjectStatus.ARCHIVED,
            ProjectStatus.SUSPENDED,
        }
    ),
    ProjectStatus.SUSPENDED: frozenset(
        {
            ProjectStatus.CAPTURED,  # pode voltar ao início
            ProjectStatus.TRIAGE,
            ProjectStatus.DISCOVERY,
            ProjectStatus.SPECIFIED,
            ProjectStatus.ARCHITECTED,
            ProjectStatus.PLANNED,
            ProjectStatus.READY,
            ProjectStatus.EXECUTING,
            ProjectStatus.REVIEWING,
            ProjectStatus.VALIDATING,
            ProjectStatus.REWORK_REQUIRED,
            ProjectStatus.AWAITING_APPROVAL,
            ProjectStatus.RELEASE_READY,
            ProjectStatus.RELEASED,
            ProjectStatus.MONITORED,
            ProjectStatus.MAINTENANCE,
            ProjectStatus.ABANDONED,
        }
    ),
    ProjectStatus.ABANDONED: frozenset(),  # terminal
    ProjectStatus.ARCHIVED: frozenset(),  # terminal
}


# =============================================================================
# TAREFA — 13 estados (Doc 5, §7)
# =============================================================================

TASK_INITIAL = TaskStatus.PROPOSED
TASK_TERMINAL: frozenset[TaskStatus] = frozenset(
    {
        TaskStatus.ACCEPTED,
        TaskStatus.CANCELLED,
        TaskStatus.SUPERSEDED,
    }
)

TASK_TRANSITIONS: dict[TaskStatus, frozenset[TaskStatus]] = {
    TaskStatus.PROPOSED: frozenset(
        {
            TaskStatus.PLANNED,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.PLANNED: frozenset(
        {
            TaskStatus.BLOCKED,
            TaskStatus.ELIGIBLE,
            TaskStatus.CANCELLED,
            TaskStatus.SUPERSEDED,
        }
    ),
    TaskStatus.BLOCKED: frozenset(
        {
            TaskStatus.ELIGIBLE,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.ELIGIBLE: frozenset(
        {
            TaskStatus.ASSIGNED,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.ASSIGNED: frozenset(
        {
            TaskStatus.RUNNING,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.RUNNING: frozenset(
        {
            TaskStatus.SUBMITTED,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.SUBMITTED: frozenset(
        {
            TaskStatus.IN_REVIEW,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.IN_REVIEW: frozenset(
        {
            TaskStatus.IN_VALIDATION,
            TaskStatus.REWORK,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.IN_VALIDATION: frozenset(
        {
            TaskStatus.ACCEPTED,
            TaskStatus.REWORK,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.REWORK: frozenset(
        {
            TaskStatus.RUNNING,
            TaskStatus.CANCELLED,
        }
    ),
    TaskStatus.ACCEPTED: frozenset(),  # terminal
    TaskStatus.CANCELLED: frozenset(),  # terminal
    TaskStatus.SUPERSEDED: frozenset(),  # terminal
}


# =============================================================================
# WORKORDER — 9 estados (Doc 5, §8)
# =============================================================================

WORKORDER_INITIAL = WorkOrderStatus.DRAFT
WORKORDER_TERMINAL: frozenset[WorkOrderStatus] = frozenset(
    {
        WorkOrderStatus.COMPLETED,
        WorkOrderStatus.EXPIRED,
        WorkOrderStatus.CANCELLED,
        WorkOrderStatus.REVOKED,
    }
)

WORKORDER_TRANSITIONS: dict[WorkOrderStatus, frozenset[WorkOrderStatus]] = {
    WorkOrderStatus.DRAFT: frozenset(
        {
            WorkOrderStatus.VALIDATED,
            WorkOrderStatus.CANCELLED,
        }
    ),
    WorkOrderStatus.VALIDATED: frozenset(
        {
            WorkOrderStatus.AUTHORIZED,
            WorkOrderStatus.CANCELLED,
        }
    ),
    WorkOrderStatus.AUTHORIZED: frozenset(
        {
            WorkOrderStatus.DISPATCHED,
            WorkOrderStatus.CANCELLED,
            WorkOrderStatus.REVOKED,
        }
    ),
    WorkOrderStatus.DISPATCHED: frozenset(
        {
            WorkOrderStatus.ACTIVE,
            WorkOrderStatus.EXPIRED,
            WorkOrderStatus.CANCELLED,
            WorkOrderStatus.REVOKED,
        }
    ),
    WorkOrderStatus.ACTIVE: frozenset(
        {
            WorkOrderStatus.COMPLETED,
            WorkOrderStatus.EXPIRED,
            WorkOrderStatus.CANCELLED,
            WorkOrderStatus.REVOKED,
        }
    ),
    WorkOrderStatus.COMPLETED: frozenset(),  # terminal
    WorkOrderStatus.EXPIRED: frozenset(),  # terminal
    WorkOrderStatus.CANCELLED: frozenset(),  # terminal
    WorkOrderStatus.REVOKED: frozenset(),  # terminal
}


# =============================================================================
# GATE — 8 estados (separados do resultado)
# =============================================================================

GATE_INITIAL = GateStatus.PENDING
GATE_TERMINAL: frozenset[GateStatus] = frozenset(
    {
        GateStatus.DECIDED,
        GateStatus.CANCELLED,
    }
)

GATE_TRANSITIONS: dict[GateStatus, frozenset[GateStatus]] = {
    GateStatus.PENDING: frozenset(
        {
            GateStatus.EVALUATING,
            GateStatus.CANCELLED,
        }
    ),
    GateStatus.EVALUATING: frozenset(
        {
            GateStatus.DECIDED,
            GateStatus.CANCELLED,
        }
    ),
    GateStatus.DECIDED: frozenset(),  # terminal — resultado em GateDecisionType
    GateStatus.CANCELLED: frozenset(),  # terminal
}


# =============================================================================
# EXECUTIONRUN — 5 estados (FI-2B)
# =============================================================================

EXECUTIONRUN_INITIAL = ExecutionRunStatus.INITIATED
EXECUTIONRUN_TERMINAL: frozenset[ExecutionRunStatus] = frozenset(
    {
        ExecutionRunStatus.COMPLETED,
        ExecutionRunStatus.FAILED,
        ExecutionRunStatus.ABANDONED,
    }
)

EXECUTIONRUN_TRANSITIONS: dict[ExecutionRunStatus, frozenset[ExecutionRunStatus]] = {
    ExecutionRunStatus.INITIATED: frozenset(
        {
            ExecutionRunStatus.RUNNING,
            ExecutionRunStatus.ABANDONED,
        }
    ),
    ExecutionRunStatus.RUNNING: frozenset(
        {
            ExecutionRunStatus.COMPLETED,
            ExecutionRunStatus.FAILED,
            ExecutionRunStatus.ABANDONED,
        }
    ),
    ExecutionRunStatus.COMPLETED: frozenset(),  # terminal
    ExecutionRunStatus.FAILED: frozenset(),  # terminal
    ExecutionRunStatus.ABANDONED: frozenset(),  # terminal
}


# =============================================================================
# REVIEW — 5 estados (FI-2B)
# =============================================================================

REVIEW_INITIAL = ReviewStatus.REQUESTED
REVIEW_TERMINAL: frozenset[ReviewStatus] = frozenset(
    {
        ReviewStatus.APPROVED,
        ReviewStatus.REJECTED,
        ReviewStatus.CHANGE_REQUESTED,
    }
)

REVIEW_TRANSITIONS: dict[ReviewStatus, frozenset[ReviewStatus]] = {
    ReviewStatus.REQUESTED: frozenset(
        {
            ReviewStatus.IN_PROGRESS,
        }
    ),
    ReviewStatus.IN_PROGRESS: frozenset(
        {
            ReviewStatus.APPROVED,
            ReviewStatus.REJECTED,
            ReviewStatus.CHANGE_REQUESTED,
        }
    ),
    ReviewStatus.APPROVED: frozenset(),  # terminal
    ReviewStatus.REJECTED: frozenset(),  # terminal
    ReviewStatus.CHANGE_REQUESTED: frozenset(),  # terminal — nova ExecutionRun necessária
}


# =============================================================================
# TESTRUN — 5 estados (FI-2B)
# =============================================================================

TESTRUN_INITIAL = TestRunStatus.PLANNED
TESTRUN_TERMINAL: frozenset[TestRunStatus] = frozenset(
    {
        TestRunStatus.PASSED,
        TestRunStatus.FAILED,
        TestRunStatus.ERROR,
    }
)

TESTRUN_TRANSITIONS: dict[TestRunStatus, frozenset[TestRunStatus]] = {
    TestRunStatus.PLANNED: frozenset(
        {
            TestRunStatus.EXECUTING,
        }
    ),
    TestRunStatus.EXECUTING: frozenset(
        {
            TestRunStatus.PASSED,
            TestRunStatus.FAILED,
            TestRunStatus.ERROR,
        }
    ),
    TestRunStatus.PASSED: frozenset(),  # terminal
    TestRunStatus.FAILED: frozenset(),  # terminal
    TestRunStatus.ERROR: frozenset(),  # terminal
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================


def get_valid_transitions(
    status_enum: type[StrEnum],
    transitions: dict[StrEnum, frozenset[StrEnum]],
    current: str,
) -> frozenset[StrEnum]:
    """Obter transições válidas para um estado atual."""
    try:
        current_enum = status_enum(current)
        return transitions.get(current_enum, frozenset())
    except ValueError:
        return frozenset()


def is_valid_transition(
    status_enum: type[StrEnum],
    transitions: dict[StrEnum, frozenset[StrEnum]],
    current: str,
    target: str,
) -> bool:
    """Verificar se uma transição é válida."""
    try:
        current_enum = status_enum(current)
        target_enum = status_enum(target)
        valid = transitions.get(current_enum, frozenset())
        return target_enum in valid
    except ValueError:
        return False
