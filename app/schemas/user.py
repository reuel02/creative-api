from pydantic import BaseModel, Field, ConfigDict

class UserCreate(BaseModel):
    nome: str = Field(..., description="Nome do usuário", max_length=30)
    telefone: str = Field(..., description="Telefone de contato", max_length=20)

class UserResponse(UserCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
