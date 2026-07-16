"""
Testes para políticas puras de domínio — FI-2A.
Cobre: casos positivos e negativos de cada política.
"""

from harness.domain.policies import (
    gate_can_advance,
    gate_can_be_waived,
    incident_can_become_closed,
    project_can_become_ready,
    project_can_become_release_ready,
    task_can_become_accepted,
)

# =============================================================================
# PROJECT → READY
# =============================================================================


class TestProjectReadyPolicy:
    def test_ready_with_plan_and_requirements(self):
        result = project_can_become_ready(
            has_approved_plan=True,
            has_approved_requirements=True,
        )
        assert result.allowed is True

    def test_ready_without_plan(self):
        result = project_can_become_ready(
            has_approved_plan=False,
            has_approved_requirements=True,
        )
        assert result.allowed is False
        assert "plano" in result.reason.lower()

    def test_ready_without_requirements(self):
        result = project_can_become_ready(
            has_approved_plan=True,
            has_approved_requirements=False,
        )
        assert result.allowed is False
        assert "requisito" in result.reason.lower()


# =============================================================================
# PROJECT → RELEASE_READY
# =============================================================================


class TestProjectReleaseReadyPolicy:
    def test_release_ready_no_blockers(self):
        result = project_can_become_release_ready(
            has_blocking_gate=False,
            pending_human_approvals=0,
        )
        assert result.allowed is True

    def test_release_ready_with_blocking_gate(self):
        result = project_can_become_release_ready(
            has_blocking_gate=True,
            pending_human_approvals=0,
        )
        assert result.allowed is False
        assert "gate" in result.reason.lower()

    def test_release_ready_with_pending_approvals(self):
        result = project_can_become_release_ready(
            has_blocking_gate=False,
            pending_human_approvals=2,
        )
        assert result.allowed is False
        assert "aprovação" in result.reason.lower()


# =============================================================================
# TASK → ACCEPTED
# =============================================================================


class TestTaskAcceptedPolicy:
    def test_accepted_all_criteria_met(self):
        result = task_can_become_accepted(
            has_changeset=True,
            review_approved=True,
            tests_passed=True,
            has_evidence=True,
            no_blockers=True,
            rework_count=0,
            rework_limit=5,
        )
        assert result.allowed is True

    def test_accepted_without_changeset(self):
        result = task_can_become_accepted(
            has_changeset=False,
            review_approved=True,
            tests_passed=True,
            has_evidence=True,
            no_blockers=True,
            rework_count=0,
            rework_limit=5,
        )
        assert result.allowed is False
        assert "changeset" in result.reason.lower()

    def test_accepted_without_review(self):
        result = task_can_become_accepted(
            has_changeset=True,
            review_approved=False,
            tests_passed=True,
            has_evidence=True,
            no_blockers=True,
            rework_count=0,
            rework_limit=5,
        )
        assert result.allowed is False
        assert "revisão" in result.reason.lower()

    def test_accepted_rework_limit_reached(self):
        result = task_can_become_accepted(
            has_changeset=True,
            review_approved=True,
            tests_passed=True,
            has_evidence=True,
            no_blockers=True,
            rework_count=5,
            rework_limit=5,
        )
        assert result.allowed is False
        assert "rework" in result.reason.lower()


# =============================================================================
# GATE → ADVANCE
# =============================================================================


class TestGateAdvancePolicy:
    def test_advance_all_met(self):
        result = gate_can_advance(
            has_criteria=True,
            has_evidence=True,
            has_authority=True,
            tests_passed=True,
        )
        assert result.allowed is True

    def test_advance_without_evidence(self):
        result = gate_can_advance(
            has_criteria=True,
            has_evidence=False,
            has_authority=True,
            tests_passed=True,
        )
        assert result.allowed is False
        assert "evidência" in result.reason.lower()


# =============================================================================
# GATE → WAIVED
# =============================================================================


class TestGateWaivedPolicy:
    def test_waived_all_met(self):
        result = gate_can_be_waived(
            has_authority=True,
            has_justification=True,
            has_scope=True,
        )
        assert result.allowed is True

    def test_waived_without_authority(self):
        result = gate_can_be_waived(
            has_authority=False,
            has_justification=True,
            has_scope=True,
        )
        assert result.allowed is False
        assert "autoridade" in result.reason.lower()


# =============================================================================
# INCIDENT → CLOSED
# =============================================================================


class TestIncidentClosedPolicy:
    def test_closed_all_met(self):
        result = incident_can_become_closed(
            has_cause=True,
            has_corrective_action=True,
            has_regression_evidence=True,
        )
        assert result.allowed is True

    def test_closed_without_cause(self):
        result = incident_can_become_closed(
            has_cause=False,
            has_corrective_action=True,
            has_regression_evidence=True,
        )
        assert result.allowed is False
        assert "causa" in result.reason.lower()

    def test_closed_without_regression(self):
        result = incident_can_become_closed(
            has_cause=True,
            has_corrective_action=True,
            has_regression_evidence=False,
        )
        assert result.allowed is False
        assert "regressão" in result.reason.lower()
