"""
Entidade Release do Harness Cognitivo — FI-2B Parte 2.

Release representa uma entrega controlada com estado, autorização
e rastreabilidade. O modelo é imutável; transições retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from harness.domain.enums import ReleaseState
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    RELEASE_INITIAL,
    RELEASE_TERMINAL,
    RELEASE_TRANSITIONS,
)


class Release(BaseModel):
    """Entidade Release — imutável.

    Representa uma entrega controlada. O modelo registra estado e contrato;
    não executa deploy.
    """

    release_id: str
    name: str = Field(description="Nome ou versão da release")
    artifact_target: str = Field(description="Artefato ou alvo liberado")
    environment: str = Field(
        default="",
        description="Ambiente de destino",
    )
    state: ReleaseState = RELEASE_INITIAL
    gate_decision_id: str | None = Field(
        default=None,
        description="GateDecision autorizadora (obrigatório para promoted)",
    )
    versioned_origin: str | None = Field(
        default=None,
        description="Origem versionada (commit, tag) — obrigatório para promoted",
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="IDs de evidências da release",
    )
    responsible: str | None = Field(
        default=None,
        description="Responsável pela release",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    promoted_at: datetime | None = Field(
        default=None,
        description="Data de promoção",
    )
    rollback_plan: str | None = Field(
        default=None,
        description="Plano de rollback (obrigatório para promoted)",
    )
    known_risks: list[str] = Field(
        default_factory=list,
        description="Riscos conhecidos",
    )
    release_notes: str | None = Field(
        default=None,
        description="Notas da release",
    )
    reverted_from_id: str | None = Field(
        default=None,
        description="Release ou evento que motivou a reversão (obrigatório para reverted)",
    )
    version: int = 1
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("release_id")
    @classmethod
    def validate_release_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at", "updated_at", "promoted_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_state_consistency(self) -> Release:
        """Impedir estados inválidos na construção e desserialização."""
        s = self.state

        # PROMOTED exige gate_decision_id
        if s == ReleaseState.PROMOTED and not self.gate_decision_id:
            raise InvariantViolationError(
                entity="Release",
                invariant="promoted_requires_gate_decision",
                details="Release promovida exige GateDecision autorizadora",
            )

        # PROMOTED exige origem versionada
        if s == ReleaseState.PROMOTED and not self.versioned_origin:
            raise InvariantViolationError(
                entity="Release",
                invariant="promoted_requires_versioned_origin",
                details="Release promovida exige origem versionada",
            )

        # PROMOTED exige plano de rollback
        if s == ReleaseState.PROMOTED and (
            not self.rollback_plan or not self.rollback_plan.strip()
        ):
            raise InvariantViolationError(
                entity="Release",
                invariant="promoted_requires_rollback_plan",
                details="Release promovida exige plano de rollback",
            )

        # REVERTED deve registrar o que motivou a reversão
        if s == ReleaseState.REVERTED and not self.reverted_from_id:
            raise InvariantViolationError(
                entity="Release",
                invariant="reverted_requires_reverted_from",
                details="Release revertida deve referenciar release ou evento que motivou a reversão",
            )

        # CANCELLED não pode estar promoted
        if s == ReleaseState.CANCELLED and self.promoted_at is not None:
            raise InvariantViolationError(
                entity="Release",
                invariant="cancelled_not_promoted",
                details="Release cancelada não pode ter sido promovida",
            )

        return self

    def can_transition_to(self, target: ReleaseState) -> bool:
        """Verificar se transição é válida."""
        valid = RELEASE_TRANSITIONS.get(self.state, frozenset())
        return target in valid

    def transition_to(
        self,
        target: ReleaseState,
        *,
        gate_decision_id: str | None = None,
        versioned_origin: str | None = None,
        rollback_plan: str | None = None,
        reverted_from_id: str | None = None,
    ) -> Release:
        """Transicionar para novo estado (retorna nova instância)."""
        if self.state == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(RELEASE_TRANSITIONS.get(self.state, frozenset()))
            raise InvalidTransitionError(
                entity="Release",
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

        if target == ReleaseState.PROMOTED:
            resolved_gate = gate_decision_id or self.gate_decision_id
            if not resolved_gate:
                raise InvariantViolationError(
                    entity="Release",
                    invariant="promoted_requires_gate_decision",
                    details="Transição para promoted requer gate_decision_id",
                )
            resolved_origin = versioned_origin or self.versioned_origin
            if not resolved_origin:
                raise InvariantViolationError(
                    entity="Release",
                    invariant="promoted_requires_versioned_origin",
                    details="Transição para promoted requer versioned_origin",
                )
            resolved_rollback = rollback_plan or self.rollback_plan
            if not resolved_rollback or not resolved_rollback.strip():
                raise InvariantViolationError(
                    entity="Release",
                    invariant="promoted_requires_rollback_plan",
                    details="Transição para promoted requer rollback_plan",
                )
            updates["gate_decision_id"] = resolved_gate
            updates["versioned_origin"] = resolved_origin
            updates["rollback_plan"] = resolved_rollback
            updates["promoted_at"] = now

        if target == ReleaseState.REVERTED:
            resolved_reverted = reverted_from_id or self.reverted_from_id
            if not resolved_reverted:
                raise InvariantViolationError(
                    entity="Release",
                    invariant="reverted_requires_reverted_from",
                    details="Transição para reverted requer reverted_from_id",
                )
            updates["reverted_from_id"] = resolved_reverted

        data = self.model_dump()
        data.update(updates)
        return type(self).model_validate(data)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.state in RELEASE_TERMINAL
