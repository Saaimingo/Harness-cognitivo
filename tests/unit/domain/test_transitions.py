"""
Testes para tabelas de transição — FI-2A.
Cobre: completude das tabelas, coleta de todos os estados, transições entre válidos.
"""

import pytest

from harness.domain.enums import (
    GateStatus,
    ProjectStatus,
    TaskStatus,
    WorkOrderStatus,
)
from harness.domain.transitions import (
    GATE_INITIAL,
    GATE_TERMINAL,
    GATE_TRANSITIONS,
    PROJECT_INITIAL,
    PROJECT_TERMINAL,
    PROJECT_TRANSITIONS,
    TASK_INITIAL,
    TASK_TERMINAL,
    TASK_TRANSITIONS,
    WORKORDER_INITIAL,
    WORKORDER_TERMINAL,
    WORKORDER_TRANSITIONS,
)

# =============================================================================
# PROJETO
# =============================================================================


class TestProjectTransitions:
    def test_initial_state_is_captured(self):
        assert PROJECT_INITIAL == ProjectStatus.CAPTURED

    def test_terminal_states(self):
        assert ProjectStatus.ARCHIVED in PROJECT_TERMINAL
        assert ProjectStatus.ABANDONED in PROJECT_TERMINAL

    def test_all_states_have_transitions(self):
        for status in ProjectStatus:
            if status not in PROJECT_TERMINAL:
                assert status in PROJECT_TRANSITIONS
                assert len(PROJECT_TRANSITIONS[status]) > 0

    def test_terminal_states_have_no_transitions(self):
        for status in PROJECT_TERMINAL:
            assert PROJECT_TRANSITIONS.get(status, frozenset()) == frozenset()

    @pytest.mark.parametrize("state", list(ProjectStatus))
    def test_all_enum_values_in_table(self, state):
        """Todos os valores do Enum devem estar na tabela."""
        assert state in PROJECT_TRANSITIONS or state in PROJECT_TERMINAL


# =============================================================================
# TAREFA
# =============================================================================


class TestTaskTransitions:
    def test_initial_state_is_proposed(self):
        assert TASK_INITIAL == TaskStatus.PROPOSED

    def test_terminal_states(self):
        assert TaskStatus.ACCEPTED in TASK_TERMINAL
        assert TaskStatus.CANCELLED in TASK_TERMINAL
        assert TaskStatus.SUPERSEDED in TASK_TERMINAL

    @pytest.mark.parametrize("state", list(TaskStatus))
    def test_all_enum_values_in_table(self, state):
        assert state in TASK_TRANSITIONS or state in TASK_TERMINAL


# =============================================================================
# WORKORDER
# =============================================================================


class TestWorkOrderTransitions:
    def test_initial_state_is_draft(self):
        assert WORKORDER_INITIAL == WorkOrderStatus.DRAFT

    def test_terminal_states(self):
        assert WorkOrderStatus.COMPLETED in WORKORDER_TERMINAL
        assert WorkOrderStatus.CANCELLED in WORKORDER_TERMINAL

    @pytest.mark.parametrize("state", list(WorkOrderStatus))
    def test_all_enum_values_in_table(self, state):
        assert state in WORKORDER_TRANSITIONS or state in WORKORDER_TERMINAL


# =============================================================================
# GATE
# =============================================================================


class TestGateTransitions:
    def test_initial_state_is_pending(self):
        assert GATE_INITIAL == GateStatus.PENDING

    def test_terminal_states(self):
        assert GateStatus.DECIDED in GATE_TERMINAL
        assert GateStatus.CANCELLED in GATE_TERMINAL

    def test_waived_not_in_gate_status(self):
        """GateStatus.WAIVED foi removido — resultado ficou em GateDecisionType."""
        from harness.domain.enums import GateDecisionType

        with pytest.raises((ValueError, AttributeError)):
            GateStatus("waived")
        assert GateDecisionType.WAIVED == "waived"

    @pytest.mark.parametrize("state", list(GateStatus))
    def test_all_enum_values_in_table(self, state):
        assert state in GATE_TRANSITIONS or state in GATE_TERMINAL
