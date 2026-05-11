from app.models.schedule import Schedule
from sqlalchemy import select
from app.models.user import User
from fastapi import Request
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, schema: UserCreate):
    try:
        dados = schema.model_dump()

        user = User(**dados)

        session.add(user)

        await session.commit()

        await session.refresh(user)

        return user
    except Exception as e:
        return {"message": str(e)}

async def get_users_by_department(session: AsyncSession, department_id: int):
    try:
        query = select(User).join(Schedule).where(Schedule.department_id == department_id)

        resultado = await session.execute(query)

        usuarios = resultado.scalars().all()

        return usuarios
    except Exception as e:
        return {"message": str(e)}




     
