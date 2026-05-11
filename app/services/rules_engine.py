from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from app.models.schedule import Schedule
from datetime import datetime, timedelta

async def check_monthly_limit(user_id: int, session: AsyncSession, mes: int, ano: int):
    try:
        query = select(func.count()).select_from(Schedule).where(
            Schedule.user_id == user_id,
            extract('month', Schedule.data_hora) == mes,
            extract('year', Schedule.data_hora) == ano
            )

        resultado = await session.execute(query)

        total_escalas = resultado.scalar()

        if total_escalas >= 4:
            return False

        return True

    except Exception as e:
        raise e

async def check_interstice(session: AsyncSession, user_id: int, nova_data_hora: datetime):
    try:
        query = select(Schedule).where(Schedule.user_id == user_id).order_by(Schedule.data_hora.desc()).limit(1)

        resultado = await session.execute(query)

        ultimo_servico = resultado.scalars().first()

        if not ultimo_servico:
            return True

        diferenca = abs(nova_data_hora - ultimo_servico.data_hora)

        if diferenca >= timedelta(hours=12):
            return True
        else:
            return False

    except Exception as e:
        raise e