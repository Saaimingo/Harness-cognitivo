"""
Erros de domínio do Harness Cognitivo — FI-2.

Exceções específicas para violações de regras de negócio.
Não usar ValueError genérico como único mecanismo de erro.
"""


class DomainError(Exception):
    """Exceção base para erros de domínio do Harness."""

    def __init__(
        self, message: str, entity: str | None = None, state: str | None = None
    ):
        self.entity = entity
        self.state = state
        super().__init__(message)


class InvalidTransitionError(DomainError):
    """Exceção para transições de estado inválidas."""

    def __init__(
        self,
        entity: str,
        current_state: str,
        target_state: str,
        allowed: list[str] | None = None,
    ):
        self.current_state = current_state
        self.target_state = target_state
        self.allowed = allowed or []
        allowed_str = ", ".join(self.allowed) if self.allowed else "nenhum"
        message = (
            f"Transição inválida em {entity}: "
            f"{current_state} → {target_state}. "
            f"Estados permitidos: {allowed_str}"
        )
        super().__init__(message, entity=entity, state=current_state)


class InvariantViolationError(DomainError):
    """Exceção para violação de invariantes de domínio."""

    def __init__(self, entity: str, invariant: str, details: str = ""):
        self.invariant = invariant
        message = f"Invariante violado em {entity}: {invariant}"
        if details:
            message += f" — {details}"
        super().__init__(message, entity=entity)


class ReworkLimitExceededError(DomainError):
    """Exceção para limite de rework atingido."""

    def __init__(self, entity: str, task_id: str, limit: int, current: int):
        self.limit = limit
        self.current = current
        message = (
            f"Limite de rework atingido em {entity} {task_id}: "
            f"{current}/{limit} tentativas"
        )
        super().__init__(message, entity=entity)


class MissingAuthorityError(DomainError):
    """Exceção para operação que exige autoridade não fornecida."""

    def __init__(self, entity: str, operation: str):
        message = (
            f"Autoridade requerida para {operation} em {entity}: "
            f"autoridade identificável é obrigatória"
        )
        super().__init__(message, entity=entity)


class MissingEvidenceError(DomainError):
    """Exceção para operação que exige evidência não fornecida."""

    def __init__(self, entity: str, operation: str, required: str = ""):
        message = f"Evidência requerida para {operation} em {entity}"
        if required:
            message += f": {required}"
        super().__init__(message, entity=entity)


class TimezoneRequiredError(DomainError):
    """Exceção para campo temporal sem timezone."""

    def __init__(self, entity: str, field: str):
        message = (
            f"Campo temporal '{field}' em {entity} requer timezone. "
            f"Use datetime com tzinfo."
        )
        super().__init__(message, entity=entity)
