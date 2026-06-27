from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Material(Base):
    __tablename__ = "materials"

    material_id: Mapped[int] = mapped_column(primary_key=True)