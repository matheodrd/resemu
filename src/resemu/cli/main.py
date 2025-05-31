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
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing output file without confirmation"
    ),
) -> None:
    """Generate a PDF resume from a YAML data file."""
    if not data_file.exists():
        typer.echo(f"Error: file '{data_file} not found.'")
        raise typer.Exit(1)

    output_path = output or data_file.with_suffix(".pdf")

    if output_path.exists() and not force:
        if not typer.confirm(f"Output file '{output_path}' already exists. Overwrite?"):
            typer.echo("Operation cancelled.")
            raise typer.Exit(0)

    with open(data_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    resume = Resume(**data)

    latex_content = generate_latex(resume, template)
    pdf_path = compile_pdf(latex_content, output_path)

    typer.echo(f"Generated resume: {pdf_path}")


@app.command()
def validate(data_file: Path) -> None:
    """Validate a YAML resume data file."""
    if not data_file.exists():
        typer.echo(f"Error: file '{data_file} not found.'")
        raise typer.Exit(1)

    try:
        with open(data_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        Resume(**data)
        typer.echo("🟢 YAML file is valid")
    except yaml.YAMLError as e:
        typer.echo(f"🔴 YAML file is invalid: parsing error: {e}")
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"🔴 YAML file is invalid: validation error: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
