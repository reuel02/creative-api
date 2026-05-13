from typing import List
from fastapi import Depends, APIRouter, HTTPException
from app.crud.crud_cult import get_all_cults, get_cult_by_id, create_cult, update_cult, delete_cult
from app.schemas.cults import CultCreate, CultUpdate, CultResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()


@router.get("/cultos/", response_model=List[CultResponse])
async def list_cults(session: AsyncSession = Depends(get_db)):
    return await get_all_cults(session)


@router.get("/cultos/{cult_id}", response_model=CultResponse)
async def get_cult(cult_id: int, session: AsyncSession = Depends(get_db)):
    culto = await get_cult_by_id(session, cult_id)
    if not culto:
        raise HTTPException(status_code=404, detail="Culto não encontrado")
    return culto


@router.post("/cultos/", response_model=CultResponse)
async def post_cult(dados: CultCreate, session: AsyncSession = Depends(get_db)):
    return await create_cult(session, dados)


@router.put("/cultos/{cult_id}", response_model=CultResponse)
async def put_cult(cult_id: int, dados: CultUpdate, session: AsyncSession = Depends(get_db)):
    culto = await update_cult(session, cult_id, dados)
    if not culto:
        raise HTTPException(status_code=404, detail="Culto não encontrado")
    return culto


@router.delete("/cultos/{cult_id}")
async def remove_cult(cult_id: int, session: AsyncSession = Depends(get_db)):
    result = await delete_cult(session, cult_id)
    if not result:
        raise HTTPException(status_code=404, detail="Culto não encontrado")
    return {"message": "Culto excluído com sucesso"}
