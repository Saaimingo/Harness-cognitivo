"""
Entidade WorkOrder do Harness Cognitivo - FI-2.

WorkOrder é a autorização estruturada para execução específica.
Registra autoridade, momento da autorização e escopo autorizado.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.enums import WorkOrderStatus
from harness.domain.errors import InvalidTransitionError, MissingAuthorityError
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    WORKORDER_INITIAL,
    WORKORDER_TERMINAL,
    WORKORDER_TRANSITIONS,
)


class WorkOrderScope(BaseModel):
    """Escopo autorizado para uma WorkOrder."""

    included: list[str] = Field(default_factory=list)
    excluded: list[str] = Field(default_factory=list)


class WorkOrder(BaseModel):
    """Entidade WorkOrder - imutável."""

    work_order_id: str
    project_id: str
    task_id: str
    title: str
    description: str = ""
    status: WorkOrderStatus = WORKORDER_INITIAL
    authority: str | None = Field(
        default=None, description="Autoridade que autorizou a execução"
    )
    authorized_at: datetime | None = Field(
        default=None, description="Momento da autorização"
    )
    scope: WorkOrderScope = Field(default_factory=WorkOrderScope)
    expires_at: datetime | None = None
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("work_order_id")
    @classmethod
    def validate_work_order_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("task_id")
    @classmethod
    def validate_task_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def can_transition_to(self, target: WorkOrderStatus) -> bool:
        """Verificar se transição é válida."""
        valid = WORKORDER_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: WorkOrderStatus,
        *,
        authority: str | None = None,
    ) -> WorkOrder:
        """Transicionar para novo estado (retorna nova instância)."""
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(WORKORDER_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="WorkOrder",
                current_state=self.status.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        updates: dict[str, Any] = {
            "status": target,
            "updated_at": datetime.now(UTC),
            "version": self.version + 1,
        }

        if target == WorkOrderStatus.AUTHORIZED:
            if authority is None:
                raise MissingAuthorityError(
                    entity="WorkOrder",
                    operation="authorize",
                )
            updates["authority"] = authority
            updates["authorized_at"] = datetime.now(UTC)

        return self.model_copy(update=updates)

    @property
    def is_terminal(self) -> bool:
        """Verificar se a WorkOrder está em estado terminal."""
        return self.status in WORKORDER_TERMINAL

    @property
    def is_executable(self) -> bool:
        """Verificar se a WorkOrder pode ser executada."""
        return self.status in {
            WorkOrderStatus.AUTHORIZED,
            WorkOrderStatus.DISPATCHED,
        }
