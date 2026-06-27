from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)