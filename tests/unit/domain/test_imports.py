"""
Teste de independência de infraestrutura — FI-2B.

Analisa imports dos módulos de domínio para confirmar ausência de
imports de banco, ORM, rede, SDKs de IA, adaptadores externos e filesystem.

Pydantic é permitido como dependência de modelagem.
"""

import ast
import importlib
from pathlib import Path

import pytest

DOMAIN_DIR = Path(__file__).parent.parent.parent.parent / "src" / "harness" / "domain"


FORBIDDEN_IMPORTS = [
    "sqlalchemy",
    "sqlite",
    "alembic",
    "peewee",
    "tortoise",
    "orm",
    "django",
    "requests",
    "httpx",
    "aiohttp",
    "urllib3",
    "openai",
    "anthropic",
    "google.generativeai",
    "cohere",
    "mcp",
    "fastapi",
    "uvicorn",
    "flask",
    "os.path",
    "shutil",
    "asyncio",
    "threading",
    "subprocess",
    "socket",
]


def get_imports_from_file(filepath: Path) -> list[str]:
    content = filepath.read_text(encoding="utf-8")
    tree = ast.parse(content)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def is_forbidden(import_name: str) -> bool:
    return any(import_name.startswith(forbidden) for forbidden in FORBIDDEN_IMPORTS)


@pytest.mark.parametrize("domain_file", list(DOMAIN_DIR.glob("*.py")))
def test_no_forbidden_imports(domain_file: Path):
    """Módulo de domínio não deve conter imports proibidos."""
    imports = get_imports_from_file(domain_file)
    forbidden_found = [imp for imp in imports if is_forbidden(imp)]
    assert not forbidden_found, (
        f"{domain_file.name} contém imports proibidos: {forbidden_found}"
    )


def test_domain_modules_importable():
    """Todos os módulos de domínio devem ser importáveis."""
    modules = [
        "harness.domain",
        "harness.domain.errors",
        "harness.domain.enums",
        "harness.domain.ids",
        "harness.domain.transitions",
        "harness.domain.policies",
        "harness.domain.project",
        "harness.domain.requirement",
        "harness.domain.plan",
        "harness.domain.task",
        "harness.domain.work_order",
        "harness.domain.execution_run",
        "harness.domain.review",
        "harness.domain.test_run",
    ]
    for mod in modules:
        importlib.import_module(mod)


def test_domain_files_count():
    """Deve haver 14 arquivos de domínio (init + 13 módulos)."""
    py_files = list(DOMAIN_DIR.glob("*.py"))
    assert len(py_files) == 14, f"Esperado 14 arquivos, encontrado {len(py_files)}"


def test_pydantic_is_present():
    """Pydantic deve estar presente como dependência de modelagem."""
    import pydantic

    assert pydantic.VERSION is not None
