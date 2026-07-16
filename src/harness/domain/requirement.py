"""
Entidade Requirement do Harness Cognitivo - FI-2.

Requirement representa comportamento, restrição ou qualidade verificável.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.ids import validate_id_format


class RequirementStatus(StrEnum):
    """Estados de um Requirement."""

    PROPOSED = "proposed"
    APPROVED = "approved"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    REJECTED = "rejected"


class RequirementPriority(StrEnum):
    """Prioridade de um Requirement."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Requirement(BaseModel):
    """Entidade Requirement - imutável."""

    requirement_id: str
    project_id: str
    description: str
    status: RequirementStatus = RequirementStatus.PROPOSED
    priority: RequirementPriority = RequirementPriority.MEDIUM
    acceptance_criteria: list[str] = Field(default_factory=list)
    source_id: str | None = None
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("requirement_id")
    @classmethod
    def validate_requirement_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def update_status(self, new_status: RequirementStatus) -> Requirement:
        """Retorna nova instância com status atualizado."""
        return self.model_copy(
            update={
                "status": new_status,
                "updated_at": datetime.now(UTC),
                "version": self.version + 1,
            }
        )

    @property
    def is_approved(self) -> bool:
        """Verificar se o requisito esta aprovado."""
        return self.status == RequirementStatus.APPROVED
