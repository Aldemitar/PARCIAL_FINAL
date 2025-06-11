from sqlmodel import SQLModel, Field
from typing import Optional, List
from datetime import date

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    cedula: str
    eliminado: bool = Field(default=False)

class Mascota(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    raza: str
    edad: int
    eliminado: bool = Field(default=False)

class Vuelo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ciudad_origen: str
    ciudad_destino: str
    precio: float
    disponible: bool
    fecha: date