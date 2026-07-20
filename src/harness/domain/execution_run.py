"""
Entidade ExecutionRun do Harness Cognitivo — FI-2B.

ExecutionRun representa uma tentativa concreta e auditável de execução de uma WorkOrder.
Máquina de estados com 5 estados (initiated, running, completed, failed, abandoned).
Modelo imutável com transições que retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

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

    @field_validator("created_at", "updated_at", "started_at", "completed_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_state_consistency(self) -> ExecutionRun:
        """Impedir estados inválidos em construção direta e desserialização."""
        s = self.status

        # --- Requisitos por estado ---
        if s == ExecutionRunStatus.COMPLETED:
            if not self.changeset_id or not self.changeset_id.strip():
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="completed_requires_changeset",
                    details="COMPLETED exige changeset_id não vazio",
                )
            if self.failure_reason or self.abandon_justification:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="completed_no_conflicting_fields",
                    details="COMPLETED não pode ter failure_reason ou abandon_justification",
                )

        if s == ExecutionRunStatus.FAILED:
            if not self.failure_reason or not self.failure_reason.strip():
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="failed_requires_reason",
                    details="FAILED exige failure_reason não vazio",
                )
            if self.changeset_id or self.abandon_justification:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="failed_no_conflicting_fields",
                    details="FAILED não pode ter changeset_id ou abandon_justification",
                )

        if s == ExecutionRunStatus.ABANDONED:
            if not self.abandon_justification or not self.abandon_justification.strip():
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="abandoned_requires_justification",
                    details="ABANDONED exige abandon_justification não vazio",
                )
            if self.changeset_id or self.failure_reason:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="abandoned_no_conflicting_fields",
                    details="ABANDONED não pode ter changeset_id ou failure_reason",
                )

        # --- INITIATED não deve ter campos de execução ---
        if s == ExecutionRunStatus.INITIATED:
            if self.started_at or self.completed_at:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="initiated_no_execution_fields",
                    details="INITIATED não pode ter started_at ou completed_at",
                )
            if self.changeset_id or self.failure_reason or self.abandon_justification:
                raise InvariantViolationError(
                    entity="ExecutionRun",
                    invariant="initiated_no_result_fields",
                    details="INITIATED não pode ter changeset_id, failure_reason ou abandon_justification",
                )

        # --- RUNNING não deve ter completed_at ---
        if s == ExecutionRunStatus.RUNNING and self.completed_at:
            raise InvariantViolationError(
                entity="ExecutionRun",
                invariant="running_no_completed_at",
                details="RUNNING não pode ter completed_at",
            )

        # --- Timestamps obrigatórios ---
        if (
            s
            in (
                ExecutionRunStatus.RUNNING,
                ExecutionRunStatus.COMPLETED,
                ExecutionRunStatus.FAILED,
                ExecutionRunStatus.ABANDONED,
            )
            and self.started_at is None
        ):
            raise InvariantViolationError(
                entity="ExecutionRun",
                invariant="non_initiated_requires_started_at",
                details=f"Estado {s.value} requer started_at preenchido",
            )

        if s in EXECUTIONRUN_TERMINAL and self.completed_at is None:
            raise InvariantViolationError(
                entity="ExecutionRun",
                invariant="terminal_requires_completed_at",
                details=f"Estado terminal {s.value} requer completed_at preenchido",
            )

        return self

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

        if (
            target
            in (
                ExecutionRunStatus.RUNNING,
                ExecutionRunStatus.COMPLETED,
                ExecutionRunStatus.FAILED,
                ExecutionRunStatus.ABANDONED,
            )
            and self.started_at is None
        ):
            updates["started_at"] = now

        if target in EXECUTIONRUN_TERMINAL:
            updates["completed_at"] = now

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

        # Usar model_validate para garantir revalidação via model_validator
        data = self.model_dump()
        data.update(updates)
        return type(self).model_validate(data)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.status in EXECUTIONRUN_TERMINAL
