from fastapi import APIRouter, HTTPException, Query
from backend.database import cursor

router = APIRouter()

@router.get("/user-plan")
def get_user_plan(username: str = Query(..., description="Nome do usuário a ser consultado")):
    """Retorna o plano do usuário cadastrado no sistema."""

    try:
        cursor.execute("SELECT plan FROM users WHERE username=?", (username,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {"username": username, "plan": result[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
