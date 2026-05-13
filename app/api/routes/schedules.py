from typing import List
from fastapi import Depends, Query
from app.crud.crud_schedule import get_monthly_schedules
from app.services.scheduler import generate_monthly_schedule
from app.schemas.schedules import DiaEscala, SchedulesCreate
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import APIRouter
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