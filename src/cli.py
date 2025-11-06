import typer
from client import MemosClient
from config import ConfigManager
import os
import tempfile
import subprocess

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
            print(f"Memos ID: {memo.get("name","")}.\n {memo.get('content', '',).strip()}\n")
            #print(f"tags {memo.get("tags: ", ["baixar"])}")

    if next_token:
        print(f"\n➡️ Próxima página: use --page-token {next_token}")


@app.command()
def show():
    """mostra  configuração atual"""
    api_url = config.get("MEMOS_API_URL")
    token = config.get("MEMOS_TOKEN")
    editor = config.get("MEMOS_EDITOR")
    print(f"🔧 Configurações atuais:")
    print(f"   API URL: {api_url}")
    print(f"Seu token: {token}")
    print(f"Seu editor: {editor}")
@app.command()
def set(
    url: str = typer.Option(None, help="URL da API do Memos"),
    token: str = typer.Option(None, help="Token de acesso"),
    editor: str = typer.Option(None, help="Editor de texto padrão (ex: nano, vim, micro)")
):

    """Define configurações"""
    if url:
        config.set("MEMOS_API_URL", url)
    if token:
        config.set("MEMOS_TOKEN", token)
    if editor:
        config.set("MEMOS_EDITOR", editor)
    config.save()
    print("✅ Configurações salvas!")
@app.command()
def get_recent(days: int = 7):
    client.print_recent_memos(days)

@app.command()
def edit(id):
    """Abre o memo no editor e salva alterações"""
    memo = client.get_by_id(id)

    if not memo:
        print("❌ Memo não encontrado.")
        return

    content = memo.get("content", "")
    #editor = os.getenv("EDITOR", "nano")
    editor = config.get("MEMOS_EDITOR", os.getenv("EDITOR", "nano"))
    
    with tempfile.NamedTemporaryFile(mode="w+",suffix=".md",delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        temp_path = tmp.name
    
    # abre o editor
    subprocess.call([editor,temp_path])

    # le o conteudo novo 

    with open(temp_path, "r") as f:
        new_content = f.read()
    

    #remove o  arquivo temporario
    os.remove(temp_path)


    # se o conteúdo mudou, atualiza
    if new_content.strip() != content.strip():
        print("✏️ Salvando alterações...")
        client.update_memo(id, new_content)
    else:
        print("ℹ️ Nenhuma alteração feita.")

@app.command()
def new_memo():
    """cria um novo memo"""
    content= ""
    editor = config.get("MEMOS_EDITOR", os.getenv("EDITOR", "nano"))

    with tempfile.NamedTemporaryFile(mode="w+",suffix=".md",delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        temp_path = tmp.name
   
    # abre o editor
    subprocess.call([editor,temp_path])


    with open(temp_path,"r") as f:
        new_content = f.read()
    client.criar_memo(new_content)

@app.command()
def del_memo(id):
    client.del_memo(id)
    
