from sqlalchemy import String
from sqlalchemy import ForeignKey
from app.models import department
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"))
