from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connect import get_db
from database.models import User, PendingUser
from database.security import hash_password, gerar_codigo, hash_codigo
from .user_schema import UserCreate, UserResend

from ..email.confirm_email import enviar_codigo

import time

CODIGO_EXPIRA_EM_SEGUNDOS = 5 * 60

router = APIRouter(
    prefix="/user/cadaster",
    tags=["cadaster_user"]
)

def salvar_ou_substituir_cadastro_pendente(db, user, codigo):
    pending = db.query(PendingUser).filter_by(email=user.email).first() or PendingUser(email=user.email)
    pending.name = user.name
    pending.password = hash_password(user.password)
    pending.codigo = hash_codigo(codigo)
    pending.expira = time.time() + CODIGO_EXPIRA_EM_SEGUNDOS
    pending.tentativas = 0
    db.add(pending)
    db.commit()

@router.post("/", status_code=202)
async def cadaster_user(user: UserCreate, db: Session = Depends(get_db)):

    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")

    codigo = gerar_codigo()
    salvar_ou_substituir_cadastro_pendente(db, user, codigo)
    await enviar_codigo(user.email, codigo)

    return {"message": "Código enviado para o email"}

@router.post("/reenviar", status_code=202)
async def reenviar_codigo(data: UserResend, db: Session = Depends(get_db)):

    pending = db.query(PendingUser).filter_by(email=data.email).first()
    if not pending:
        raise HTTPException(status_code=404, detail="Nenhum cadastro pendente para esse email")

    codigo = gerar_codigo()
    pending.codigo = hash_codigo(codigo)
    pending.expira = time.time() + CODIGO_EXPIRA_EM_SEGUNDOS
    pending.tentativas = 0
    db.commit()

    await enviar_codigo(data.email, codigo)

    return {"message": "Novo código enviado para o email"}
