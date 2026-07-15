"""
Regras de IDs do domínio Harness Cognitivo — FI-2.

Reutiliza a validação de IDs criada na FI-1.
Não cria segunda expressão regular ou mecanismo incompatível.
"""

from harness.contracts.context import validate_id_format, check_duplicate_ids


# Re-exportar funções de validação da FI-1
__all__ = ["validate_id_format", "check_duplicate_ids"]
