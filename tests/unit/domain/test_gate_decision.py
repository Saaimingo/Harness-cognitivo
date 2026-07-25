"""
Testes completos para a entidade GateDecision — FI-2B Parte 2.
Cobre: construção, validações, invariantes, serialização.
GateDecision não possui transições (registro imutável).
"""

from datetime import datetime

import pytest

from harness.domain.enums import GateDecisionState
from harness.domain.errors import InvariantViolationError
from harness.domain.gate_decision import GateDecision


def make_gate_decision(
    decision_state: GateDecisionState = GateDecisionState.APPROVED,
    **overrides,
) -> GateDecision:
    """Helper para criar GateDecision com estado específico."""
    kwargs: dict = {
        "gate_decision_id": "gd_test001",
        "target": "plan_test123",
        "gate_stage": "architectural",
        "decision_state": decision_state,
        "justification": "Decisão de teste",
        "evidence_ids": ["ev_001"],
    }
    if decision_state in (GateDecisionState.BLOCKED, GateDecisionState.REJECTED):
        kwargs["blockers"] = overrides.pop("blockers", ["Falha em teste crítico"])
        kwargs.pop("evidence_ids", None)
    if decision_state == GateDecisionState.REWORK_REQUIRED:
        kwargs["corrective_actions"] = overrides.pop(
            "corrective_actions", ["Refatorar módulo X"]
        )
        kwargs.pop("evidence_ids", None)
    kwargs.update(overrides)
    return GateDecision(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestGateDecisionConstruction:
    def test_creation_approved(self):
        """GateDecision aprovado deve ser criado com evidência e justificativa."""
        gd = make_gate_decision()
        assert gd.gate_decision_id == "gd_test001"
        assert gd.decision_state == GateDecisionState.APPROVED
        assert gd.justification == "Decisão de teste"
        assert len(gd.evidence_ids) > 0

    def test_creation_approved_with_reservations(self):
        """GateDecision com ressalvas deve ser criado."""
        gd = make_gate_decision(
            decision_state=GateDecisionState.APPROVED_WITH_RESERVATIONS,
        )
        assert gd.decision_state == GateDecisionState.APPROVED_WITH_RESERVATIONS
        assert len(gd.evidence_ids) > 0

    def test_creation_blocked(self):
        """GateDecision bloqueado deve informar blockers."""
        gd = make_gate_decision(
            decision_state=GateDecisionState.BLOCKED,
            blockers=["Sem cobertura de testes"],
        )
        assert gd.decision_state == GateDecisionState.BLOCKED
        assert len(gd.blockers) > 0

    def test_creation_rejected(self):
        """GateDecision rejeitado deve informar blockers."""
        gd = make_gate_decision(
            decision_state=GateDecisionState.REJECTED,
            blockers=["Violação de invariante arquitetural"],
        )
        assert gd.decision_state == GateDecisionState.REJECTED
        assert len(gd.blockers) > 0

    def test_creation_rework_required(self):
        """GateDecision com rework deve possuir ações corretivas."""
        gd = make_gate_decision(
            decision_state=GateDecisionState.REWORK_REQUIRED,
            corrective_actions=["Adicionar testes de regressão"],
        )
        assert gd.decision_state == GateDecisionState.REWORK_REQUIRED
        assert len(gd.corrective_actions) > 0

    def test_creation_with_authority(self):
        """GateDecision deve aceitar autoridade."""
        gd = make_gate_decision(authority="tubarao")
        assert gd.authority == "tubarao"

    def test_creation_with_previous_decision(self):
        """GateDecision deve referenciar decisão anterior sem alterá-la."""
        gd = make_gate_decision(previous_decision_id="gd_prev001")
        assert gd.previous_decision_id == "gd_prev001"

    def test_invalid_gate_decision_id_rejected(self):
        """gate_decision_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            GateDecision(
                gate_decision_id="invalid-id",
                target="plan_test123",
                decision_state=GateDecisionState.APPROVED,
                justification="Teste",
                evidence_ids=["ev_001"],
            )


# =============================================================================
# VALIDAÇÕES DE INVARIANTES
# =============================================================================


class TestGateDecisionInvariants:
    def test_justification_required(self):
        """GateDecision sem justificativa deve falhar."""
        with pytest.raises(InvariantViolationError, match="justification"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.APPROVED,
                justification="",
                evidence_ids=["ev_001"],
            )

    def test_approved_requires_evidence(self):
        """APPROVED sem evidência deve falhar."""
        with pytest.raises(InvariantViolationError, match="evidence"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.APPROVED,
                justification="Aprovado",
            )

    def test_approved_with_reservations_requires_evidence(self):
        """APPROVED_WITH_RESERVATIONS sem evidência deve falhar."""
        with pytest.raises(InvariantViolationError, match="evidence"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.APPROVED_WITH_RESERVATIONS,
                justification="Aprovado com ressalvas",
            )

    def test_blocked_requires_blockers(self):
        """BLOCKED sem blockers deve falhar."""
        with pytest.raises(InvariantViolationError, match="blockers"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.BLOCKED,
                justification="Bloqueado",
            )

    def test_rejected_requires_blockers(self):
        """REJECTED sem blockers deve falhar."""
        with pytest.raises(InvariantViolationError, match="blockers"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.REJECTED,
                justification="Rejeitado",
            )

    def test_rework_requires_corrective_actions(self):
        """REWORK_REQUIRED sem ações corretivas deve falhar."""
        with pytest.raises(InvariantViolationError, match="corrective"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.REWORK_REQUIRED,
                justification="Corrigir",
            )

    def test_naive_datetime_rejected(self):
        """GateDecision rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            GateDecision(
                gate_decision_id="gd_test001",
                target="plan_test123",
                decision_state=GateDecisionState.APPROVED,
                justification="Teste",
                evidence_ids=["ev_001"],
                decided_at=datetime(2026, 1, 1),
            )


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


class TestGateDecisionSerialization:
    def test_json_roundtrip(self):
        """GateDecision deve serializar e desserializar corretamente."""
        gd = make_gate_decision(authority="tubarao")
        json_str = gd.model_dump_json()
        gd2 = GateDecision.model_validate_json(json_str)
        assert gd.gate_decision_id == gd2.gate_decision_id
        assert gd.decision_state == gd2.decision_state
        assert gd.justification == gd2.justification
        assert gd.authority == gd2.authority

    def test_dict_roundtrip(self):
        """GateDecision deve serializar e reconstruir via dict."""
        gd = make_gate_decision()
        data = gd.model_dump()
        gd2 = GateDecision.model_validate(data)
        assert gd == gd2


# =============================================================================
# REFERÊNCIAS ENTRE MODELOS
# =============================================================================


class TestGateDecisionReferences:
    def test_references_are_preserved(self):
        """GateDecision preserva referências (evidências, critérios, decisão anterior)."""
        gd = GateDecision(
            gate_decision_id="gd_test001",
            target="plan_test123",
            decision_state=GateDecisionState.APPROVED_WITH_RESERVATIONS,
            justification="Aprovado com observações",
            evidence_ids=["ev_001", "ev_002"],
            evaluated_criteria=["req-01", "req-02"],
            previous_decision_id="gd_prev001",
        )
        assert gd.evidence_ids == ["ev_001", "ev_002"]
        assert gd.evaluated_criteria == ["req-01", "req-02"]
        assert gd.previous_decision_id == "gd_prev001"


# =============================================================================
# ESTADOS CONTRADITÓRIOS
# =============================================================================


class TestGateDecisionContradictoryStates:
    def test_approved_with_blockers_is_contradictory_logic(self):
        """APPROVED não pode ter blockers (regra de negócio, não de código).

        O código atual não impede blockers em APPROVED porque o campo é
        uma lista genérica. A regra de negócio diz que aprovado com blockers
        é contraditório — isso seria tratado em camada superior (política).
        """
        gd = GateDecision(
            gate_decision_id="gd_test001",
            target="plan_test123",
            decision_state=GateDecisionState.APPROVED,
            justification="Aprovado",
            evidence_ids=["ev_001"],
            blockers=["não deveria ter"],  # permitido pelo modelo, política decide
        )
        assert gd.decision_state == GateDecisionState.APPROVED
