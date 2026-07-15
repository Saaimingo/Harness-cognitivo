"""
CLI do Harness Cognitivo.

Interface de linha de comando para interação com o sistema.
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from harness import __version__

app = typer.Typer(
    name="harness",
    help="Harness Cognitivo - Sistema Operacional de IA",
    no_args_is_help=True,
)
console = Console()


@app.command()
def version() -> None:
    """Mostrar versão do Harness."""
    console.print(f"[bold green]Harness Cognitivo[/bold green] v{__version__}")


@app.command()
def status() -> None:
    """Mostrar status do sistema."""
    table = Table(title="Harness Cognitivo - Status")
    table.add_column("Componente", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Observação")

    table.add_row("Versão", __version__, "FI-0 - Fundação")
    table.add_row("Motor de IA", "⏳ Pendente", "Aguarda FI-2")
    table.add_row("Memória", "⏳ Pendente", "Aguarda FI-3")
    table.add_row("RAG", "⏳ Pendente", "Aguarda FI-5")
    table.add_row("Ferramentas", "⏳ Pendente", "Aguarda FI-7")
    table.add_row("Guardrails", "⏳ Pendente", "Aguarda FI-8")
    table.add_row("Observabilidade", "✅ Ativo", "Logging estruturado")

    console.print(table)


@app.command()
def doctor() -> None:
    """Verificar integridade do sistema."""
    console.print("[bold]Verificando integridade...[/bold]")

    checks = [
        ("Estrutura de diretórios", _check_directories),
        ("Contratos de eventos", _check_contracts),
        ("Logging", _check_logging),
    ]

    all_passed = True
    for name, check_fn in checks:
        try:
            check_fn()
            console.print(f"  [green]✓[/green] {name}")
        except Exception as e:
            console.print(f"  [red]✗[/red] {name}: {e}")
            all_passed = False

    if all_passed:
        console.print("\n[bold green]Todos os checks passaram![/bold green]")
    else:
        console.print("\n[bold red]Alguns checks falharam.[/bold red]")
        raise typer.Exit(1)


def _check_directories() -> None:
    """Verificar se estrutura de diretórios existe."""
    from pathlib import Path

    required_dirs = [
        "src/harness",
        "tests",
        "docs",
        "evidence",
        "var",
    ]

    base = Path(__file__).parent.parent.parent
    for d in required_dirs:
        if not (base / d).exists():
            raise FileNotFoundError(f"Diretório não encontrado: {d}")


def _check_contracts() -> None:
    """Verificar se contratos de eventos estão funcionais."""
    from harness.contracts.events import Event, EventType

    event = Event(event_type=EventType.TASK_CREATED)
    assert event.event_id
    assert event.event_type == EventType.TASK_CREATED


def _check_logging() -> None:
    """Verificar se logging está configurado."""
    from harness.logging import get_logger

    logger = get_logger("test")
    assert logger is not None


if __name__ == "__main__":
    app()
