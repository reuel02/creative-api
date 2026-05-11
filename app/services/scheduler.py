from app.schemas.schedules import Culto
from app.services.rules_engine import check_monthly_limit
from app.models import department
from app.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from datetime import datetime

# Recebe os dias de culto, busca todos os voluntarios de um determinado departamento e retorna os voluntarios disponiveis

async def generate_monthly_schedule(cultos: list[Culto], session: AsyncSession, department_id):
    try:
        query = select(User).where(User.department_id == department_id)
        resultado = await session.execute(query)
        usuarios = resultado.scalars().all()

        escalas_confirmadas = []

        for culto in cultos:
            for usuario in usuarios:
                limite_ok = await check_monthly_limit(usuario.id, session, culto.data.month, culto.data.year)

                if not limite_ok:
                    continue
            
                descanso_ok = await check_interstice(session, usuario.id, culto.data)

                if not descanso_ok:
                    continue

                nova_escala = Schedule(
                    user_id=usuario.id,
                    department_id=department_id,
                    data_hora=culto.data
                )

                session.add(nova_escala)
                escalas_confirmadas.append(nova_escala)
                
                break
            
        await session.commit()

        return escalas_confirmadas

    except Exception as e:
        raise e
        

