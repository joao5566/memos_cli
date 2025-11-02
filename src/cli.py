import typer
from config import ConfigManager


config_app = typer.Typer()
config = ConfigManager()



api_url = config.get("MEMOS_API_URL")
token = config.get("MEMOS_TOKEN")

print("URL:", api_url)
print("Token:", token)


@config_app.command("set")
def set_config(key: str,value:str):
    """Define a configuração local"""
    config.set(key,value)
    typer.echo(f"{key} definido  como {value}")

@config_app.command("get")
def get_config(key: str):
    """Consulta uma configuração"""
    value = config.get(key)
    typer.echo(f"{key}: {value if value else 'Não definido'}")

