from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

class Culto(BaseModel):
    nome: str
    data: datetime

class SchedulesCreate(BaseModel):
    department_id: int = Field(..., description="Id do departamento", max_length=3)
    mes: str = Field(..., description="Mes da escala", max_length=20)
    cultos: List[Culto] = Field(..., description="Lista de cultos enviados")