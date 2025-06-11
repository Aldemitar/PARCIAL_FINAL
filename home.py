from contextlib import asynccontextmanager
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Usuario, Mascota, Vuelo
from operations.operations_db import (
    obtener_usuarios, crear_usuario, actualizar_usuario, eliminar_usuario,
    obtener_mascotas, crear_mascota, actualizar_mascota, eliminar_mascota,
    obtener_vuelos, crear_vuelo, actualizar_vuelo, eliminar_vuelo
    )
from utils.connection_db import get_session, init_db

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@asynccontextmanager
async def lifespan(app: APIRouter):
    await init_db()
    yield

@router.get("/usuarios", response_class=HTMLResponse)
async def list_usuarios(request: Request, session: AsyncSession = Depends(get_session)):
    usuarios = await obtener_usuarios(session)
    return templates.TemplateResponse("usuarios_registro.html", {"request": request, "sesiones": usuarios, "titulo": "Usuarios"})

@router.get("/usuarios/add", response_class=HTMLResponse)
async def add_usuario_form(request: Request):
    return templates.TemplateResponse("add_usuario.html", {"request": request, "titulo": "Agregar Usuario"})

@router.post("/usuarios/add", status_code=status.HTTP_303_SEE_OTHER)
async def add_usuario(
    nombre: str = Form(...),
    cedula: str = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    usuario = Usuario(nombre=nombre, cedula=cedula)
    await crear_usuario(session, usuario)
    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/usuarios/edit/{usuario_id}", response_class=HTMLResponse)
async def edit_usuario_form(request: Request, usuario_id: int, session: AsyncSession = Depends(get_session)):
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("edit_usuario.html", {"request": request, "usuario": usuario, "titulo": "Editar Usuario"})

@router.post("/usuarios/edit/{usuario_id}", status_code=status.HTTP_303_SEE_OTHER)
async def edit_usuario(
    usuario_id: int,
    nombre: str = Form(...),
    cedula: str = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    usuario_data = Usuario(nombre=nombre, cedula=cedula)
    await actualizar_usuario(session, usuario_id, usuario_data)
    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/usuarios/delete/{usuario_id}", status_code=status.HTTP_303_SEE_OTHER)
async def delete_usuario(usuario_id: int, session: AsyncSession = Depends(get_session)):
    await eliminar_usuario(session, usuario_id)
    return RedirectResponse(url="/usuarios", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/mascotas", response_class=HTMLResponse)
async def list_mascotas(request: Request, session: AsyncSession = Depends(get_session)):
    mascotas = await obtener_mascotas(session)
    return templates.TemplateResponse("mascotas.html", {"request": request, "sesiones": mascotas, "titulo": "Mascotas"})

@router.get("/mascotas/add", response_class=HTMLResponse)
async def add_mascota_form(request: Request):
    return templates.TemplateResponse("add_mascota.html", {"request": request, "titulo": "Agregar Mascota"})

@router.post("/mascotas/add", status_code=status.HTTP_303_SEE_OTHER)
async def add_mascota(
    nombre: str = Form(...),
    raza: str = Form(...),
    edad: int = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    mascota = Mascota(nombre=nombre, raza=raza, edad=edad)
    await crear_mascota(session, mascota)
    return RedirectResponse(url="/mascotas", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/mascotas/edit/{mascota_id}", response_class=HTMLResponse)
async def edit_mascota_form(request: Request, mascota_id: int, session: AsyncSession = Depends(get_session)):
    mascota = await session.get(Mascota, mascota_id)
    if not mascota:
        return RedirectResponse(url="/mascotas", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("edit_mascota.html", {"request": request, "mascota": mascota, "titulo": "Editar Mascota"})

@router.post("/mascotas/edit/{mascota_id}", status_code=status.HTTP_303_SEE_OTHER)
async def edit_mascota(
    mascota_id: int,
    nombre: str = Form(...),
    raza: str = Form(...),
    edad: int = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    mascota_data = Mascota(nombre=nombre, raza=raza, edad=edad)
    await actualizar_mascota(session, mascota_id, mascota_data)
    return RedirectResponse(url="/mascotas", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/mascotas/delete/{mascota_id}", status_code=status.HTTP_303_SEE_OTHER)
async def delete_mascota(mascota_id: int, session: AsyncSession = Depends(get_session)):
    await eliminar_mascota(session, mascota_id)
    return RedirectResponse(url="/mascotas", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/vuelos", response_class=HTMLResponse)
async def list_vuelos(request: Request, session: AsyncSession = Depends(get_session)):
    vuelos = await obtener_vuelos(session)
    return templates.TemplateResponse("vuelos.html", {"request": request, "sesiones": vuelos, "titulo": "Vuelos"})

@router.get("/vuelos/add", response_class=HTMLResponse)
async def add_vuelo_form(request: Request):
    return templates.TemplateResponse("add_vuelo.html", {"request": request, "titulo": "Agregar Vuelo"})

@router.post("/vuelos/add", status_code=status.HTTP_303_SEE_OTHER)
async def add_vuelo(
    ciudad_origen: str = Form(...),
    ciudad_destino: str = Form(...),
    precio: float = Form(...),
    disponible: bool = Form(...),
    fecha: str = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    from datetime import datetime
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    vuelo = Vuelo(
    ciudad_origen=ciudad_origen,
    ciudad_destino=ciudad_destino,
    precio=precio,
    disponible=disponible,
    fecha=fecha_dt
    )
    await crear_vuelo(session, vuelo)
    return RedirectResponse(url="/vuelos", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/vuelos/edit/{vuelo_id}", response_class=HTMLResponse)
async def edit_vuelo_form(request: Request, vuelo_id: int, session: AsyncSession = Depends(get_session)):
    vuelo = await session.get(Vuelo, vuelo_id)
    if not vuelo:
        return RedirectResponse(url="/vuelos", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("edit_vuelo.html", {"request": request, "vuelo": vuelo, "titulo": "Editar Vuelo"})

@router.post("/vuelos/edit/{vuelo_id}", status_code=status.HTTP_303_SEE_OTHER)
async def edit_vuelo(
    vuelo_id: int,
    ciudad_origen: str = Form(...),
    ciudad_destino: str = Form(...),
    precio: float = Form(...),
    disponible: bool = Form(...),
    fecha: str = Form(...),
    session: AsyncSession = Depends(get_session)
    ):
    from datetime import datetime
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d").date()
    vuelo_data = Vuelo(
    ciudad_origen=ciudad_origen,
    ciudad_destino=ciudad_destino,
    precio=precio,
    disponible=disponible,
    fecha=fecha_dt
    )
    await actualizar_vuelo(session, vuelo_id, vuelo_data)
    return RedirectResponse(url="/vuelos", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/vuelos/delete/{vuelo_id}", status_code=status.HTTP_303_SEE_OTHER)
async def delete_vuelo(vuelo_id: int, session: AsyncSession = Depends(get_session)):
    await eliminar_vuelo(session, vuelo_id)
    return RedirectResponse(url="/vuelos", status_code=status.HTTP_303_SEE_OTHER)