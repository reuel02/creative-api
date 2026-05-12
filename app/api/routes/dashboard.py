from app.crud.crud_dashboard import get_total_cults
from app.crud.crud_dashboard import get_total_departments
from app.crud.crud_dashboard import get_total_users
from app.crud.crud_dashboard import get_total_schedules
from app.core.database import get_db
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

router = APIRouter()

class MetricsResponse(BaseModel):
    total_schedules: int
    total_users: int
    total_departments: int
    total_cults: int

@router.get("/dashboard/metricas", response_model=MetricsResponse)
async def get_metrics(session: AsyncSession = Depends(get_db)):
    total_schedules = await get_total_schedules(session)
    
    total_users = await get_total_users(session)

    total_departments = await get_total_departments(session)

    total_cults = await get_total_cults(session)

    response: MetricsResponse = {
        total_schedules,
        total_users,
        total_departments,
        total_cults
    }

    return response