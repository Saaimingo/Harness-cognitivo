"""
Testes completos para a entidade Release — FI-2B Parte 2.
Cobre: construção, validações, transições, invariantes, serialização,
referências a GateDecision.
"""

from datetime import UTC, datetime

import pytest

from harness.domain.enums import ReleaseState
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.release import Release
from harness.domain.transitions import RELEASE_TERMINAL


def make_release(
    state: ReleaseState = ReleaseState.CANDIDATE,
    **overrides,
) -> Release:
    """Helper para criar Release com estado específico."""
    kwargs: dict = {
        "release_id": "rel_test001",
        "name": "v1.0.0",
        "artifact_target": "harness-core",
        "environment": "staging",
        "state": state,
    }
    if state == ReleaseState.PROMOTED:
        kwargs["gate_decision_id"] = overrides.pop("gate_decision_id", "gd_test001")
        kwargs["versioned_origin"] = overrides.pop("versioned_origin", "abc123def")
        kwargs["rollback_plan"] = overrides.pop(
            "rollback_plan", "Reverter commit abc123def"
        )
        kwargs["promoted_at"] = overrides.pop(
            "promoted_at", datetime(2026, 7, 1, tzinfo=UTC)
        )
    if state == ReleaseState.REVERTED:
        kwargs["reverted_from_id"] = overrides.pop("reverted_from_id", "rel_failed001")
    kwargs.update(overrides)
    return Release(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestReleaseConstruction:
    def test_creation_minimal(self):
        """Release deve ser criado com campos mínimos."""
        rel = make_release()
        assert rel.release_id == "rel_test001"
        assert rel.name == "v1.0.0"
        assert rel.state == ReleaseState.CANDIDATE
        assert rel.gate_decision_id is None

    def test_creation_candidate(self):
        """Release candidata não exige gate_decision."""
        rel = make_release(state=ReleaseState.CANDIDATE)
        assert rel.state == ReleaseState.CANDIDATE

    def test_creation_authorized(self):
        """Release autorizada (aguardando promoção)."""
        rel = make_release(state=ReleaseState.AUTHORIZED)
        assert rel.state == ReleaseState.AUTHORIZED

    def test_creation_promoted(self):
        """Release promovida deve ter gate_decision, origem e rollback."""
        rel = make_release(state=ReleaseState.PROMOTED)
        assert rel.state == ReleaseState.PROMOTED
        assert rel.gate_decision_id == "gd_test001"
        assert rel.versioned_origin == "abc123def"
        assert rel.rollback_plan is not None
        assert rel.promoted_at is not None

    def test_creation_with_responsible(self):
        """Release deve aceitar responsável."""
        rel = make_release(responsible="tubarao")
        assert rel.responsible == "tubarao"

    def test_invalid_release_id_rejected(self):
        """release_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            Release(
                release_id="invalid-id",
                name="v1.0.0",
                artifact_target="harness-core",
            )


# =============================================================================
# VALIDAÇÕES DE INVARIANTES
# =============================================================================


class TestReleaseInvariants:
    def test_promoted_requires_gate_decision(self):
        """PROMOTED sem gate_decision_id deve falhar."""
        with pytest.raises(InvariantViolationError, match="gate_decision"):
            make_release(
                state=ReleaseState.PROMOTED,
                gate_decision_id=None,
            )

    def test_promoted_requires_versioned_origin(self):
        """PROMOTED sem versioned_origin deve falhar."""
        with pytest.raises(InvariantViolationError, match="versioned_origin"):
            make_release(
                state=ReleaseState.PROMOTED,
                versioned_origin=None,
            )

    def test_promoted_requires_rollback_plan(self):
        """PROMOTED sem rollback_plan deve falhar."""
        with pytest.raises(InvariantViolationError, match="rollback"):
            make_release(
                state=ReleaseState.PROMOTED,
                rollback_plan=None,
            )

    def test_reverted_requires_reverted_from(self):
        """REVERTED sem reverted_from_id deve falhar."""
        with pytest.raises(InvariantViolationError, match="reverted_from"):
            make_release(
                state=ReleaseState.REVERTED,
                reverted_from_id=None,
            )

    def test_naive_datetime_rejected(self):
        """Release rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            Release(
                release_id="rel_test001",
                name="v1.0.0",
                artifact_target="harness-core",
                created_at=datetime(2026, 1, 1),
            )


# =============================================================================
# TRANSIÇÕES PERMITIDAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ReleaseState.CANDIDATE, ReleaseState.AUTHORIZED),
        (ReleaseState.CANDIDATE, ReleaseState.CANCELLED),
        (ReleaseState.AUTHORIZED, ReleaseState.PROMOTED),
        (ReleaseState.AUTHORIZED, ReleaseState.CANCELLED),
        (ReleaseState.PROMOTED, ReleaseState.FAILED),
        (ReleaseState.PROMOTED, ReleaseState.REVERTED),
    ],
)
def test_release_valid_transitions(current: ReleaseState, target: ReleaseState):
    """Transições válidas devem ser aceitas."""
    rel = make_release(state=current)
    kwargs: dict = {}
    if target == ReleaseState.PROMOTED:
        kwargs = {
            "gate_decision_id": "gd_test001",
            "versioned_origin": "abc123def",
            "rollback_plan": "Reverter commit",
        }
    if target == ReleaseState.REVERTED:
        kwargs = {"reverted_from_id": "rel_failed001"}
    new_rel = rel.transition_to(target, **kwargs)
    assert new_rel.state == target


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ReleaseState.CANDIDATE, ReleaseState.PROMOTED),  # precisa autorizar antes
        (ReleaseState.CANDIDATE, ReleaseState.FAILED),
        (ReleaseState.PROMOTED, ReleaseState.CANDIDATE),  # não pode voltar
        (ReleaseState.CANCELLED, ReleaseState.AUTHORIZED),  # terminal
        (ReleaseState.FAILED, ReleaseState.PROMOTED),  # terminal
        (ReleaseState.REVERTED, ReleaseState.PROMOTED),  # terminal
    ],
)
def test_release_invalid_transitions_rejected(
    current: ReleaseState, target: ReleaseState
):
    """Transições inválidas devem ser rejeitadas."""
    rel = make_release(state=current)
    with pytest.raises(InvalidTransitionError):
        rel.transition_to(target)


# =============================================================================
# TRANSIÇÕES PARA TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_state", list(RELEASE_TERMINAL))
def test_release_terminal_states(terminal_state: ReleaseState):
    """Releases em estados terminais são marcados como is_terminal."""
    if terminal_state in (ReleaseState.FAILED, ReleaseState.REVERTED):
        # Precisam vir de PROMOTED
        if terminal_state == ReleaseState.FAILED:
            rel = make_release(state=ReleaseState.AUTHORIZED)
            rel = rel.transition_to(
                ReleaseState.PROMOTED,
                gate_decision_id="gd_test001",
                versioned_origin="abc123def",
                rollback_plan="Reverter commit",
            )
            rel = rel.transition_to(ReleaseState.FAILED)
        else:
            rel = make_release(state=ReleaseState.AUTHORIZED)
            rel = rel.transition_to(
                ReleaseState.PROMOTED,
                gate_decision_id="gd_test001",
                versioned_origin="abc123def",
                rollback_plan="Reverter commit",
            )
            rel = rel.transition_to(
                ReleaseState.REVERTED, reverted_from_id="rel_failed001"
            )
    else:
        # CANCELLED: vem de CANDIDATE ou AUTHORIZED
        rel = make_release(state=ReleaseState.AUTHORIZED)
        rel = rel.transition_to(ReleaseState.CANCELLED)
    assert rel.is_terminal


# =============================================================================
# IDEMPOTÊNCIA E IMUTABILIDADE
# =============================================================================


def test_release_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    rel = make_release(state=ReleaseState.CANDIDATE)
    result = rel.transition_to(ReleaseState.CANDIDATE)
    assert result is rel


def test_release_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição."""
    rel = make_release(state=ReleaseState.CANDIDATE)
    original_state = rel.state
    _ = rel.transition_to(ReleaseState.AUTHORIZED)
    assert rel.state == original_state


def test_release_version_increments():
    """Versão incrementa a cada transição."""
    rel = make_release(state=ReleaseState.CANDIDATE)
    new_rel = rel.transition_to(ReleaseState.AUTHORIZED)
    assert new_rel.version == rel.version + 1


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


def test_release_json_roundtrip():
    """Release deve serializar e desserializar corretamente."""
    rel = make_release(
        state=ReleaseState.CANDIDATE,
        responsible="tubarao",
    )
    json_str = rel.model_dump_json()
    rel2 = Release.model_validate_json(json_str)
    assert rel.release_id == rel2.release_id
    assert rel.state == rel2.state
    assert rel.name == rel2.name


def test_release_dict_roundtrip():
    """Release deve serializar e reconstruir via dict."""
    rel = make_release(state=ReleaseState.AUTHORIZED)
    data = rel.model_dump()
    rel2 = Release.model_validate(data)
    assert rel == rel2


# =============================================================================
# PROMOÇÃO COMPLETA
# =============================================================================


def test_release_full_promotion_flow():
    """Fluxo completo: candidate → authorized → promoted."""
    rel = make_release(state=ReleaseState.CANDIDATE)
    rel = rel.transition_to(ReleaseState.AUTHORIZED)
    rel = rel.transition_to(
        ReleaseState.PROMOTED,
        gate_decision_id="gd_test001",
        versioned_origin="abc123def",
        rollback_plan="Reverter commit abc123def",
    )
    assert rel.state == ReleaseState.PROMOTED
    assert rel.gate_decision_id == "gd_test001"
    assert rel.promoted_at is not None
    assert not rel.is_terminal  # PROMOTED pode falhar ou ser revertido
