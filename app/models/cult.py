from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Cult(Base):
    __tablename__ = "cultos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
