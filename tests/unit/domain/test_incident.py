"""
Testes completos para a entidade Incident — FI-2B Parte 2.
Cobre: construção, validações, transições, invariantes, serialização,
severidades, referências a releases e GateDecision.
"""

from datetime import UTC, datetime

import pytest

from harness.domain.enums import IncidentSeverityLevel, IncidentState
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.incident import Incident
from harness.domain.transitions import INCIDENT_TERMINAL


def make_incident(
    state: IncidentState = IncidentState.DETECTED,
    severity: IncidentSeverityLevel = IncidentSeverityLevel.MEDIUM,
    **overrides,
) -> Incident:
    """Helper para criar Incident com estado específico."""
    kwargs: dict = {
        "incident_id": "inc_test001",
        "title": "Falha no deploy",
        "description": "Deploy falhou no ambiente staging",
        "severity": severity,
        "state": state,
        "impact": "Serviço indisponível por 5 minutos",
    }
    if severity == IncidentSeverityLevel.CRITICAL:
        kwargs["responsible"] = overrides.pop("responsible", "saimon")
    if state == IncidentState.CONTAINED:
        kwargs["containment_actions"] = overrides.pop(
            "containment_actions", ["Rollback imediato"]
        )
    if state == IncidentState.RESOLVED:
        kwargs["corrective_actions"] = overrides.pop(
            "corrective_actions", ["Corrigido script de deploy"]
        )
        kwargs["resolved_at"] = overrides.pop(
            "resolved_at",
            datetime(2026, 7, 1, 12, 0, tzinfo=UTC),
        )
        kwargs.setdefault(
            "detected_at",
            datetime(2026, 7, 1, 10, 0, tzinfo=UTC),
        )
    if state == IncidentState.CLOSED:
        kwargs["corrective_actions"] = overrides.pop(
            "corrective_actions", ["Corrigido script de deploy"]
        )
        kwargs["resolved_at"] = overrides.pop(
            "resolved_at",
            datetime(2026, 7, 1, 12, 0, tzinfo=UTC),
        )
        kwargs.setdefault(
            "detected_at",
            datetime(2026, 7, 1, 10, 0, tzinfo=UTC),
        )
        kwargs["close_record"] = overrides.pop(
            "close_record", "Incidente encerrado após validação"
        )
    kwargs.update(overrides)
    return Incident(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestIncidentConstruction:
    def test_creation_minimal(self):
        """Incident deve ser criado com campos mínimos."""
        inc = make_incident()
        assert inc.incident_id == "inc_test001"
        assert inc.state == IncidentState.DETECTED
        assert inc.severity == IncidentSeverityLevel.MEDIUM

    def test_creation_with_all_severities(self):
        """Incident deve aceitar todas as severidades."""
        for sev in IncidentSeverityLevel:
            inc = make_incident(severity=sev)
            assert inc.severity == sev

    def test_creation_critical_requires_responsible(self):
        """Incidente crítico exige responsável."""
        inc = make_incident(
            severity=IncidentSeverityLevel.CRITICAL,
            responsible="saimon",
        )
        assert inc.severity == IncidentSeverityLevel.CRITICAL
        assert inc.responsible == "saimon"

    def test_creation_with_related_releases(self):
        """Incident deve referenciar releases relacionadas."""
        inc = make_incident(
            related_release_ids=["rel_001", "rel_002"],
        )
        assert inc.related_release_ids == ["rel_001", "rel_002"]

    def test_creation_with_cause_hypothesis(self):
        """Incident deve aceitar hipótese de causa."""
        inc = make_incident(
            cause_hypothesis="Possível race condition no deploy",
        )
        assert inc.cause_hypothesis is not None
        assert inc.known_cause is None

    def test_creation_with_known_cause(self):
        """Incident deve aceitar causa confirmada."""
        inc = make_incident(
            known_cause="Variável de ambiente ausente",
        )
        assert inc.known_cause is not None

    def test_invalid_incident_id_rejected(self):
        """incident_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            Incident(
                incident_id="invalid-id",
                title="Falha",
                description="Descrição",
                severity=IncidentSeverityLevel.MEDIUM,
                impact="Impacto",
            )


# =============================================================================
# VALIDAÇÕES DE INVARIANTES
# =============================================================================


class TestIncidentInvariants:
    def test_description_required(self):
        """Incident sem descrição deve falhar."""
        with pytest.raises(InvariantViolationError, match="description"):
            Incident(
                incident_id="inc_test001",
                title="Falha",
                description="",
                severity=IncidentSeverityLevel.MEDIUM,
                impact="Impacto",
            )

    def test_impact_required(self):
        """Incident sem impacto deve falhar."""
        with pytest.raises(InvariantViolationError, match="impact"):
            Incident(
                incident_id="inc_test001",
                title="Falha",
                description="Descrição",
                severity=IncidentSeverityLevel.MEDIUM,
                impact="",
            )

    def test_critical_requires_responsible(self):
        """Incidente CRITICAL sem responsável deve falhar."""
        with pytest.raises(
            InvariantViolationError, match="critical_requires_responsible"
        ):
            Incident(
                incident_id="inc_test001",
                title="Falha crítica",
                description="Descrição",
                severity=IncidentSeverityLevel.CRITICAL,
                impact="Impacto severo",
            )

    def test_contained_requires_containment_actions(self):
        """CONTAINED sem ações de contenção deve falhar."""
        with pytest.raises(InvariantViolationError, match="containment_actions"):
            make_incident(
                state=IncidentState.CONTAINED,
                containment_actions=[],
            )

    def test_resolved_requires_corrective_actions(self):
        """RESOLVED sem ações corretivas deve falhar."""
        with pytest.raises(InvariantViolationError, match="corrective_actions"):
            make_incident(
                state=IncidentState.RESOLVED,
                corrective_actions=[],
            )

    def test_resolved_requires_resolved_at(self):
        """RESOLVED sem resolved_at deve falhar."""
        with pytest.raises(InvariantViolationError, match="resolved_at"):
            make_incident(
                state=IncidentState.RESOLVED,
                corrective_actions=["Correção"],
                resolved_at=None,
            )

    def test_closed_requires_close_record(self):
        """CLOSED sem close_record deve falhar."""
        with pytest.raises(InvariantViolationError, match="close_record"):
            make_incident(
                state=IncidentState.CLOSED,
                close_record="",
            )

    def test_closed_requires_resolved_at(self):
        """CLOSED sem resolved_at deve falhar."""
        with pytest.raises(InvariantViolationError, match="resolved_at"):
            make_incident(
                state=IncidentState.CLOSED,
                resolved_at=None,
            )

    def test_resolved_at_not_before_detected_at(self):
        """resolved_at não pode anteceder detected_at."""
        with pytest.raises(
            InvariantViolationError, match="resolved_not_before_detected"
        ):
            Incident(
                incident_id="inc_test001",
                title="Falha",
                description="Descrição",
                severity=IncidentSeverityLevel.MEDIUM,
                impact="Impacto",
                state=IncidentState.RESOLVED,
                corrective_actions=["Correção"],
                detected_at=datetime(2026, 7, 2, tzinfo=UTC),
                resolved_at=datetime(2026, 7, 1, tzinfo=UTC),
            )

    def test_naive_datetime_rejected(self):
        """Incident rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            Incident(
                incident_id="inc_test001",
                title="Falha",
                description="Descrição",
                severity=IncidentSeverityLevel.MEDIUM,
                impact="Impacto",
                detected_at=datetime(2026, 1, 1),
            )


# =============================================================================
# TRANSIÇÕES PERMITIDAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (IncidentState.DETECTED, IncidentState.TRIAGED),
        (IncidentState.TRIAGED, IncidentState.CONTAINED),
        (IncidentState.TRIAGED, IncidentState.INVESTIGATING),
        (IncidentState.CONTAINED, IncidentState.INVESTIGATING),
        (IncidentState.INVESTIGATING, IncidentState.FIXING),
        (IncidentState.FIXING, IncidentState.RESOLVED),
        (IncidentState.RESOLVED, IncidentState.CLOSED),
    ],
)
def test_incident_valid_transitions(current: IncidentState, target: IncidentState):
    """Transições válidas devem ser aceitas."""
    inc = make_incident(state=current)
    kwargs: dict = {}
    if target == IncidentState.CONTAINED:
        kwargs = {"containment_actions": ["Rollback imediato"]}
    if target == IncidentState.RESOLVED:
        kwargs = {"corrective_actions": ["Correção aplicada"]}
    if target == IncidentState.CLOSED:
        kwargs = {"close_record": "Encerrado após validação"}
    new_inc = inc.transition_to(target, **kwargs)
    assert new_inc.state == target


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (IncidentState.DETECTED, IncidentState.RESOLVED),  # pula etapas
        (IncidentState.DETECTED, IncidentState.CLOSED),
        (IncidentState.CLOSED, IncidentState.INVESTIGATING),  # terminal
        (IncidentState.RESOLVED, IncidentState.DETECTED),  # não volta
        (IncidentState.FIXING, IncidentState.DETECTED),
    ],
)
def test_incident_invalid_transitions_rejected(
    current: IncidentState, target: IncidentState
):
    """Transições inválidas devem ser rejeitadas."""
    inc = make_incident(state=current)
    with pytest.raises(InvalidTransitionError):
        inc.transition_to(target)


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================


def test_incident_terminal_state():
    """Incident em CLOSED é terminal."""
    inc = make_incident(state=IncidentState.CLOSED)
    assert inc.is_terminal


def test_incident_non_terminal_states():
    """Estados não-terminais não são marcados como is_terminal."""
    for state in IncidentState:
        if state not in INCIDENT_TERMINAL:
            inc = make_incident(state=state)
            assert not inc.is_terminal


# =============================================================================
# IDEMPOTÊNCIA E IMUTABILIDADE
# =============================================================================


def test_incident_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    inc = make_incident(state=IncidentState.DETECTED)
    result = inc.transition_to(IncidentState.DETECTED)
    assert result is inc


def test_incident_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição."""
    inc = make_incident(state=IncidentState.DETECTED)
    original_state = inc.state
    _ = inc.transition_to(IncidentState.TRIAGED)
    assert inc.state == original_state


def test_incident_version_increments():
    """Versão incrementa a cada transição."""
    inc = make_incident(state=IncidentState.DETECTED)
    new_inc = inc.transition_to(IncidentState.TRIAGED)
    assert new_inc.version == inc.version + 1


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


def test_incident_json_roundtrip():
    """Incident deve serializar e desserializar corretamente."""
    inc = make_incident(
        state=IncidentState.TRIAGED,
        severity=IncidentSeverityLevel.HIGH,
    )
    json_str = inc.model_dump_json()
    inc2 = Incident.model_validate_json(json_str)
    assert inc.incident_id == inc2.incident_id
    assert inc.state == inc2.state
    assert inc.severity == inc2.severity


def test_incident_dict_roundtrip():
    """Incident deve serializar e reconstruir via dict."""
    inc = make_incident(state=IncidentState.INVESTIGATING)
    data = inc.model_dump()
    inc2 = Incident.model_validate(data)
    assert inc == inc2


# =============================================================================
# FLUXO COMPLETO
# =============================================================================


def test_incident_full_lifecycle():
    """Fluxo completo: detected → triaged → investigating → fixing → resolved → closed."""
    inc = make_incident(state=IncidentState.DETECTED)
    assert inc.state == IncidentState.DETECTED

    inc = inc.transition_to(IncidentState.TRIAGED)
    assert inc.state == IncidentState.TRIAGED

    inc = inc.transition_to(IncidentState.INVESTIGATING)
    assert inc.state == IncidentState.INVESTIGATING

    inc = inc.transition_to(IncidentState.FIXING)
    assert inc.state == IncidentState.FIXING

    inc = inc.transition_to(
        IncidentState.RESOLVED,
        corrective_actions=["Corrigido script de deploy"],
    )
    assert inc.state == IncidentState.RESOLVED
    assert inc.resolved_at is not None

    inc = inc.transition_to(
        IncidentState.CLOSED,
        close_record="Validado em staging, sem regressão",
    )
    assert inc.state == IncidentState.CLOSED
    assert inc.is_terminal


# =============================================================================
# FLUXO COM CONTENÇÃO
# =============================================================================


def test_incident_containment_flow():
    """Fluxo: detected → triaged → contained → investigating → ..."""
    inc = make_incident(state=IncidentState.DETECTED)
    inc = inc.transition_to(IncidentState.TRIAGED)
    inc = inc.transition_to(
        IncidentState.CONTAINED,
        containment_actions=["Bloquear endpoint afetado"],
    )
    assert inc.state == IncidentState.CONTAINED
    assert inc.containment_actions == ["Bloquear endpoint afetado"]
    assert not inc.is_terminal


# =============================================================================
# REFERÊNCIAS A RELEASES E GATEDECISION
# =============================================================================


class TestIncidentReferences:
    def test_related_release_ids(self):
        """Incident referencia releases relacionadas."""
        inc = make_incident(
            related_release_ids=["rel_001", "rel_002"],
        )
        assert "rel_001" in inc.related_release_ids

    def test_resolution_gate_decision(self):
        """Incident pode originar GateDecision na resolução."""
        inc = make_incident(
            resolution_gate_decision_id="gd_resolution001",
        )
        assert inc.resolution_gate_decision_id == "gd_resolution001"


# =============================================================================
# CAUSA CONFIRMADA vs HIPÓTESE
# =============================================================================


class TestIncidentCauseSeparation:
    def test_hypothesis_not_confused_with_known_cause(self):
        """Hipótese e causa confirmada são campos separados."""
        inc = make_incident(
            known_cause="Variável de ambiente ausente",
            cause_hypothesis="Possível race condition",
        )
        assert inc.known_cause == "Variável de ambiente ausente"
        assert inc.cause_hypothesis == "Possível race condition"

    def test_hypothesis_without_known_cause(self):
        """Hipótese pode existir sem causa confirmada."""
        inc = make_incident(
            cause_hypothesis="Possível falha de rede",
        )
        assert inc.cause_hypothesis is not None
        assert inc.known_cause is None
