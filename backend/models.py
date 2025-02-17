from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class APIKey(BaseModel):
    api_key: str
