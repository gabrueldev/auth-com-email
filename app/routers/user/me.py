from fastapi import APIRouter, Depends

from database.models import User
from database.security import get_current_user
from ..auth.user_schema import UserOut

router = APIRouter(
    prefix="/user/me",
    tags=["user"]
)

@router.get("/", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
