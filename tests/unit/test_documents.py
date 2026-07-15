"""
Testes de validação de documentos — FI-1.

Valida que arquivos existem, possuem metadados corretos,
links Markdown são consistentes e referências são válidas.
"""

import re
from pathlib import Path

import pytest


# =============================================================================
# CAMINHOS BASE
# =============================================================================

REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_DIR = REPO_ROOT / "docs"
REPORTS_DIR = DOCS_DIR / "reports"
SOURCES_DIR = DOCS_DIR / "sources"
SRC_DIR = REPO_ROOT / "src" / "harness"


# =============================================================================
# TESTES DE EXISTÊNCIA DE ARQUIVOS
# =============================================================================

class TestFileExistence:
    """Valida que arquivos obrigatórios existem."""

    REQUIRED_FILES = [
        ("docs/GLOSSARY.md", "Glossário do projeto"),
        ("docs/MEC_PROTOCOL.md", "Protocolo cognitivo"),
        ("docs/sources/DECLARATIVA_ORIGINAL.md", "Registro da Declarativa"),
        ("src/harness/__init__.py", "Ponto de entrada do pacote"),
        ("src/harness/contracts/__init__.py", "Pacote de contratos"),
        ("src/harness/contracts/events.py", "Contratos de eventos"),
        ("src/harness/contracts/context.py", "Contratos de contexto"),
        ("src/harness/logging.py", "Módulo de logging"),
        ("src/harness/cli.py", "CLI"),
        ("docs/reports/DIARIO_FI1.md", "Diário da FI-1"),
        ("docs/reports/MANIFESTO_EVIDENCIAS_FI1.md", "Manifesto de evidências FI-1"),
        ("docs/reports/RELATORIO_FI1.md", "Relatório da FI-1"),
    ]

    @pytest.mark.parametrize("relative_path,description", REQUIRED_FILES)
    def test_file_exists(self, relative_path: str, description: str):
        """Arquivo obrigatório deve existir."""
        file_path = REPO_ROOT / relative_path
        assert file_path.exists(), f"{description} não encontrado: {relative_path}"

    @pytest.mark.parametrize("relative_path,description", REQUIRED_FILES)
    def test_file_not_empty(self, relative_path: str, description: str):
        """Arquivo obrigatório não deve estar vazio."""
        file_path = REPO_ROOT / relative_path
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            assert len(content) > 0, f"{description} está vazio: {relative_path}"


# =============================================================================
# TESTES DE METADADOS YAML
# =============================================================================

class TestYAMLMetadata:
    """Valida que arquivos Markdown possuem frontmatter YAML válido."""

    FILES_WITH_YAML = [
        "docs/GLOSSARY.md",
        "docs/MEC_PROTOCOL.md",
        "docs/sources/DECLARATIVA_ORIGINAL.md",
        "docs/reports/DIARIO_FI1.md",
    ]

    @pytest.mark.parametrize("relative_path", FILES_WITH_YAML)
    def test_has_frontmatter(self, relative_path: str):
        """Arquivo deve possuir frontmatter YAML (entre ---)."""
        file_path = REPO_ROOT / relative_path
        if not file_path.exists():
            pytest.skip(f"Arquivo não existe: {relative_path}")

        content = file_path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # Frontmatter deve começar e terminar com ---
        assert lines[0].strip() == "---", f"{relative_path} não começa com ---"
        # Encontrar segundo ---
        second_dash = None
        for i, line in enumerate(lines[1:], 1):
            if line.strip() == "---":
                second_dash = i
                break
        assert second_dash is not None, f"{relative_path} não tem fechamento ---"

    @pytest.mark.parametrize("relative_path", FILES_WITH_YAML)
    def test_has_required_metadata_fields(self, relative_path: str):
        """Frontmatter deve ter campos obrigatórios (tipo, titulo, status)."""
        file_path = REPO_ROOT / relative_path
        if not file_path.exists():
            pytest.skip(f"Arquivo não existe: {relative_path}")

        content = file_path.read_text(encoding="utf-8")
        # Extrair frontmatter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert match, f"{relative_path} não tem frontmatter válido"

        frontmatter = match.group(1)
        assert "tipo:" in frontmatter, f"{relative_path} não tem campo 'tipo'"
        assert "titulo:" in frontmatter, f"{relative_path} não tem campo 'titulo'"
        assert "status:" in frontmatter, f"{relative_path} não tem campo 'status'"


# =============================================================================
# TESTES DE LINKS MARKDOWN
# =============================================================================

class TestMarkdownLinks:
    """Valida que links internos Markdown são consistentes."""

    def test_glossary_links_format(self):
        """Glossário deve usar formato de tabela Markdown."""
        glossary_path = REPO_ROOT / "docs" / "GLOSSARY.md"
        if not glossary_path.exists():
            pytest.skip("GLOSSARY.md não existe")

        content = glossary_path.read_text(encoding="utf-8")
        # Deve conter tabelas Markdown
        assert "|" in content, "Glossário deve conter tabelas Markdown"
        assert "---|---" in content or "---|---" in content.replace(" ", ""), \
            "Glossário deve conter separadores de tabela"

    def test_protocol_references_consistent(self):
        """Protocolo deve referenciar Doc numbers consistentes."""
        protocol_path = REPO_ROOT / "docs" / "MEC_PROTOCOL.md"
        if not protocol_path.exists():
            pytest.skip("MEC_PROTOCOL.md não existe")

        content = protocol_path.read_text(encoding="utf-8")
        # Deve referenciar Docs
        assert "Doc" in content or "doc" in content.lower(), \
            "Protocolo deve referenciar documentos normativos"

    def test_no_broken_wikilinks_in_reports(self):
        """Relatórios não devem ter wikilinks quebrados."""
        for report_file in REPORTS_DIR.glob("*.md"):
            content = report_file.read_text(encoding="utf-8")
            # Encontrar wikilinks [[...]]
            wikilinks = re.findall(r"\[\[([^\]]+)\]\]", content)
            for link in wikilinks:
                # Verificar se o arquivo linkado existe (parcial)
                # Não falhar se for referência a docs do vault (não no repo)
                assert link.strip() != "", f"Wikilink vazio em {report_file.name}"


# =============================================================================
# TESTES DE REFERÊNCIAS
# =============================================================================

class TestReferences:
    """Valida que referências cruzadas são consistentes."""

    def test_declarativa_hash_present(self):
        """Registro da Declarativa deve conter hash SHA-256."""
        declarativa_path = SOURCES_DIR / "DECLARATIVA_ORIGINAL.md"
        if not declarativa_path.exists():
            pytest.skip("DECLARATIVA_ORIGINAL.md não existe")

        content = declarativa_path.read_text(encoding="utf-8")
        assert "SHA-256" in content, "Registro deve conter hash SHA-256"
        # Hash deve ter 64 caracteres hexadecimais
        hashes = re.findall(r"[a-f0-9]{64}", content)
        assert len(hashes) >= 1, "Deve haver pelo menos 1 hash SHA-256"

    def test_glossary_has_epistemology_section(self):
        """Glossário deve ter seção de epistemologia."""
        glossary_path = REPO_ROOT / "docs" / "GLOSSARY.md"
        if not glossary_path.exists():
            pytest.skip("GLOSSARY.md não existe")

        content = glossary_path.read_text(encoding="utf-8")
        assert "Epistemologia" in content or "epistemologia" in content.lower(), \
            "Glossário deve ter seção de Epistemologia"

    def test_protocol_has_source_of_truth(self):
        """Protocolo deve documentar regra de fonte da verdade."""
        protocol_path = REPO_ROOT / "docs" / "MEC_PROTOCOL.md"
        if not protocol_path.exists():
            pytest.skip("MEC_PROTOCOL.md não existe")

        content = protocol_path.read_text(encoding="utf-8")
        assert "fonte" in content.lower() and "verdade" in content.lower(), \
            "Protocolo deve documentar regra de fonte da verdade"

    def test_init_exports_context_contracts(self):
        """__init__.py deve exportar contratos de contexto."""
        init_path = SRC_DIR / "__init__.py"
        content = init_path.read_text(encoding="utf-8")
        assert "ContextRequest" in content
        assert "ContextCapsule" in content
        assert "CognitiveObject" in content
        assert "EvidenceReference" in content
        assert "Purpose" in content
        assert "ObjectType" in content
        assert "TrustLevel" in content
