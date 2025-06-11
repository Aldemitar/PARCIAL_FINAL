from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from pydantic import validator
from datetime import date
from sqlalchemy import Column, Boolean

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cedula: str
    eliminado: bool = Field(default=False)
    vuelo_id: Optional[int] = Field(default=None, foreign_key="vuelo.id")
    mascota_id: Optional[int] = Field(default=None, foreign_key="mascota.id")
    vuelo: Optional["Vuelo"] = Relationship(back_populates="usuarios")
    mascota: Optional["Mascota"] = Relationship(back_populates="usuario")

class Mascota(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    edad: int
    eliminado: bool = Field(default=False)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    usuario: Optional[Usuario] = Relationship(back_populates="mascotas")

class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ciudad_origen: str
    ciudad_destino: str
    precio: float
    disponible: bool
    fecha: date
    usuarios: List[Usuario] = Relationship(back_populates="vuelo")

Usuario.mascota = Relationship(back_populates="usuario")
Mascota.usuario = Relationship(back_populates="mascotas")
Usuario.vuelo = Relationship(back_populates="usuarios")
Vuelo.usuarios = Relationship(back_populates="vuelo")