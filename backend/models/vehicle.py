from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)