"""
Entidade TestRun do Harness Cognitivo — FI-2B.

TestRun representa uma execução verificável de testes ou validações.
Máquina de estados com 5 estados (planned, executing, passed, failed, error).
Modelo imutável com transições que retornam nova instância.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

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

    @field_validator("created_at")
    @classmethod
    def validate_created_at_timezone(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            raise ValueError("created_at requer timezone")
        return v

    def can_transition_to(self, target: TestRunStatus) -> bool:
        """Verificar se transição é válida."""
        valid = TESTRUN_TRANSITIONS.get(self.status, frozenset())
        return target in valid

    def transition_to(
        self,
        target: TestRunStatus,
        *,
        total_tests: int | None = None,
        failure_details: list[str] | None = None,
        error_message: str | None = None,
        error_type: str | None = None,
    ) -> TestRun:
        """Transicionar para novo estado (retorna nova instância).

        Para PASSED: fornecer total_tests.
        Para FAILED: fornecer failure_details.
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
            resolved_tt = total_tests or self.total_tests
            if resolved_tt is None or resolved_tt < 1:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="passed_requires_total_tests",
                    details="Transição para passed requer total_tests >= 1",
                )
            updates["total_tests"] = resolved_tt

        if target == TestRunStatus.FAILED:
            resolved_fd = failure_details or self.failure_details
            if not resolved_fd:
                raise InvariantViolationError(
                    entity="TestRun",
                    invariant="failed_requires_failure_details",
                    details="Transição para failed requer lista de failure_details",
                )
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

        return self.model_copy(update=updates)

    @property
    def is_terminal(self) -> bool:
        """Verificar se está em estado terminal."""
        return self.status in TESTRUN_TERMINAL
