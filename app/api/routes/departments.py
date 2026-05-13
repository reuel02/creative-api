from typing import List
from fastapi import Depends, APIRouter
from app.models.department import Department
from app.schemas.departments import DepartmentResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()


@router.get("/departments/", response_model=List[DepartmentResponse])
async def list_departments(session: AsyncSession = Depends(get_db)):
    query = select(Department).order_by(Department.nome)
    resultado = await session.execute(query)
    return resultado.scalars().all()
