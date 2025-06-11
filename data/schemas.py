from fastapi import Form
from pydantic import BaseModel
from typing import Optional
from datetime import date

class UsuarioBase(BaseModel):
    nombre: str
    cedula: str
    eliminado: bool = False
    vuelo_id: Optional[int] = None
    mascota_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioCreateForm:
    def init(
        self,
        nombre: str = Form(...),
        cedula: str = Form(...),
    ):
        self.nombre = nombre
        self.cedula = cedula

class MascotaBase(BaseModel):
    nombre: str
    raza: str
    edad: int
    eliminado: bool = False
    usuario_id: Optional[int] = None

class MascotaCreate(MascotaBase):
    pass

class MascotaCreateForm:
    def init(
        self,
        nombre: str = Form(...),
        raza: str = Form(...),
        edad: int = Form(...),
        usuario_id: Optional[int] = Form(None),
    ):
        self.nombre = nombre
        self.raza = raza
        self.edad = edad
        self.usuario_id = usuario_id