"""
Enums compartilhados do dominio Harness Cognitivo - FI-2B.

Vocabulario controlado para estados, severidades e classificacoes.
Extends FI-2A enums with ExecutionRun, Review, and TestRun status.
"""

from enum import StrEnum


class ProjectStatus(StrEnum):
    """Estados do ciclo de vida de um Projeto."""

    CAPTURED = "captured"
    TRIAGE = "triage"
    DISCOVERY = "discovery"
    SPECIFIED = "specified"
    ARCHITECTED = "architected"
    PLANNED = "planned"
    READY = "ready"
    EXECUTING = "executing"
    REVIEWING = "reviewing"
    VALIDATING = "validating"
    REWORK_REQUIRED = "rework_required"
    AWAITING_APPROVAL = "awaiting_approval"
    RELEASE_READY = "release_ready"
    RELEASED = "released"
    MONITORED = "monitored"
    MAINTENANCE = "maintenance"
    SUSPENDED = "suspended"
    ABANDONED = "abandoned"
    ARCHIVED = "archived"


class TaskStatus(StrEnum):
    """Estados do ciclo de vida de uma Tarefa."""

    PROPOSED = "proposed"
    PLANNED = "planned"
    BLOCKED = "blocked"
    ELIGIBLE = "eligible"
    ASSIGNED = "assigned"
    RUNNING = "running"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    IN_VALIDATION = "in_validation"
    REWORK = "rework"
    ACCEPTED = "accepted"
    CANCELLED = "cancelled"
    SUPERSEDED = "superseded"


class WorkOrderStatus(StrEnum):
    """Estados do ciclo de vida de uma WorkOrder."""

    DRAFT = "draft"
    VALIDATED = "validated"
    AUTHORIZED = "authorized"
    DISPATCHED = "dispatched"
    ACTIVE = "active"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    REVOKED = "revoked"


class GateStatus(StrEnum):
    """Estados do ciclo de vida do processo de Gate.

    Representa o ESTADO DO PROCESSO de avaliação do gate.
    O resultado da decisão é capturado por GateDecisionType.
    """

    PENDING = "pending"
    EVALUATING = "evaluating"
    DECIDED = "decided"
    CANCELLED = "cancelled"


class GateDecisionType(StrEnum):
    """Resultado da decisao de Gate (separado do estado do processo)."""

    ADVANCE = "advance"
    REWORK = "rework"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    AWAITING_HUMAN = "awaiting_human"
    WAIVED = "waived"


class Severity(StrEnum):
    """Severidade de achados de revisao e incidentes."""

    BLOCKER = "blocker"
    MAJOR = "major"
    MINOR = "minor"
    SUGGESTION = "suggestion"
    QUESTION = "question"


class MaintenanceType(StrEnum):
    """Tipos de manutencao de incidentes."""

    CORRECTIVE = "corrective"
    PREVENTIVE = "preventive"
    ADAPTIVE = "adaptive"
    EVOLUTIONARY = "evolutionary"


class ReleaseStatus(StrEnum):
    """Estados do ciclo de vida de uma Release."""

    DRAFT = "draft"
    CANDIDATE = "candidate"
    VALIDATING = "validating"
    APPROVED = "approved"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    VERIFYING = "verifying"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"
    SUPERSEDED = "superseded"
    RETIRED = "retired"


class IncidentStatus(StrEnum):
    """Estados do ciclo de vida de um Incidente."""

    DETECTED = "detected"
    TRIAGED = "triaged"
    INVESTIGATING = "investigating"
    MITIGATING = "mitigating"
    CONTAINED = "contained"
    REPRODUCED = "reproduced"
    FIXING = "fixing"
    VALIDATING_FIX = "validating_fix"
    RESOLVED = "resolved"
    MONITORING = "monitoring"
    CLOSED = "closed"
    REOPENED = "reopened"


class RiskLevel(StrEnum):
    """Nivel de risco de um projeto."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


# =============================================================================
# FI-2B ENUMS
# =============================================================================


class ExecutionRunStatus(StrEnum):
    """Estados do ciclo de vida de uma ExecutionRun."""

    INITIATED = "initiated"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class ReviewType(StrEnum):
    """Tipos de revisão suportados."""

    FUNCTIONAL = "functional"
    DOMAIN = "domain"
    STRUCTURAL = "structural"
    SECURITY = "security"


class ReviewStatus(StrEnum):
    """Estados do ciclo de vida de uma Review."""

    REQUESTED = "requested"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGE_REQUESTED = "change_requested"


class TestRunStatus(StrEnum):
    """Estados do ciclo de vida de uma TestRun."""

    PLANNED = "planned"
    EXECUTING = "executing"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
