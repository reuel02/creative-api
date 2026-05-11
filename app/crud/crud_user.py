from app.models.schedule import Schedule
from Lib.site-packages.sqlalchemy.sql import select
from Lib.site-packages.sqlalchemy import select
from Lib.site-packages.sqlalchemy.orm import query
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

async def get_users_by_department(session: AsyncSession, department_id):
    try:
        query = select(User).join(Schedule).where(Schedule.department_id == department_id)

        resultado
    except Exception as e:
        return {"message": str(e)}




     
