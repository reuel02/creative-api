from typing import List, Literal
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class Culto(BaseModel):
    nome: str
    data: datetime

class SchedulesCreate(BaseModel):
    department_id: int = Field(..., description="Id do departamento", max_length=3)
    mes: str = Field(..., description="Mes da escala", max_length=20)
    cultos: List[Culto] = Field(..., description="Lista de cultos enviados")

# --- Schemas de Resposta para Listagem Mensal ---

class MembroEquipe(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)

class DepartamentoEscala(BaseModel):
    id: int
    nome: str
    equipe: List[MembroEquipe]
    alerta: str | None = None

class DiaEscala(BaseModel):
    dia: str = Field(..., description="Data no formato YYYY-MM-DD")
    dia_formatado: str = Field(..., description="Data formatada (ex: 04 de Maio)")
    dia_semana: str = Field(..., description="Dia da semana e horário (ex: Domingo — 19h)")
    status: Literal["confirmada", "alerta", "critica"]
    departamentos: List[DepartamentoEscala]