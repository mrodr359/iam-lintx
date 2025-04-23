"""
iam-lintx CLI

This file defines the main command-line interface using Typer.
Commands are grouped into subcommands (e.g., scan policy).

Author: Manuel Rodriguez
Created: 2025-04-23
"""

import typer
from pathlib import Path
from rich.console import Console
from rich.markup import escape
from iam_lintx.scanner import scan_json_policy


# Rich console for colorized CLI output
console = Console()


app = typer.Typer()
scan_app = typer.Typer()  # ← subcommand group


@scan_app.command("policy")
def scan_policy(
    path: str = typer.Argument(..., help="Path to policy file (JSON or Terraform)"),
):
    """
    Scan a policy file (JSON only for now) and print any issues.

    This currently checks for:
    - Wildcard Action ("Action": "*")
    - TODO: Add rules for Resource wildcards, missing Conditions, etc.
    """
    file_path = Path(path)
    if not file_path.exists():
        console.print(f"[bold red][ERROR][/bold red] File not found: {escape(path)}")
        raise typer.Exit(code=1)

    try:
        issues = scan_json_policy(file_path)
    except ValueError as e:
        console.print(f"[bold red][ERROR][/bold red] {escape(str(e))}")
        raise typer.Exit(code=1)

    if not issues:
        console.print("[bold green][PASS][/bold green] No wildcard Actions found.")
        raise typer.Exit(code=0)
    else:
        for issue in issues:
            console.print(
                f"[bold yellow][{issue['type']}][/bold yellow] Statement {issue['statement_index']}: {issue['message']}"
            )
        raise typer.Exit(code=1)


# Register subcommands
app.add_typer(scan_app, name="scan")
