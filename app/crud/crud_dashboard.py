from app.models.cult import Cult
from app.models.department import Department
from app.models.user import User
from sqlalchemy import select, func, extract
from app.models.schedule import Schedule
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

async def get_total_schedules(session: AsyncSession):
    try:
        current_date = datetime.now()
        
        # Cria a query para contar as escalas
        query = select(func.count()).select_from(Schedule).where(
            extract('year', Schedule.data_hora) == current_date.year,
            extract('month', Schedule.data_hora) == current_date.month
        )

        resultado = await session.execute(query)
        total = resultado.scalar() or 0

        return total
    except Exception as e:
        return {"message": str(e)}

async def get_total_users(session: AsyncSession):
    try:
        query = select(func.count()).select_from(User)

        resultado = await session.execute(query)
        total = resultado.scalar() or 0

        return total
    except Exception as e:
        return {"message": str(e)}

async def get_total_departments(session: AsyncSession):
    try:
        query = select(func.count()).select_from(Department)

        resultado = await session.execute(query)
        total = resultado.scalar() or 0

        return total
    except Exception as e:
        return {"message": str(e)}

async def get_total_cults(session: AsyncSession):
    try:
        current_date = datetime.now()
        
        query = select(func.count()).select_from(Cult).where(
            extract('year', Schedule.data_hora) == current_date.year,
            extract('month', Schedule.data_hora) == current_date.month
            )

        resultado = await session.execute(query)
        total = resultado.scalar() or 0

        return total
    except Exception as e:
        return {"message": str(e)}