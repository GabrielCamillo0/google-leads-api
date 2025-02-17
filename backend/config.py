import os
from dotenv import load_dotenv

# Carregar as variáveis do .env
load_dotenv()

# Configuração da API do Google Custom Search
API_KEY = os.getenv("API_KEY")
CX_ID = os.getenv("CX_ID")

# Configuração do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

# Configuração de Segurança (JWT)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"

# Configuração do Stripe (Pagamentos)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Verifica se todas as variáveis foram carregadas corretamente
if not all([API_KEY, CX_ID, SECRET_KEY, STRIPE_SECRET_KEY]):
    raise ValueError("⚠️ Erro: Algumas variáveis de ambiente estão ausentes no .env")
