from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import relationship

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cedula: str
    eliminado: bool = Field(default=False)
    vuelo_id: Optional[int] = Field(default=None, foreign_key="vuelo.id")
    mascota_id: Optional[int] = Field(default=None, foreign_key="mascota.id")

    vuelo: Optional["Vuelo"] = Relationship(
        back_populates="usuarios",
        sa_relationship=relationship("Vuelo", back_populates="usuarios", foreign_keys=[vuelo_id])
    )
    mascota: Optional["Mascota"] = Relationship(
        back_populates="usuario",
        sa_relationship=relationship("Mascota", back_populates="usuario", foreign_keys=[mascota_id])
    )

class Mascota(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    edad: int
    eliminado: bool = Field(default=False)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(
        back_populates="mascotas",
        sa_relationship=relationship("Usuario", back_populates="mascotas", foreign_keys=[usuario_id])
    )

class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ciudad_origen: str
    ciudad_destino: str
    precio: float
    disponible: bool
    fecha: date
    usuarios: List[Usuario] = Relationship(
        back_populates="vuelo",
        sa_relationship=relationship("Usuario", back_populates="vuelo", foreign_keys=[Usuario.vuelo_id])
    )

Usuario.mascota = Relationship(back_populates="usuario")
Usuario.vuelo = Relationship(back_populates="usuarios")
Mascota.usuario = Relationship(back_populates="mascotas")
Vuelo.usuarios = Relationship(back_populates="vuelo")