from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from app.db import engine
from app.models.user_model import User
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(tags=["Users"])


# =========================
# Schemas
# =========================

class RegisterRequest(BaseModel):
    email: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# Register
# =========================

@router.post("/register")
def register_user(data: RegisterRequest):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(User.email == data.email)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(data.password)

        new_user = User(
            email=data.email,
            password=hashed_password
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return {
        "success": True,
        "message": "User registered successfully"
    }


# =========================
# Login
# =========================

@router.post("/login")
def login_user(data: LoginRequest):
    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == data.email)
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.email})

        return {
            "success": True,
            "access_token": token,
            "token_type": "bearer"
        }
