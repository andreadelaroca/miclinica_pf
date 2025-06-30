#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo de Autenticación y Estadísticas
Centraliza autenticación y funciones auxiliares del sistema
"""


def iniciar_sesion(usuario_dao):
    """Permite iniciar sesión a un usuario"""
    print("\n--- INICIAR SESIÓN ---")
    email = input("Email: ")
    password = input("Contraseña: ")
    
    # Buscar usuario por email
    usuarios = usuario_dao.obtener_todos_usuarios()
    usuario_encontrado = None
    
    for usuario in usuarios:
        if usuario.email == email and usuario.password == password:
            usuario_encontrado = usuario
            break
    
    if not usuario_encontrado:
        print("Credenciales incorrectas.")
        return None
    
    print(f"¡Bienvenido {usuario_encontrado.nombre} {usuario_encontrado.apellido}!")
    return usuario_encontrado


def mostrar_estadisticas(file_manager, usuario_dao, expediente_dao, usuario_logueado):
    """Muestra estadísticas del centro del usuario logueado"""
    print("\n" + "="*40)
    print(f"    ESTADÍSTICAS DEL CENTRO {usuario_logueado.id_centro}")
    print("="*40)
    
    # Estadísticas específicas del centro
    usuarios_centro = usuario_dao.obtener_usuarios_por_centro(usuario_logueado.id_centro)
    medicos_centro = [u for u in usuarios_centro if u.es_medico()]
    pacientes_centro = [u for u in usuarios_centro if u.es_paciente()]
    administradores_centro = [u for u in usuarios_centro if u.es_administrador()]
    
    # Contar expedientes del centro
    expedientes_centro = 0
    todos_expedientes = expediente_dao.obtener_todos_expedientes()
    for expediente in todos_expedientes:
        if expediente.id_centro == usuario_logueado.id_centro:
            expedientes_centro += 1
    
    print(f"Total de Usuarios: {len(usuarios_centro)}")
    print(f"  - Médicos: {len(medicos_centro)}")
    print(f"  - Pacientes: {len(pacientes_centro)}")
    print(f"  - Administradores: {len(administradores_centro)}")
    print(f"Total de Expedientes: {expedientes_centro}")
    print("="*40)

