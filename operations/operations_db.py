from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Usuario, Mascota, Vuelo

from typing import List, Optional


async def obtener_usuarios_db(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario).order_by(Usuario.id))
    return result.scalars().all()

async def crear_usuario_db(usuario_create, session: AsyncSession):
    usuario = Usuario(**usuario_create.dict())
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario) 
    return usuario

async def eliminar_usuario_db(usuario_id: int, session: AsyncSession):
    result = await session.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.eliminado = True
    session.add(usuario)
    await session.commit()
    return usuario

async def actualizar_usuario_db(usuario_id: int, usuario_update, session: AsyncSession):
    result = await session.execute(select(Usuario).where(Usuario.id == usuario_id))
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = usuario_update.nombre
    usuario.cedula = usuario_update.cedula
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def obtener_mascotas_db(session: AsyncSession) -> List[Mascota]:
    result = await session.execute(select(Mascota).order_by(Mascota.id))
    return result.scalars().all()

async def crear_mascota_db(mascota_create, session: AsyncSession):
    mascota = Mascota(**mascota_create.dict())
    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    return mascota

