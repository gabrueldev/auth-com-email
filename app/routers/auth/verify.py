
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time

from .user_schema import UserVerify
from database.connect import get_db
from database.models import User, PendingUser
from database.security import verify_codigo

MAX_TENTATIVAS = 5

router = APIRouter(
    prefix="/user/verify",
    tags=["verify"]
)

@router.post("/", status_code=201)
async def verify_email(data: UserVerify, db: Session = Depends(get_db)):

    registro = db.query(PendingUser).filter_by(email=data.email).first()

    if not registro:
        raise HTTPException(status_code=404, detail="Código não encontrado")
    if time.time() > registro.expira:
        raise HTTPException(status_code=400, detail="Código expirado, peça um novo")
    if registro.tentativas >= MAX_TENTATIVAS:
        raise HTTPException(status_code=429, detail="Muitas tentativas, peça um novo código")
    if not verify_codigo(data.codigo, registro.codigo):
        registro.tentativas += 1
        db.commit()
        raise HTTPException(status_code=400, detail="Código inválido")

    new_user = User(
        email=registro.email,
        name=registro.name,
        password=registro.password
    )
    db.add(new_user)
    db.delete(registro)
    db.commit()

    return {"message": "Usuário cadastrado com sucesso!"}
