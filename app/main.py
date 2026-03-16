
from fastapi import FastAPI

from .routers.email import send_email, confirm_email
from .routers.auth import cadaster_user, login_user, verify
from database.connect import engine
from database.models import Base

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(cadaster_user.router)
app.include_router(login_user.router)
app.include_router(send_email.router)
app.include_router(confirm_email.router)
app.include_router(verify.router)