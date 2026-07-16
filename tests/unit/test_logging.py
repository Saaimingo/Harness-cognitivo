"""
Testes unitários para o módulo de logging do Harness.
"""

from harness.logging import EventLogger, get_logger, setup_logging


class TestSetupLogging:
    """Testes para configuração de logging."""

    def test_setup_logging_default(self):
        """Setup com configurações padrão não deve falhar."""
        setup_logging()
        logger = get_logger("test")
        assert logger is not None

    def test_setup_logging_json(self):
        """Setup com saída JSON não deve falhar."""
        setup_logging(json_output=True)
        logger = get_logger("test_json")
        assert logger is not None

    def test_setup_logging_with_level(self):
        """Setup com nível específico não deve falhar."""
        setup_logging(level="DEBUG")
        logger = get_logger("test_debug")
        assert logger is not None


class TestGetLogger:
    """Testes para obtenção de logger."""

    def test_get_logger_returns_bound_logger(self):
        """get_logger deve retornar um logger configurado."""
        setup_logging()
        logger = get_logger("meu_modulo")
        assert logger is not None

    def test_get_logger_without_name(self):
        """get_logger deve funcionar sem nome."""
        setup_logging()
        logger = get_logger()
        assert logger is not None


class TestEventLogger:
    """Testes para o EventLogger."""

    def test_event_logger_creation(self):
        """EventLogger deve ser criado sem erros."""
        setup_logging()
        event_logger = EventLogger()
        assert event_logger is not None

    def test_log_event(self):
        """log_event deve registrar evento sem falhas."""
        setup_logging()
        event_logger = EventLogger()
        # Não deve lançar exceção
        event_logger.log_event("test.event", key="value")

    def test_log_task_created(self):
        """log_task_created deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_task_created(
            task_id="task-123",
            task_name="minha-tarefa",
        )

    def test_log_task_started(self):
        """log_task_started deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_task_started(task_id="task-123")

    def test_log_task_completed(self):
        """log_task_completed deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_task_completed(
            task_id="task-123",
            duration_seconds=10.5,
        )

    def test_log_task_failed(self):
        """log_task_failed deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_task_failed(
            task_id="task-123",
            error="Algo deu errado",
        )

    def test_log_model_called(self):
        """log_model_called deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_model_called(
            model_id="gpt-4",
            provider="openai",
            tokens_input=100,
            tokens_output=50,
            cost_usd=0.01,
            duration_ms=500,
        )

    def test_log_tool_called(self):
        """log_tool_called deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_tool_called(
            tool_name="read_file",
            duration_ms=50,
        )

    def test_log_error(self):
        """log_error deve funcionar."""
        setup_logging()
        event_logger = EventLogger()
        event_logger.log_error(
            error_type="ValueError",
            error_message="Valor inválido",
            severity="warning",
        )
