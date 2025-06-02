<h1 align="center">
  <br>
  <img src="docs/img/resemu.png" alt="resemu" width="200">
  <br>
  resemu
  <br>
</h1>

<h4 align="center">A simple CLI tool to generate clean resumes from YAML data.</h4>

![screenshot](docs/img/resemu-demo.gif)

## Installation

You need Python 3.12 or newer.

```bash
pip install resemu
```

Or, if you want the latest development version:

```bash
pip install git+https://github.com/matheodrd/resemu.git
```

## CLI Usage

### `resemu`

```console
$ resemu [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate a PDF resume from a YAML data file
* `validate`: Validate a YAML resume data file
* `templates`: List available resume templates
* `version`: Show version information

### `resemu generate`

Generate a PDF resume from a YAML data file.

This command processes your YAML resume data and generates a clean PDF using the specified template.

**Usage**:

```console
$ resemu generate [OPTIONS] DATA_FILE
```

**Arguments**:

* `DATA_FILE`: YAML file containing resume data  [required]

**Options**:

* `-t, --template TEXT`: Resume template to use  [default: engineering]
* `-o, --output PATH`: Output file path (defaults to input filename with .pdf extension)
* `-f, --force`: Overwrite existing output file without confirmation
* `--help`: Show this message and exit.

### `resemu validate`

Validate a YAML resume data file.

Checks if your YAML file is properly formatted and contains all required fields.

**Usage**:

```console
$ resemu validate [OPTIONS] DATA_FILE
```

**Arguments**:

* `DATA_FILE`: YAML file to validate  [required]

**Options**:

* `-v, --verbose`: Show detailed validation information
* `--help`: Show this message and exit.

### `resemu templates`

List available resume templates.

Shows all available templates you can use with the generate command.

**Usage**:

```console
$ resemu templates [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `resemu version`

Show version information.

**Usage**:

```console
$ resemu version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
