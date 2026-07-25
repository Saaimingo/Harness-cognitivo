"""
Entidade GateDecision do Harness Cognitivo — FI-2B Parte 2.

GateDecision representa o registro formal de uma decisão de gate.
Não é uma máquina de estados com transições: o desfecho é imutável
após registro. O estado é o próprio resultado da decisão.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from harness.domain.enums import GateDecisionState
from harness.domain.errors import InvariantViolationError
from harness.domain.ids import validate_id_format


class GateDecision(BaseModel):
    """Registro formal de uma decisão de gate — imutável.

    Representa o desfecho documentado de uma avaliação de gate.
    O campo decision_state captura o resultado; o modelo não executa
    nem promove nada sozinho.
    """

    gate_decision_id: str
    target: str = Field(description="Alvo avaliado (ID de artefato, projeto, etc.)")
    gate_stage: str = Field(
        default="",
        description="Tipo ou estágio do gate (ex.: 'architectural', 'security')",
    )
    decision_state: GateDecisionState
    justification: str = Field(description="Justificativa da decisão (obrigatória)")
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="IDs de evidências utilizadas na decisão",
    )
    evaluated_criteria: list[str] = Field(
        default_factory=list,
        description="Requisitos ou critérios avaliados",
    )
    authority: str | None = Field(
        default=None,
        description="Responsável ou autoridade que emitiu a decisão",
    )
    blockers: list[str] = Field(
        default_factory=list,
        description="Bloqueios encontrados (obrigatório para blocked/rejected)",
    )
    corrective_actions: list[str] = Field(
        default_factory=list,
        description="Ações corretivas exigidas (obrigatório para rework_required)",
    )
    previous_decision_id: str | None = Field(
        default=None,
        description="Relação com decisão anterior (referência, não altera a anterior)",
    )
    decided_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Data e hora da decisão",
    )
    version: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("gate_decision_id")
    @classmethod
    def validate_gate_decision_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("decided_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_state_consistency(self) -> GateDecision:
        """Impedir estados inválidos na construção e desserialização."""
        s = self.decision_state

        # Toda decisão deve possuir justificativa
        if not self.justification or not self.justification.strip():
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="decision_requires_justification",
                details="Toda decisão de gate exige justificativa não vazia",
            )

        # APPROVED requer evidência
        if s == GateDecisionState.APPROVED and not self.evidence_ids:
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="approved_requires_evidence",
                details="Decisão aprovada exige ao menos uma evidência",
            )

        # APPROVED_WITH_RESERVATIONS requer evidência
        if s == GateDecisionState.APPROVED_WITH_RESERVATIONS and not self.evidence_ids:
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="approved_with_reservations_requires_evidence",
                details="Aprovação com ressalvas exige ao menos uma evidência",
            )

        # BLOCKED deve informar blockers
        if s == GateDecisionState.BLOCKED and not self.blockers:
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="blocked_requires_blockers",
                details="Decisão bloqueada deve informar ao menos um bloqueio",
            )

        # REJECTED deve informar blockers
        if s == GateDecisionState.REJECTED and not self.blockers:
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="rejected_requires_blockers",
                details="Decisão rejeitada deve informar ao menos um bloqueio",
            )

        # REWORK_REQUIRED deve possuir ao menos uma ação corretiva
        if s == GateDecisionState.REWORK_REQUIRED and not self.corrective_actions:
            raise InvariantViolationError(
                entity="GateDecision",
                invariant="rework_requires_corrective_actions",
                details="Correção necessária exige ao menos uma ação corretiva",
            )

        return self
