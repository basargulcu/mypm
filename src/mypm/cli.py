import click

from mypm.main import (
    compile_version,
    get_latest_version,
    increment_version,
    install_mypm,
)
from mypm.settings import CONFIG_PATH


@click.group()
def cli():
    pass


@cli.command(name="compile")
@click.argument("version", required=False, default=None)
@click.option(
    "--config",
    default=str(CONFIG_PATH),
    show_default=True,
    help="Path to projects.yml.",
)
@click.option(
    "--silent",
    "-s",
    is_flag=True,
    default=False,
    help="Overwrite latest version without prompting.",
)
def _compile(version, config, silent):
    """Compile projects.yml into shell scripts for VERSION."""
    if version is None:
        current = get_latest_version()
        if current is None:
            raise click.UsageError(
                "No existing version found. Please provide a version."
            )
        if silent:
            version = current
        else:
            overwrite = click.confirm(
                f"Overwrite latest version ({current})?", default=True
            )
            version = current if overwrite else increment_version(current)

    config_path = click.Path(exists=True)(config)
    click.echo(f"Compiling {version} from {config}...")
    compile_version(version, config_path)  # type: ignore
    click.echo("Done.")


@cli.command(name="install")
@click.option(
    "--config",
    default=str(CONFIG_PATH),
    show_default=True,
    help="Path to projects.yml.",
)
def _install_mypm():
    """Add mypm to .zshrc."""
    added = install_mypm()  # type: ignore
    if added:
        click.echo("Installed. Restart your shell or run: source ~/.zshrc")
    else:
        click.echo("Already installed in ~/.zshrc.")


def main():
    cli()
