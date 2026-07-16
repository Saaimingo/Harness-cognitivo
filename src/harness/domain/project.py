"""
Entidade Project do Harness Cognitivo - FI-2.

Project é a unidade de ciclo de vida no Harness.
Máquina de estados com 19 estados (Doc 5, §6).
Transições retornam nova instância (imutabilidade).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.enums import ProjectStatus, RiskLevel
from harness.domain.errors import InvalidTransitionError, InvariantViolationError
from harness.domain.transitions import (
    PROJECT_INITIAL,
    PROJECT_TERMINAL,
    PROJECT_TRANSITIONS,
)


class Project(BaseModel):
    """Entidade Project - imutável."""

    project_id: str
    name: str
    description: str = ""
    status: ProjectStatus = PROJECT_INITIAL
    risk_level: RiskLevel = RiskLevel.LOW
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        from harness.domain.ids import validate_id_format

        return validate_id_format(v)

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def can_transition_to(self, target: ProjectStatus) -> bool:
        """Verificar se transicao e valida."""
        valid = PROJECT_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: ProjectStatus,
        *,
        authority: str | None = None,
        reason: str | None = None,
    ) -> Project:
        """
        Transicionar para novo estado.

        Retorna nova instância (imutabilidade).
        Lança InvalidTransitionError se transição inválida.
        Lança IdempotentTransitionError se já está no estado.
        """
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(PROJECT_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="Project",
                current_state=self.status.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        if (
            target in PROJECT_TERMINAL
            and self.status not in PROJECT_TERMINAL
            and authority is None
        ):
            raise InvariantViolationError(
                entity="Project",
                invariant="terminal_transition_requires_authority",
                details=f"Transicao para estado terminal {target.value} requer autoridade",
            )

        return self.model_copy(
            update={
                "status": target,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    @property
    def is_terminal(self) -> bool:
        """Verificar se o projeto esta em estado terminal."""
        return self.status in PROJECT_TERMINAL

    @property
    def is_suspended(self) -> bool:
        """Verificar se o projeto esta suspenso."""
        return self.status == ProjectStatus.SUSPENDED
