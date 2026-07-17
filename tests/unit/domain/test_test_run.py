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
) -> DomainTestRun:
    """Helper para criar DomainTestRun com estado específico."""
    kwargs: dict = {
        "test_run_id": "tst_test123",
        "execution_run_id": "exr_test456",
        "status": status,
    }
    if total_tests is not None:
        kwargs["total_tests"] = total_tests
    if failure_details is not None:
        kwargs["failure_details"] = failure_details
    if error_message is not None:
        kwargs["error_message"] = error_message
    if evidence_hashes is not None:
        kwargs["evidence_hashes"] = evidence_hashes
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
        new_tr = tr.transition_to(DomainTestRunStatus.PASSED, total_tests=10)
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
    new_tr = tr.transition_to(DomainTestRunStatus.PASSED, total_tests=10)
    assert new_tr.completed_at is not None


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(TESTRUN_TERMINAL))
def test_test_run_terminal_states(terminal_status: DomainTestRunStatus):
    """DomainTestRuns em estados terminais são marcados como is_terminal."""
    kwargs: dict = {"status": terminal_status}
    if terminal_status == DomainTestRunStatus.PASSED:
        kwargs["total_tests"] = 10
    if terminal_status == DomainTestRunStatus.FAILED:
        kwargs["failure_details"] = ["test_x failed"]
    if terminal_status == DomainTestRunStatus.ERROR:
        kwargs["error_message"] = "Timeout"
    tr = make_test_run(**kwargs)
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
    tr = make_test_run(status=DomainTestRunStatus.EXECUTING, total_tests=10)
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


# =============================================================================
# ESTADOS TERMINAIS BLOQUEIAM TRANSMISSÕES
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(TESTRUN_TERMINAL))
def test_test_run_terminal_blocks_further_transitions(
    terminal_status: DomainTestRunStatus,
):
    """DomainTestRun em estado terminal bloqueia transições."""
    kwargs: dict = {"status": terminal_status}
    if terminal_status == DomainTestRunStatus.PASSED:
        kwargs["total_tests"] = 10
    if terminal_status == DomainTestRunStatus.FAILED:
        kwargs["failure_details"] = ["test_x failed"]
    if terminal_status == DomainTestRunStatus.ERROR:
        kwargs["error_message"] = "Timeout"
    tr = make_test_run(**kwargs)
    with pytest.raises(InvalidTransitionError):
        tr.transition_to(DomainTestRunStatus.EXECUTING)
