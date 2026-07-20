"""
Entidade Review do Harness Cognitivo — FI-2B.

Review representa uma avaliação estruturada do resultado de uma ExecutionRun.
Suporta 4 tipos de revisão: functional, domain, structural, security.
Máquina de estados com 5 estados (requested, in_progress, approved, rejected, change_requested).
Modelo imutável com transições que retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from harness.domain.enums import ReviewStatus, ReviewType
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    REVIEW_INITIAL,
    REVIEW_TERMINAL,
    REVIEW_TRANSITIONS,
)


class Review(BaseModel):
    """Entidade Review — imutável.

    Avaliação estruturada do resultado de uma ExecutionRun.
    Cada Review possui tipo explícito, responsável, e resultado.
    reviewer e executor não podem ser a mesma autoridade.
    """

    review_id: str
    execution_run_id: str
    review_type: ReviewType
    status: ReviewStatus = REVIEW_INITIAL
    reviewer: str | None = Field(default=None, description="Autoridade do revisor")
    executor: str | None = Field(
        default=None,
        description="Autoridade do executor (para verificação de independência)",
    )
    justification: str | None = Field(
        default=None,
        description="Justificativa da decisão (obrigatória para approved/rejected)",
    )
    findings: list[str] = Field(
        default_factory=list, description="Lista de achados ou findings"
    )
    blocking_findings: list[str] = Field(
        default_factory=list,
        description="Achados bloqueadores que impedem aprovação",
    )
    requested_changes: list[str] = Field(
        default_factory=list,
        description="Alterações solicitadas (obrigatório para change_requested)",
    )
    referenced_rules: list[str] = Field(
        default_factory=list,
        description="IDs de regras de negócio referenciadas (para domain review)",
    )
    referenced_requirements: list[str] = Field(
        default_factory=list,
        description="IDs de requisitos referenciados (para functional review)",
    )
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("review_id")
    @classmethod
    def validate_review_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("execution_run_id")
    @classmethod
    def validate_execution_run_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at", "updated_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_reviewer_executor_independence(self) -> Review:
        """Reviewer e executor não podem ser a mesma autoridade."""
        # Independência reviewer/executor
        if (
            self.reviewer is not None
            and self.executor is not None
            and self.reviewer == self.executor
        ):
            raise InvariantViolationError(
                entity="Review",
                invariant="reviewer_must_differ_from_executor",
                details="Reviewer e executor não podem ser a mesma autoridade",
            )

        # Reviewer não pode ser string vazia
        if self.reviewer is not None and not self.reviewer.strip():
            raise InvariantViolationError(
                entity="Review",
                invariant="reviewer_must_not_be_empty",
                details="Reviewer não pode ser string vazia",
            )

        # Estados terminais exigem reviewer identificado
        if self.status in REVIEW_TERMINAL and self.reviewer is None:
            raise InvariantViolationError(
                entity="Review",
                invariant="terminal_requires_reviewer",
                details=f"Estado {self.status.value} requer reviewer identificado",
            )

        # CHANGE_REQUESTED exige reviewer (não apenas terminais)
        if self.status == ReviewStatus.CHANGE_REQUESTED and self.reviewer is None:
            raise InvariantViolationError(
                entity="Review",
                invariant="change_requested_requires_reviewer",
                details="CHANGE_REQUESTED requer reviewer identificado",
            )

        # APPROVED não pode ter bloqueadores
        if self.status == ReviewStatus.APPROVED and self.blocking_findings:
            raise InvariantViolationError(
                entity="Review",
                invariant="approved_requires_no_blockers",
                details=f"Aprovada com {len(self.blocking_findings)} achado(s) bloqueador(es)",
            )

        # APPROVED/REJECTED exigem justificativa não vazia
        if self.status in (ReviewStatus.APPROVED, ReviewStatus.REJECTED) and (
            self.justification is None or not self.justification.strip()
        ):
            raise InvariantViolationError(
                entity="Review",
                invariant="terminal_requires_justification",
                details=f"Estado {self.status.value} requer justificativa não vazia",
            )

        # CHANGE_REQUESTED exige requested_changes não vazio
        if self.status == ReviewStatus.CHANGE_REQUESTED and not self.requested_changes:
            raise InvariantViolationError(
                entity="Review",
                invariant="change_requested_requires_changes",
                details="CHANGE_REQUESTED sem requested_changes",
            )

        return self

    def can_transition_to(self, target: ReviewStatus) -> bool:
        """Verificar se transição é válida."""
        valid = REVIEW_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: ReviewStatus,
        *,
        justification: str | None = None,
        requested_changes: list[str] | None = None,
    ) -> Review:
        """Transicionar para novo estado (retorna nova instância).

        Para APPROVED: fornecer justification.
        Para REJECTED: fornecer justification.
        Para CHANGE_REQUESTED: fornecer requested_changes.
        """
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(REVIEW_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="Review",
                current_state=self.status.value,
                target_state=target.value,
                allowed=[s.value for s in valid],
            )

        updates: dict[str, Any] = {
            "status": target,
            "updated_at": datetime.now(UTC),
            "version": self.version + 1,
        }

        if target == ReviewStatus.APPROVED:
            resolved_just = justification or self.justification
            if resolved_just is None:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="approved_requires_justification",
                    details="Transição para approved requer justificativa",
                )
            if self.reviewer is None:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="approved_requires_reviewer",
                    details="Transição para approved requer reviewer identificado",
                )
            if self.blocking_findings:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="approved_requires_no_blockers",
                    details=f"Transição para approved impedida: {len(self.blocking_findings)} achado(s) bloqueador(es)",
                )
            updates["justification"] = resolved_just

        if target == ReviewStatus.REJECTED:
            resolved_just = justification or self.justification
            if resolved_just is None:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="rejected_requires_justification",
                    details="Transição para rejected requer justificativa",
                )
            if self.reviewer is None:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="rejected_requires_reviewer",
                    details="Transição para rejected requer reviewer identificado",
                )
            updates["justification"] = resolved_just

        if target == ReviewStatus.CHANGE_REQUESTED:
            resolved_changes = requested_changes or self.requested_changes
            if not resolved_changes:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="change_requested_requires_changes",
                    details="Transição para change_requested requer lista de alterações solicitadas",
                )
            if self.reviewer is None:
                raise InvariantViolationError(
                    entity="Review",
                    invariant="change_requested_requires_reviewer",
                    details="Transição para change_requested requer reviewer identificado",
                )
            updates["requested_changes"] = resolved_changes

        # Usar model_validate para garantir revalidação via model_validator
        data = self.model_dump()
        data.update(updates)
        return type(self).model_validate(data)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.status in REVIEW_TERMINAL
