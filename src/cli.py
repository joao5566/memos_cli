import typer
from client import MemosClient
from config import ConfigManager


app = typer.Typer()
client = MemosClient()
config = ConfigManager()

@app.command()
def list(limit: int = 10, page_token: str = typer.Option(None, help="Token da próxima página"), tag:  list[str] = None):
    """Lista memos com paginação"""
    actual_limit = 1000000000 if tag else limit
    memos,next_token = client.get(limit=actual_limit,page_token=page_token)
    if not memos:
        print("nenhum memo encontrado")
        return
    
    print(f"Mostrando {len(memos)} memos (limit={limit})\n")
    
    for i,memo in enumerate(memos, start=1):
        memo_tags = memo.get("tags", [])
        if tag is None or any(t in memo_tags for t in tag):
            print(f"{i}. {memo.get('content', '',).strip()}")
            #print(f"tags {memo.get("tags: ", ["baixar"])}")

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
def set(url: str =typer.Option(None) , token: str=typer.Option(None)):
    """Define configurações"""
    config.set("MEMOS_API_URL", url)
    config.set("MEMOS_TOKEN", token)
    config.save()
    print("✅ Configurações salvas!")

@app.command()
def get_recent(days: int = 7):
    client.print_recent_memos(days)


