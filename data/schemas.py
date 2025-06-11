from fastapi import Form
from pydantic import BaseModel
from typing import Optional
from datetime import date


class UsuarioBase(BaseModel):
    nombre: str
    cedula: str
    vuelo_id: Optional[int] = None
    mascota_id: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioCreateForm:
    def __init__(
        self,
        nombre: str = Form(...),
        cedula: str = Form(...),
    ):
        self.nombre = nombre
        self.cedula = cedula
