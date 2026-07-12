import click

from mypm.main import compile_version, get_latest_version, increment_version, setup_mypm


@click.group()
def cli():
    pass


@cli.command(name="compile")
@click.argument("version", required=False, default=None)
@click.option(
    "--silent",
    "-s",
    is_flag=True,
    default=False,
    help="Overwrite latest version without prompting.",
)
def _compile(version, silent):
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

    click.echo(f"Compiling {version}...")
    compile_version(version)
    click.echo("Done.")


@cli.command(name="setup")
def _setup_mypm():
    """Add mypm to .zshrc."""
    added = setup_mypm()
    if added:
        click.echo("Installed. Restart your shell or run: source ~/.zshrc")
    else:
        click.echo("Already installed in ~/.zshrc.")


def main():
    cli()
