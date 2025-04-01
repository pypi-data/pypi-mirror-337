import click

from tinybird.tb.modules.cli import cli


@cli.command(
    name="push",
    context_settings=dict(
        ignore_unknown_options=True,
    ),
)
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def push(args) -> None:
    """
    `tb push` is deprecated. Use `tb deploy` instead.
    """
    click.echo(
        "You are using Tinybird Forward CLI. This command is deprecated. Use `tb deploy` instead. "
        "You can find more information in the docs at https://www.tinybird.co/docs/forward"
    )
