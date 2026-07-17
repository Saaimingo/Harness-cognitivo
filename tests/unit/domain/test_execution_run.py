"""
Testes completos para a entidade ExecutionRun — FI-2B.
Cobre: construção, validações, transições, estados terminais, timestamps,
número de tentativa, WorkOrder ID, falha, abandono, conclusão,
imutabilidade, idempotência, serialização.
"""

from datetime import UTC, datetime

import pytest

from harness.domain.enums import ExecutionRunStatus
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.execution_run import ExecutionRun
from harness.domain.transitions import EXECUTIONRUN_TERMINAL


def make_execution_run(
    status: ExecutionRunStatus = ExecutionRunStatus.INITIATED,
    changeset_id: str | None = None,
    failure_reason: str | None = None,
    abandon_justification: str | None = None,
    executor: str | None = None,
) -> ExecutionRun:
    """Helper para criar ExecutionRun com estado específico.

    Estados não-initiated exigem started_at; terminais exigem completed_at.
    """
    now = datetime.now(UTC)
    kwargs: dict = {
        "execution_run_id": "exr_test123",
        "work_order_id": "wo_test456",
        "attempt_number": 1,
        "status": status,
    }
    if status != ExecutionRunStatus.INITIATED:
        kwargs["started_at"] = now
    if status in EXECUTIONRUN_TERMINAL:
        kwargs["completed_at"] = now
    if status == ExecutionRunStatus.COMPLETED:
        kwargs["changeset_id"] = changeset_id or "chs_default"
    if status == ExecutionRunStatus.FAILED:
        kwargs["failure_reason"] = failure_reason or "Falha padrão"
    if status == ExecutionRunStatus.ABANDONED:
        kwargs["abandon_justification"] = (
            abandon_justification or "Justificativa padrão"
        )
    if executor is not None:
        kwargs["executor"] = executor
    return ExecutionRun(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestExecutionRunConstruction:
    def test_creation_minimal(self):
        """ExecutionRun deve ser criado com campos obrigatórios."""
        run = ExecutionRun(
            execution_run_id="exr_test123",
            work_order_id="wo_test456",
            attempt_number=1,
        )
        assert run.execution_run_id == "exr_test123"
        assert run.work_order_id == "wo_test456"
        assert run.attempt_number == 1
        assert run.status == ExecutionRunStatus.INITIATED
        assert run.changeset_id is None
        assert run.failure_reason is None
        assert run.abandon_justification is None

    def test_creation_with_all_fields(self):
        """ExecutionRun deve aceitar todos os campos."""
        run = ExecutionRun(
            execution_run_id="exr_test123",
            work_order_id="wo_test456",
            attempt_number=1,
            status=ExecutionRunStatus.RUNNING,
            executor="freebuff",
            started_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        assert run.executor == "freebuff"
        assert run.started_at is not None

    def test_attempt_number_must_be_positive(self):
        """attempt_number deve ser >= 1."""
        with pytest.raises(ValueError):
            ExecutionRun(
                execution_run_id="exr_test123",
                work_order_id="wo_test456",
                attempt_number=0,
            )

    def test_invalid_execution_run_id_rejected(self):
        """execution_run_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            ExecutionRun(
                execution_run_id="invalid-id",
                work_order_id="wo_test456",
                attempt_number=1,
            )

    def test_invalid_work_order_id_rejected(self):
        """work_order_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            ExecutionRun(
                execution_run_id="exr_test123",
                work_order_id="invalid-id",
                attempt_number=1,
            )


# =============================================================================
# VALIDAÇÕES
# =============================================================================


class TestExecutionRunValidations:
    def test_rejects_naive_datetime(self):
        """ExecutionRun rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            ExecutionRun(
                execution_run_id="exr_test123",
                work_order_id="wo_test456",
                attempt_number=1,
                created_at=datetime(2026, 1, 1),
            )

    def test_accepts_aware_datetime(self):
        """ExecutionRun aceita datetime com timezone."""
        run = ExecutionRun(
            execution_run_id="exr_test123",
            work_order_id="wo_test456",
            attempt_number=1,
            created_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        assert run.created_at.tzinfo is not None


# =============================================================================
# TRANSIÇÕES PERMITIDAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ExecutionRunStatus.INITIATED, ExecutionRunStatus.RUNNING),
        (ExecutionRunStatus.INITIATED, ExecutionRunStatus.ABANDONED),
        (ExecutionRunStatus.RUNNING, ExecutionRunStatus.COMPLETED),
        (ExecutionRunStatus.RUNNING, ExecutionRunStatus.FAILED),
        (ExecutionRunStatus.RUNNING, ExecutionRunStatus.ABANDONED),
    ],
)
def test_execution_run_valid_transitions(
    current: ExecutionRunStatus, target: ExecutionRunStatus
):
    """Transições válidas devem ser aceitas."""
    run = make_execution_run(status=current)
    kwargs: dict = {}
    if target == ExecutionRunStatus.COMPLETED:
        kwargs["changeset_id"] = "chs_abc123"
    if target == ExecutionRunStatus.FAILED:
        kwargs["failure_reason"] = "Erro de compilação"
    if target == ExecutionRunStatus.ABANDONED:
        kwargs["abandon_justification"] = "Escopo alterado"
    new_run = run.transition_to(target, **kwargs)
    assert new_run.status == target


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ExecutionRunStatus.INITIATED, ExecutionRunStatus.COMPLETED),
        (ExecutionRunStatus.INITIATED, ExecutionRunStatus.FAILED),
        (ExecutionRunStatus.COMPLETED, ExecutionRunStatus.RUNNING),
        (ExecutionRunStatus.FAILED, ExecutionRunStatus.RUNNING),
        (ExecutionRunStatus.ABANDONED, ExecutionRunStatus.RUNNING),
    ],
)
def test_execution_run_invalid_transitions_rejected(
    current: ExecutionRunStatus, target: ExecutionRunStatus
):
    """Transições inválidas devem ser rejeitadas."""
    run = make_execution_run(status=current)
    with pytest.raises(InvalidTransitionError):
        run.transition_to(target)


# =============================================================================
# TRANSIÇÕES PARA ESTADOS TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(EXECUTIONRUN_TERMINAL))
def test_execution_run_terminal_states(terminal_status: ExecutionRunStatus):
    """ExecutionRuns em estados terminais são marcados como is_terminal."""
    run = make_execution_run(status=terminal_status)
    assert run.is_terminal


def test_execution_run_non_terminal_states():
    """ExecutionRuns em estados não-terminais não são marcados como is_terminal."""
    for status in ExecutionRunStatus:
        if status not in EXECUTIONRUN_TERMINAL:
            if status == ExecutionRunStatus.INITIATED:
                run = make_execution_run(status=status)
            else:
                run = make_execution_run(status=status)
            assert not run.is_terminal


# =============================================================================
# TIMESTAMP DE INÍCIO
# =============================================================================


def test_started_at_set_on_running():
    """started_at deve ser preenchido ao transicionar para running."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    new_run = run.transition_to(ExecutionRunStatus.RUNNING)
    assert new_run.started_at is not None


def test_started_at_preserved_on_subsequent_transitions():
    """started_at deve ser preservado em transições subsequentes."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    run = run.transition_to(ExecutionRunStatus.RUNNING)
    started_at = run.started_at
    new_run = run.transition_to(ExecutionRunStatus.COMPLETED, changeset_id="chs_abc123")
    assert new_run.started_at == started_at


# =============================================================================
# TIMESTAMP DE ENCERRAMENTO
# =============================================================================


def test_completed_at_set_on_terminal():
    """completed_at deve ser preenchido ao transicionar para estado final."""
    run = make_execution_run(status=ExecutionRunStatus.RUNNING)
    assert run.completed_at is None
    new_run = run.transition_to(ExecutionRunStatus.COMPLETED, changeset_id="chs_abc123")
    assert new_run.completed_at is not None


# =============================================================================
# CONCLUSÃO COM CHANGESET
# =============================================================================


def test_completed_requires_changeset():
    """Transição para completed requer changeset_id."""
    run = make_execution_run(status=ExecutionRunStatus.RUNNING)
    with pytest.raises(InvariantViolationError, match="changeset"):
        run.transition_to(ExecutionRunStatus.COMPLETED)


def test_completed_with_changeset():
    """Transição para completed com changeset funciona."""
    run = make_execution_run(status=ExecutionRunStatus.RUNNING)
    new_run = run.transition_to(ExecutionRunStatus.COMPLETED, changeset_id="chs_abc123")
    assert new_run.status == ExecutionRunStatus.COMPLETED
    assert new_run.changeset_id == "chs_abc123"


# =============================================================================
# FALHA
# =============================================================================


def test_failed_requires_reason():
    """Transição para failed requer failure_reason."""
    run = make_execution_run(status=ExecutionRunStatus.RUNNING)
    with pytest.raises(InvariantViolationError, match="failure_reason"):
        run.transition_to(ExecutionRunStatus.FAILED)


def test_failed_with_reason():
    """Transição para failed com motivo funciona."""
    run = make_execution_run(status=ExecutionRunStatus.RUNNING)
    new_run = run.transition_to(
        ExecutionRunStatus.FAILED, failure_reason="Erro de compilação"
    )
    assert new_run.status == ExecutionRunStatus.FAILED
    assert new_run.failure_reason == "Erro de compilação"


# =============================================================================
# ABANDONO
# =============================================================================


def test_abandoned_requires_justification():
    """Transição para abandoned requer abandon_justification."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    with pytest.raises(InvariantViolationError, match="abandon_justification"):
        run.transition_to(ExecutionRunStatus.ABANDONED)


def test_abandoned_with_justification():
    """Transição para abandoned com justificativa funciona."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    new_run = run.transition_to(
        ExecutionRunStatus.ABANDONED,
        abandon_justification="Escopo alterado pelo usuário",
    )
    assert new_run.status == ExecutionRunStatus.ABANDONED
    assert new_run.abandon_justification == "Escopo alterado pelo usuário"


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================


def test_execution_run_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    result = run.transition_to(ExecutionRunStatus.INITIATED)
    assert result is run


# =============================================================================
# IMUTABILIDADE
# =============================================================================


def test_execution_run_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    original_status = run.status
    _ = run.transition_to(ExecutionRunStatus.RUNNING)
    assert run.status == original_status


def test_execution_run_version_increments():
    """Versão incrementa a cada transição."""
    run = make_execution_run(status=ExecutionRunStatus.INITIATED)
    new_run = run.transition_to(ExecutionRunStatus.RUNNING)
    assert new_run.version == run.version + 1


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


def test_execution_run_json_roundtrip():
    """ExecutionRun deve serializar e desserializar corretamente."""
    run = make_execution_run(
        status=ExecutionRunStatus.RUNNING,
        executor="freebuff",
    )
    json_str = run.model_dump_json()
    run2 = ExecutionRun.model_validate_json(json_str)
    assert run.execution_run_id == run2.execution_run_id
    assert run.status == run2.status
    assert run.attempt_number == run2.attempt_number
    assert run2.started_at is not None


# =============================================================================
# ESTADOS TERMINAIS BLOQUEIAM TRANSMISSÕES
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(EXECUTIONRUN_TERMINAL))
def test_execution_run_terminal_blocks_further_transitions(
    terminal_status: ExecutionRunStatus,
):
    """ExecutionRun em estado terminal bloqueia transições."""
    run = make_execution_run(status=terminal_status)
    with pytest.raises(InvalidTransitionError):
        run.transition_to(ExecutionRunStatus.RUNNING)
