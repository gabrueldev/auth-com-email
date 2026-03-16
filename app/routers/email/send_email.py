
from fastapi import APIRouter

from fastapi_mail import FastMail, MessageSchema
from .email_config import conf
from pydantic import BaseModel, EmailStr
from typing import List
from starlette.responses import JSONResponse

class EmailSchema(BaseModel):
    email: List[EmailStr]

router = APIRouter(
    prefix="/email",
    tags=["send_email"]
)

@router.post("/email/")
async def send_email(email: EmailSchema):
    message = MessageSchema(
        subject = "Teste de Email",
        recipients = email.email,
        body = "<h1>Isso é um teste!</h1>",
        subtype = "html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(
        status_code=200,
        content={"message": "Email enviado com sucesso!"}
        )
