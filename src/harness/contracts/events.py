"""
Contratos de Eventos do Harness Cognitivo.

Define os eventos fundamentais para observabilidade desde a primeira versão.
Cada execução deve gerar eventos que permitam reconstruir o que aconteceu.
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class EventType(StrEnum):
    """Tipos de eventos do sistema."""

    # Eventos de Tarefa
    TASK_CREATED = "task.created"
    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_CANCELLED = "task.cancelled"

    # Eventos de Etapa
    STEP_STARTED = "step.started"
    STEP_COMPLETED = "step.completed"
    STEP_FAILED = "step.failed"

    # Eventos de Modelo
    MODEL_CALLED = "model.called"
    MODEL_RESPONSE = "model.response"
    MODEL_ERROR = "model.error"

    # Eventos de Ferramenta
    TOOL_CALLED = "tool.called"
    TOOL_RESULT = "tool.result"
    TOOL_ERROR = "tool.error"

    # Eventos de Erro
    ERROR_RECORDED = "error.recorded"

    # Eventos de Teste
    TEST_EXECUTED = "test.executed"
    TEST_PASSED = "test.passed"
    TEST_FAILED = "test.failed"

    # Eventos de Execução
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"


class Event(BaseModel):
    """Evento base do sistema."""

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None
    causation_id: str | None = None
    project_id: str | None = None
    task_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class TaskCreated(Event):
    """Evento de criação de tarefa."""

    event_type: EventType = EventType.TASK_CREATED
    task_name: str = ""
    description: str = ""


class TaskStarted(Event):
    """Evento de início de tarefa."""

    event_type: EventType = EventType.TASK_STARTED
    agent: str | None = None


class TaskCompleted(Event):
    """Evento de conclusão de tarefa."""

    event_type: EventType = EventType.TASK_COMPLETED
    duration_seconds: float | None = None


class TaskFailed(Event):
    """Evento de falha de tarefa."""

    event_type: EventType = EventType.TASK_FAILED
    error_message: str = ""
    error_type: str | None = None


class StepStarted(Event):
    """Evento de início de etapa."""

    event_type: EventType = EventType.STEP_STARTED
    step_name: str = ""


class StepCompleted(Event):
    """Evento de conclusão de etapa."""

    event_type: EventType = EventType.STEP_COMPLETED
    step_name: str = ""
    duration_seconds: float | None = None


class ModelCalled(Event):
    """Evento de chamada de modelo."""

    event_type: EventType = EventType.MODEL_CALLED
    model_id: str = ""
    provider: str = ""
    tokens_input: int | None = None
    tokens_output: int | None = None
    cost_usd: float | None = None
    duration_ms: float | None = None


class ToolCalled(Event):
    """Evento de chamada de ferramenta."""

    event_type: EventType = EventType.TOOL_CALLED
    tool_name: str = ""
    tool_args: dict[str, Any] = Field(default_factory=dict)
    duration_ms: float | None = None


class ErrorRecorded(Event):
    """Evento de erro registrado."""

    event_type: EventType = EventType.ERROR_RECORDED
    error_message: str = ""
    error_type: str | None = None
    severity: str = "error"


class ResultRecorded(Event):
    """Evento de resultado de teste registrado."""

    event_type: EventType = EventType.TEST_EXECUTED
    test_name: str = ""
    test_file: str | None = None
    passed: bool = False
    duration_seconds: float | None = None


class ExecutionCompleted(Event):
    """Evento de execução concluída."""

    event_type: EventType = EventType.EXECUTION_COMPLETED
    total_duration_seconds: float | None = None
    total_tokens: int | None = None
    total_cost_usd: float | None = None
