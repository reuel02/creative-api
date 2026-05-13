from app.models.cult import Cult
from app.schemas.cults import CultCreate, CultUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_cults(session: AsyncSession):
    try:
        query = select(Cult).order_by(Cult.data.desc())
        resultado = await session.execute(query)
        return resultado.scalars().all()
    except Exception as e:
        raise e


async def get_cult_by_id(session: AsyncSession, cult_id: int):
    try:
        query = select(Cult).where(Cult.id == cult_id)
        resultado = await session.execute(query)
        return resultado.scalars().first()
    except Exception as e:
        raise e


async def create_cult(session: AsyncSession, schema: CultCreate):
    try:
        dados = schema.model_dump()
        culto = Cult(**dados)
        session.add(culto)
        await session.commit()
        await session.refresh(culto)
        return culto
    except Exception as e:
        await session.rollback()
        raise e


async def update_cult(session: AsyncSession, cult_id: int, schema: CultUpdate):
    try:
        culto = await get_cult_by_id(session, cult_id)
        if not culto:
            return None

        dados = schema.model_dump(exclude_unset=True)
        for key, value in dados.items():
            setattr(culto, key, value)

        await session.commit()
        await session.refresh(culto)
        return culto
    except Exception as e:
        await session.rollback()
        raise e


async def delete_cult(session: AsyncSession, cult_id: int):
    try:
        culto = await get_cult_by_id(session, cult_id)
        if not culto:
            return None

        await session.delete(culto)
        await session.commit()
        return True
    except Exception as e:
        await session.rollback()
        raise e
