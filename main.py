from fastapi import FastAPI, HTTPException
from database import create_tables
from models import UserModel, TransactionModel
import services

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

#Users

@app.post("/users")
def create_user(user: UserModel):
    if user.role not in ["admin", "analyst", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    services.add_user(user)
    return {"message": "User created"}

@app.get("/users")
def get_users():
    return services.fetch_users()


#Transactions

@app.post("/transactions")
def create_transaction(txn: dict):
    if txn["amount"] <= 0:
        raise HTTPException(400, "Amount must be positive")

    txn_obj = TransactionModel(**txn)
    services.add_transaction(txn_obj)

    return {"message": "Transaction added"}


@app.get("/transactions")
def get_transactions(type: str = None, category: str = None):
    return services.fetch_transactions(type, category)


#Dashboard

@app.get("/dashboard")
def summary():
    return services.get_dashboard_data()
