from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

# --- Schemas de Cultos ---

class CultCreate(BaseModel):
    nome: str = Field(..., description="Nome do culto", max_length=30)
    data: datetime = Field(..., description="Data e horário do culto")

class CultUpdate(BaseModel):
    nome: str | None = None
    data: datetime | None = None

class CultResponse(BaseModel):
    id: int
    nome: str
    data: datetime

    model_config = ConfigDict(from_attributes=True)
