from fastapi import FastAPI

from .routers.auth import cadaster_user, login_user, verify
from .routers.user import me
from database.connect import engine
from database.models import Base

app = FastAPI(title="Auth com Email")

Base.metadata.create_all(bind=engine)

app.include_router(cadaster_user.router)
app.include_router(verify.router)
app.include_router(login_user.router)
app.include_router(me.router)
