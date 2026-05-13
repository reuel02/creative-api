from typing import List
from datetime import datetime
from fastapi import Depends, Query, APIRouter
from app.crud.crud_schedule import get_monthly_schedules
from app.services.scheduler import generate_monthly_schedule
from app.models.schedule import Schedule
from app.schemas.schedules import DiaEscala, SchedulesCreate
from app.schemas.reports import ScheduleManualCreate
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.core.database import get_db


router = APIRouter()

@router.post("/schedules/generate")
async def post_schedules(dadosEscala: SchedulesCreate, session: AsyncSession = Depends(get_db)):
    
    nova_escala = await generate_monthly_schedule(
        cultos=dadosEscala.cultos, 
        session=session, 
        department_id=dadosEscala.department_id
    )

    return nova_escala

@router.get("/schedules/monthly", response_model=List[DiaEscala])
async def list_monthly_schedules(
    mes: int = Query(..., ge=1, le=12, description="Mês da busca (1-12)"),
    ano: int = Query(..., ge=2020, description="Ano da busca"),
    session: AsyncSession = Depends(get_db),
):
    """Retorna as escalas do mês agrupadas por Dia → Departamentos → Equipe."""
    return await get_monthly_schedules(session, mes, ano)


@router.post("/schedules/create")
async def create_manual_schedule(dados: ScheduleManualCreate, session: AsyncSession = Depends(get_db)):
    """Cria escalas manualmente a partir do formulário (1 registro por voluntário)."""
    try:
        data_hora = datetime.fromisoformat(dados.data_hora)
        escalas_criadas = []

        for user_id in dados.voluntarios_ids:
            nova_escala = Schedule(
                user_id=user_id,
                department_id=dados.department_id,
                data_hora=data_hora,
                culto_id=dados.culto_id,
                observacoes=dados.observacoes,
            )
            session.add(nova_escala)
            escalas_criadas.append(nova_escala)

        await session.commit()

        return {"message": f"{len(escalas_criadas)} escala(s) criada(s) com sucesso"}
    except Exception as e:
        await session.rollback()
        raise e