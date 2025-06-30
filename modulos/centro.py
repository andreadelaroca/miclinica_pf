#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo Centro Médico
Clase para gestionar centros médicos
"""

from datetime import datetime
from typing import List


class CentroMedico:
    """Clase que representa un centro médico"""
    
    def __init__(self, id_centro: int = 0, nombre: str = "", 
                 direccion: str = "", telefono: str = "", 
                 activo: bool = True, fecha_creacion: str = ""):
        self.id_centro = id_centro
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.activo = activo
        self.fecha_creacion = fecha_creacion if fecha_creacion else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"{self.nombre} - {self.direccion}"
    
    def to_list(self) -> List[str]:
        """Convierte el centro a lista para guardar en archivo DAT"""
        return [
            self.nombre,
            self.direccion,
            self.telefono,
            str(self.activo),
            self.fecha_creacion
        ]
    
    @classmethod
    def from_list(cls, datos: List[str]):
        """Crea un centro desde una lista de datos del archivo DAT"""
        if len(datos) >= 6:  # ID + 5 campos
            return cls(
                id_centro=int(datos[0]),
                nombre=datos[1],
                direccion=datos[2],
                telefono=datos[3],
                activo=datos[4].lower() == 'true',
                fecha_creacion=datos[5]
            )
        return None

