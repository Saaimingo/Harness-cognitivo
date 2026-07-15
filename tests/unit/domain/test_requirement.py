"""
Testes para a entidade Requirement — FI-2A.
Cobre: criação, status, prioridade, timezone.
"""

import pytest
from datetime import datetime, timezone

from harness.domain.requirement import Requirement, RequirementStatus, RequirementPriority


def make_requirement(status: RequirementStatus = RequirementStatus.PROPOSED) -> Requirement:
    return Requirement(
        requirement_id="req_test123",
        project_id="prj_test123",
        description="Requisito Teste",
        status=status,
    )


class TestRequirementCreation:
    def test_creation_minimal(self):
        req = make_requirement()
        assert req.status == RequirementStatus.PROPOSED
        assert req.priority == RequirementPriority.MEDIUM
        assert req.version == 1

    def test_rejects_naive_datetime(self):
        with pytest.raises(ValueError, match="timezone"):
            Requirement(
                requirement_id="req_test123",
                project_id="prj_test123",
                description="Teste",
                created_at=datetime(2026, 1, 1),
            )

    def test_accepts_aware_datetime(self):
        req = Requirement(
            requirement_id="req_test123",
            project_id="prj_test123",
            description="Teste",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        assert req.created_at.tzinfo is not None


class TestRequirementStatus:
    def test_update_status(self):
        req = make_requirement()
        new_req = req.update_status(RequirementStatus.APPROVED)
        assert new_req.status == RequirementStatus.APPROVED
        assert req.status == RequirementStatus.PROPOSED  # original inalterado

    def test_is_approved(self):
        assert make_requirement(status=RequirementStatus.APPROVED).is_approved
        assert not make_requirement(status=RequirementStatus.PROPOSED).is_approved
