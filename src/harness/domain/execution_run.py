"""
Entidade ExecutionRun do Harness Cognitivo — FI-2B.

ExecutionRun representa uma tentativa concreta e auditável de execução de uma WorkOrder.
Máquina de estados com 5 estados (initiated, running, completed, failed, abandoned).
Modelo imutável com transições que retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.enums import ExecutionRunStatus
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    EXECUTIONRUN_INITIAL,
    EXECUTIONRUN_TERMINAL,
    EXECUTIONRUN_TRANSITIONS,
)


class ExecutionRun(BaseModel):
    """Entidade ExecutionRun — imutável.

    Representa uma tentativa concreta de cumprir uma WorkOrder.
    Cada ExecutionRun possui ID próprio, referência à WorkOrder, e número de tentativa.
    """

    execution_run_id: str
    work_order_id: str
    attempt_number: int = Field(
        ge=1, description="Número da tentativa (inteiro positivo)"
    )
    status: ExecutionRunStatus = EXECUTIONRUN_INITIAL
    changeset_id: str | None = Field(
        default=None,
        description="ID do changeset produzido (obrigatório para completed)",
    )
    failure_reason: str | None = Field(
        default=None, description="Motivo da falha (obrigatório para failed)"
    )
    abandon_justification: str | None = Field(
        default=None,
        description="Justificativa do abandono (obrigatório para abandoned)",
    )
    executor: str | None = Field(default=None, description="Autoridade que executou")
    started_at: datetime | None = Field(
        default=None,
        description="Timestamp de início (preenchido ao transicionar para running)",
    )
    completed_at: datetime | None = Field(
        default=None, description="Timestamp de encerramento"
    )
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("execution_run_id")
    @classmethod
    def validate_execution_run_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("work_order_id")
    @classmethod
    def validate_work_order_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def can_transition_to(self, target: ExecutionRunStatus) -> bool:
        """Verificar se transição é válida."""
        valid = EXECUTIONRUN_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: ExecutionRunStatus,
        *,
        changeset_id: str | None = None,
        failure_reason: str | None = None,
        abandon_justification: str | None = None,
    ) -> ExecutionRun:
        """Transicionar para novo estado (retorna nova instância).

        Para COMPLETED: fornecer changeset_id.
        Para FAILED: fornecer failure_reason.
        Para ABANDONED: fornecer abandon_justification.
        """
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(EXECUTIONRUN_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="ExecutionRun",
                current_state=self.status.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        updates: dict[str, Any] = {
            "status": target,
            "updated_at": datetime.now(UTC),
            "version": self.version + 1,
        }

        now = datetime.now(UTC)

        if target == ExecutionRunStatus.RUNNING and self.started_at is None:
            updates["started_at"] = now

        if target in EXECUTIONRUN_TERMINAL:
            updates["completed_at"] = now
            if self.started_at is None:
                updates["started_at"] = now

        if target == ExecutionRunStatus.COMPLETED:
            resolved_cs = changeset_id or self.changeset_id
            if resolved_cs is None:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="completed_requires_changeset",
                    details="Transição para completed requer changeset_id",
                )
            updates["changeset_id"] = resolved_cs

        if target == ExecutionRunStatus.FAILED:
            resolved_fr = failure_reason or self.failure_reason
            if resolved_fr is None:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="failed_requires_reason",
                    details="Transição para failed requer failure_reason",
                )
            updates["failure_reason"] = resolved_fr

        if target == ExecutionRunStatus.ABANDONED:
            resolved_aj = abandon_justification or self.abandon_justification
            if resolved_aj is None:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="abandoned_requires_justification",
                    details="Transição para abandoned requer abandon_justification",
                )
            updates["abandon_justification"] = resolved_aj

        return self.model_copy(update=updates)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.status in EXECUTIONRUN_TERMINAL
