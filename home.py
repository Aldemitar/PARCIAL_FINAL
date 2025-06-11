from contextlib import asynccontextmanager
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

from utils.connection_db import init_db, get_session

from data.models import Usuario, Mascota, Vuelo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import func

from typing import List, Optional

from operations.operations_db import obtener_usuarios_db

@asynccontextmanager
async def lifespan(app: APIRouter):
    await init_db()
    yield

templates = Jinja2Templates(directory="templates")
router = APIRouter(lifespan=lifespan)

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("usuario_registro.html", {"request": request})

@router.get("/usuarios_registro", response_class=HTMLResponse, tags=["Usuarios"])
async def usuario_html(
    request: Request,
    session: AsyncSession = Depends(get_session),
    id: int = None,
):
    usuarios = []
    usuarios = await obtener_usuarios_db(session)

    return templates.TemplateResponse("usuarios_registro.html", {
        "request": request,
        "sesiones": usuarios,
        "titulo": "Usuarios registrados",
    })