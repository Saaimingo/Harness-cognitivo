"""
Testes parametrizados para a entidade WorkOrder — FI-2A.
Cobre: transições, autoridade, escopo, expiração, idempotência, imutabilidade.
"""

import pytest
from datetime import datetime, timezone

from harness.domain.work_order import WorkOrder, WorkOrderScope
from harness.domain.enums import WorkOrderStatus
from harness.domain.transitions import WORKORDER_TRANSITIONS, WORKORDER_TERMINAL
from harness.domain.errors import InvalidTransitionError, MissingAuthorityError


def make_work_order(status: WorkOrderStatus = WorkOrderStatus.DRAFT) -> WorkOrder:
    """Helper para criar WorkOrder com estado específico."""
    return WorkOrder(
        work_order_id="wo_test123",
        project_id="prj_test123",
        task_id="tsk_test123",
        title="WorkOrder Teste",
        status=status,
    )


# =============================================================================
# TRANSIÇÕES PERMITIDAS (sem necessidade de autoridade)
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (WorkOrderStatus.DRAFT, WorkOrderStatus.VALIDATED),
    (WorkOrderStatus.DISPATCHED, WorkOrderStatus.ACTIVE),
    (WorkOrderStatus.ACTIVE, WorkOrderStatus.COMPLETED),
])
def test_work_order_valid_transitions(current: WorkOrderStatus, target: WorkOrderStatus):
    """Transições válidas sem autoridade devem ser aceitas."""
    wo = make_work_order(status=current)
    new_wo = wo.transition_to(target)
    assert new_wo.status == target


# =============================================================================
# AUTORIZAÇÃO COM AUTORIDADE
# =============================================================================

def test_work_order_authorize_requires_authority():
    """Transição para AUTHORIZED requer autoridade."""
    wo = make_work_order(status=WorkOrderStatus.VALIDATED)
    with pytest.raises(MissingAuthorityError):
        wo.transition_to(WorkOrderStatus.AUTHORIZED)


def test_work_order_authorize_with_authority():
    """Transição para AUTHORIZED com autoridade funciona."""
    wo = make_work_order(status=WorkOrderStatus.VALIDATED)
    new_wo = wo.transition_to(WorkOrderStatus.AUTHORIZED, authority="saimon")
    assert new_wo.status == WorkOrderStatus.AUTHORIZED
    assert new_wo.authority == "saimon"
    assert new_wo.authorized_at is not None


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================

@pytest.mark.parametrize("current,target", [
    (WorkOrderStatus.DRAFT, WorkOrderStatus.ACTIVE),
    (WorkOrderStatus.DRAFT, WorkOrderStatus.COMPLETED),
    (WorkOrderStatus.ACTIVE, WorkOrderStatus.DRAFT),
    (WorkOrderStatus.COMPLETED, WorkOrderStatus.ACTIVE),
])
def test_work_order_invalid_transitions_rejected(current: WorkOrderStatus, target: WorkOrderStatus):
    """Transições inválidas devem ser rejeitadas."""
    wo = make_work_order(status=current)
    with pytest.raises(InvalidTransitionError):
        wo.transition_to(target)


# =============================================================================
# ESCOPO
# =============================================================================

def test_work_order_scope_preserved():
    """Escopo é preservado na transição."""
    wo = make_work_order(status=WorkOrderStatus.DRAFT)
    wo_with_scope = wo.model_copy(update={
        "scope": WorkOrderScope(included=["src/"], excluded=["tests/"])
    })
    new_wo = wo_with_scope.transition_to(WorkOrderStatus.VALIDATED)
    assert new_wo.scope.included == ["src/"]
    assert new_wo.scope.excluded == ["tests/"]


# =============================================================================
# EXPIRAÇÃO
# =============================================================================

def test_work_order_expiry_field():
    """Campo expires_at pode ser definido."""
    wo = WorkOrder(
        work_order_id="wo_test123",
        project_id="prj_test123",
        task_id="tsk_test123",
        title="Teste",
        expires_at=datetime(2026, 12, 31, tzinfo=timezone.utc),
    )
    assert wo.expires_at is not None


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================

def test_work_order_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    wo = make_work_order(status=WorkOrderStatus.DRAFT)
    result = wo.transition_to(WorkOrderStatus.DRAFT)
    assert result is wo


# =============================================================================
# IMUTABILIDADE
# =============================================================================

def test_work_order_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    wo = make_work_order(status=WorkOrderStatus.DRAFT)
    original_status = wo.status
    _ = wo.transition_to(WorkOrderStatus.VALIDATED)
    assert wo.status == original_status


# =============================================================================
# PROPRIEDADES
# =============================================================================

def test_work_order_is_executable():
    """Propriedade is_executable retorna True para AUTHORIZED e DISPATCHED."""
    assert make_work_order(status=WorkOrderStatus.AUTHORIZED).is_executable
    assert make_work_order(status=WorkOrderStatus.DISPATCHED).is_executable
    assert not make_work_order(status=WorkOrderStatus.DRAFT).is_executable
