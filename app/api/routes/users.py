from typing import List
from fastapi import Depends, APIRouter, HTTPException
from app.crud.crud_user import get_all_users, get_user_profile, update_user, create_user, get_users_by_department
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserProfileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

router = APIRouter()


@router.get("/users/")
async def list_users(session: AsyncSession = Depends(get_db)):
    """Lista todos os usuários agrupados por departamento."""
    rows = await get_all_users(session)
    resultado = []
    for user, dept_nome in rows:
        resultado.append({
            "id": user.id,
            "nome": user.nome,
            "telefone": user.telefone,
            "department_id": user.department_id,
            "email": user.email,
            "cargo": user.cargo,
            "ativo": user.ativo,
            "data_entrada": user.data_entrada,
            "departamento_nome": dept_nome,
        })
    return resultado


@router.get("/users/department/{department_id}", response_model=List[UserResponse])
async def list_users_by_department(department_id: int, session: AsyncSession = Depends(get_db)):
    return await get_users_by_department(session, department_id)


@router.get("/users/{user_id}", response_model=UserProfileResponse)
async def get_profile(user_id: int, session: AsyncSession = Depends(get_db)):
    perfil = await get_user_profile(session, user_id)
    if not perfil:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return perfil


@router.post("/users/", response_model=UserResponse)
async def post_user(usuario: UserCreate, session: AsyncSession = Depends(get_db)):
    return await create_user(session, usuario)


@router.put("/users/{user_id}", response_model=UserResponse)
async def put_user(user_id: int, dados: UserUpdate, session: AsyncSession = Depends(get_db)):
    user = await update_user(session, user_id, dados)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
