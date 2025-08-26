# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uvicorn
from icp_client import register_user, take_loan, repay_loan, get_user, get_all_users, deposit_btc, delete_user

app = FastAPI(title="Bitcoin Loan API", version="1.0.0")

class RegisterIn(BaseModel):
    name: str = Field(..., min_length=1)

class LoanIn(BaseModel):
    name: str
    amount: int = Field(..., ge=0)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/register")
def api_register(payload: RegisterIn):
    try:
        msg = register_user(payload.name)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/loan")
def api_loan(payload: LoanIn):
    try:
        msg = take_loan(payload.name, payload.amount)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/repay")
def api_repay(payload: LoanIn):
    try:
        msg = repay_loan(payload.name, payload.amount)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/deposit")
def api_deposit(payload: LoanIn):
    try:
        msg = deposit_btc(payload.name, payload.amount)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/user/{name}")
def api_get_user(name: str):
    try:
        u = get_user(name)
        if not u:
            raise HTTPException(404, "User not found")
        return u
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/users")
def api_get_users():
    try:
        return {"users": get_all_users()}
    except Exception as e:
        raise HTTPException(500, str(e))

@app.delete("/user/{name}")
def api_delete_user(name: str):
    try:
        msg = delete_user(name)
        return {"message": msg}
    except Exception as e:
        raise HTTPException(500, str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
