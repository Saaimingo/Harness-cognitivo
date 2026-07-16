"""
Testes de invariantes de dominio — FI-2A.
Cobre: model_copy safety, reutilizacao de IDs, transicoes terminais, excecoes.
"""

import pytest

from harness.contracts.context import validate_id_format as fi1_validate_id
from harness.domain.enums import ProjectStatus, TaskStatus
from harness.domain.errors import (
    DomainError,
    InvalidTransitionError,
    InvariantViolationError,
    MissingAuthorityError,
    MissingEvidenceError,
    ReworkLimitExceededError,
    TimezoneRequiredError,
)
from harness.domain.ids import validate_id_format as domain_validate_id
from harness.domain.project import Project
from harness.domain.task import Task

# =============================================================================
# EXCECOES — CONTAGEM
# =============================================================================


class TestExceptionCount:
    def test_domain_error_is_base(self):
        assert issubclass(InvalidTransitionError, DomainError)
        assert issubclass(InvariantViolationError, DomainError)
        assert issubclass(ReworkLimitExceededError, DomainError)
        assert issubclass(MissingAuthorityError, DomainError)
        assert issubclass(MissingEvidenceError, DomainError)
        assert issubclass(TimezoneRequiredError, DomainError)

    def test_six_specialized_exceptions(self):
        """1 base + 6 especializadas = 7 classes no total."""
        specialized = [
            InvalidTransitionError,
            InvariantViolationError,
            ReworkLimitExceededError,
            MissingAuthorityError,
            MissingEvidenceError,
            TimezoneRequiredError,
        ]
        assert len(specialized) == 6


# =============================================================================
# MODEL_COPY SAFETY
# =============================================================================


class TestModelCopySafety:
    def test_invalid_status_rejected_at_construction(self):
        """Construtor rejeita status invalido."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            Project(
                project_id="prj_test123",
                name="Teste",
                status="invalid_status",
            )


# =============================================================================
# ID VALIDATION REUSE
# =============================================================================


class TestIDValidationReuse:
    def test_domain_ids_reuses_fi1(self):
        """Dominio reutiliza validacao de IDs da FI-1."""
        assert fi1_validate_id is domain_validate_id

    def test_invalid_ids_rejected(self):
        """IDs invalidos sao rejeitados pela validacao reutilizada."""
        with pytest.raises(ValueError):
            fi1_validate_id("invalid-id")
        with pytest.raises(ValueError):
            domain_validate_id("invalid-id")


# =============================================================================
# TERMINAL TRANSITIONS — InvariantViolationError
# =============================================================================


class TestTerminalTransitions:
    def test_project_terminal_requires_authority(self):
        """Transicao para estado terminal requer autoridade."""
        project = Project(
            project_id="prj_test123",
            name="Teste",
            status=ProjectStatus.MONITORED,
        )
        with pytest.raises(InvariantViolationError):
            project.transition_to(ProjectStatus.ARCHIVED)

    def test_project_terminal_with_authority(self):
        """Transicao para estado terminal com autoridade funciona."""
        project = Project(
            project_id="prj_test123",
            name="Teste",
            status=ProjectStatus.MONITORED,
        )
        new_project = project.transition_to(
            ProjectStatus.ARCHIVED,
            authority="saimon",
        )
        assert new_project.status == ProjectStatus.ARCHIVED

    def test_task_terminal_blocks_further_transitions(self):
        """Task em estado terminal bloqueia transicoes."""
        task = Task(
            task_id="tsk_test123",
            project_id="prj_test123",
            plan_id="pln_test123",
            title="Teste",
            status=TaskStatus.IN_VALIDATION,
        )
        accepted = task.transition_to(TaskStatus.ACCEPTED, authority="test")
        with pytest.raises(InvalidTransitionError):
            accepted.transition_to(TaskStatus.RUNNING)

    def test_missing_evidence_error_raised(self):
        """MissingEvidenceError pode ser disparada corretamente."""
        with pytest.raises(MissingEvidenceError):
            raise MissingEvidenceError("Test", "validate")
