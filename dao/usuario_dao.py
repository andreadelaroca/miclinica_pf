#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - DAO Usuario
Data Access Object para usuarios usando archivos DAT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Optional
from modulos.usuario import Usuario
from modulos.utils import FileManager


class UsuarioDAO:
    """DAO para manejo de usuarios en archivos DAT"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.archivo = "usuarios"
    
    def crear_usuario(self, usuario: Usuario) -> int:
        """Crea un nuevo usuario"""
        return self.file_manager.insertar_registro(self.archivo, usuario.to_list())
    
    def obtener_usuario_por_id(self, id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        registro = self.file_manager.obtener_registro_por_id(self.archivo, id_usuario)
        if registro:
            return Usuario.from_list(registro)
        return None
    
    def obtener_todos_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        registros = self.file_manager.obtener_registros(self.archivo)
        usuarios = []
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo:
                usuarios.append(usuario)
        return usuarios
    
    def obtener_medicos(self) -> List[Usuario]:
        """Obtiene todos los médicos activos"""
        registros = self.file_manager.buscar_registros(self.archivo, 4, "medico")
        medicos = []
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo:
                medicos.append(usuario)
        return medicos
    
    def obtener_pacientes(self) -> List[Usuario]:
        """Obtiene todos los pacientes activos"""
        registros = self.file_manager.buscar_registros(self.archivo, 4, "paciente")
        pacientes = []
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo:
                pacientes.append(usuario)
        return pacientes
    
    def actualizar_usuario(self, usuario: Usuario) -> bool:
        """Actualiza un usuario existente"""
        return self.file_manager.actualizar_registro(self.archivo, usuario.id_usuario, usuario.to_list())
    
    def eliminar_usuario(self, id_usuario: int) -> bool:
        """Elimina (desactiva) un usuario"""
        usuario = self.obtener_usuario_por_id(id_usuario)
        if usuario:
            usuario.activo = False
            return self.actualizar_usuario(usuario)
        return False
    
    def buscar_usuarios(self, termino: str) -> List[Usuario]:
        """Busca usuarios por nombre, apellido o email"""
        usuarios_encontrados = []
        
        # Buscar por nombre
        registros = self.file_manager.buscar_registros(self.archivo, 1, termino)
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo:
                usuarios_encontrados.append(usuario)
        
        # Buscar por apellido
        registros = self.file_manager.buscar_registros(self.archivo, 2, termino)
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo and usuario not in usuarios_encontrados:
                usuarios_encontrados.append(usuario)
        
        # Buscar por email
        registros = self.file_manager.buscar_registros(self.archivo, 3, termino)
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo and usuario not in usuarios_encontrados:
                usuarios_encontrados.append(usuario)
        
        return usuarios_encontrados

