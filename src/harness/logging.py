"""
Configuração de Logging Estruturado do Harness Cognitivo.

Utiliza structlog para logging estruturado e observável desde a primeira versão.
"""

from __future__ import annotations

import logging
import sys
from typing import Any

import structlog


def setup_logging(
    level: str = "INFO",
    json_output: bool = False,
    log_file: str | None = None,
) -> None:
    """
    Configurar logging estruturado para o Harness.

    Args:
        level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_output: Se True, saída em JSON. Se False, saída legível.
        log_file: Caminho para arquivo de log (opcional)
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if json_output:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=[
            *shared_processors,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )

    # Configurar logging padrão do Python para compatibilidade
    logging.basicConfig(
        format="%(message)s",
        level=logging.getLevelName(level),
        handlers=[logging.StreamHandler(sys.stderr)],
    )

    # Configurar handler de arquivo se especificado
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.getLevelName(level))
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """
    Obter logger estruturado.

    Args:
        name: Nome do logger (opcional)

    Returns:
        Logger configurado
    """
    return structlog.get_logger(name)


class EventLogger:
    """
    Logger de eventos para observabilidade.

    Registra eventos de execução de forma estruturada para posterior análise.
    """

    def __init__(self, logger: structlog.stdlib.BoundLogger | None = None):
        self._logger = logger or get_logger("harness.events")

    def log_event(
        self,
        event_type: str,
        **kwargs: Any,
    ) -> None:
        """
        Registrar um evento.

        Args:
            event_type: Tipo do evento
            **kwargs: Dados adicionais do evento
        """
        self._logger.info(
            "event",
            event_type=event_type,
            **kwargs,
        )

    def log_task_created(self, task_id: str, task_name: str, **kwargs: Any) -> None:
        """Registrar criação de tarefa."""
        self.log_event(
            "task.created",
            task_id=task_id,
            task_name=task_name,
            **kwargs,
        )

    def log_task_started(self, task_id: str, **kwargs: Any) -> None:
        """Registrar início de tarefa."""
        self.log_event("task.started", task_id=task_id, **kwargs)

    def log_task_completed(
        self, task_id: str, duration_seconds: float | None = None, **kwargs: Any
    ) -> None:
        """Registrar conclusão de tarefa."""
        self.log_event(
            "task.completed",
            task_id=task_id,
            duration_seconds=duration_seconds,
            **kwargs,
        )

    def log_task_failed(
        self, task_id: str, error: str, **kwargs: Any
    ) -> None:
        """Registrar falha de tarefa."""
        self.log_event(
            "task.failed",
            task_id=task_id,
            error=error,
            **kwargs,
        )

    def log_model_called(
        self,
        model_id: str,
        provider: str,
        tokens_input: int | None = None,
        tokens_output: int | None = None,
        cost_usd: float | None = None,
        duration_ms: float | None = None,
        **kwargs: Any,
    ) -> None:
        """Registrar chamada de modelo."""
        self.log_event(
            "model.called",
            model_id=model_id,
            provider=provider,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost_usd=cost_usd,
            duration_ms=duration_ms,
            **kwargs,
        )

    def log_tool_called(
        self,
        tool_name: str,
        duration_ms: float | None = None,
        **kwargs: Any,
    ) -> None:
        """Registrar chamada de ferramenta."""
        self.log_event(
            "tool.called",
            tool_name=tool_name,
            duration_ms=duration_ms,
            **kwargs,
        )

    def log_error(
        self,
        error_type: str,
        error_message: str,
        severity: str = "error",
        **kwargs: Any,
    ) -> None:
        """Registrar erro."""
        self.log_event(
            "error.recorded",
            error_type=error_type,
            error_message=error_message,
            severity=severity,
            **kwargs,
        )
