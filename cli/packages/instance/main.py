import sys

import typer
from rich import print

app = typer.Typer(rich_markup_mode="rich")

import instance.impl


#=====
# Build the CLI
@app.command()
def add(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Add instance
    """
    target = instance.impl.InstanceImpl(name)
    target.add()


@app.command()
def remove(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Remove instance
    """
    target = instance.impl.InstanceImpl(name)
    target.remove()


@app.command()
def list(
):
    """
    List known instances
    """
    instance.impl.InstanceImpl.list()


@app.command()
def start(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Start instance
    """
    target = instance.impl.InstanceImpl(name)
    target.start()


@app.command()
def stop(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Stop instance
    """
    target = instance.impl.InstanceImpl(name)
    target.stop()


@app.command()
def restart(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Restart instance
    """
    target = instance.impl.InstanceImpl(name)
    target.restart()


@app.command()
def status(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Show instance status
    """
    target = instance.impl.InstanceImpl(name)
    target.status()


@app.command()
def kill(
    name: str = typer.Argument(..., help="Instance name"),
):
    """
    Forcefully stop an instance
    """
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
    """
    Execute commands against an instance
    """
    target = instance.impl.InstanceImpl(name)
    target.cli(command, file)
#-----


if __name__ == "__main__":
    app()