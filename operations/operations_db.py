from sqlmodel import select
from data.models import Usuario, Mascota, Vuelo
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

async def obtener_usuarios(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario).where(Usuario.eliminado == False))
    return result.scalars().all()

async def obtener_usuario_por_id(session: AsyncSession, usuario_id: int) -> Optional[Usuario]:
    return await session.get(Usuario, usuario_id)

async def crear_usuario(session: AsyncSession, usuario: Usuario) -> Usuario:
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def actualizar_usuario(session: AsyncSession, usuario_id: int, usuario_data: Usuario) -> Optional[Usuario]:
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        return None
    usuario.nombre = usuario_data.nombre
    usuario.cedula = usuario_data.cedula
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

async def eliminar_usuario(session: AsyncSession, usuario_id: int) -> bool:
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        return False
    usuario.eliminado = True
    session.add(usuario)
    await session.commit()
    return True

async def obtener_mascotas(session: AsyncSession) -> List[Mascota]:
    result = await session.execute(select(Mascota).where(Mascota.eliminado == False))
    return result.scalars().all()

async def obtener_mascota_por_id(session: AsyncSession, mascota_id: int) -> Optional[Mascota]:
    return await session.get(Mascota, mascota_id)

async def crear_mascota(session: AsyncSession, mascota: Mascota) -> Mascota:
    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    return mascota

async def actualizar_mascota(session: AsyncSession, mascota_id: int, mascota_data: Mascota) -> Optional[Mascota]:
    mascota = await session.get(Mascota, mascota_id)
    if not mascota:
        return None
    mascota.nombre = mascota_data.nombre
    mascota.raza = mascota_data.raza
    mascota.edad = mascota_data.edad
    session.add(mascota)
    await session.commit()
    await session.refresh(mascota)
    return mascota

async def eliminar_mascota(session: AsyncSession, mascota_id: int) -> bool:
    mascota = await session.get(Mascota, mascota_id)
    if not mascota:
        return False
    mascota.eliminado = True
    session.add(mascota)
    await session.commit()
    return True

async def obtener_vuelos(session: AsyncSession) -> List[Vuelo]:
    result = await session.execute(select(Vuelo))
    return result.scalars().all()

async def obtener_vuelo_por_id(session: AsyncSession, vuelo_id: int) -> Optional[Vuelo]:
    return await session.get(Vuelo, vuelo_id)

async def crear_vuelo(session: AsyncSession, vuelo: Vuelo) -> Vuelo:
    session.add(vuelo)
    await session.commit()
    await session.refresh(vuelo)
    return vuelo

async def actualizar_vuelo(session: AsyncSession, vuelo_id: int, vuelo_data: Vuelo) -> Optional[Vuelo]:
    vuelo = await session.get(Vuelo, vuelo_id)
    if not vuelo:
        return None
    vuelo.ciudad_origen = vuelo_data.ciudad_origen
    vuelo.ciudad_destino = vuelo_data.ciudad_destino
    vuelo.precio = vuelo_data.precio
    vuelo.disponible = vuelo_data.disponible
    vuelo.fecha = vuelo_data.fecha
    session.add(vuelo)
    await session.commit()
    await session.refresh(vuelo)
    return vuelo

async def eliminar_vuelo(session: AsyncSession, vuelo_id: int) -> bool:
    vuelo = await session.get(Vuelo, vuelo_id)
    if not vuelo:
        return False
    await session.delete(vuelo)
    await session.commit()
    return True