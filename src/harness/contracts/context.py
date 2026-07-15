"""
Contratos de Contexto do Harness Cognitivo — FI-1.

Define os schemas iniciais para solicitação e recuperação de contexto,
conforme o Protocolo de Integração Cognitiva (Doc 6).

Regras aplicadas:
- Vocabulário controlado via Enum (não texto arbitrário)
- Field(default_factory) para listas e dicionários mutáveis
- Separação entre object_type (natureza) e trust_level (confiança)
- Validação de formato para IDs
- EvidenceReference para fontes e checksums
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


# =============================================================================
# VOCABULÁRIO CONTROLADO — Enums
# =============================================================================

class Purpose(str, Enum):
    """Finalidade da solicitação de contexto."""
    DISCOVER_PROJECT = "discover_project"
    SPECIFY_REQUIREMENTS = "specify_requirements"
    DESIGN_ARCHITECTURE = "design_architecture"
    PLAN_TASKS = "plan_tasks"
    IMPLEMENT_TASK = "implement_task"
    REVIEW_CHANGESET = "review_changeset"
    DESIGN_TESTS = "design_tests"
    EVALUATE_GATE = "evaluate_gate"
    PREPARE_RELEASE = "prepare_release"
    INVESTIGATE_INCIDENT = "investigate_incident"
    PERFORM_MAINTENANCE = "perform_maintenance"
    ANSWER_USER = "answer_user"


class ObjectType(str, Enum):
    """Natureza do objeto cognitivo (o que ele É)."""
    FACT = "fact"
    HYPOTHESIS = "hypothesis"
    INFERENCE = "inference"
    DECISION = "decision"
    PREFERENCE = "preference"
    EVENT = "event"
    LESSON = "lesson"
    REQUIREMENT = "requirement"
    INCIDENT = "incident"


class TrustLevel(str, Enum):
    """Nível ou origem de confiança do objeto (QUÃO CONFIÁVEL é)."""
    OWNER_DECLARED = "owner_declared"
    VERIFIED = "verified"
    INFERRED = "inferred"
    OBSERVED = "observed"
    UNVERIFIED = "unverified"
    UNKNOWN = "unknown"


class ChecksumAlgorithm(str, Enum):
    """Algoritmos de checksum suportados."""
    SHA256 = "sha256"
    SHA512 = "sha512"
    MD5 = "md5"


# =============================================================================
# VALIDAÇÃO DE IDs
# =============================================================================

# Padrão aceito: prefixo_alfanumérico + underscore + alfanumérico
# Exemplos: prj_abc123, tsk_def456, evt_789ghi
ID_PATTERN = re.compile(r"^[a-z][a-z0-9]*_[a-zA-Z0-9]+$")


def validate_id_format(value: str) -> str:
    """Validar formato de ID: prefixo_snake_case com pelo menos um underscore."""
    if not ID_PATTERN.match(value):
        raise ValueError(
            f"ID inválido: '{value}'. "
            "Formato esperado: prefixo_snake_case (ex: prj_abc123, tsk_def456)"
        )
    return value


def check_duplicate_ids(ids: list[str]) -> list[str]:
    """Detectar IDs duplicados em uma lista."""
    seen: set[str] = set()
    duplicates: list[str] = []
    for id_val in ids:
        if id_val in seen:
            duplicates.append(id_val)
        seen.add(id_val)
    return duplicates


# =============================================================================
# EVIDÊNCIAS
# =============================================================================

class EvidenceReference(BaseModel):
    """Referência a uma evidência armazenada (fonte, checksum, localização)."""
    evidence_id: str = Field(description="ID único da evidência")
    source_description: str = Field(description="Descrição da fonte da evidência")
    checksum: str = Field(description="Valor do checksum")
    algorithm: ChecksumAlgorithm = Field(
        default=ChecksumAlgorithm.SHA256,
        description="Algoritmo usado no checksum"
    )
    location: str = Field(description="Caminho ou URI da evidência")
    captured_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data/hora de captura da evidência"
    )
    size_bytes: int | None = Field(
        default=None,
        description="Tamanho em bytes (opcional)"
    )

    @field_validator("evidence_id")
    @classmethod
    def validate_evidence_id(cls, v: str) -> str:
        return validate_id_format(v)


# =============================================================================
# SOLICITAÇÃO DE CONTEXTO
# =============================================================================

class ContextRequest(BaseModel):
    """Solicitação de contexto à MEC."""
    query_id: str = Field(description="ID único da consulta")
    project_id: str | None = Field(
        default=None,
        description="ID do projeto relacionado"
    )
    task_id: str | None = Field(
        default=None,
        description="ID da tarefa relacionada"
    )
    purpose: Purpose = Field(
        description="Finalidade da solicitação"
    )
    requesting_role: str = Field(
        description="Papel que solicita o contexto"
    )
    objective: str = Field(
        description="Objetivo da solicitação"
    )
    required_object_types: list[ObjectType] = Field(
        default_factory=list,
        description="Tipos de objetos cognitivos desejados"
    )
    limits: dict[str, Any] = Field(
        default_factory=dict,
        description="Limites da consulta (max_items, max_tokens, etc.)"
    )

    @field_validator("query_id")
    @classmethod
    def validate_query_id(cls, v: str) -> str:
        return validate_id_format(v)


# =============================================================================
# ITENS E CÁPSULA DE CONTEXTO
# =============================================================================

class ContextItem(BaseModel):
    """Item individual dentro de uma cápsula de contexto."""
    object_id: str = Field(description="ID do objeto cognitivo")
    object_type: ObjectType = Field(
        description="Natureza do objeto (fact, hypothesis, etc.)"
    )
    content: str = Field(description="Conteúdo do item")
    source: str | None = Field(
        default=None,
        description="Referência à fonte original"
    )
    trust_level: TrustLevel = Field(
        description="Nível de confiança no item"
    )
    relevance_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Score de relevância (0.0 a 1.0)"
    )
    evidence: list[EvidenceReference] = Field(
        default_factory=list,
        description="Evidências que sustentam este item"
    )

    @field_validator("object_id")
    @classmethod
    def validate_object_id(cls, v: str) -> str:
        return validate_id_format(v)


class ContextCapsule(BaseModel):
    """Cápsula de contexto recuperada da MEC."""
    capsule_id: str = Field(description="ID único da cápsula")
    query_id: str = Field(description="ID da consulta que gerou esta cápsula")
    items: list[ContextItem] = Field(
        default_factory=list,
        description="Itens de contexto recuperados"
    )
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data/hora de geração da cápsula"
    )
    expires_at: datetime | None = Field(
        default=None,
        description="Data/hora de expiração da cápsula"
    )
    fingerprint: str | None = Field(
        default=None,
        description="Fingerprint do contexto no momento da geração"
    )
    missing_context: list[str] = Field(
        default_factory=list,
        description="Descrição de contextos ausentes"
    )

    @field_validator("capsule_id")
    @classmethod
    def validate_capsule_id(cls, v: str) -> str:
        return validate_id_format(v)

    @field_validator("query_id")
    @classmethod
    def validate_query_id(cls, v: str) -> str:
        return validate_id_format(v)


# =============================================================================
# OBJETO COGNITIVO
# =============================================================================

class CognitiveObject(BaseModel):
    """Objeto cognitivo armazenado na MEC."""
    object_id: str = Field(description="ID único do objeto")
    object_type: ObjectType = Field(
        description="Natureza do objeto (fact, hypothesis, etc.)"
    )
    content: str = Field(description="Conteúdo do objeto")
    source_id: str | None = Field(
        default=None,
        description="ID da fonte que originou este objeto"
    )
    trust_level: TrustLevel = Field(
        default=TrustLevel.UNVERIFIED,
        description="Nível de confiança no objeto"
    )
    project_id: str | None = Field(
        default=None,
        description="ID do projeto relacionado"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data/hora de criação"
    )
    updated_at: datetime | None = Field(
        default=None,
        description="Data/hora da última atualização"
    )
    relations: list[str] = Field(
        default_factory=list,
        description="IDs de objetos relacionados"
    )
    evidence: list[EvidenceReference] = Field(
        default_factory=list,
        description="Evidências que sustentam este objeto"
    )

    @field_validator("object_id")
    @classmethod
    def validate_object_id(cls, v: str) -> str:
        return validate_id_format(v)
