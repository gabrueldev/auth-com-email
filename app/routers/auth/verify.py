
from fastapi import APIRouter
import time
from .user_schema import UserVerify
from database.connect import SessionLocal
from .cadaster_user import codigos_verificacao
from database.models import User

router = APIRouter(
    prefix="/user/verify",
    tags=["verify"]
)

@router.post("/")
async def verify_email(data: UserVerify):
    registro = codigos_verificacao.get(data.email)

    if not registro:
        return {"error": "Código não encontrado"}
    if time.time() > registro["expira"]:
        del codigos_verificacao[data.email]
        return {"error": "Código expirado"}
    if registro["codigo"] != data.codigo:
        return {"error": "Código inválido"}

    db = SessionLocal()
    new_user = User(
        email=data.email,
        name=registro["name"],
        password=registro["password"]
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    del codigos_verificacao[data.email]

    return {"message": "Usuário cadastrado com sucesso!"}