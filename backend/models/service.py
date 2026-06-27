from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Service(Base):
    __tablename__ = "services"

    service_id: Mapped[int] = mapped_column(primary_key=True)