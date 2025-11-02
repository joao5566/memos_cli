---

## 📝 Memos CLI

**Memos CLI** é um cliente de terminal para o [Memos](https://usememos.com), feito em Python, que permite gerenciar suas notas diretamente do terminal com comandos estilo Git.

---

### 🚀 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/memos-cli.git
cd memos-cli
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

### ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
MEMOS_API_URL=https://seu-memos.com
MEMOS_TOKEN=seu_token_aqui
EDITOR=nano  # ou vim, code, etc.
```

Você pode gerar seu token no painel do Memos em **Configurações > API Token**.

---

### 🧩 Estrutura do Projeto

```
memos_cli/
├── main.py              # Ponto de entrada da aplicação
├── cli.py               # Comandos Typer organizados
├── client.py            # Comunicação com a API do Memos
├── editor.py            # Abre editor de texto para editar notas
├── config.py            # Gerencia configurações locais
├── memo.py              # Representa uma nota individual
├── store.py             # Armazena notas localmente
├── sync.py              # Sincroniza com o servidor
├── utils.py             # Funções auxiliares
└── constants.py         # Constantes globais
```

---

### 📦 Comandos disponíveis

```bash
memos add "Minha nota"         # Adiciona uma nova nota
memos list                     # Lista todas as notas
memos edit <id>               # Edita uma nota existente
memos delete <id>             # Remove uma nota
memos sync                    # Sincroniza notas locais com o servidor
memos config set <chave> <valor>  # Define uma configuração
```

---

### 🛠 Requisitos

- Python 3.8+
- Editor de texto instalado (nano, vim, etc.)
- Conta no Memos com token de API

---


