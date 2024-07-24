import sys

import typer
from rich import print

app = typer.Typer(rich_markup_mode="rich")

import expression.impl


#=====
# Build the CLI
@app.command()
def encrypt(
    name: str = typer.Argument(..., help="Instance name"),
    expr: str = typer.Argument(..., help="Expression"),
    resolver: str = typer.Option(None, help="Encryption resolver to use"),
):
    """
    [bold italic orange_red1]Not yet implemented[/bold italic orange_red1] Encrypts an expression.
    """
    target = expression.impl.ExpressionImpl(name)
    target.encrypt(expr, resolver)


if __name__ == "__main__":
    app()