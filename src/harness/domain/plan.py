"""
Entidade Plan do Harness Cognitivo - FI-2.

Plan representa uma versao aprovada da decomposicao do trabalho.
Versionamento com numero positivo e referencia a versao anterior.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from harness.domain.ids import validate_id_format


class PlanStatus(str, Enum):
    """Estados de um Plan."""
    DRAFT = "draft"
    APPROVED = "approved"
    SUPERSEDED = "superseded"


class Plan(BaseModel):
    """Entidade Plan - imutavel com versionamento."""

    plan_id: str
    project_id: str
    version: int = Field(ge=1, description="Numero de versao positivo")
    title: str
    description: str = ""
    status: PlanStatus = PlanStatus.DRAFT
    previous_version_id: str | None = Field(
        default=None,
        description="ID da versao anterior quando houver substituicao"
    )
    tasks_planned: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("plan_id")
    @classmethod
    def validate_plan_id(cls, v: str) -> str:
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

    def approve(self) -> Plan:
        """Aprovar o plano - retorna nova instancia."""
        return self.model_copy(update={
            "status": PlanStatus.APPROVED,
            "updated_at": datetime.now(timezone.utc),
        })

    def supersede(self, new_version_id: str) -> Plan:
        """Substituir por nova versao - retorna nova instancia."""
        return self.model_copy(update={
            "status": PlanStatus.SUPERSEDED,
            "updated_at": datetime.now(timezone.utc),
        })

    def create_next_version(self, new_plan_id: str) -> Plan:
        """Criar proxima versao do plano."""
        return Plan(
            plan_id=new_plan_id,
            project_id=self.project_id,
            version=self.version + 1,
            title=self.title,
            description=self.description,
            previous_version_id=self.plan_id,
        )

    @property
    def is_approved(self) -> bool:
        """Verificar se o plano esta aprovado."""
        return self.status == PlanStatus.APPROVED
