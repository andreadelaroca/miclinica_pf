#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo de Gestión de Usuarios
Centraliza todas las operaciones CRUD de usuarios
"""

from modulos.usuario import Usuario


def registrar_usuario(usuario_dao, centro_dao):
    """Registra un nuevo usuario"""
    print("\n--- REGISTRAR USUARIO ---")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    email = input("Email: ")
    password = input("Contraseña: ")
    
    print("Tipo de usuario:")
    print("1. Médico")
    print("2. Paciente")
    print("3. Administrador")
    tipo_opcion = input("Seleccione (1-3): ")
    
    if tipo_opcion not in ["1", "2", "3"]:
        print("Opción no válida. Intente de nuevo.")
        return
    
    tipo_usuario = "medico" if tipo_opcion == "1" else "paciente" if tipo_opcion == "2" else "administrador"
    
    # Mostrar centros disponibles
    centros = centro_dao.obtener_todos_centros()
    if not centros:
        print("No hay centros disponibles. Registra un centro primero.")
        return
    
    print("\nCentros disponibles:")
    for centro in centros:
        print(f"ID: {centro.id_centro} | {centro.nombre}")
    
    try:
        id_centro = int(input("\nSeleccione ID del centro: "))
        if not any(centro.id_centro == id_centro for centro in centros):
            print("Centro no válido.")
            return
    except ValueError:
        print("ID del centro inválido.")
        return
    
    usuario = Usuario(nombre=nombre, apellido=apellido, email=email, tipo_usuario=tipo_usuario,
                      password=password, id_centro=id_centro)
    
    try:
        id_usuario = usuario_dao.crear_usuario(usuario)
        print(f"Usuario registrado exitosamente con ID: {id_usuario}")
    except Exception as e:
        print(f"Error al registrar usuario: {e}")


def listar_usuarios(usuario_dao, usuario_logueado=None):
    """Lista usuarios (todos o del centro del administrador)"""
    if usuario_logueado and usuario_logueado.es_administrador():
        usuarios = usuario_dao.obtener_usuarios_por_centro(usuario_logueado.id_centro)
        titulo = f"USUARIOS DEL CENTRO {usuario_logueado.id_centro}"
    else:
        usuarios = usuario_dao.obtener_todos_usuarios()
        titulo = "LISTA DE USUARIOS"
    
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print(f"\n--- {titulo} ---")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
    print()
    print("-" * 64)


def editar_usuario(usuario_dao, usuario_logueado=None):
    """Edita un usuario existente (del mismo centro si es administrador)"""
    print("\n--- EDITAR USUARIO ---")
    
    # Obtener usuarios según el tipo de usuario logueado
    if usuario_logueado and usuario_logueado.es_administrador():
        usuarios = usuario_dao.obtener_usuarios_por_centro(usuario_logueado.id_centro)
        titulo = f"USUARIOS DEL CENTRO {usuario_logueado.id_centro}"
    else:
        usuarios = usuario_dao.obtener_todos_usuarios()
        titulo = "USUARIOS DISPONIBLES"
    
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print(f"\n{titulo}:")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.tipo_usuario}")
    
    try:
        id_usuario = int(input("\nID del usuario a editar: "))
        usuario = usuario_dao.obtener_usuario_por_id(id_usuario)
        
        if not usuario or id_usuario == 0:
            print("Usuario no encontrado.")
            return
        
        # Verificar si el usuario pertenece al centro del administrador
        if usuario_logueado and usuario_logueado.es_administrador():
            if usuario.id_centro != usuario_logueado.id_centro:
                print("No puede editar usuarios de otros centros.")
                return
        
        print(f"\nEditando usuario: {usuario.nombre} {usuario.apellido}")
        print("(Presione Enter para mantener el valor actual)")
        
        nuevo_nombre = input(f"Nombre [{usuario.nombre}]: ").strip()
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        
        nuevo_apellido = input(f"Apellido [{usuario.apellido}]: ").strip()
        if nuevo_apellido:
            usuario.apellido = nuevo_apellido
        
        nuevo_email = input(f"Email [{usuario.email}]: ").strip()
        if nuevo_email:
            usuario.email = nuevo_email
        
        if usuario_dao.actualizar_usuario(usuario):
            print("Usuario actualizado exitosamente.")
        else:
            print("Error al actualizar usuario.")
    
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Error: {e}")


def eliminar_usuario(usuario_dao, usuario_logueado=None):
    """Elimina (desactiva) un usuario (del mismo centro si es administrador)"""
    print("\n--- ELIMINAR USUARIO ---")
    
    # Obtener usuarios según el tipo de usuario logueado
    if usuario_logueado and usuario_logueado.es_administrador():
        usuarios = usuario_dao.obtener_usuarios_por_centro(usuario_logueado.id_centro)
        titulo = f"USUARIOS DEL CENTRO {usuario_logueado.id_centro}"
    else:
        usuarios = usuario_dao.obtener_todos_usuarios()
        titulo = "USUARIOS DISPONIBLES"
    
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print(f"\n{titulo}:")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.tipo_usuario}")
    
    try:
        id_usuario = int(input("\nID del usuario a eliminar: "))
        usuario = usuario_dao.obtener_usuario_por_id(id_usuario)
        
        if not usuario:
            print("Usuario no encontrado.")
            return
        
        # Verificar si el usuario pertenece al centro del administrador
        if usuario_logueado and usuario_logueado.es_administrador():
            if usuario.id_centro != usuario_logueado.id_centro:
                print("No puede eliminar usuarios de otros centros.")
                return
        
        confirmacion = input(f"¿Está seguro de eliminar a {usuario.nombre} {usuario.apellido}? (s/N): ")
        if confirmacion.lower() == 's':
            if usuario_dao.eliminar_usuario(id_usuario):
                print("Usuario eliminado exitosamente.")
            else:
                print("Error al eliminar usuario.")
        else:
            print("Operación cancelada.")
    
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Error: {e}")


def buscar_usuario(usuario_dao, usuario_logueado=None):
    """Busca usuarios por término"""
    termino = input("Ingrese la ID del usuario: ")
    try:
        usuario = usuario_dao.obtener_usuario_por_id(int(termino))
    except TypeError:
        print("ERROR: La ID introducida no es válida")
        return
    
    # Filtrar solo usuarios del mismo centro si es administrador
    if usuario_logueado and usuario_logueado.es_administrador():
        if usuario.id_centro == usuario_logueado.id_centro:
            print(f"\n--- RESULTADOS DE BÚSQUEDA (CENTRO {usuario_logueado.id_centro}) ---")
            print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
        else:
            print("No se encontraron usuarios en su centro.")
    else:
        if usuario:
            print("\n--- RESULTADOS DE BÚSQUEDA ---")
            
            print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
        else:
            print("No se encontraron usuarios.")


def listar_medicos(usuario_dao, usuario_logueado=None):
    """Lista médicos (todos o del centro del administrador)"""
    if usuario_logueado and usuario_logueado.es_administrador():
        medicos = usuario_dao.obtener_medicos_por_centro(usuario_logueado.id_centro)
        titulo = f"MÉDICOS DEL CENTRO {usuario_logueado.id_centro}"
    else:
        medicos = usuario_dao.obtener_medicos()
        titulo = "LISTA DE MÉDICOS"
    
    if not medicos:
        print("No hay médicos registrados.")
        return
    
    print(f"\n--- {titulo} ---")
    for medico in medicos:
        print(f"ID: {medico.id_usuario} | {medico.nombre} {medico.apellido} | {medico.email}")


def listar_pacientes(usuario_dao, usuario_logueado=None):
    """Lista pacientes (todos o del centro del administrador)"""
    if usuario_logueado and usuario_logueado.es_administrador():
        pacientes = usuario_dao.obtener_pacientes_por_centro(usuario_logueado.id_centro)
        titulo = f"PACIENTES DEL CENTRO {usuario_logueado.id_centro}"
    else:
        pacientes = usuario_dao.obtener_pacientes()
        titulo = "LISTA DE PACIENTES"
    
    if not pacientes:
        print("No hay pacientes registrados.")
        return
    
    print(f"\n--- {titulo} ---")
    for paciente in pacientes:
        print(f"ID: {paciente.id_usuario} | {paciente.nombre} {paciente.apellido} | {paciente.email}")

