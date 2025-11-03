import typer
from client import MemosClient
from config import ConfigManager


app = typer.Typer()
client = MemosClient()
config = ConfigManager()

@app.command()
#def list(limit: int = 10, offset: int = 0):
def list(limit: int = 10, page_token: str = typer.Option(None, help="Token da próxima página")):
    """Lista memos com paginação"""
    memos,next_token = client.get(limit=limit,page_token=page_token)
    if not memos:
        print("nenhum memo encontrado")
        return
    
    print(f"Mostrando {len(memos)} memos (limit={limit})\n")
    
    for i,memo in enumerate(memos, start=1):
        print(f"{i}. {memo.get('content', '').strip()}")

    if next_token:
        print(f"\n➡️ Próxima página: use --page-token {next_token}")


@app.command()
def show():
    """mostra  configuração atual"""
    api_url = config.get("MEMOS_API_URL")
    token = config.get("MEMOS_TOKEN")

    print(f"🔧 Configurações atuais:")
    print(f"   API URL: {api_url}")
    print(f"Seu token: {token}")

@app.command()
def set(url: str, token: str):
    """Define configurações"""
    config.set("MEMOS_API_URL", url)
    config.set("MEMOS_TOKEN", token)
    config.save()
    print("✅ Configurações salvas!")

