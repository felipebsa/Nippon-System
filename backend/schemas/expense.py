from pydantic import BaseModel
from datetime import datetime

class SchemaExpenseCreate(BaseModel):

    name: str
    value: float
    date: datetime

class SchemaExpenseUpdate(BaseModel):

    name: str
    value: float
    date: datetime

class SchemaExpenseResponse(BaseModel):

    expense_id: int
    name: str
    value: float
    date: datetime
    origin: str