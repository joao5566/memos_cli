import typer
from cli import config_app

app = typer.Typer()

app.add_typer(config_app, name="config")
