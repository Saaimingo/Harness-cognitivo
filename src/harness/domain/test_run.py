"""
Entidade TestRun do Harness Cognitivo — FI-2B.

TestRun representa uma execução verificável de testes ou validações.
Máquina de estados com 5 estados (planned, executing, passed, failed, error).
Modelo imutável com transições que retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator

from harness.domain.enums import TestRunStatus
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.ids import validate_id_format
from harness.domain.transitions import (
    TESTRUN_INITIAL,
    TESTRUN_TERMINAL,
    TESTRUN_TRANSITIONS,
)


class TestRun(BaseModel):
    """Entidade TestRun — imutável.

    Representa uma execução de testes e suas evidências.
    Distingue falha de teste (failed) de erro de infraestrutura (error).
    """

    test_run_id: str
    execution_run_id: str
    status: TestRunStatus = TESTRUN_INITIAL
    total_tests: int | None = Field(
        default=None, description="Total de testes executados (obrigatório para passed)"
    )
    passed_tests: int | None = Field(default=None, description="Testes que passaram")
    failed_tests: int | None = Field(default=None, description="Testes que falharam")
    failure_details: list[str] = Field(
        default_factory=list,
        description="Detalhes das falhas (obrigatório para failed)",
    )
    error_message: str | None = Field(
        default=None,
        description="Mensagem de erro operacional (obrigatório para error)",
    )
    error_type: str | None = Field(default=None, description="Tipo do erro operacional")
    evidence_hashes: list[str] = Field(
        default_factory=list, description="Hashes das evidências preservadas"
    )
    executor: str | None = Field(
        default=None, description="Autoridade que executou os testes"
    )
    started_at: datetime | None = Field(
        default=None, description="Timestamp de início da execução"
    )
    completed_at: datetime | None = Field(
        default=None, description="Timestamp de encerramento"
    )
    version: int = 1
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("test_run_id")
    @classmethod
    def validate_test_run_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("execution_run_id")
    @classmethod
    def validate_execution_run_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("created_at", "updated_at", "started_at", "completed_at")
    @classmethod
    def validate_temporal_timezone(cls, v: datetime | None) -> datetime | None:
        if v is not None and v.tzinfo is None:
            raise ValueError("Campo temporal requer timezone")
        return v

    @model_validator(mode="after")
    def validate_state_consistency(self) -> TestRun:
        """Impedir estados inválidos em construção direta e desserialização."""
        s = self.status

        # --- Contagens não negativas ---
        for field_name in ("total_tests", "passed_tests", "failed_tests"):
            val = getattr(self, field_name)
            if val is not None and val < 0:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="non_negative_counts",
                    details=f"{field_name}={val} é negativo",
                )

        # --- Coerência quando as três contagens são conhecidas ---
        if (
            self.total_tests is not None
            and self.passed_tests is not None
            and self.failed_tests is not None
            and self.passed_tests + self.failed_tests != self.total_tests
        ):
            raise InvariantViolationError(
                entity="TestRun",
                invariant="counts_coherence",
                details=f"passed({self.passed_tests}) + failed({self.failed_tests}) != total({self.total_tests})",
            )

        # --- EXECUTING exige started_at ---
        if s == TestRunStatus.EXECUTING and self.started_at is None:
            raise InvariantViolationError(
                entity="TestRun",
                invariant="executing_requires_started_at",
                details="EXECUTING exige started_at",
            )

        # --- Terminais exigem started_at e completed_at ---
        if s in TESTRUN_TERMINAL:
            if self.started_at is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="terminal_requires_started_at",
                    details=f"Estado terminal {s.value} requer started_at",
                )
            if self.completed_at is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="terminal_requires_completed_at",
                    details=f"Estado terminal {s.value} requer completed_at",
                )

        # --- PASSED: rigor total ---
        if s == TestRunStatus.PASSED:
            if self.total_tests is None or self.total_tests < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_total_tests",
                    details="PASSED exige total_tests >= 1",
                )
            if self.passed_tests is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_passed_tests",
                    details="PASSED exige passed_tests obrigatório",
                )
            if self.failed_tests is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_failed_tests",
                    details="PASSED exige failed_tests obrigatório",
                )
            if self.failed_tests != 0:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_zero_failures",
                    details=f"PASSED com failed_tests={self.failed_tests}",
                )
            if self.passed_tests != self.total_tests:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_tests_must_match_total",
                    details=f"passed_tests={self.passed_tests} != total_tests={self.total_tests}",
                )
            if not self.evidence_hashes:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_evidence",
                    details="PASSED exige evidence_hashes não vazio",
                )
            # PASSED não pode ter campos de FAILED/ERROR
            if self.failure_details:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_no_failure_details",
                    details="PASSED não pode ter failure_details",
                )
            if self.error_message or self.error_type:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_no_error_fields",
                    details="PASSED não pode ter error_message ou error_type",
                )

        # --- PLANNED: não pode ter dados de execução/resultados ---
        if s == TestRunStatus.PLANNED:
            if self.started_at or self.completed_at:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="planned_no_execution_timestamps",
                    details="PLANNED não pode ter started_at ou completed_at",
                )
            if any(
                value is not None
                for value in (self.total_tests, self.passed_tests, self.failed_tests)
            ):
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="planned_no_test_counts",
                    details="PLANNED não pode ter contagens de resultado",
                )
            if (
                self.failure_details
                or self.error_message
                or self.error_type
                or self.evidence_hashes
            ):
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="planned_no_result_fields",
                    details="PLANNED não pode ter dados conclusivos de execução",
                )

        # --- EXECUTING: deve ter started_at, não pode ter completed_at nem resultados ---
        if s == TestRunStatus.EXECUTING:
            if self.started_at is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="executing_requires_started_at",
                    details="EXECUTING exige started_at",
                )
            if self.completed_at is not None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="executing_no_completed_at",
                    details="EXECUTING não pode ter completed_at",
                )
            if any(
                value is not None
                for value in (self.total_tests, self.passed_tests, self.failed_tests)
            ):
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="executing_no_final_counts",
                    details="EXECUTING não pode ter contagens finais",
                )
            if (
                self.failure_details
                or self.error_message
                or self.error_type
                or self.evidence_hashes
            ):
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="executing_no_result_fields",
                    details="EXECUTING não pode ter dados conclusivos de resultado",
                )

        # --- FAILED: rigor total ---
        if s == TestRunStatus.FAILED:
            if self.total_tests is None or self.total_tests < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_total_tests",
                    details="FAILED exige total_tests >= 1",
                )
            if self.passed_tests is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_passed_tests",
                    details="FAILED exige passed_tests obrigatório",
                )
            if self.failed_tests is None or self.failed_tests < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_nonzero_failures",
                    details="FAILED exige failed_tests >= 1",
                )
            if self.passed_tests + self.failed_tests != self.total_tests:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="counts_coherence",
                    details=(
                        f"passed({self.passed_tests}) + failed({self.failed_tests}) "
                        f"!= total({self.total_tests})"
                    ),
                )
            if not self.failure_details:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_failure_details",
                    details="FAILED exige failure_details não vazio",
                )
            if self.error_message or self.error_type:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_no_error_fields",
                    details="FAILED não pode ter error_message ou error_type",
                )

        # --- ERROR: rigor ---
        if s == TestRunStatus.ERROR:
            if not self.error_message or not self.error_message.strip():
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="error_requires_error_message",
                    details="ERROR exige error_message não vazio",
                )
            # ERROR não pode ter dados conclusivos de teste
            if (
                self.total_tests is not None
                or self.passed_tests is not None
                or self.failed_tests is not None
            ):
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="error_no_test_counts",
                    details="ERROR não pode ter total_tests, passed_tests ou failed_tests",
                )
            if self.failure_details:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="error_no_failure_details",
                    details="ERROR não pode ter failure_details",
                )

        return self

    def can_transition_to(self, target: TestRunStatus) -> bool:
        """Verificar se transição é válida."""
        valid = TESTRUN_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: TestRunStatus,
        *,
        total_tests: int | None = None,
        passed_tests: int | None = None,
        failed_tests: int | None = None,
        failure_details: list[str] | None = None,
        error_message: str | None = None,
        error_type: str | None = None,
        evidence_hashes: list[str] | None = None,
    ) -> TestRun:
        """Transicionar para novo estado (retorna nova instância).

        Para PASSED: fornecer total_tests.
        Para FAILED: fornecer total_tests, passed_tests, failed_tests, failure_details.
        Para ERROR: fornecer error_message.
        """
        if self.status == target:
            return self  # idempotente

        if not self.can_transition_to(target):
            valid = list(TESTRUN_TRANSITIONS.get(self.status, frozenset()))
            raise InvalidTransitionError(
                entity="TestRun",
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

        if target == TestRunStatus.EXECUTING and self.started_at is None:
            updates["started_at"] = now

        if target in TESTRUN_TERMINAL:
            updates["completed_at"] = now
            if self.started_at is None:
                updates["started_at"] = now

        if target == TestRunStatus.PASSED:
            resolved_tt = total_tests if total_tests is not None else self.total_tests
            resolved_eh = (
                evidence_hashes if evidence_hashes is not None else self.evidence_hashes
            )
            if resolved_tt is None or resolved_tt < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_total_tests",
                    details="Transição para passed requer total_tests >= 1",
                )
            if not resolved_eh:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_evidence",
                    details="Transição para passed requer evidence_hashes",
                )
            updates["total_tests"] = resolved_tt
            updates["failed_tests"] = 0
            updates["passed_tests"] = resolved_tt
            updates["evidence_hashes"] = resolved_eh

        if target == TestRunStatus.FAILED:
            resolved_tt = total_tests if total_tests is not None else self.total_tests
            resolved_pt = (
                passed_tests if passed_tests is not None else self.passed_tests
            )
            resolved_ft = (
                failed_tests if failed_tests is not None else self.failed_tests
            )
            resolved_fd = failure_details or self.failure_details
            if resolved_tt is None or resolved_tt < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_total_tests",
                    details="Transição para failed requer total_tests >= 1",
                )
            if resolved_pt is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_passed_tests",
                    details="Transição para failed requer passed_tests",
                )
            if resolved_ft is None or resolved_ft < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_nonzero_failures",
                    details="Transição para failed requer failed_tests >= 1",
                )
            if resolved_pt + resolved_ft != resolved_tt:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="counts_coherence",
                    details="Transição para failed requer contagens coerentes",
                )
            if not resolved_fd:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_failure_details",
                    details="Transição para failed requer failure_details",
                )
            updates["total_tests"] = resolved_tt
            updates["passed_tests"] = resolved_pt
            updates["failed_tests"] = resolved_ft
            updates["failure_details"] = resolved_fd

        if target == TestRunStatus.ERROR:
            resolved_em = error_message or self.error_message
            if resolved_em is None:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="error_requires_error_message",
                    details="Transição para error requer error_message",
                )
            updates["error_message"] = resolved_em
            if error_type is not None:
                updates["error_type"] = error_type

        # Usar model_validate para garantir revalidação via model_validator
        data = self.model_dump()
        data.update(updates)
        return type(self).model_validate(data)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.status in TESTRUN_TERMINAL
