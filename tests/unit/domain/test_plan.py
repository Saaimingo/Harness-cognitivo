"""
Testes para a entidade Plan — FI-2A.
Cobre: versionamento, aprovação, superseding, criação de próxima versão.
"""

import pytest
from datetime import datetime, timezone

from harness.domain.plan import Plan, PlanStatus


def make_plan(version: int = 1, status: PlanStatus = PlanStatus.DRAFT) -> Plan:
    return Plan(
        plan_id="pln_test123",
        project_id="prj_test123",
        version=version,
        title="Plano Teste",
        status=status,
    )


class TestPlanCreation:
    def test_plan_creation_minimal(self):
        plan = make_plan()
        assert plan.version == 1
        assert plan.status == PlanStatus.DRAFT
        assert plan.previous_version_id is None

    def test_plan_requires_positive_version(self):
        with pytest.raises(Exception):
            Plan(
                plan_id="pln_test123",
                project_id="prj_test123",
                version=0,
                title="Teste",
            )

    def test_plan_rejects_naive_datetime(self):
        with pytest.raises(ValueError, match="timezone"):
            Plan(
                plan_id="pln_test123",
                project_id="prj_test123",
                title="Teste",
                created_at=datetime(2026, 1, 1),
            )


class TestPlanTransitions:
    def test_approve(self):
        plan = make_plan()
        approved = plan.approve()
        assert approved.status == PlanStatus.APPROVED
        assert plan.status == PlanStatus.DRAFT  # original inalterado

    def test_supersede(self):
        plan = make_plan(status=PlanStatus.APPROVED)
        superseded = plan.supersede(new_version_id="pln_new123")
        assert superseded.status == PlanStatus.SUPERSEDED


class TestPlanVersioning:
    def test_create_next_version(self):
        plan = make_plan(version=1)
        next_plan = plan.create_next_version(new_plan_id="pln_v2")
        assert next_plan.version == 2
        assert next_plan.previous_version_id == "pln_test123"
        assert next_plan.project_id == plan.project_id

    def test_is_approved(self):
        assert make_plan(status=PlanStatus.APPROVED).is_approved
        assert not make_plan(status=PlanStatus.DRAFT).is_approved
