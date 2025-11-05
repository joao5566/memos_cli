from click import exceptions
import requests
from requests.models import Response
from config import ConfigManager
from datetime import datetime
config = ConfigManager()

class MemosClient():
    def __init__(self):
        self.limit = 10
        self.offset = 0
        self.days = 7
        self.memos_data = None
        self.next_token = None
    def get_memos_url(self):
        """Obtém a URL base da API"""
        api_url = config.get("MEMOS_API_URL", "").rstrip('/')
        if not api_url:
            raise ValueError("API URL não configurada")
        return f"{api_url}/api/v1/memos"

    def get_headers(self):
        """Obtém os headers com o token"""
        token = config.get("MEMOS_TOKEN")
        if not token:
            raise ValueError("Token não configurado")
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
                }

    def get(self, limit=None, page_token=None):
        """
        Lista todos os memos com paginação
        """
        # Usa valores padrão se não fornecidos
        limit = limit or self.limit
        params = {"pageSize": limit}
        
        if page_token:
            params["pageToken"] = page_token


        try:
            url = self.get_memos_url()
            headers = self.get_headers()
            
            response = requests.get(url, headers=headers, params=params)
             
            response = requests.get(url, headers=headers, params=params)

            # --- DEBUG do Status Code ---
            print(f"🔍 [DEBUG] Código de Status HTTP recebido: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                memos = data.get("memos", [])
                next_token = data.get("nextPageToken", None)

                self.memos_data = memos
                self.next_token = next_token
                return memos, next_token
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                return []
            
                
        except Exception as e:
            print(f"🚨 Erro: {e}")
            return [], None

   
    def get_memos_recent(self, days=7):
        """Retorna memos dos últimos N dias - busca TODAS as páginas"""
        print("📥 Buscando TODOS os memos...")
        
        # Buscar todas as páginas
        all_memos = []
        current_token = None
        
        while True:
            memos, next_token = self.get(limit=100, page_token=current_token)
            if memos:
                all_memos.extend(memos)
            
            if not next_token:
                break
            current_token = next_token
        
        print(f"✅ Total de memos carregados: {len(all_memos)}")
        
        # Agora usar todos os memos para o filtro
        memos_recentes = []
        data_limite = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        print(f"🔍 Data limite: {datetime.fromtimestamp(data_limite)}")
        print(f"📅 Hoje: {datetime.now()}")
        
        for memo in all_memos:
            create_time = memo.get("createTime", "")
            if create_time:
                try:
                    if create_time.endswith('Z'):
                        create_time = create_time.replace('Z', '+00:00')
                    memo_timestamp = datetime.fromisoformat(create_time).timestamp()
                    
                    if memo_timestamp >= data_limite:
                        memos_recentes.append(memo)
                        
                except ValueError:
                    continue
        
        print(f"📊 Memos recentes encontrados: {len(memos_recentes)}")
        memos_recentes.sort(key=lambda x: x.get("createTime", ""), reverse=True)
        return memos_recentes

    
    def print_recent_memos(self, days=7):
        """Imprime memos recentes de forma bonita"""
        recent_memos = self.get_memos_recent(days)
        
        if not recent_memos:
            print(f"📭 Nenhum memo encontrado nos últimos {days} dias")
            return
        
        print(f"\n{'='*60}")
        print(f"📅 MEMOS DOS ÚLTIMOS {days} DIAS".center(60))
        print(f"{'='*60}")
        print(f"📊 Total encontrado: {len(recent_memos)} memo(s)")
        print(f"{'='*60}\n")
        
        for i, memo in enumerate(recent_memos, 1):
            content = memo.get('content', '').strip()
            create_time = memo.get('createTime', '')
            tags = memo.get('tags', [])
            
            # Formata a data
            date_str = ""
            if create_time:
                try:
                    dt = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
                    date_str = dt.strftime('%d/%m/%Y %H:%M')
                except:
                    date_str = create_time
            
            # Header do memo
            print(f"🆔 MEMO #{i}")
            print(f"⏰ {date_str}")
            
            # Tags
            if tags:
                print(f"🏷️  Tags: {', '.join(tags)}")
            
            # Conteúdo
            print("📝 Conteúdo:")
            if content:
                # Quebra o conteúdo em linhas para melhor legibilidade
                lines = content.split('\n')
                for line in lines:
                    if line.strip():  # Não imprime linhas vazias
                        print(f"   {line}")
            else:
                print("   (Sem conteúdo)")
            
            # Separador entre memos
            if i < len(recent_memos):
                print(f"\n{'─'*50}\n")
            else:
                print(f"\n{'='*60}")
    
    def get_by_id(self, memo_id):
        """Obtém um memo específico pelo ID"""
        try:
            url = f"{self.get_memos_url()}/{memo_id}"
            headers = self.get_headers()
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"🚨 Erro de conexão: {e}")
            return None
    def update_memo(self, memo_name: str, new_content: str):
        url = f"{self.get_memos_url()}/{memo_name}"
        payload = {"content": new_content}
        res = requests.patch(url, headers=self.get_headers(), json=payload)
        res.raise_for_status()
        return res.json()

    
    def criar_memo(self,content,visibility="PRIVATE",tags=None,pinned=False):
        """
        Cria um novo memo

        Args:
            conteudo (str): Texto do memo
            visibility (str): "PUBLIC" ou "PRIVATE"
            tags (list): Lista de tags
            pinned (bool): Se deve fixar o memo

        Returns:
            dict: Memo criado ou None em caso de erro
        """
        if tags is None:
            tags = []

        payload = {
                "content": content,
                "visibility": visibility,
                "tags":tags,
                "pinned": pinned
                }
        
        try:
            response = requests.post(self.get_memos_url(),headers=self.get_headers(),json=payload)

            if response.status_code == 200:
                print("✅ Memo criado com sucesso!")
                return response.json()
            else:
                print(f"❌ Erro ao criar memo: {response.status_code}")
                print(f"📄 Detalhes: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
             print(f"🚨 Erro de conexão: {e}")
             return None

    def del_memo(self, id):
        """
        Exclui um memo específico

        Args:
            memo_name (str): ID do memo (ex: "memos/ID_UNICO")

        Returns:
            bool: True se sucesso, False se erro
        """
        dele_url = f"{self.get_memos_url()}/{id}"
        
        try:
            response = requests.delete(dele_url,headers=self.get_headers())

            if response.status_code == 200:
                print("✅ Memo excluído com sucesso!")
                return True
            else:
                print(f"❌ Erro ao excluir memo: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"🚨 Erro de conexão: {e}")
            return False
