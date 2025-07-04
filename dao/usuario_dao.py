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
    
    def obtener_usuarios_por_centro(self, id_centro: int) -> List[Usuario]:
        """Obtiene todos los usuarios activos de un centro específico"""
        registros = self.file_manager.buscar_registros(self.archivo, 6, str(id_centro))
        usuarios = []
        for registro in registros:
            usuario = Usuario.from_list(registro)
            if usuario and usuario.activo:
                usuarios.append(usuario)
        return usuarios
    
    def obtener_medicos_por_centro(self, id_centro: int) -> List[Usuario]:
        """Obtiene todos los médicos activos de un centro específico"""
        usuarios = self.obtener_usuarios_por_centro(id_centro)
        return [usuario for usuario in usuarios if usuario.es_medico()]
    
    def obtener_pacientes_por_centro(self, id_centro: int) -> List[Usuario]:
        """Obtiene todos los pacientes activos de un centro específico"""
        usuarios = self.obtener_usuarios_por_centro(id_centro)
        return [usuario for usuario in usuarios if usuario.es_paciente()]
    
    def obtener_administradores_por_centro(self, id_centro: int) -> List[Usuario]:
        """Obtiene todos los administradores activos de un centro específico"""
        usuarios = self.obtener_usuarios_por_centro(id_centro)
        return [usuario for usuario in usuarios if usuario.es_administrador()]
    
    def iniciar_sesion(self, email: str, password: str) -> Optional[Usuario]:
        """Verifica las credenciales de un usuario y devuelve el usuario si son correctas"""
        usuarios = self.obtener_todos_usuarios()
        for usuario in usuarios:
            if usuario.email == email and usuario.password == password:
                return usuario
        return None
    
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
   