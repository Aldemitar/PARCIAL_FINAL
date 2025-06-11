from fastapi import HTTPException, status

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Usuario, Mascota, Vuelo

from typing import List, Optional


async def obtener_usuarios_db(session: AsyncSession) -> List[Usuario]:
    result = await session.execute(select(Usuario).order_by(Usuario.id))
    return result.scalars().all()
