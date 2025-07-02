#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo de Gestión de Centros Médicos
Centraliza todas las operaciones CRUD de centros médicos
"""

from modulos.centro import CentroMedico


def registrar_centro(centro_dao):
    """Registra un nuevo centro médico"""
    print("\n--- REGISTRAR CENTRO MÉDICO ---")
    nombre = input("Nombre del centro: ")
    direccion = input("Dirección: ")
    
    # Validación del teléfono
    while True:
        telefono = input("Teléfono (8 dígitos): ")
        if telefono.isdigit() and len(telefono) == 8:
            break
        else:
            print("Error: El teléfono debe tener exactamente 8 dígitos numéricos.")
    
    centro = CentroMedico(nombre=nombre, direccion=direccion, telefono=telefono)
    
    try:
        id_centro = centro_dao.crear_centro(centro)
        print(f"Centro médico registrado exitosamente con ID: {id_centro}")
    except Exception as e:
        print(f"Error al registrar centro: {e}")


def listar_centros(centro_dao):
    """Lista todos los centros médicos"""
    centros = centro_dao.obtener_todos_centros()
    
    if not centros:
        print("No hay centros registrados.")
        return
    
    print("\n--- LISTA DE CENTROS MÉDICOS ---")
    for centro in centros:
        print(f"ID: {centro.id_centro} | {centro.nombre} | {centro.direccion} | {centro.telefono}")


def buscar_centro(centro_dao):
    """Busca centros por término"""
    termino = input("Nombre del centro a buscar: ")
    centros = centro_dao.buscar_centros(termino)
    if centros:
        print("\n--- RESULTADOS DE BÚSQUEDA ---")
        for centro in centros:
            print(f"ID: {centro.id_centro} | {centro.nombre} | {centro.direccion} | {centro.telefono}")
    else:
        print("No se encontraron centros.")


def editar_centro(centro_dao, usuario_logueado=None):
    """Edita un centro médico existente (solo su propio centro si es administrador)"""
    print("\n--- EDITAR CENTRO MÉDICO ---")
    
    if usuario_logueado and usuario_logueado.es_administrador():
        # Los administradores solo pueden editar su propio centro
        centro = centro_dao.obtener_centro_por_id(usuario_logueado.id_centro)
        if not centro:
            print("No se encontró su centro médico.")
            return
        
        print(f"\nEditando SU centro: {centro.nombre}")
        print("(Presione Enter para mantener el valor actual)")
        
        nuevo_nombre = input(f"Nombre [{centro.nombre}]: ").strip()
        if nuevo_nombre:
            centro.nombre = nuevo_nombre
        
        nueva_direccion = input(f"Dirección [{centro.direccion}]: ").strip()
        if nueva_direccion:
            centro.direccion = nueva_direccion
        
        nuevo_telefono = input(f"Teléfono [{centro.telefono}]: ").strip()
        if nuevo_telefono:
            centro.telefono = nuevo_telefono
        
        if centro_dao.actualizar_centro(centro):
            print("Centro actualizado exitosamente.")
        else:
            print("Error al actualizar centro.")
        
    else:
        # Para usuarios no administradores (funcionalidad original)
        centros = centro_dao.obtener_todos_centros()
        if not centros:
            print("No hay centros registrados.")
            return
        
        print("\nCentros disponibles:")
        for centro in centros:
            print(f"ID: {centro.id_centro} | {centro.nombre} | {centro.direccion}")
        
        try:
            id_centro = int(input("\nID del centro a editar: "))
            centro = centro_dao.obtener_centro_por_id(id_centro)
            
            if not centro:
                print("Centro no encontrado.")
                return
            
            print(f"\nEditando centro: {centro.nombre}")
            print("(Presione Enter para mantener el valor actual)")
            
            nuevo_nombre = input(f"Nombre [{centro.nombre}]: ").strip()
            if nuevo_nombre:
                centro.nombre = nuevo_nombre
            
            nueva_direccion = input(f"Dirección [{centro.direccion}]: ").strip()
            if nueva_direccion:
                centro.direccion = nueva_direccion
            
            nuevo_telefono = input(f"Teléfono [{centro.telefono}]: ").strip()
            if nuevo_telefono:
                centro.telefono = nuevo_telefono
            
            if centro_dao.actualizar_centro(centro):
                print("Centro actualizado exitosamente.")
            else:
                print("Error al actualizar centro.")
        
        except ValueError:
            print("ID inválido.")
        except Exception as e:
            print(f"Error: {e}")


def eliminar_centro(centro_dao):
    """Elimina (desactiva) un centro médico"""
    print("\n--- ELIMINAR CENTRO MÉDICO ---")
    
    # Mostrar centros disponibles
    centros = centro_dao.obtener_todos_centros()
    if not centros:
        print("No hay centros registrados.")
        return
    
    print("\nCentros disponibles:")
    for centro in centros:
        print(f"ID: {centro.id_centro} | {centro.nombre} | {centro.direccion}")
    
    try:
        id_centro = int(input("\nID del centro a eliminar: "))
        centro = centro_dao.obtener_centro_por_id(id_centro)
        
        if not centro:
            print("Centro no encontrado.")
            return
        
        confirmacion = input(f"¿Está seguro de eliminar {centro.nombre}? (s/N): ")
        if confirmacion.lower() == 's':
            if centro_dao.eliminar_centro(id_centro):
                print("Centro eliminado exitosamente.")
            else:
                print("Error al eliminar centro.")
        else:
            print("Operación cancelada.")
    
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Error: {e}")

