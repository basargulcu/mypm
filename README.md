# mypm

## Summary
This project, taking a yaml file, we compile to create shell scripts that will help us to perform our projects.

## Project Structure
- `src/mypm/cli.py`: user-facing CLI entry points (`_mypm compile`, `_mypm install`)
- `src/mypm/settings.py`: project-wide variables and environment configuration
- `src/mypm/main.py`: core logic (compile, install)
- `src/mypm/compiler/`: shell script generators
- `src/mypm/installer/`: install helpers
- `bin/`: compiled shell script assets, historic
- `bin/latest/`: latest compiled version
- `config/`: configuration files parsed during compilation
- `extensions/`: optional extension scripts that can be included during compilation
- `tests/`: unit tests

## How it works

### Assets
- aliases
- definitions
- main

### Extensions

Place extension scripts in the `extensions/` folder. List the ones to include in `config/extensions.yml`:

```yaml
extensions:
  - my_extension
```

Only extensions listed in `extensions.yml` will be picked up during compilation.

## How to run

### 1. Configure your projects

Copy `config/sample_projects.yml` to `config/projects.yml` and fill in your values:

```
cp config/sample_projects.yml config/projects.yml
```

### 2. Install dependencies

```
uv sync
```

To include dev dependencies (pytest, ruff, pre-commit):

```
uv sync --group dev
```

### 3. Compile

```
_mypm compile <version>
```

Example:

```
_mypm compile v0.0.1
```

If no version is given, you will be prompted to overwrite the latest or auto-increment:

```
_mypm compile
```

This writes the generated shell scripts to `bin/<version>/` and updates `bin/latest/`.

## Running tests

```
uv run pytest tests/
```

## Code quality

Run pre-commit checks manually against all files:

```
uv run pre-commit run --all-files
```

## How to install

```
_mypm install
```

## How to manually install

Add the following to `.zshrc`:

```
export MYPM_BIN="{path to this repo}/bin/latest"
if [ -f ${MYPM_BIN}/aliases.sh ]; then source ${MYPM_BIN}/aliases.sh; fi
```
