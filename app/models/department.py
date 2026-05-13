from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Department(Base):
    __tablename__ = "departamentos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)

    usuarios: Mapped[list["User"]] = relationship("User", back_populates="departamento")
    escalas: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="departamento")
