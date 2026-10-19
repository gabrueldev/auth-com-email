from fastapi_mail import FastMail, MessageSchema
from .email_config import conf

async def enviar_codigo(email: str, codigo: str):

    html = f"""
    <div style="
        font-family: Arial;
        background:#f4f6f8;
        padding:40px;
    ">

        <div style="
            max-width:500px;
            background:white;
            margin:auto;
            padding:30px;
            border-radius:10px;
            text-align:center;
            box-shadow:0 5px 15px rgba(0,0,0,0.1);
        ">

            <h2>Confirme seu cadastro</h2>

            <p>Use o código abaixo para finalizar sua conta:</p>

            <div style="
                font-size:36px;
                font-weight:bold;
                letter-spacing:6px;
                background:#f2f2f2;
                padding:15px;
                border-radius:8px;
                margin:20px 0;
            ">
                {codigo}
            </div>

            <p>Esse código expira em <b>5 minutos</b>.</p>

        </div>

    </div>
    """

    message = MessageSchema(
        subject="Confirmação de cadastro",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)