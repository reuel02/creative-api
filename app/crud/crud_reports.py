from app.models.schedule import Schedule
from app.models.user import User
from app.models.department import Department
from sqlalchemy import select, func, extract
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


async def get_report_metrics(session: AsyncSession, mes: int, ano: int):
    """Calcula métricas: participação média, faltas, escalas concluídas."""
    try:
        # Total de escalas no mês
        total_query = select(func.count()).select_from(Schedule).where(
            extract('month', Schedule.data_hora) == mes,
            extract('year', Schedule.data_hora) == ano,
        )
        total_result = await session.execute(total_query)
        total_escalas = total_result.scalar() or 0

        # Escalas concluídas (passadas = concluídas)
        agora = datetime.now()
        concluidas_query = select(func.count()).select_from(Schedule).where(
            extract('month', Schedule.data_hora) == mes,
            extract('year', Schedule.data_hora) == ano,
            Schedule.data_hora < agora,
        )
        concluidas_result = await session.execute(concluidas_query)
        escalas_concluidas = concluidas_result.scalar() or 0

        # Total de voluntários ativos
        total_voluntarios_query = select(func.count()).select_from(User).where(User.ativo == True)
        vol_result = await session.execute(total_voluntarios_query)
        total_voluntarios = vol_result.scalar() or 1  # evitar divisão por zero

        # Voluntários que participaram de pelo menos 1 escala no mês
        participantes_query = (
            select(func.count(func.distinct(Schedule.user_id)))
            .select_from(Schedule)
            .where(
                extract('month', Schedule.data_hora) == mes,
                extract('year', Schedule.data_hora) == ano,
            )
        )
        participantes_result = await session.execute(participantes_query)
        participantes = participantes_result.scalar() or 0

        participacao_media = round((participantes / total_voluntarios) * 100, 1)

        # Faltas = voluntários ativos que NÃO participaram
        faltas = total_voluntarios - participantes

        return {
            "participacao_media": participacao_media,
            "faltas_no_mes": faltas,
            "escalas_concluidas": escalas_concluidas,
            "total_escalas": total_escalas,
        }
    except Exception as e:
        raise e


async def get_volunteer_ranking(session: AsyncSession):
    """Ranking dos voluntários por total de escalas (todas)."""
    try:
        query = (
            select(User.id, User.nome, func.count(Schedule.id).label("total_escalas"))
            .join(Schedule, User.id == Schedule.user_id)
            .group_by(User.id, User.nome)
            .order_by(func.count(Schedule.id).desc())
            .limit(10)
        )
        resultado = await session.execute(query)
        rows = resultado.all()

        return [
            {"id": row.id, "nome": row.nome, "total_escalas": row.total_escalas}
            for row in rows
        ]
    except Exception as e:
        raise e
