from contextlib import asynccontextmanager
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

from utils.connection_db import init_db, get_session

from data.models import Usuario, Mascota, Vuelo
from data.schemas import UsuarioCreateForm, UsuarioCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import func

from typing import List, Optional

from operations.operations_db import obtener_usuarios_db, crear_usuario_db

@asynccontextmanager
async def lifespan(app: APIRouter):
    await init_db()
    yield

templates = Jinja2Templates(directory="templates")
router = APIRouter(lifespan=lifespan)

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("vuelos.html", {"request": request})

@router.get("/usuarios_registro", response_class=HTMLResponse, tags=["Usuarios"])
async def usuario_html(request: Request,session: AsyncSession = Depends(get_session),id: int = None,):
    usuarios = []
    usuarios = await obtener_usuarios_db(session)

    usuarios = [u for u in usuarios if not u.eliminado]

    return templates.TemplateResponse("usuarios_registro.html", {
        "request": request,
        "sesiones": usuarios,
        "titulo": "Usuarios registrados",
    })

@router.get("/usuarios/add", response_class=HTMLResponse, tags=["Usuarios"])
async def show_usuario_form(request: Request):
    return templates.TemplateResponse("add_usuario.html", {"request": request, "titulo": "Creación vehículo"})

@router.post("/usuarios/add", status_code=status.HTTP_303_SEE_OTHER, tags=["Usuarios"])
async def submit_usuario_form(
    usuario_form: UsuarioCreateForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    usuario_create = UsuarioCreate(
        nombre=usuario_form.nombre,
        cedula=usuario_form.cedula,
    )
    await crear_usuario_db(usuario_create, session)
    return RedirectResponse(url="/usuarios_registro", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/mascotas_registro", response_class=HTMLResponse, tags=["Mascotas"])
async def mascotas_html(
    request: Request,
    session: AsyncSession = Depends(get_session),
    raza: str = None,
    buscar_id: int = None,
    ):
    query = select(Mascota)
    if raza:
        query = query.where(Mascota.raza == raza)
    if buscar_id:
        query = query.where(Mascota.id == buscar_id)

    result = await session.execute(query)
    mascotas = result.scalars().all()

    razas_result = await session.execute(select(Mascota.raza).distinct())
    razas_disponibles = [r[0] for r in razas_result.all()]


    usuarios_result = await session.execute(select(Usuario))
    usuarios_disponibles = usuarios_result.scalars().all()

    return templates.TemplateResponse("mascotas_registro.html", {
        "request": request,
        "mascotas": mascotas,
        "razas_disponibles": razas_disponibles,
        "usuarios_disponibles": usuarios_disponibles,
        "raza": raza,
        "titulo": "Listado de Mascotas",
        "buscar_id": buscar_id,
    })