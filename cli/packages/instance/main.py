import sys

import typer
from rich import print

app = typer.Typer(rich_markup_mode="rich")

import instance.impl


#=====
# Build the CLI
@app.command()
def start(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = instance.impl.InstanceImpl(name)
    target.start()


@app.command()
def stop(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = instance.impl.InstanceImpl(name)
    target.stop()


@app.command()
def restart(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = instance.impl.InstanceImpl(name)
    target.restart()


@app.command()
def status(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = instance.impl.InstanceImpl(name)
    target.status()


@app.command()
def kill(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = instance.impl.InstanceImpl(name)
    target.kill()


# TODO Make `command` multi-value
# TODO Make `command` and `file` mutually exclusive
@app.command()
def cli(
    name: str = typer.Argument(..., help="Instance name"),
    command: str = typer.Option(None, help="Command to execute"),
    file: str = typer.Option(None, help="File containing commands to execute"),
):
    target = instance.impl.InstanceImpl(name)
    target.cli(command, file)
#-----


if __name__ == "__main__":
    app()