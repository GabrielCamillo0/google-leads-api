from fastapi import APIRouter, HTTPException
import requests
from backend.database import cursor
from backend.models import APIKey

router = APIRouter()

@router.post("/search-leads")
def search_leads(api: APIKey, site: str, keyword: str):
    cursor.execute("SELECT plan FROM users WHERE api_key=?", (api.api_key,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="API Key inválida")

    plan = user[0]
    limit = 5 if plan == "free" else 50

    query = f"site:{site} \"{keyword}\""
    response = requests.get(f"https://www.googleapis.com/customsearch/v1?q={query}&key=API_KEY&cx=CX_ID")
    results = response.json().get("items", [])[:limit]

    return [{"title": r["title"], "link": r["link"], "snippet": r.get("snippet", "")} for r in results]
