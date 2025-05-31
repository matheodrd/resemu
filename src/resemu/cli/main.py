from pathlib import Path

import typer
import yaml

from resemu.models.resume import Resume
from resemu.generators.latex import generate_latex
from resemu.generators.pdf import compile_pdf

app = typer.Typer()


@app.command()
def generate(
    data_file: Path = typer.Argument(..., help="YAML file containing resume data"),
    template: str = typer.Option("engineering", help="Resume template to use"),
    output: Path | None = typer.Option(None, help="Output file path"),
) -> None:
    """Generate a PDF resume from a YAML data file."""

    with open(data_file, "r") as f:
        data = yaml.safe_load(f)

    resume = Resume(**data)

    latex_content = generate_latex(resume, template)
    pdf_path = compile_pdf(latex_content, output or data_file.with_suffix(".pdf"))

    typer.echo(f"Generated resume: {pdf_path}")


@app.command()
def validate(data_file: Path) -> None:
    """Validate a YAML resume data file."""
    try:
        with open(data_file) as f:
            data = yaml.safe_load(f)
        Resume(**data)
        typer.echo("🟢 YAML file is valid")
    except Exception as e:
        typer.echo(f"🔴 YAML file is invalid: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
