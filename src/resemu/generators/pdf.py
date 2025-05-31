import subprocess


def is_pdflatex_available() -> bool:
    """Check if the `pdflatex` command is available on the system."""
    try:
        result = subprocess.run(
            ["pdflatex", "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False
