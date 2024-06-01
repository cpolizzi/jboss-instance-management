import sys

import typer
from rich import print

app = typer.Typer(rich_markup_mode="rich")

import service.impl


#=====
# Build the CLI
@app.command()
def add(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = service.impl.ServiceImpl(name)
    target.add()


@app.command()
def remove(
    name: str = typer.Argument(..., help="Instance name"),
):
    target = service.impl.ServiceImpl(name)
    target.remove()
#-----


if __name__ == "__main__":
    app()