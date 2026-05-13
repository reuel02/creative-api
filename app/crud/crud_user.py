from app.models.schedule import Schedule
from app.models.user import User
from app.models.department import Department
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy import select, func
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
        await session.rollback()
        raise e


async def get_all_users(session: AsyncSession):
    """Retorna todos os usuários com o nome do departamento."""
    try:
        query = (
            select(User, Department.nome.label("departamento_nome"))
            .join(Department, User.department_id == Department.id)
            .order_by(Department.nome, User.nome)
        )
        resultado = await session.execute(query)
        return resultado.all()
    except Exception as e:
        raise e


async def get_users_by_department(session: AsyncSession, department_id: int):
    try:
        query = select(User).where(User.department_id == department_id).order_by(User.nome)
        resultado = await session.execute(query)
        return resultado.scalars().all()
    except Exception as e:
        raise e


async def get_user_profile(session: AsyncSession, user_id: int):
    """Retorna perfil completo do usuário com departamento e total de escalas."""
    try:
        # Buscar usuário + departamento
        query = (
            select(User, Department.nome.label("departamento_nome"))
            .join(Department, User.department_id == Department.id)
            .where(User.id == user_id)
        )
        resultado = await session.execute(query)
        row = resultado.first()

        if not row:
            return None

        user, dept_nome = row

        # Contar total de escalas
        count_query = select(func.count()).select_from(Schedule).where(Schedule.user_id == user_id)
        count_result = await session.execute(count_query)
        total_escalas = count_result.scalar() or 0

        return {
            "id": user.id,
            "nome": user.nome,
            "telefone": user.telefone,
            "department_id": user.department_id,
            "email": user.email,
            "cargo": user.cargo,
            "ativo": user.ativo,
            "data_entrada": user.data_entrada,
            "departamento_nome": dept_nome,
            "total_escalas": total_escalas,
        }
    except Exception as e:
        raise e


async def update_user(session: AsyncSession, user_id: int, schema: UserUpdate):
    try:
        query = select(User).where(User.id == user_id)
        resultado = await session.execute(query)
        user = resultado.scalars().first()

        if not user:
            return None

        dados = schema.model_dump(exclude_unset=True)
        for key, value in dados.items():
            setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        await session.rollback()
        raise e
