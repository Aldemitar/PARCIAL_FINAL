from contextlib import asynccontextmanager
from fastapi import APIRouter, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

from utils.connection_db import init_db, get_session

from data.models import Usuario, Mascota, Vuelo
from data.schemas import UsuarioCreateForm, UsuarioCreate, MascotaCreateForm, MascotaCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy import func

from typing import List, Optional

from operations.operations_db import obtener_usuarios_db, crear_usuario_db, crear_mascota_db, obtener_mascotas_db, actualizar_usuario_db, eliminar_usuario_db

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
async def mascota_html(
    request: Request,
    session: AsyncSession = Depends(get_session),
    id: int = None,
    ):
    mascotas = []
    mascotas = await obtener_mascotas_db(session)

    mascotas = [m for m in mascotas if not m.eliminado]

    return templates.TemplateResponse("mascotas.html", {
        "request": request,
        "sesiones": mascotas,
        "titulo": "Mascotas registradas",
    })


@router.get("/mascotas/add", response_class=HTMLResponse, tags=["Mascotas"])
async def show_mascota_form(request: Request):
    return templates.TemplateResponse("add_mascota.html", {"request": request, "titulo": "Creación mascota"})

@router.post("/mascotas/add", status_code=status.HTTP_303_SEE_OTHER, tags=["Mascotas"])
async def submit_mascota_form(
    mascota_form: MascotaCreateForm = Depends(),
    session: AsyncSession = Depends(get_session)
    ):
        mascota_create = MascotaCreate(
        nombre=mascota_form.nombre,
        raza=mascota_form.raza,
        edad=mascota_form.edad,
        usuario_id=mascota_form.usuario_id,
    )
        await crear_mascota_db(mascota_create, session)
        return RedirectResponse(url="/mascotas_registro", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/usuarios/edit/{usuario_id}", response_class=HTMLResponse, tags=["Usuarios"])
async def edit_usuario_form(request: Request, usuario_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario or usuario.eliminado:
        return RedirectResponse(url="/usuarios_registro", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("edit_usuario.html", {"request": request, "usuario": usuario, "titulo": "Editar Usuario"})

@router.post("/usuarios/edit/{usuario_id}", status_code=status.HTTP_303_SEE_OTHER, tags=["Usuarios"])
async def submit_edit_usuario_form(
    usuario_id: int,
    usuario_form: UsuarioCreateForm = Depends(),
    session: AsyncSession = Depends(get_session)
    ):
    usuario_update = UsuarioCreate(
    nombre=usuario_form.nombre,
    cedula=usuario_form.cedula,
    )
    await actualizar_usuario_db(usuario_id, usuario_update, session)
    return RedirectResponse(url="/usuarios_registro", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/usuarios/delete/{usuario_id}", status_code=status.HTTP_303_SEE_OTHER, tags=["Usuarios"])
async def delete_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    await eliminar_usuario_db(usuario_id, session)
    return RedirectResponse(url="/usuarios_registro", status_code=status.HTTP_303_SEE_OTHER)