"""
Testes completos para a entidade Review — FI-2B.
Cobre: construção, quatro tipos, independência, transições, aprovação,
rejeição, solicitação de mudança, achados bloqueadores, referências
a requisitos e regras, imutabilidade, idempotência, serialização.
"""

from datetime import UTC, datetime

import pytest

from harness.domain.enums import ReviewStatus, ReviewType
from harness.domain.errors import (
    InvalidTransitionError,
    InvariantViolationError,
)
from harness.domain.review import Review
from harness.domain.transitions import REVIEW_TERMINAL


def make_review(
    status: ReviewStatus = ReviewStatus.REQUESTED,
    review_type: ReviewType = ReviewType.FUNCTIONAL,
    reviewer: str | None = None,
    executor: str | None = None,
) -> Review:
    """Helper para criar Review com estado específico."""
    kwargs: dict = {
        "review_id": "rev_test123",
        "execution_run_id": "exr_test456",
        "review_type": review_type,
        "status": status,
    }
    if reviewer is not None:
        kwargs["reviewer"] = reviewer
    if executor is not None:
        kwargs["executor"] = executor
    return Review(**kwargs)


# =============================================================================
# CONSTRUÇÃO VÁLIDA
# =============================================================================


class TestReviewConstruction:
    def test_creation_minimal(self):
        """Review deve ser criado com campos obrigatórios."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
        )
        assert review.review_id == "rev_test123"
        assert review.execution_run_id == "exr_test456"
        assert review.review_type == ReviewType.FUNCTIONAL
        assert review.status == ReviewStatus.REQUESTED
        assert review.reviewer is None

    def test_creation_with_all_fields(self):
        """Review deve aceitar todos os campos."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.SECURITY,
            reviewer="security_agent",
            executor="freebuff",
        )
        assert review.reviewer == "security_agent"
        assert review.executor == "freebuff"

    def test_invalid_review_id_rejected(self):
        """review_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            Review(
                review_id="invalid-id",
                execution_run_id="exr_test456",
                review_type=ReviewType.FUNCTIONAL,
            )

    def test_invalid_execution_run_id_rejected(self):
        """execution_run_id inválido deve ser rejeitado."""
        with pytest.raises(ValueError, match="ID inválido"):
            Review(
                review_id="rev_test123",
                execution_run_id="invalid-id",
                review_type=ReviewType.FUNCTIONAL,
            )


# =============================================================================
# QUATRO TIPOS DE REVIEW
# =============================================================================


class TestReviewTypes:
    @pytest.mark.parametrize("review_type", list(ReviewType))
    def test_all_four_types(self, review_type: ReviewType):
        """Todos os 4 tipos de review devem ser suportados."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=review_type,
        )
        assert review.review_type == review_type

    def test_functional_type(self):
        """Tipo functional deve ser aceito."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
        )
        assert review.review_type == ReviewType.FUNCTIONAL

    def test_domain_type(self):
        """Tipo domain deve ser aceito."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.DOMAIN,
        )
        assert review.review_type == ReviewType.DOMAIN

    def test_structural_type(self):
        """Tipo structural deve ser aceito."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.STRUCTURAL,
        )
        assert review.review_type == ReviewType.STRUCTURAL

    def test_security_type(self):
        """Tipo security deve ser aceito."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.SECURITY,
        )
        assert review.review_type == ReviewType.SECURITY


# =============================================================================
# VALIDAÇÕES
# =============================================================================


class TestReviewValidations:
    def test_rejects_naive_datetime(self):
        """Review rejeita datetime sem timezone."""
        with pytest.raises(ValueError, match="timezone"):
            Review(
                review_id="rev_test123",
                execution_run_id="exr_test456",
                review_type=ReviewType.FUNCTIONAL,
                created_at=datetime(2026, 1, 1),
            )

    def test_accepts_aware_datetime(self):
        """Review aceita datetime com timezone."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
            created_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        assert review.created_at.tzinfo is not None


# =============================================================================
# INDEPENDÊNCIA ENTRE TIPOS
# =============================================================================


class TestReviewIndependence:
    def test_different_types_are_independent(self):
        """Reviews de tipos diferentes são independentes."""
        func_review = Review(
            review_id="rev_func123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
            status=ReviewStatus.APPROVED,
            reviewer="func_agent",
            justification="OK",
        )
        domain_review = Review(
            review_id="rev_domain123",
            execution_run_id="exr_test456",
            review_type=ReviewType.DOMAIN,
            status=ReviewStatus.REJECTED,
            reviewer="domain_agent",
            justification="Regras violadas",
        )
        assert func_review.status == ReviewStatus.APPROVED
        assert domain_review.status == ReviewStatus.REJECTED


# =============================================================================
# INDEPENDÊNCIA DE REVISOR/EXECUTOR
# =============================================================================


class TestReviewReviewerExecutorIndependence:
    def test_reviewer_must_differ_from_executor(self):
        """Reviewer e executor não podem ser a mesma autoridade."""
        with pytest.raises(
            InvariantViolationError, match="reviewer_must_differ_from_executor"
        ):
            Review(
                review_id="rev_test123",
                execution_run_id="exr_test456",
                review_type=ReviewType.FUNCTIONAL,
                reviewer="freebuff",
                executor="freebuff",
            )

    def test_reviewer_and_executor_can_differ(self):
        """Reviewer e executor diferentes são aceitos."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
            reviewer="reviewer_agent",
            executor="freebuff",
        )
        in_progress = review.transition_to(ReviewStatus.IN_PROGRESS)
        new_review = in_progress.transition_to(
            ReviewStatus.APPROVED, justification="OK"
        )
        assert new_review.status == ReviewStatus.APPROVED

    def test_no_executor_allows_any_reviewer(self):
        """Sem executor definido, reviewer pode ser qualquer um."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
            reviewer="agent",
        )
        in_progress = review.transition_to(ReviewStatus.IN_PROGRESS)
        new_review = in_progress.transition_to(
            ReviewStatus.APPROVED, justification="OK"
        )
        assert new_review.status == ReviewStatus.APPROVED


# =============================================================================
# TRANSIÇÕES PERMITIDAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ReviewStatus.REQUESTED, ReviewStatus.IN_PROGRESS),
        (ReviewStatus.IN_PROGRESS, ReviewStatus.APPROVED),
        (ReviewStatus.IN_PROGRESS, ReviewStatus.REJECTED),
        (ReviewStatus.IN_PROGRESS, ReviewStatus.CHANGE_REQUESTED),
    ],
)
def test_review_valid_transitions(current: ReviewStatus, target: ReviewStatus):
    """Transições válidas devem ser aceitas."""
    kwargs: dict = {"status": current, "reviewer": "agent"}
    transition_kwargs: dict = {}
    if target == ReviewStatus.APPROVED:
        transition_kwargs["justification"] = "Aprovado"
    if target == ReviewStatus.REJECTED:
        transition_kwargs["justification"] = "Rejeitado"
    if target == ReviewStatus.CHANGE_REQUESTED:
        transition_kwargs["requested_changes"] = ["Corrigir erro X"]
    review = make_review(**kwargs)
    new_review = review.transition_to(target, **transition_kwargs)
    assert new_review.status == target


# =============================================================================
# TRANSIÇÕES REJEITADAS
# =============================================================================


@pytest.mark.parametrize(
    "current,target",
    [
        (ReviewStatus.REQUESTED, ReviewStatus.APPROVED),
        (ReviewStatus.REQUESTED, ReviewStatus.REJECTED),
        (ReviewStatus.APPROVED, ReviewStatus.IN_PROGRESS),
        (ReviewStatus.REJECTED, ReviewStatus.IN_PROGRESS),
        (ReviewStatus.CHANGE_REQUESTED, ReviewStatus.IN_PROGRESS),
    ],
)
def test_review_invalid_transitions_rejected(
    current: ReviewStatus, target: ReviewStatus
):
    """Transições inválidas devem ser rejeitadas."""
    kwargs: dict = {"status": current, "reviewer": "agent"}
    review = make_review(**kwargs)
    with pytest.raises(InvalidTransitionError):
        review.transition_to(target)


# =============================================================================
# APROVAÇÃO
# =============================================================================


class TestReviewApproval:
    def test_approved_requires_justification(self):
        """Aprovação requer justificativa."""
        review = make_review(status=ReviewStatus.IN_PROGRESS, reviewer="agent")
        with pytest.raises(InvariantViolationError, match="justificativa"):
            review.transition_to(ReviewStatus.APPROVED)

    def test_approved_requires_reviewer(self):
        """Aprovação requer reviewer."""
        review = make_review(status=ReviewStatus.IN_PROGRESS)
        with pytest.raises(InvariantViolationError, match="reviewer"):
            review.transition_to(ReviewStatus.APPROVED, justification="OK")

    def test_approved_with_justification_and_reviewer(self):
        """Aprovação com justificativa e reviewer funciona."""
        review = make_review(status=ReviewStatus.IN_PROGRESS, reviewer="agent")
        new_review = review.transition_to(
            ReviewStatus.APPROVED, justification="Aprovado after review"
        )
        assert new_review.status == ReviewStatus.APPROVED


# =============================================================================
# REJEIÇÃO
# =============================================================================


class TestReviewRejection:
    def test_rejected_requires_justification(self):
        """Rejeição requer justificativa."""
        review = make_review(status=ReviewStatus.IN_PROGRESS)
        with pytest.raises(InvariantViolationError, match="justificativa"):
            review.transition_to(ReviewStatus.REJECTED)

    def test_rejected_with_justification(self):
        """Rejeição com justificativa funciona."""
        review = make_review(status=ReviewStatus.IN_PROGRESS)
        new_review = review.transition_to(
            ReviewStatus.REJECTED, justification="Código não atende requisitos"
        )
        assert new_review.status == ReviewStatus.REJECTED


# =============================================================================
# SOLICITAÇÃO DE MUDANÇA
# =============================================================================


class TestReviewChangeRequested:
    def test_change_requested_requires_changes(self):
        """change_requested requer lista de alterações."""
        review = make_review(status=ReviewStatus.IN_PROGRESS)
        with pytest.raises(InvariantViolationError, match="alterações"):
            review.transition_to(ReviewStatus.CHANGE_REQUESTED)

    def test_change_requested_with_changes(self):
        """change_requested com alterações funciona."""
        review = make_review(status=ReviewStatus.IN_PROGRESS)
        new_review = review.transition_to(
            ReviewStatus.CHANGE_REQUESTED,
            requested_changes=["Corrigir erro X", "Adicionar teste Y"],
        )
        assert new_review.status == ReviewStatus.CHANGE_REQUESTED
        assert len(new_review.requested_changes) == 2


# =============================================================================
# ESTADOS TERMINAIS
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(REVIEW_TERMINAL))
def test_review_terminal_states(terminal_status: ReviewStatus):
    """Reviews em estados terminais são marcados como is_terminal."""
    kwargs: dict = {"status": terminal_status, "reviewer": "agent"}
    if terminal_status == ReviewStatus.APPROVED:
        kwargs["status"] = ReviewStatus.APPROVED
    if terminal_status == ReviewStatus.REJECTED:
        kwargs["status"] = ReviewStatus.REJECTED
    if terminal_status == ReviewStatus.CHANGE_REQUESTED:
        kwargs["status"] = ReviewStatus.CHANGE_REQUESTED
    review = make_review(**kwargs)
    assert review.is_terminal


def test_review_non_terminal_states():
    """Reviews em estados não-terminais não são marcados como is_terminal."""
    for status in ReviewStatus:
        if status not in REVIEW_TERMINAL:
            review = make_review(status=status)
            assert not review.is_terminal


# =============================================================================
# IDEMPOTÊNCIA
# =============================================================================


def test_review_idempotent_transition():
    """Transição para estado atual retorna a própria instância."""
    review = make_review(status=ReviewStatus.REQUESTED)
    result = review.transition_to(ReviewStatus.REQUESTED)
    assert result is review


# =============================================================================
# IMUTABILIDADE
# =============================================================================


def test_review_original_unchanged_after_transition():
    """Entidade original permanece inalterada após transição válida."""
    review = make_review(status=ReviewStatus.REQUESTED)
    original_status = review.status
    _ = review.transition_to(ReviewStatus.IN_PROGRESS)
    assert review.status == original_status


def test_review_version_increments():
    """Versão incrementa a cada transição."""
    review = make_review(status=ReviewStatus.REQUESTED)
    new_review = review.transition_to(ReviewStatus.IN_PROGRESS)
    assert new_review.version == review.version + 1


# =============================================================================
# SERIALIZAÇÃO
# =============================================================================


def test_review_json_roundtrip():
    """Review deve serializar e desserializar corretamente."""
    review = make_review(
        status=ReviewStatus.IN_PROGRESS,
        review_type=ReviewType.DOMAIN,
    )
    json_str = review.model_dump_json()
    review2 = Review.model_validate_json(json_str)
    assert review.review_id == review2.review_id
    assert review.review_type == review2.review_type
    assert review.status == review2.status


# =============================================================================
# REFERÊNCIAS A REGRAS E REQUISITOS
# =============================================================================


class TestReviewReferences:
    def test_domain_review_with_rules(self):
        """Domain review pode referenciar regras de negócio."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.DOMAIN,
            referenced_rules=["rul_abc123", "rul_def456"],
        )
        assert len(review.referenced_rules) == 2

    def test_functional_review_with_requirements(self):
        """Functional review pode referenciar requisitos."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.FUNCTIONAL,
            referenced_requirements=["req_abc123", "req_def456"],
        )
        assert len(review.referenced_requirements) == 2

    def test_structural_review_with_findings(self):
        """Structural review pode registrar achados."""
        review = Review(
            review_id="rev_test123",
            execution_run_id="exr_test456",
            review_type=ReviewType.STRUCTURAL,
            findings=["Dívida técnica no módulo X", "Acoplamento alto"],
        )
        assert len(review.findings) == 2


# =============================================================================
# ESTADOS TERMINAIS BLOQUEIAM TRANSMISSÕES
# =============================================================================


@pytest.mark.parametrize("terminal_status", list(REVIEW_TERMINAL))
def test_review_terminal_blocks_further_transitions(terminal_status: ReviewStatus):
    """Review em estado terminal bloqueia transições."""
    kwargs: dict = {"status": terminal_status, "reviewer": "agent"}
    review = make_review(**kwargs)
    with pytest.raises(InvalidTransitionError):
        review.transition_to(ReviewStatus.IN_PROGRESS)
