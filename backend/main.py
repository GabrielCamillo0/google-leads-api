from fastapi import FastAPI
from routes import auth, users, payments, leads


app = FastAPI(title="Google Leads Scraper API")

# Registrar rotas
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(payments.router)
app.include_router(leads.router)

@app.get("/")
def home():
    return {"message": "Bem-vindo à API do Google Leads Scraper!"}
