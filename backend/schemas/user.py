from pydantic import BaseModel

class SchemaRegister(BaseModel):
    email: str
    password: str
    role: str

class SchemaLogin(BaseModel):
    email: str
    password: str

class SchemaUserResponse(BaseModel):
    access_token: str
    token_type: str