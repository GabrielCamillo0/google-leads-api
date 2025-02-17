from fastapi import APIRouter, HTTPException
from backend.database import conn, cursor
from backend.models import User
import bcrypt

router = APIRouter()

@router.post("/register")
def register(user: User):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    api_key = bcrypt.gensalt().decode("utf-8")[:20]

    try:
        cursor.execute("INSERT INTO users (username, password, api_key, plan) VALUES (?, ?, ?, ?)",
                       (user.username, hashed_password, api_key, "free"))
        conn.commit()
        return {"message": "Usuário registrado", "api_key": api_key}
    except:
        raise HTTPException(status_code=400, detail="Usuário já existe")

@router.post("/login")
def login(user: User):
    cursor.execute("SELECT id, password, api_key, plan FROM users WHERE username=?", (user.username,))
    result = cursor.fetchone()

    if not result or not bcrypt.checkpw(user.password.encode("utf-8"), result[1].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"api_key": result[2], "plan": result[3]}
