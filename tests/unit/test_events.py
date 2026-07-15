"""
Testes unitários para os contratos de eventos do Harness.
"""

import pytest
from datetime import datetime, timezone

from harness.contracts.events import (
    Event,
    EventType,
    TaskCreated,
    TaskStarted,
    TaskCompleted,
    TaskFailed,
    StepStarted,
    StepCompleted,
    ModelCalled,
    ToolCalled,
    ErrorRecorded,
    ResultRecorded,
    ExecutionCompleted,
)


class TestEvent:
    """Testes para a classe Event base."""

    def test_event_creation(self):
        """Evento deve ser criado com campos padrão."""
        event = Event(event_type=EventType.TASK_CREATED)
        assert event.event_id
        assert event.event_type == EventType.TASK_CREATED
        assert isinstance(event.timestamp, datetime)

    def test_event_immutability(self):
        """Evento deve ser imutável (frozen)."""
        event = Event(event_type=EventType.TASK_CREATED)
        with pytest.raises(Exception):
            event.event_type = EventType.TASK_COMPLETED

    def test_event_with_correlation(self):
        """Evento deve suportar correlation_id e causation_id."""
        event = Event(
            event_type=EventType.TASK_CREATED,
            correlation_id="corr-123",
            causation_id="cause-456",
        )
        assert event.correlation_id == "corr-123"
        assert event.causation_id == "cause-456"

    def test_event_with_metadata(self):
        """Evento deve suportar metadata customizada."""
        event = Event(
            event_type=EventType.TASK_CREATED,
            metadata={"key": "value", "number": 42},
        )
        assert event.metadata["key"] == "value"
        assert event.metadata["number"] == 42


class TestEventTypes:
    """Testes para os tipos de eventos."""

    def test_all_event_types_exist(self):
        """Todos os tipos de eventos devem existir."""
        expected_types = [
            "task.created", "task.started", "task.completed",
            "task.failed", "task.cancelled",
            "step.started", "step.completed", "step.failed",
            "model.called", "model.response", "model.error",
            "tool.called", "tool.result", "tool.error",
            "error.recorded",
            "test.executed", "test.passed", "test.failed",
            "execution.completed", "execution.failed",
        ]
        for et in expected_types:
            assert EventType(et) is not None

    def test_event_type_as_string(self):
        """EventType deve funcionar como string."""
        assert EventType.TASK_CREATED == "task.created"
        assert EventType.MODEL_CALLED == "model.called"


class TestSpecificEvents:
    """Testes para eventos específicos."""

    def test_task_created(self):
        """TaskCreated deve ter campos específicos."""
        event = TaskCreated(
            task_name="minha-tarefa",
            description="Descrição da tarefa",
        )
        assert event.event_type == EventType.TASK_CREATED
        assert event.task_name == "minha-tarefa"
        assert event.description == "Descrição da tarefa"

    def test_task_started(self):
        """TaskStarted deve ter agent."""
        event = TaskStarted(agent="freebuff")
        assert event.event_type == EventType.TASK_STARTED
        assert event.agent == "freebuff"

    def test_task_completed_with_duration(self):
        """TaskCompleted deve suportar duração."""
        event = TaskCompleted(duration_seconds=123.45)
        assert event.event_type == EventType.TASK_COMPLETED
        assert event.duration_seconds == 123.45

    def test_task_failed_with_error(self):
        """TaskFailed deve ter mensagem de erro."""
        event = TaskFailed(
            error_message="Algo deu errado",
            error_type="ValueError",
        )
        assert event.event_type == EventType.TASK_FAILED
        assert event.error_message == "Algo deu errado"
        assert event.error_type == "ValueError"

    def test_model_called(self):
        """ModelCalled deve ter informações do modelo."""
        event = ModelCalled(
            model_id="gpt-4",
            provider="openai",
            tokens_input=100,
            tokens_output=50,
            cost_usd=0.01,
            duration_ms=500,
        )
        assert event.model_id == "gpt-4"
        assert event.provider == "openai"
        assert event.tokens_input == 100
        assert event.cost_usd == 0.01

    def test_tool_called(self):
        """ToolCalled deve ter informações da ferramenta."""
        event = ToolCalled(
            tool_name="read_file",
            tool_args={"path": "/tmp/test.txt"},
            duration_ms=50,
        )
        assert event.tool_name == "read_file"
        assert event.tool_args["path"] == "/tmp/test.txt"

    def test_error_recorded(self):
        """ErrorRecorded deve ter severidade."""
        event = ErrorRecorded(
            error_message="Falha crítica",
            error_type="RuntimeError",
            severity="critical",
        )
        assert event.severity == "critical"

    def test_result_recorded(self):
        """ResultRecorded deve ter resultado."""
        event = ResultRecorded(
            test_name="test_meu_modulo",
            test_file="tests/unit/test_modulo.py",
            passed=True,
            duration_seconds=0.5,
        )
        assert event.passed is True

    def test_execution_completed(self):
        """ExecutionCompleted deve ter métricas."""
        event = ExecutionCompleted(
            total_duration_seconds=300,
            total_tokens=5000,
            total_cost_usd=0.15,
        )
        assert event.total_tokens == 5000
        assert event.total_cost_usd == 0.15
