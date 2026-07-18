"""
Testes completos para a entidade TestRun — FI-2B.
Cobre: construção, transições, passed, failed, error, distinção entre
failed e error, timestamps, resultados, imutabilidade, idempotência, serialização.
"""

from datetime import UTC, datetime

import pytest

from harness.domain.enums import TestRunStatus as DomainTestRunStatus
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.test_run import TestRun as DomainTestRun
from harness.domain.transitions import TESTRUN_TERMINAL


def make_test_run(
    status: DomainTestRunStatus = DomainTestRunStatus.PLANNED,
    total_tests: int | None = None,
    failure_details: list[str] | None = None,
    error_message: str | None = None,
    evidence_hashes: list[str] | None = None,
    passed_tests: int | None = None,
    failed_tests: int | None = None,
) -> DomainTestRun:
    """Helper para criar DomainTestRun com estado específico.

    PASSED exige total_tests >= 1, passed_tests, failed_tests=0, evidence, timestamps.
    FAILED exige failure_details, started_at, completed_at.
    ERROR exige error_message, started_at, completed_at.
    EXECUTING exige started_at.
    """
    now = datetime.now(UTC)
    kwargs: dict = {
        "test_run_id": "tst_test123",
        "execution_run_id": "exr_test456",
        "status": status,
    }
    # EXECUTING e terminais exigem started_at
    if status == DomainTestRunStatus.EXECUTING or status in TESTRUN_TERMINAL:
        kwargs["started_at"] = now
    # Terminais exigem completed_at
    if status in TESTRUN_TERMINAL:
        kwargs["completed_at"] = now
    if total_tests is not None:
        kwargs["total_tests"] = total_tests
    if passed_tests is not None:
        kwargs["passed_tests"] = passed_tests
    if failed_tests is not None:
        kwargs["failed_tests"] = failed_tests
    if failure_details is not None:
        kwargs["failure_details"] = failure_details
    if error_message is not None:
        kwargs["error_message"] = error_message
    if evidence_hashes is not None:
        kwargs["evidence_hashes"] = evidence_hashes
    if status == DomainTestRunStatus.PASSED:
        tt = total_tests or 10
        kwargs["total_tests"] = tt
        kwargs["passed_tests"] = passed_tests if passed_tests is not None else tt
        kwargs["failed_tests"] = failed_tests if failed_tests is not None else 0
        kwargs["evidence_hashes"] = evidence_hashes or ["sha256_default"]
    if status == DomainTestRunStatus.FAILED:
        kwargs["failure_details"] = failure_details or ["Falha padrão"]
    if status == DomainTestRunStatus.ERROR:
        kwargs["error_message"] = error_message or "Erro padrão"
    return DomainTestRun(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestTestRunConstruction:
    def test_creation_minimal(self):
        """DomainTestRun deve ser criado com campos obrigatórios."""
        tr = DomainTestRun(
            test_run_id="tst_test123",
            execution_run_id="exr_test456",
        )
        assert tr.test_run_id == "tst_test123"
        assert tr.execution_run_id == "exr_test456"
        assert tr.status == DomainTestRunStatus.PLANNED
        assert tr.total_tests is None
        assert tr.failure_details == []
        assert tr.error_message is None

    def test_creation_with_all_fields(self):
        """DomainTestRun deve aceitar todos os campos."""
        tr = DomainTestRun(
            test_run_id="tst_test123",
            execution_run_id="exr_test456",
            total_tests=10,
            passed_tests=10,
            evidence_hashes=["abc123"],
            executor="freebuff",
        )
        assert tr.total_tests == 10
        assert tr.passed_tests == 10
        assert len(tr.evidence_hashes) == 1

    def test_invalid_test_run_id_rejected(self):
        """test_run_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            DomainTestRun(
                test_run_id="invalid-id",
                execution_run_id="exr_test456",
            )

    def test_invalid_execution_run_id_rejected(self):
        """execution_run_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="invalid-id",
            )


# =============================================================================
# VALIDAÇÕES
# =============================================================================


class TestTestRunValidations:
    def test_rejects_naive_datetime(self):
        """DomainTestRun rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                created_at=datetime(2026, 1, 1),
            )

    def test_accepts_aware_datetime(self):
        """DomainTestRun aceita datetime com timezone."""
        tr = DomainTestRun(
            test_run_id="tst_test123",
            execution_run_id="exr_test456",
            created_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        assert tr.created_at.tzinfo is not None


# =============================================================================
# TRANSIÇÕES PERMITIDAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (DomainTestRunStatus.PLANNED, DomainTestRunStatus.EXECUTING),
        (DomainTestRunStatus.EXECUTING, DomainTestRunStatus.PASSED),
        (DomainTestRunStatus.EXECUTING, DomainTestRunStatus.FAILED),
        (DomainTestRunStatus.EXECUTING, DomainTestRunStatus.ERROR),
    ],
)
def test_test_run_valid_transitions(
    current: DomainTestRunStatus, target: DomainTestRunStatus
):
    """Transições válidas devem ser aceitas."""
    tr = make_test_run(status=current)
    transition_kwargs: dict = {}
    if target == DomainTestRunStatus.PASSED:
        transition_kwargs["total_tests"] = 10
        transition_kwargs["evidence_hashes"] = ["sha256_test"]
    if target == DomainTestRunStatus.FAILED:
        transition_kwargs["failure_details"] = ["test_foo failed"]
    if target == DomainTestRunStatus.ERROR:
        transition_kwargs["error_message"] = "Timeout"
    new_tr = tr.transition_to(target, **transition_kwargs)
    assert new_tr.status == target


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (DomainTestRunStatus.PLANNED, DomainTestRunStatus.PASSED),
        (DomainTestRunStatus.PLANNED, DomainTestRunStatus.FAILED),
        (DomainTestRunStatus.PLANNED, DomainTestRunStatus.ERROR),
        (DomainTestRunStatus.PASSED, DomainTestRunStatus.EXECUTING),
        (DomainTestRunStatus.FAILED, DomainTestRunStatus.EXECUTING),
        (DomainTestRunStatus.ERROR, DomainTestRunStatus.EXECUTING),
    ],
)
def test_test_run_invalid_transitions_rejected(
    current: DomainTestRunStatus, target: DomainTestRunStatus
):
    """Transições inválidas devem ser rejeitadas."""
    tr = make_test_run(status=current)
    with pytest.raises(InvalidTransitionError):
        tr.transition_to(target)


# =============================================================================
# PASSED
# =============================================================================


class TestTestRunPassed:
    def test_passed_requires_total_tests(self):
        """Transição para passed requer total_tests."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        with pytest.raises(InvariantViolationError, match="total_tests"):
            tr.transition_to(DomainTestRunStatus.PASSED)

    def test_passed_with_total_tests(self):
        """Transição para passed com total_tests funciona."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(
            DomainTestRunStatus.PASSED,
            total_tests=10,
            evidence_hashes=["sha256_test"],
        )
        assert new_tr.status == DomainTestRunStatus.PASSED
        assert new_tr.total_tests == 10


# =============================================================================
# FAILED
# =============================================================================


class TestTestRunFailed:
    def test_failed_requires_failure_details(self):
        """Transição para failed requer failure_details."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        with pytest.raises(InvariantViolationError, match="failure_details"):
            tr.transition_to(DomainTestRunStatus.FAILED)

    def test_failed_with_failure_details(self):
        """Transição para failed com failure_details funciona."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(
            DomainTestRunStatus.FAILED,
            failure_details=["test_auth failed", "test_login failed"],
        )
        assert new_tr.status == DomainTestRunStatus.FAILED
        assert len(new_tr.failure_details) == 2


# =============================================================================
# ERROR
# =============================================================================


class TestTestRunError:
    def test_error_requires_error_message(self):
        """Transição para error requer error_message."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        with pytest.raises(InvariantViolationError, match="error_message"):
            tr.transition_to(DomainTestRunStatus.ERROR)

    def test_error_with_error_message(self):
        """Transição para error com error_message funciona."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(
            DomainTestRunStatus.ERROR,
            error_message="Connection timeout",
            error_type="TimeoutError",
        )
        assert new_tr.status == DomainTestRunStatus.ERROR
        assert new_tr.error_message == "Connection timeout"
        assert new_tr.error_type == "TimeoutError"


# =============================================================================
# DISTINÇÃO FAILED VS ERROR
# =============================================================================


class TestTestRunFailureVsError:
    def test_failed_and_error_are_distinct(self):
        """failed e error são estados distintos com semânticas diferentes."""
        failed_tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        error_tr = make_test_run(
            status=DomainTestRunStatus.EXECUTING,
        )
        failed_result = failed_tr.transition_to(
            DomainTestRunStatus.FAILED, failure_details=["test_x failed"]
        )
        error_result = error_tr.transition_to(
            DomainTestRunStatus.ERROR, error_message="Timeout"
        )
        assert failed_result.status == DomainTestRunStatus.FAILED
        assert error_result.status == DomainTestRunStatus.ERROR
        assert failed_result.status != error_result.status


# =============================================================================
# TIMESTAMP DE INÍCIO
# =============================================================================


def test_started_at_set_on_executing():
    """started_at deve ser preenchido ao transicionar para executing."""
    tr = make_test_run(status=DomainTestRunStatus.PLANNED)
    new_tr = tr.transition_to(DomainTestRunStatus.EXECUTING)
    assert new_tr.started_at is not None


# =============================================================================
# TIMESTAMP DE ENCERRAMENTO
# =============================================================================


def test_completed_at_set_on_terminal():
    """completed_at deve ser preenchido ao transicionar para estado final."""
    tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
    new_tr = tr.transition_to(
        DomainTestRunStatus.PASSED,
        total_tests=10,
        evidence_hashes=["sha256_test"],
    )
    assert new_tr.completed_at is not None


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(TESTRUN_TERMINAL))
def test_test_run_terminal_states(terminal_status: DomainTestRunStatus):
    """DomainTestRuns em estados terminais são marcados como is_terminal."""
    tr = make_test_run(status=terminal_status)
    assert tr.is_terminal


def test_test_run_non_terminal_states():
    """DomainTestRuns em estados não-terminais não são marcados como is_terminal."""
    for status in DomainTestRunStatus:
        if status not in TESTRUN_TERMINAL:
            tr = make_test_run(status=status)
            assert not tr.is_terminal


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================


def test_test_run_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    tr = make_test_run(status=DomainTestRunStatus.PLANNED)
    result = tr.transition_to(DomainTestRunStatus.PLANNED)
    assert result is tr


# =============================================================================
# IMUTABILIDADE
# =============================================================================


def test_test_run_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    tr = make_test_run(status=DomainTestRunStatus.PLANNED)
    original_status = tr.status
    _ = tr.transition_to(DomainTestRunStatus.EXECUTING)
    assert tr.status == original_status


def test_test_run_version_increments():
    """Versão incrementa a cada transição."""
    tr = make_test_run(status=DomainTestRunStatus.PLANNED)
    new_tr = tr.transition_to(DomainTestRunStatus.EXECUTING)
    assert new_tr.version == tr.version + 1


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


def test_test_run_json_roundtrip():
    """DomainTestRun deve serializar e desserializar corretamente."""
    tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
    json_str = tr.model_dump_json()
    tr2 = DomainTestRun.model_validate_json(json_str)
    assert tr.test_run_id == tr2.test_run_id
    assert tr.status == tr2.status
    assert tr.total_tests == tr2.total_tests


# =============================================================================
# EVIDÊNCIAS
# =============================================================================


class TestTestRunEvidence:
    def test_evidence_hashes_preserved(self):
        """Hashes de evidências devem ser preservados."""
        tr = make_test_run(
            status=DomainTestRunStatus.PASSED,
            total_tests=10,
            evidence_hashes=["sha256_abc123", "sha256_def456"],
        )
        assert len(tr.evidence_hashes) == 2
        assert "sha256_abc123" in tr.evidence_hashes

    def test_passed_requires_evidence(self):
        """PASSED sem evidence_hashes deve ser rejeitado."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        with pytest.raises(InvariantViolationError, match="evidence"):
            tr.transition_to(DomainTestRunStatus.PASSED, total_tests=10)


# =============================================================================
# ESTADOS TERMINAIS BLOQUEIAM TRANSMISSÕES
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(TESTRUN_TERMINAL))
def test_test_run_terminal_blocks_further_transitions(
    terminal_status: DomainTestRunStatus,
):
    """DomainTestRun em estado terminal bloqueia transições."""
    tr = make_test_run(status=terminal_status)
    with pytest.raises(InvalidTransitionError):
        tr.transition_to(DomainTestRunStatus.EXECUTING)


# =============================================================================
# TESTES ADVERSARIAIS — Construção direta inválida
# =============================================================================


class TestTestRunAdversarialConstruction:
    """Testes que tentam construir TestRun em estados inválidos diretamente."""

    def test_passed_without_total_tests(self):
        """PASSED sem total_tests deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="passed_requires_total_tests"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_passed_without_passed_tests(self):
        """PASSED sem passed_tests deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="passed_requires_passed_tests"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                failed_tests=0,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_passed_without_failed_tests(self):
        """PASSED sem failed_tests deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="passed_requires_failed_tests"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_passed_with_failure_details(self):
        """PASSED com failure_details deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(InvariantViolationError, match="passed_no_failure_details"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
                failure_details=["algo"],
            )

    def test_passed_with_error_message(self):
        """PASSED com error_message deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(InvariantViolationError, match="passed_no_error_fields"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
                error_message="erro",
            )

    def test_passed_without_evidence(self):
        """PASSED sem evidence_hashes deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(InvariantViolationError, match="passed_requires_evidence"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                started_at=now,
                completed_at=now,
            )

    def test_passed_counts_mismatch(self):
        """PASSED com passed_tests != total_tests deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError,
            match="passed_tests_must_match_total|counts_coherence",
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=8,
                failed_tests=0,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_passed_with_nonzero_failures(self):
        """PASSED com failed_tests != 0 deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError,
            match="passed_requires_zero_failures|counts_coherence",
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=2,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_failed_without_failure_details(self):
        """FAILED sem failure_details deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="failed_requires_failure_details"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.FAILED,
                started_at=now,
                completed_at=now,
            )

    def test_failed_with_error_message(self):
        """FAILED com error_message deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(InvariantViolationError, match="failed_no_error_fields"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.FAILED,
                failure_details=["falha"],
                error_message="erro",
                started_at=now,
                completed_at=now,
            )

    def test_error_without_error_message(self):
        """ERROR sem error_message deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="error_requires_error_message"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.ERROR,
                started_at=now,
                completed_at=now,
            )

    def test_error_with_empty_error_message(self):
        """ERROR com error_message vazio deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="error_requires_error_message"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.ERROR,
                error_message="  ",
                started_at=now,
                completed_at=now,
            )

    def test_error_with_total_tests(self):
        """ERROR com total_tests deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError,
            match="error_no_test_counts|error_no_failure_details",
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.ERROR,
                error_message="erro",
                total_tests=10,
                started_at=now,
                completed_at=now,
            )

    def test_error_with_failure_details(self):
        """ERROR com failure_details deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError,
            match="error_no_failure_details|error_no_test_counts",
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.ERROR,
                error_message="erro",
                failure_details=["falha"],
                started_at=now,
                completed_at=now,
            )

    def test_executing_without_started_at(self):
        """EXECUTING sem started_at deve falhar."""
        with pytest.raises(
            InvariantViolationError, match="executing_requires_started_at"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.EXECUTING,
            )

    def test_terminal_without_started_at(self):
        """Terminal sem started_at deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="terminal_requires_started_at"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )

    def test_terminal_without_completed_at(self):
        """Terminal sem completed_at deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(
            InvariantViolationError, match="terminal_requires_completed_at"
        ):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.FAILED,
                failure_details=["falha"],
                started_at=now,
            )

    def test_created_at_naive(self):
        """created_at sem timezone deve falhar."""
        with pytest.raises(ValueError, match="timezone"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                created_at=datetime(2026, 1, 1),
            )

    def test_started_at_naive(self):
        """started_at sem timezone deve falhar."""
        with pytest.raises(ValueError, match="timezone"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.EXECUTING,
                started_at=datetime(2026, 1, 1),
            )

    def test_completed_at_naive(self):
        """completed_at sem timezone deve falhar."""
        with pytest.raises(ValueError, match="timezone"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=10,
                failed_tests=0,
                started_at=datetime(2026, 1, 1, tzinfo=UTC),
                completed_at=datetime(2026, 1, 2),
                evidence_hashes=["sha256_abc"],
            )

    def test_updated_at_naive(self):
        """updated_at sem timezone deve falhar."""
        with pytest.raises(ValueError, match="timezone"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                updated_at=datetime(2026, 1, 1),
            )

    def test_negative_total_tests(self):
        """total_tests negativo deve falhar."""
        with pytest.raises(InvariantViolationError, match="non_negative_counts"):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                total_tests=-1,
            )

    def test_counts_incoherent(self):
        """passed + failed != total deve falhar."""
        now = datetime.now(UTC)
        with pytest.raises(InvariantViolationError):
            DomainTestRun(
                test_run_id="tst_test123",
                execution_run_id="exr_test456",
                status=DomainTestRunStatus.PASSED,
                total_tests=10,
                passed_tests=8,
                failed_tests=2,
                started_at=now,
                completed_at=now,
                evidence_hashes=["sha256_abc"],
            )


class TestTestRunAdversarialModelValidate:
    """Testes via model_validate e model_validate_json."""

    def test_model_validate_passed_without_passed_tests(self):
        """model_validate com PASSED sem passed_tests deve falhar."""
        now = datetime.now(UTC)
        data = {
            "test_run_id": "tst_test123",
            "execution_run_id": "exr_test456",
            "status": "passed",
            "total_tests": 10,
            "failed_tests": 0,
            "started_at": now.isoformat(),
            "completed_at": now.isoformat(),
            "evidence_hashes": ["sha256_abc"],
        }
        with pytest.raises(InvariantViolationError):
            DomainTestRun.model_validate(data)

    def test_model_validate_json_passed_without_failed_tests(self):
        """model_validate_json com PASSED sem failed_tests deve falhar."""
        import json

        now = datetime.now(UTC)
        data = {
            "test_run_id": "tst_test123",
            "execution_run_id": "exr_test456",
            "status": "passed",
            "total_tests": 10,
            "passed_tests": 10,
            "started_at": now.isoformat(),
            "completed_at": now.isoformat(),
            "evidence_hashes": ["sha256_abc"],
        }
        with pytest.raises(InvariantViolationError):
            DomainTestRun.model_validate_json(json.dumps(data))

    def test_model_validate_executing_without_started_at(self):
        """model_validate com EXECUTING sem started_at deve falhar."""
        data = {
            "test_run_id": "tst_test123",
            "execution_run_id": "exr_test456",
            "status": "executing",
        }
        with pytest.raises(InvariantViolationError):
            DomainTestRun.model_validate(data)

    def test_model_validate_error_with_failure_details(self):
        """model_validate com ERROR + failure_details deve falhar."""
        now = datetime.now(UTC)
        data = {
            "test_run_id": "tst_test123",
            "execution_run_id": "exr_test456",
            "status": "error",
            "error_message": "timeout",
            "failure_details": ["falha"],
            "started_at": now.isoformat(),
            "completed_at": now.isoformat(),
        }
        with pytest.raises(InvariantViolationError):
            DomainTestRun.model_validate(data)

    def test_model_validate_failed_with_error_message(self):
        """model_validate com FAILED + error_message deve falhar."""
        now = datetime.now(UTC)
        data = {
            "test_run_id": "tst_test123",
            "execution_run_id": "exr_test456",
            "status": "failed",
            "failure_details": ["falha"],
            "error_message": "erro",
            "started_at": now.isoformat(),
            "completed_at": now.isoformat(),
        }
        with pytest.raises(InvariantViolationError):
            DomainTestRun.model_validate(data)

    def test_roundtrip_valid_passed(self):
        """Roundtrip de PASSED válido."""
        tr = make_test_run(status=DomainTestRunStatus.PASSED)
        json_str = tr.model_dump_json()
        tr2 = DomainTestRun.model_validate_json(json_str)
        assert tr2.status == DomainTestRunStatus.PASSED
        assert tr2.total_tests is not None
        assert tr2.passed_tests is not None
        assert tr2.failed_tests is not None
        assert tr2.evidence_hashes
        assert tr2.started_at is not None
        assert tr2.completed_at is not None

    def test_roundtrip_valid_failed(self):
        """Roundtrip de FAILED válido."""
        tr = make_test_run(status=DomainTestRunStatus.FAILED)
        json_str = tr.model_dump_json()
        tr2 = DomainTestRun.model_validate_json(json_str)
        assert tr2.status == DomainTestRunStatus.FAILED
        assert tr2.failure_details
        assert tr2.error_message is None

    def test_roundtrip_valid_error(self):
        """Roundtrip de ERROR válido."""
        tr = make_test_run(status=DomainTestRunStatus.ERROR)
        json_str = tr.model_dump_json()
        tr2 = DomainTestRun.model_validate_json(json_str)
        assert tr2.status == DomainTestRunStatus.ERROR
        assert tr2.error_message
        assert tr2.total_tests is None
        assert tr2.failure_details == []


class TestTestRunAdversarialTransition:
    """Testes de transições que produzem objetos normativamente válidos."""

    def test_transition_to_executing_produces_valid_object(self):
        """Transição para EXECUTING deve produzir objeto válido via model_validate."""
        tr = make_test_run(status=DomainTestRunStatus.PLANNED)
        new_tr = tr.transition_to(DomainTestRunStatus.EXECUTING)
        data = new_tr.model_dump()
        revalidated = DomainTestRun.model_validate(data)
        assert revalidated.status == DomainTestRunStatus.EXECUTING
        assert revalidated.started_at is not None

    def test_transition_to_passed_produces_valid_object(self):
        """Transição para PASSED deve produzir objeto válido via model_validate."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(
            DomainTestRunStatus.PASSED,
            total_tests=10,
            evidence_hashes=["sha256_test"],
        )
        data = new_tr.model_dump()
        revalidated = DomainTestRun.model_validate(data)
        assert revalidated.status == DomainTestRunStatus.PASSED
        assert revalidated.total_tests == 10
        assert revalidated.passed_tests == 10
        assert revalidated.failed_tests == 0
        assert revalidated.evidence_hashes == ["sha256_test"]
        assert revalidated.started_at is not None
        assert revalidated.completed_at is not None

    def test_transition_to_failed_produces_valid_object(self):
        """Transição para FAILED deve produzir objeto válido via model_validate."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(
            DomainTestRunStatus.FAILED, failure_details=["test_x failed"]
        )
        data = new_tr.model_dump()
        revalidated = DomainTestRun.model_validate(data)
        assert revalidated.status == DomainTestRunStatus.FAILED
        assert revalidated.failure_details == ["test_x failed"]
        assert revalidated.error_message is None
        assert revalidated.error_type is None

    def test_transition_to_error_produces_valid_object(self):
        """Transição para ERROR deve produzir objeto válido via model_validate."""
        tr = make_test_run(status=DomainTestRunStatus.EXECUTING)
        new_tr = tr.transition_to(DomainTestRunStatus.ERROR, error_message="Timeout")
        data = new_tr.model_dump()
        revalidated = DomainTestRun.model_validate(data)
        assert revalidated.status == DomainTestRunStatus.ERROR
        assert revalidated.error_message == "Timeout"
        assert revalidated.total_tests is None
        assert revalidated.failure_details == []
