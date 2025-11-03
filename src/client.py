import requests
from config import ConfigManager

config = ConfigManager()

class MemosClient():
    def __init__(self):
        self.limit = 10
        self.offset = 0

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
                return memos, next_token
            else:
                print(f"❌ Erro {response.status_code}: {response.text}")
                return []
            
                
        except Exception as e:
            print(f"🚨 Erro: {e}")
            return [], None
