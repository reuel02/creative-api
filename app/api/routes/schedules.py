from fastapi import Depends
from app.services.scheduler import generate_monthly_schedule
from app.schemas.schedules import SchedulesCreate
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