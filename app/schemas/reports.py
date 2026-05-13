from pydantic import BaseModel, Field
from typing import Optional

class ScheduleManualCreate(BaseModel):
    """Schema para criação manual de escala via formulário."""
    data_hora: str = Field(..., description="Data e hora da escala (ISO format)")
    department_id: int = Field(..., description="ID do departamento")
    culto_id: int | None = Field(None, description="ID do culto vinculado")
    voluntarios_ids: list[int] = Field(..., description="Lista de IDs dos voluntários selecionados")
    observacoes: str | None = Field(None, description="Observações opcionais")


class ReportMetrics(BaseModel):
    participacao_media: float
    faltas_no_mes: int
    escalas_concluidas: int
    total_escalas: int


class VoluntarioRanking(BaseModel):
    id: int
    nome: str
    total_escalas: int
