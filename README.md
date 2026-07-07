# mypm

## Summary
This project, taking a yaml file, we compile to create shell scripts that will help us to perform our projects.

## Project Structure
- src/mypm: project code root
- bin: compiled shell script assets, historic
- bin/latest: latest compiled version
- config: various configuration files that gets parsed by this application to create the assets

## How it works

### Assets
- aliases
- definitions
- main

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
