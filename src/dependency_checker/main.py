import importlib.metadata
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table


app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """Check Python dependencies from requirements files."""


@app.command()
def check(requirements: Path = typer.Argument(Path("requirements.txt"), help="Requirements file to inspect.")) -> None:
    table = Table(title="Dependencies")
    table.add_column("Package")
    table.add_column("Installed Version")
    for line in requirements.read_text(encoding="utf-8").splitlines():
        package = line.strip().split("==")[0].split(">=")[0].split("<")[0]
        if not package or package.startswith("#"):
            continue
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = "not installed"
        table.add_row(package, version)
    console.print(table)
