"""
Harness Cognitivo - Sistema Operacional de IA

Um sistema capaz de receber uma tarefa, entender seu contexto, planejar sua execução,
selecionar modelos e ferramentas, controlar custo e tempo, executar o trabalho,
testar o resultado, revisar possíveis falhas, registrar evidências e manter
continuidade entre sessões.

Versão: 0.1.0 (FI-0 - Fundação)
"""

__version__ = "0.1.0"
__author__ = "Saimon"
__status__ = "development"
__phase__ = "FI-0"

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

from harness.contracts.context import (
    Purpose,
    ObjectType,
    TrustLevel,
    ChecksumAlgorithm,
    EvidenceReference,
    ContextRequest,
    ContextItem,
    ContextCapsule,
    CognitiveObject,
)

__all__ = [
    "__version__",
    "__author__",
    "__status__",
    "__phase__",
    # Eventos
    "Event",
    "EventType",
    "TaskCreated",
    "TaskStarted",
    "TaskCompleted",
    "TaskFailed",
    "StepStarted",
    "StepCompleted",
    "ModelCalled",
    "ToolCalled",
    "ErrorRecorded",
    "ResultRecorded",
    "ExecutionCompleted",
    # Contratos de contexto (FI-1)
    "Purpose",
    "ObjectType",
    "TrustLevel",
    "ChecksumAlgorithm",
    "EvidenceReference",
    "ContextRequest",
    "ContextItem",
    "ContextCapsule",
    "CognitiveObject",
]


def main() -> None:
    """Ponto de entrada principal para o CLI."""
    from harness.cli import app
    app()
