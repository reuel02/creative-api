from fastapi import Depends
from app.crud.crud_user import create_user
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.user import UserCreate
from fastapi import APIRouter
from app.core.database import get_db


router = APIRouter()

@router.post("/users/")
async def post_user(usuario: UserCreate, session: AsyncSession = Depends(get_db)):
    novo_usuario = await create_user(session, usuario)

    return novo_usuario

