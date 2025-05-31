from pathlib import Path

import typer
import yaml
from rich.console import Console
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel

from resemu.models.resume import Resume
from resemu.generators.latex import generate_latex
from resemu.generators.pdf import compile_pdf

app = typer.Typer(
    name="resemu",
    help="Generate solid resumes from YAML data.",
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def generate(
    data_file: Path = typer.Argument(
        ...,
        help="YAML file containing resume data",
    ),
    template: str = typer.Option(
        "engineering",
        "--template",
        "-t",
        help="Resume template to use",
        rich_help_panel="Template Options",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (defaults to input filename with .pdf extension)",
        rich_help_panel="Output Options",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing output file without confirmation",
        rich_help_panel="Output Options",
    ),
) -> None:
    """
    [bold green]Generate a PDF resume from a YAML data file.[/bold green]

    This command processes your YAML resume data and generates a clean PDF using the specified template.
    """
    if not data_file.exists():
        console.print(f"[bold red]❌ Error:[/bold red] File '{data_file}' not found", style="red")
        raise typer.Exit(1)

    output_path = output or data_file.with_suffix(".pdf")

    if output_path.exists() and not force:
        if not Confirm.ask(
            f"Output file '{output_path}' already exists. Overwrite?",
            default=False,
        ):
            console.print("[yellow]Operation cancelled[/yellow]")
            raise typer.Exit(0)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        # Load and validate YAML
        task = progress.add_task("[cyan]Loading YAML data...", total=100)
        with open(data_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        progress.update(task, advance=25)

        # Validate data structure
        progress.update(task, description="[cyan]Validating data structure...")
        resume = Resume(**data)
        progress.update(task, advance=25)

        # Generate LaTeX
        progress.update(task, description="[cyan]Generating LaTeX content...")
        latex_content = generate_latex(resume, template)
        progress.update(task, advance=25)

        # Compile PDF
        progress.update(task, description="[cyan]Compiling PDF...")
        pdf_path = compile_pdf(latex_content, output_path)
        progress.update(task, advance=25)

    success_panel = Panel(
        f"[bold green]✅ Resume generated successfully![/bold green]\n\n"
        f"📄 Template: [bold]{template}[/bold]\n"
        f"📁 Output: [bold blue]{pdf_path}[/bold blue]\n"
        f"📊 Size: {pdf_path.stat().st_size / 1024:.1f} KB",
        title="[bold green]Generation Complete[/bold green]",
        border_style="green",
    )
    console.print(success_panel)


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
