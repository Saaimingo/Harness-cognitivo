"""
Testes parametrizados para a entidade Project — FI-2A.
Cobre: transições permitidas, rejeitadas, idempotência, imutabilidade, timezone.
"""

import pytest
from datetime import datetime, timezone

from harness.domain.project import Project
from harness.domain.enums import ProjectStatus
from harness.domain.transitions import PROJECT_TRANSITIONS, PROJECT_TERMINAL
from harness.domain.errors import InvalidTransitionError, InvariantViolationError


def make_project(status: ProjectStatus = ProjectStatus.CAPTURED) -> Project:
    """Helper para criar Project com estado específico."""
    return Project(
        project_id="prj_test123",
        name="Projeto Teste",
        status=status,
    )


# =============================================================================
# TRANSIÇÕES PERMITIDAS (não-terminais)
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (ProjectStatus.CAPTURED, ProjectStatus.TRIAGE),
    (ProjectStatus.TRIAGE, ProjectStatus.DISCOVERY),
    (ProjectStatus.DISCOVERY, ProjectStatus.SPECIFIED),
    (ProjectStatus.SPECIFIED, ProjectStatus.ARCHITECTED),
    (ProjectStatus.ARCHITECTED, ProjectStatus.PLANNED),
    (ProjectStatus.PLANNED, ProjectStatus.READY),
    (ProjectStatus.READY, ProjectStatus.EXECUTING),
    (ProjectStatus.EXECUTING, ProjectStatus.REVIEWING),
    (ProjectStatus.REVIEWING, ProjectStatus.VALIDATING),
    (ProjectStatus.VALIDATING, ProjectStatus.RELEASE_READY),
    (ProjectStatus.RELEASE_READY, ProjectStatus.RELEASED),
    (ProjectStatus.RELEASED, ProjectStatus.MONITORED),
    (ProjectStatus.EXECUTING, ProjectStatus.REWORK_REQUIRED),
    (ProjectStatus.REWORK_REQUIRED, ProjectStatus.PLANNED),
    (ProjectStatus.READY, ProjectStatus.SUSPENDED),
])
def test_project_valid_transitions(current: ProjectStatus, target: ProjectStatus):
    """Transições válidas não-terminais devem ser aceitas sem autoridade."""
    project = make_project(status=current)
    new_project = project.transition_to(target)
    assert new_project.status == target


# =============================================================================
# TRANSIÇÕES PARA ESTADOS TERMINAIS (com autoridade)
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (ProjectStatus.MONITORED, ProjectStatus.ARCHIVED),
])
def test_project_terminal_transitions_with_authority(
    current: ProjectStatus, target: ProjectStatus
):
    """Transições para estados terminais requerem autoridade."""
    project = make_project(status=current)
    new_project = project.transition_to(target, authority="test")
    assert new_project.status == target


# =============================================================================
# TRANSIÇÕES TERMINAIS SEM AUTORIDADE
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (ProjectStatus.MONITORED, ProjectStatus.ARCHIVED),
])
def test_project_terminal_transitions_without_authority_rejected(
    current: ProjectStatus, target: ProjectStatus
):
    """Transições para estados terminais sem autoridade são rejeitadas."""
    project = make_project(status=current)
    with pytest.raises(InvariantViolationError):
        project.transition_to(target)


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (ProjectStatus.CAPTURED, ProjectStatus.READY),
    (ProjectStatus.CAPTURED, ProjectStatus.RELEASED),
    (ProjectStatus.READY, ProjectStatus.CAPTURED),
    (ProjectStatus.RELEASED, ProjectStatus.CAPTURED),
    (ProjectStatus.ABANDONED, ProjectStatus.CAPTURED),
    (ProjectStatus.ARCHIVED, ProjectStatus.CAPTURED),
])
def test_project_invalid_transitions_rejected(current: ProjectStatus, target: ProjectStatus):
    """Transições inválidas devem ser rejeitadas."""
    project = make_project(status=current)
    with pytest.raises(InvalidTransitionError):
        project.transition_to(target)


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================

def test_project_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    project = make_project(status=ProjectStatus.CAPTURED)
    result = project.transition_to(ProjectStatus.CAPTURED)
    assert result is project


# =============================================================================
# IMUTABILIDADE
# =============================================================================

def test_project_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    project = make_project(status=ProjectStatus.CAPTURED)
    original_status = project.status
    _ = project.transition_to(ProjectStatus.TRIAGE)
    assert project.status == original_status


def test_project_version_increments():
    """Versão incrementa a cada transição."""
    project = make_project(status=ProjectStatus.CAPTURED)
    new_project = project.transition_to(ProjectStatus.TRIAGE)
    assert new_project.version == project.version + 1


# =============================================================================
# TIMEZONE
# =============================================================================

def test_project_rejects_naive_datetime():
    """Project rejeita datetime sem timezone."""
    with pytest.raises(ValueError, match="timezone"):
        Project(
            project_id="prj_test123",
            name="Teste",
            created_at=datetime(2026, 1, 1),
        )


def test_project_accepts_aware_datetime():
    """Project aceita datetime com timezone."""
    project = Project(
        project_id="prj_test123",
        name="Teste",
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert project.created_at.tzinfo is not None


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================

@pytest.mark.parametrize("terminal_status", list(PROJECT_TERMINAL))
def test_project_terminal_states(terminal_status: ProjectStatus):
    """Projetos em estados terminais são marcados como is_terminal."""
    project = make_project(status=terminal_status)
    assert project.is_terminal


def test_project_suspended_state():
    """Projetos suspensos são marcados como is_suspended."""
    project = make_project(status=ProjectStatus.SUSPENDED)
    assert project.is_suspended
