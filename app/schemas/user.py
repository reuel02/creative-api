from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    nome: str = Field(..., description="Nome do usuário", max_length=30)
    telefone: str = Field(..., description="Telefone de contato", max_length=20)
    department_id: int = Field(..., description="ID do departamento")
    email: str | None = Field(None, description="Email do voluntário", max_length=100)
    cargo: str = Field("Voluntário", description="Cargo: Líder ou Voluntário", max_length=20)

class UserUpdate(BaseModel):
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None
    cargo: str | None = None
    ativo: bool | None = None
    department_id: int | None = None

class UserResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    department_id: int
    email: str | None = None
    cargo: str
    ativo: bool
    data_entrada: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(UserResponse):
    """Resposta com dados extras para a tela de perfil."""
    departamento_nome: str
    total_escalas: int
