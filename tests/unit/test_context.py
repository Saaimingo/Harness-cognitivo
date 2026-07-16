"""
Testes unitários para os contratos de contexto — FI-1.

Cobre:
- Criação de schemas com Enums e Field(default_factory)
- Validação de formato de IDs
- Rejeição de IDs inválidos
- Detecção de IDs duplicados
- Serialização/deserialização
- Separação object_type vs trust_level
- EvidenceReference
"""

from datetime import UTC, datetime

import pytest

from harness.contracts.context import (
    ChecksumAlgorithm,
    CognitiveObject,
    ContextCapsule,
    ContextItem,
    ContextRequest,
    EvidenceReference,
    ObjectType,
    Purpose,
    TrustLevel,
    check_duplicate_ids,
    validate_id_format,
)

# =============================================================================
# TESTES DE VOCABULÁRIO CONTROLADO (Enums)
# =============================================================================


class TestEnums:
    """Testes para os Enums de vocabulário controlado."""

    def test_purpose_values(self):
        """Purpose deve ter todos os valores definidos."""
        assert Purpose.DISCOVER_PROJECT == "discover_project"
        assert Purpose.IMPLEMENT_TASK == "implement_task"
        assert Purpose.ANSWER_USER == "answer_user"
        assert len(Purpose) == 12

    def test_object_type_values(self):
        """ObjectType deve ter todos os valores definidos."""
        assert ObjectType.FACT == "fact"
        assert ObjectType.HYPOTHESIS == "hypothesis"
        assert ObjectType.INFERENCE == "inference"
        assert ObjectType.DECISION == "decision"
        assert len(ObjectType) == 9

    def test_trust_level_values(self):
        """TrustLevel deve ter todos os valores definidos."""
        assert TrustLevel.OWNER_DECLARED == "owner_declared"
        assert TrustLevel.VERIFIED == "verified"
        assert TrustLevel.INFERRED == "inferred"
        assert len(TrustLevel) == 6

    def test_checksum_algorithm_values(self):
        """ChecksumAlgorithm deve ter valores corretos."""
        assert ChecksumAlgorithm.SHA256 == "sha256"
        assert ChecksumAlgorithm.SHA512 == "sha512"
        assert ChecksumAlgorithm.MD5 == "md5"

    def test_purpose_rejects_arbitrary_text(self):
        """Purpose deve rejeitar texto arbitrário."""
        with pytest.raises(ValueError):
            Purpose("texto_invalido")

    def test_object_type_rejects_arbitrary_text(self):
        """ObjectType deve rejeitar texto arbitrário."""
        with pytest.raises(ValueError):
            ObjectType("texto_invalido")

    def test_trust_level_rejects_arbitrary_text(self):
        """TrustLevel deve rejeitar texto arbitrário."""
        with pytest.raises(ValueError):
            TrustLevel("texto_invalido")


# =============================================================================
# TESTES DE VALIDAÇÃO DE IDs
# =============================================================================


class TestIDValidation:
    """Testes para validação de formato de IDs."""

    def test_valid_ids(self):
        """IDs com formato válido devem ser aceitos."""
        valid_ids = [
            "prj_abc123",
            "tsk_def456",
            "evt_789ghi",
            "req_abc",
            "capsule_xyz123",
            "a1_b2c3",
        ]
        for id_val in valid_ids:
            assert validate_id_format(id_val) == id_val

    def test_invalid_ids_rejected(self):
        """IDs com formato inválido devem ser rejeitados."""
        invalid_ids = [
            "abc123",  # sem underscore
            "_abc123",  # começa com underscore
            "123_abc",  # começa com número
            "Prj_abc123",  # maiúscula no prefixo
            "prj_",  # termina com underscore
            "prj-abc123",  # hífen em vez de underscore
            "",  # vazio
            "prj abc123",  # espaço
        ]
        for id_val in invalid_ids:
            with pytest.raises(ValueError, match="ID inválido"):
                validate_id_format(id_val)

    def test_duplicate_ids_detected(self):
        """IDs duplicados devem ser detectados."""
        ids = ["prj_abc", "tsk_def", "prj_abc", "evt_ghi", "tsk_def"]
        duplicates = check_duplicate_ids(ids)
        assert "prj_abc" in duplicates
        assert "tsk_def" in duplicates
        assert len(duplicates) == 2

    def test_no_duplicates_when_unique(self):
        """Lista sem duplicatas deve retornar lista vazia."""
        ids = ["prj_abc", "tsk_def", "evt_ghi"]
        duplicates = check_duplicate_ids(ids)
        assert duplicates == []


# =============================================================================
# TESTES DE EVIDENCE_REFERENCE
# =============================================================================


class TestEvidenceReference:
    """Testes para o contrato EvidenceReference."""

    def test_creation_with_defaults(self):
        """EvidenceReference deve ser criado com defaults corretos."""
        ref = EvidenceReference(
            evidence_id="evd_test123",
            source_description="Teste unitário",
            checksum="abc123def456",
            location="/tmp/test.txt",
        )
        assert ref.algorithm == ChecksumAlgorithm.SHA256
        assert ref.size_bytes is None
        assert isinstance(ref.captured_at, datetime)

    def test_creation_with_all_fields(self):
        """EvidenceReference deve aceitar todos os campos."""
        ref = EvidenceReference(
            evidence_id="evd_test123",
            source_description="Fonte de teste",
            checksum="sha256hash",
            algorithm=ChecksumAlgorithm.SHA512,
            location="/evidence/test.json",
            captured_at=datetime(2026, 1, 1, tzinfo=UTC),
            size_bytes=1024,
        )
        assert ref.algorithm == ChecksumAlgorithm.SHA512
        assert ref.size_bytes == 1024

    def test_invalid_evidence_id_rejected(self):
        """EvidenceReference deve rejeitar ID inválido."""
        with pytest.raises(ValueError):
            EvidenceReference(
                evidence_id="invalid-id",
                source_description="Teste",
                checksum="abc",
                location="/tmp/test.txt",
            )


# =============================================================================
# TESTES DE CONTEXT_REQUEST
# =============================================================================


class TestContextRequest:
    """Testes para o contrato ContextRequest."""

    def test_creation_minimal(self):
        """ContextRequest deve ser criado com campos obrigatórios."""
        req = ContextRequest(
            query_id="qry_test123",
            purpose=Purpose.IMPLEMENT_TASK,
            requesting_role="implementador",
            objective="Implementar módulo X",
        )
        assert req.query_id == "qry_test123"
        assert req.purpose == Purpose.IMPLEMENT_TASK
        assert req.project_id is None
        assert req.task_id is None
        assert req.required_object_types == []
        assert req.limits == {}

    def test_creation_complete(self):
        """ContextRequest deve aceitar todos os campos."""
        req = ContextRequest(
            query_id="qry_test123",
            project_id="prj_abc123",
            task_id="tsk_def456",
            purpose=Purpose.DESIGN_ARCHITECTURE,
            requesting_role="arquiteto",
            objective="Projetar módulo de persistência",
            required_object_types=[ObjectType.FACT, ObjectType.DECISION],
            limits={"max_items": 10},
        )
        assert req.project_id == "prj_abc123"
        assert len(req.required_object_types) == 2
        assert req.limits["max_items"] == 10

    def test_invalid_query_id_rejected(self):
        """ContextRequest deve rejeitar query_id inválido."""
        with pytest.raises(ValueError, match="ID inválido"):
            ContextRequest(
                query_id="invalid",
                purpose=Purpose.ANSWER_USER,
                requesting_role="user",
                objective="Pergunta",
            )

    def test_invalid_purpose_rejected(self):
        """ContextRequest deve rejeitar purpose inválido."""
        with pytest.raises(ValueError):
            ContextRequest(
                query_id="qry_test123",
                purpose="invalid_purpose",
                requesting_role="user",
                objective="Teste",
            )

    def test_default_factory_lists(self):
        """required_object_types e limits devem ser independentes entre instâncias."""
        req1 = ContextRequest(
            query_id="qry_one123",
            purpose=Purpose.ANSWER_USER,
            requesting_role="user",
            objective="Teste 1",
        )
        req2 = ContextRequest(
            query_id="qry_two123",
            purpose=Purpose.ANSWER_USER,
            requesting_role="user",
            objective="Teste 2",
        )
        req1.required_object_types.append(ObjectType.FACT)
        assert req2.required_object_types == []


# =============================================================================
# TESTES DE CONTEXT_ITEM E CAPSULE
# =============================================================================


class TestContextItem:
    """Testes para o contrato ContextItem."""

    def test_creation(self):
        """ContextItem deve ser criado corretamente."""
        item = ContextItem(
            object_id="obj_test123",
            object_type=ObjectType.FACT,
            content="O sistema usa Python 3.12",
            trust_level=TrustLevel.VERIFIED,
        )
        assert item.object_type == ObjectType.FACT
        assert item.trust_level == TrustLevel.VERIFIED
        assert item.evidence == []

    def test_separation_object_type_trust_level(self):
        """object_type e trust_level devem ser independentes."""
        item = ContextItem(
            object_id="obj_test123",
            object_type=ObjectType.HYPOTHESIS,
            content="Pode ser que X",
            trust_level=TrustLevel.INFERRED,
        )
        assert item.object_type == ObjectType.HYPOTHESIS
        assert item.trust_level == TrustLevel.INFERRED


class TestContextCapsule:
    """Testes para o contrato ContextCapsule."""

    def test_creation(self):
        """ContextCapsule deve ser criado corretamente."""
        capsule = ContextCapsule(
            capsule_id="cap_test123",
            query_id="qry_test123",
        )
        assert capsule.items == []
        assert capsule.missing_context == []
        assert isinstance(capsule.generated_at, datetime)

    def test_with_items(self):
        """ContextCapsule deve aceitar itens."""
        capsule = ContextCapsule(
            capsule_id="cap_test123",
            query_id="qry_test123",
            items=[
                ContextItem(
                    object_id="obj_one123",
                    object_type=ObjectType.FACT,
                    content="Fato 1",
                    trust_level=TrustLevel.VERIFIED,
                ),
            ],
        )
        assert len(capsule.items) == 1

    def test_invalid_ids_rejected(self):
        """ContextCapsule deve rejeitar IDs inválidos."""
        with pytest.raises(ValueError, match="ID inválido"):
            ContextCapsule(
                capsule_id="invalid",
                query_id="qry_test123",
            )


# =============================================================================
# TESTES DE COGNITIVE_OBJECT
# =============================================================================


class TestCognitiveObject:
    """Testes para o contrato CognitiveObject."""

    def test_creation(self):
        """CognitiveObject deve ser criado corretamente."""
        obj = CognitiveObject(
            object_id="cog_test123",
            object_type=ObjectType.FACT,
            content="O projeto usa uv para gerenciamento de dependências",
        )
        assert obj.trust_level == TrustLevel.UNVERIFIED
        assert obj.relations == []
        assert obj.evidence == []

    def test_separation_object_type_trust_level(self):
        """object_type e trust_level devem ser independentes e semânticos."""
        obj = CognitiveObject(
            object_id="cog_test123",
            object_type=ObjectType.INFERENCE,
            content="Possivelmente o sistema precisa de cache",
            trust_level=TrustLevel.INFERRED,
        )
        assert obj.object_type == ObjectType.INFERENCE
        assert obj.trust_level == TrustLevel.INFERRED

    def test_with_evidence(self):
        """CognitiveObject deve aceitar evidências."""
        obj = CognitiveObject(
            object_id="cog_test123",
            object_type=ObjectType.FACT,
            content="Fato com evidência",
            evidence=[
                EvidenceReference(
                    evidence_id="evd_test123",
                    source_description="Teste",
                    checksum="abc123",
                    location="/tmp/test.txt",
                ),
            ],
        )
        assert len(obj.evidence) == 1


# =============================================================================
# TESTES DE SERIALIZAÇÃO
# =============================================================================


class TestSerialization:
    """Testes de serialização dos schemas."""

    def test_context_request_json_roundtrip(self):
        """ContextRequest deve serializar e desserializar corretamente."""
        req = ContextRequest(
            query_id="qry_test123",
            purpose=Purpose.IMPLEMENT_TASK,
            requesting_role="implementador",
            objective="Teste",
        )
        json_str = req.model_dump_json()
        req2 = ContextRequest.model_validate_json(json_str)
        assert req.query_id == req2.query_id
        assert req.purpose == req2.purpose

    def test_capsule_json_roundtrip(self):
        """ContextCapsule deve serializar e desserializar corretamente."""
        capsule = ContextCapsule(
            capsule_id="cap_test123",
            query_id="qry_test123",
            items=[
                ContextItem(
                    object_id="obj_test123",
                    object_type=ObjectType.FACT,
                    content="Teste",
                    trust_level=TrustLevel.VERIFIED,
                ),
            ],
        )
        json_str = capsule.model_dump_json()
        capsule2 = ContextCapsule.model_validate_json(json_str)
        assert capsule.capsule_id == capsule2.capsule_id
        assert len(capsule2.items) == 1
