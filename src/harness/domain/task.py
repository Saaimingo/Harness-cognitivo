"""
Entidade Task do Harness Cognitivo - FI-2.

Task é a unidade planejada com dependências e critério de aceite.
Máquina de estados com 13 estados (Doc 5, §7).
Limite de rework configurável.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.enums import TaskStatus
from harness.domain.transitions import TASK_TRANSITIONS, TASK_INITIAL, TASK_TERMINAL
from harness.domain.errors import (
    InvalidTransitionError,
    ReworkLimitExceededError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format

DEFAULT_REWORK_LIMIT = 5


class Task(BaseModel):
    """Entidade Task - imutável."""

    task_id: str
    project_id: str
    plan_id: str
    title: str
    description: str = ""
    status: TaskStatus = TASK_INITIAL
    assigned_to: str | None = None
    rework_count: int = 0
    rework_limit: int = DEFAULT_REWORK_LIMIT
    requirements: list[str] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    changeset_id: str | None = None
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("plan_id")
    @classmethod
    def validate_plan_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def can_transition_to(self, target: TaskStatus) -> bool:
        """Verificar se transição é válida."""
        valid = TASK_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: TaskStatus,
        *,
        authority: str | None = None,
    ) -> Task:
        """Transicionar para novo estado (retorna nova instância)."""
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(TASK_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="Task",
                current_state=self.status.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        updates: dict[str, Any] = {
            "status": target,
            "updated_at": datetime.now(timezone.utc),
            "version": self.version + 1,
        }

        if target == TaskStatus.REWORK:
            new_count = self.rework_count + 1
            if new_count >= self.rework_limit:
                raise ReworkLimitExceededError(
                    entity="Task",
                    task_id=self.task_id,
                    limit=self.rework_limit,
                    current=new_count,
                )
            updates["rework_count"] = new_count

        if target in TASK_TERMINAL and self.status not in TASK_TERMINAL:
            if authority is None:
                raise InvariantViolationError(
                    entity="Task",
                    invariant="terminal_transition_requires_authority",
                    details=f"Transição para estado terminal {target.value} requer autoridade",
                )

        return self.model_copy(update=updates)

    @property
    def is_terminal(self) -> bool:
        """Verificar se a tarefa está em estado terminal."""
        return self.status in TASK_TERMINAL

    @property
    def rework_exhausted(self) -> bool:
        """Verificar se o limite de rework foi atingido."""
        return self.rework_count >= self.rework_limit
