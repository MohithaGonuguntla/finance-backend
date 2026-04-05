from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    email: str
    role: str
    status: str = "active"

class TransactionModel(BaseModel):
    amount: float
    type: str
    category: str
    date: str
    notes: str
    user_id: int
