import typer
from cli import app as cli_app

app = typer.Typer()
app.add_typer(cli_app, name="memos")

if __name__ == "__main__":
    app()
