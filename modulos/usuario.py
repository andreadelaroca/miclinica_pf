#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo Usuario
Clase para gestionar usuarios (médicos y pacientes)
"""

from datetime import datetime
from typing import List, Optional


class Usuario:
    """Clase que representa un usuario del sistema"""
    
    def __init__(self, id_usuario: int = 0, nombre: str = "", 
                 apellido: str = "", email: str = "", 
                 tipo_usuario: str = "", activo: bool = True,
                 fecha_registro: str = ""):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.tipo_usuario = tipo_usuario  # 'medico' o 'paciente'
        self.activo = activo
        self.fecha_registro = fecha_registro if fecha_registro else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"
    
    def to_list(self) -> List[str]:
        """Convierte el usuario a lista para guardar en archivo DAT"""
        return [
            self.nombre,
            self.apellido,
            self.email,
            self.tipo_usuario,
            str(self.activo),
            self.fecha_registro
        ]
    
    @classmethod
    def from_list(cls, datos: List[str]):
        """Crea un usuario desde una lista de datos del archivo DAT"""
        if len(datos) >= 7:  # ID + 6 campos
            return cls(
                id_usuario=int(datos[0]),
                nombre=datos[1],
                apellido=datos[2],
                email=datos[3],
                tipo_usuario=datos[4],
                activo=datos[5].lower() == 'true',
                fecha_registro=datos[6]
            )
        return None
    
    def es_medico(self) -> bool:
        """Verifica si el usuario es médico"""
        return self.tipo_usuario == 'medico'
    
    def es_paciente(self) -> bool:
        """Verifica si el usuario es paciente"""
        return self.tipo_usuario == 'paciente'

