
from fastapi import APIRouter
from database.models import User
from database.security import hash_password
from database.connect import SessionLocal
from .user_schema import UserCreate

from ..email.confirm_email import enviar_codigo

import time
import random

codigos_verificacao = {}

def gerar_codigo():
    return str(random.randint(1000, 9999))

router = APIRouter(
    prefix="/user/cadaster",
    tags=["cadaster_user"]
)

@router.post("/")
async def cadaster_user(user: UserCreate):

    codigo = gerar_codigo()
    hashed_password = hash_password(user.password)

    codigos_verificacao[user.email] = {
        "codigo": codigo,
        "name": user.name,
        "password": hashed_password,
        "expira": time.time() + 300
    }

    await enviar_codigo(user.email, codigo)

    return {"message": "Código enviado para o email"}
