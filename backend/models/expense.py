from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Expense(Base):
    __tablename__ = "expenses"

    expense_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    value: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
    origin: Mapped[str] = mapped_column()