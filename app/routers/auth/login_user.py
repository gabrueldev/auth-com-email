
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connect import get_db
from database.models import User
from database.security import verify_password, create_access_token
from .user_schema import UserLogin

router = APIRouter(
    prefix="/user/login",
    tags=["login_user"]
)

@router.post("/")
async def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter_by(email=user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        data={"sub": db_user.email}
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }
