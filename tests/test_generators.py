import pytest
from pathlib import Path
import datetime

from resemu.generators.latex import generate_latex
from resemu.generators.pdf import compile_pdf, PDFCompilationError


class DummyObj:
    """Small object to simulate Resume model fields."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@pytest.fixture
def dummy_resume():
    return DummyObj(
        contact=DummyObj(
            name="Jean-Pierre & Co",
            email="jp@example.com",
            portfolio=None,
            github=None,
        ),
        summary="Resume with $ and % and _ and \\ and { and }",
        skills=[DummyObj(category="Langages", skills=["Python", "C++ & Bash"])],
        experience=[
            DummyObj(
                title="Lead Dev $",
                company="BigCorp & Sons",
                location="London",
                start_date=datetime.date(2021, 1, 1),
                end_date=None,
                bullets=["Development on a $machine", "A 10 000£ budget & team management"],
            )
        ],
        projects=[
            DummyObj(
                title="Open-Source Project",
                url=None,
                bullets=["CLI tool compatible with $ and %", "Documentation written in LaTeX"],
            )
        ],
        education=[
            DummyObj(
                school="{LaTeX} University",
                degree="Master #1",
                field="Computer science",
                graduation_date=datetime.date(2019, 6, 1),
            )
        ],
    )


def test_generate_latex_output(dummy_resume):
    """Check if all special chars are escaped in generated LaTeX."""
    latex_code = generate_latex(dummy_resume)

    assert r"\&" in latex_code
    assert r"\$" in latex_code
    assert r"\%" in latex_code
    assert r"\_" in latex_code
    assert r"\{" in latex_code
    assert r"\}" in latex_code
    assert r"\textbackslash{}" in latex_code or "\\\\" in latex_code
    assert "Jean-Pierre \\& Co" in latex_code
    assert "BigCorp \\& Sons" in latex_code
    assert "Resume with \\$ and \\% and \\_ and " in latex_code


def test_generate_latex_valid_document(dummy_resume):
    """The generated LaTeX must contains essential elements of a document."""
    latex_code = generate_latex(dummy_resume)
    assert "\\begin{document}" in latex_code
    assert "\\end{document}" in latex_code
    assert "section" in latex_code


def test_compile_pdf_success(monkeypatch, tmp_path):
    latex = r"""
    \documentclass{article}
    \begin{document}
    Hello World!
    \end{document}
    """

    class DummyCompletedProcess:
        def __init__(self):
            self.returncode = 0
            self.stderr = ""
            self.stdout = ""

    def dummy_run(cmd, *args, **kwargs):
        try:
            idx = cmd.index("-output-directory")
            temp_dir = cmd[idx + 1]
        except (ValueError, IndexError):
            temp_dir = tmp_path
        pdf_file = Path(temp_dir) / "resume.pdf"
        pdf_file.touch()
        return DummyCompletedProcess()

    monkeypatch.setattr("subprocess.run", dummy_run)
    monkeypatch.setattr("shutil.copy2", lambda src, dst: Path(dst).write_bytes(b"PDF!"))
    output = tmp_path / "output.pdf"
    result = compile_pdf(latex, output)
    assert result.exists()
    assert result.suffix == ".pdf"


def test_compile_pdf_error(monkeypatch, tmp_path):
    """Test PDF compilation error handling."""
    latex = "illegal content!"

    class DummyCompletedProcess:
        def __init__(self):
            self.returncode = 1
            self.stderr = "LaTeX Error"
            self.stdout = "Log"

    def dummy_run(*a, **k):
        return DummyCompletedProcess()

    monkeypatch.setattr("subprocess.run", dummy_run)
    output = tmp_path / "output2.pdf"
    with pytest.raises(PDFCompilationError):
        compile_pdf(latex, output)
