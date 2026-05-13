from sqlalchemy import String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from datetime import datetime
from typing import Optional
from app.core.database import Base

class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"))

    # Novos campos
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    cargo: Mapped[str] = mapped_column(String(20), nullable=False, server_default="Voluntário")
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="true")
    data_entrada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    departamento: Mapped["Department"] = relationship("Department", back_populates="usuarios")
    escalas: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="usuario")
