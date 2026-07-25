"""
Entidade Incident do Harness Cognitivo — FI-2B Parte 2.

Incident representa um incidente operacional detectado na plataforma.
O modelo é imutável; transições retornam nova instância.
O modelo não executa contenção automaticamente.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from harness.domain.enums import IncidentSeverityLevel, IncidentState
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    INCIDENT_INITIAL,
    INCIDENT_TERMINAL,
    INCIDENT_TRANSITIONS,
)


class Incident(BaseModel):
    """Entidade Incident — imutável.

    Representa um incidente operacional. O modelo registra estado,
    severidade, evidências e ações; não executa contenção automaticamente.
    """

    incident_id: str
    title: str = Field(description="Título do incidente")
    description: str = Field(description="Descrição do incidente")
    severity: IncidentSeverityLevel
    state: IncidentState = INCIDENT_INITIAL
    affected_component: str | None = Field(
        default=None,
        description="Origem ou componente afetado",
    )
    detected_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Data de detecção",
    )
    responsible: str | None = Field(
        default=None,
        description="Responsável (obrigatório para severidade critical)",
    )
    impact: str = Field(
        default="",
        description="Descrição do impacto",
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="IDs de evidências do incidente",
    )
    containment_actions: list[str] = Field(
        default_factory=list,
        description="Ações de contenção (obrigatório para contained)",
    )
    known_cause: str | None = Field(
        default=None,
        description="Causa conhecida (fato confirmado)",
    )
    cause_hypothesis: str | None = Field(
        default=None,
        description="Hipótese de causa (não confirmada)",
    )
    corrective_actions: list[str] = Field(
        default_factory=list,
        description="Ações corretivas (obrigatório para resolved)",
    )
    related_release_ids: list[str] = Field(
        default_factory=list,
        description="IDs de releases relacionadas",
    )
    resolved_at: datetime | None = Field(
        default=None,
        description="Data de resolução (não pode anteceder detected_at)",
    )
    close_record: str | None = Field(
        default=None,
        description="Registro de encerramento (obrigatório para closed)",
    )
    resolution_gate_decision_id: str | None = Field(
        default=None,
        description="GateDecision originada pela resolução",
    )
    version: int = 1
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("incident_id")
    @classmethod
    def validate_incident_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("detected_at", "updated_at", "resolved_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_state_consistency(self) -> Incident:
        """Impedir estados inválidos na construção e desserialização."""
        s = self.state

        # Incidente deve registrar descrição e impacto
        if not self.description or not self.description.strip():
            raise InvariantViolationError(
                entity="Incident",
                invariant="incident_requires_description",
                details="Incidente deve possuir descrição",
            )

        if not self.impact or not self.impact.strip():
            raise InvariantViolationError(
                entity="Incident",
                invariant="incident_requires_impact",
                details="Incidente deve registrar impacto",
            )

        # Incidente crítico deve possuir responsável
        if self.severity == IncidentSeverityLevel.CRITICAL and not self.responsible:
            raise InvariantViolationError(
                entity="Incident",
                invariant="critical_requires_responsible",
                details="Incidente crítico exige responsável identificado",
            )

        # CONTAINED deve possuir ação de contenção
        if s == IncidentState.CONTAINED and not self.containment_actions:
            raise InvariantViolationError(
                entity="Incident",
                invariant="contained_requires_containment_actions",
                details="Estado contido exige ao menos uma ação de contenção",
            )

        # RESOLVED deve possuir ação corretiva
        if s == IncidentState.RESOLVED and not self.corrective_actions:
            raise InvariantViolationError(
                entity="Incident",
                invariant="resolved_requires_corrective_actions",
                details="Estado resolvido exige ao menos uma ação corretiva",
            )

        # RESOLVED requer resolved_at
        if s == IncidentState.RESOLVED and self.resolved_at is None:
            raise InvariantViolationError(
                entity="Incident",
                invariant="resolved_requires_resolved_at",
                details="Estado resolvido exige data de resolução",
            )

        # CLOSED deve possuir registro de encerramento
        if s == IncidentState.CLOSED and (
            not self.close_record or not self.close_record.strip()
        ):
            raise InvariantViolationError(
                entity="Incident",
                invariant="closed_requires_close_record",
                details="Estado encerrado exige registro de encerramento",
            )

        # CLOSED requer resolved_at
        if s == IncidentState.CLOSED and self.resolved_at is None:
            raise InvariantViolationError(
                entity="Incident",
                invariant="closed_requires_resolved_at",
                details="Estado encerrado exige data de resolução",
            )

        # Data de resolução não pode anteceder data de detecção
        if (
            self.resolved_at is not None
            and self.detected_at is not None
            and self.resolved_at < self.detected_at
        ):
            raise InvariantViolationError(
                entity="Incident",
                invariant="resolved_not_before_detected",
                details="Data de resolução não pode anteceder data de detecção",
            )

        return self

    def can_transition_to(self, target: IncidentState) -> bool:
        """Verificar se transição é válida."""
        valid = INCIDENT_TRANSITIONS.get(self.state, frozenset())
        return target in valid

    def transition_to(
        self,
        target: IncidentState,
        *,
        containment_actions: list[str] | None = None,
        corrective_actions: list[str] | None = None,
        close_record: str | None = None,
    ) -> Incident:
        """Transicionar para novo estado (retorna nova instância)."""
        if self.state == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(INCIDENT_TRANSITIONS.get(self.state, frozenset()))
            raise InvalidTransitionError(
                entity="Incident",
                current_state=self.state.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        now = datetime.now(UTC)
        updates: dict[str, Any] = {
            "state": target,
            "updated_at": now,
            "version": self.version + 1,
        }

        if target == IncidentState.CONTAINED:
            resolved_actions = containment_actions or self.containment_actions
            if not resolved_actions:
                raise InvariantViolationError(
                    entity="Incident",
                    invariant="contained_requires_containment_actions",
                    details="Transição para contained requer containment_actions",
                )
            updates["containment_actions"] = resolved_actions

        if target == IncidentState.RESOLVED:
            resolved_corrective = corrective_actions or self.corrective_actions
            if not resolved_corrective:
                raise InvariantViolationError(
                    entity="Incident",
                    invariant="resolved_requires_corrective_actions",
                    details="Transição para resolved requer corrective_actions",
                )
            updates["corrective_actions"] = resolved_corrective
            updates["resolved_at"] = self.resolved_at or now

        if target == IncidentState.CLOSED:
            resolved_close = close_record or self.close_record
            if not resolved_close or not resolved_close.strip():
                raise InvariantViolationError(
                    entity="Incident",
                    invariant="closed_requires_close_record",
                    details="Transição para closed requer close_record",
                )
            updates["close_record"] = resolved_close
            if self.resolved_at is None:
                raise InvariantViolationError(
                    entity="Incident",
                    invariant="closed_requires_resolved_at",
                    details="Transição para closed requer resolved_at (resolva antes de encerrar)",
                )

        data = self.model_dump()
        data.update(updates)
        return type(self).model_validate(data)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.state in INCIDENT_TERMINAL
