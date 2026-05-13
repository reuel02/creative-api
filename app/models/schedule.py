from sqlalchemy import ForeignKey
from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime
from sqlalchemy import DateTime

class Schedule(Base):
    __tablename__ = 'escalas'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    department_id: Mapped[int] = mapped_column(ForeignKey("departamentos.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    usuario: Mapped["User"] = relationship("User", back_populates="escalas")
    departamento: Mapped["Department"] = relationship("Department", back_populates="escalas")
