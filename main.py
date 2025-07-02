#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Sistema de Gestión de Clínica Médica (REFACTORIZADO)
Archivo principal del sistema usando archivos DAT con funciones organizadas en módulos
"""

import sys
import os

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulos'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'dao'))

# Importar clases de datos
from modulos.usuario import Usuario
from modulos.centro import CentroMedico
from modulos.expediente import Expediente
from modulos.utils import FileManager, obtener_fecha_actual

# Importar DAOs
from dao.usuario_dao import UsuarioDAO
from dao.centro_dao import CentroDAO
from dao.expediente_dao import ExpedienteDAO

# Importar módulos de gestión
from modulos.menu_manager import (
    mostrar_menu_principal, mostrar_menu_usuarios, mostrar_menu_centros,
    mostrar_menu_administrador, mostrar_menu_medico, mostrar_menu_paciente,
    limpiar_pantalla
)
from modulos.usuario_manager import (
    registrar_usuario, listar_usuarios, editar_usuario, eliminar_usuario,
    buscar_usuario, listar_medicos, listar_pacientes
)
from modulos.centro_manager import (
    registrar_centro, listar_centros, buscar_centro, editar_centro, eliminar_centro
)
from modulos.expediente_manager import (
    crear_expediente, editar_expediente, listar_expedientes, buscar_expediente,
    ver_expedientes_por_paciente, ver_expedientes_por_medico, ver_mis_expedientes
)
from modulos.auth_manager import iniciar_sesion, mostrar_estadisticas


def manejar_modulo_centros(centro_dao):
    """Maneja el módulo de centros médicos"""
    while True:
        limpiar_pantalla()
        mostrar_menu_centros()
        sub_opcion = input("\nSeleccione una opción: ").strip()
        
        if sub_opcion == "0":
            break
        elif sub_opcion == "1":
            registrar_centro(centro_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "2":
            listar_centros(centro_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "3":
            buscar_centro(centro_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "4":
            editar_centro(centro_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "5":
            eliminar_centro(centro_dao)
            input("Presione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def manejar_modulo_usuarios(usuario_dao, centro_dao):
    """Maneja el módulo de usuarios"""
    while True:
        limpiar_pantalla()
        mostrar_menu_usuarios()
        sub_opcion = input("\nSeleccione una opción: ").strip()
        
        if sub_opcion == "0":
            break
        elif sub_opcion == "1":
            registrar_usuario(usuario_dao, centro_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "2":
            listar_usuarios(usuario_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "3":
            buscar_usuario(usuario_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "4":
            editar_usuario(usuario_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "5":
            eliminar_usuario(usuario_dao)
            input("Presione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def manejar_sesion_administrador(usuario_dao, centro_dao, expediente_dao, file_manager, usuario_logueado):
    """Maneja la sesión de un administrador"""
    while True:
        limpiar_pantalla()
        mostrar_menu_administrador()
        sub_opcion = input("\nSeleccione una opción: ").strip()
        
        if sub_opcion == "0":
            print("Cerrando sesión...")
            break
        elif sub_opcion == "1":
            listar_usuarios(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "2":
            buscar_usuario(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "3":
            editar_usuario(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "4":
            eliminar_usuario(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "5":
            editar_centro(centro_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "6":
            print("Los administradores no pueden eliminar centros médicos.")
            input("Presione Enter para continuar...")
        elif sub_opcion == "7":
            ver_expedientes_por_medico(expediente_dao, usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "8":
            listar_medicos(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "9":
            listar_pacientes(usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "10":
            mostrar_estadisticas(file_manager, usuario_dao, expediente_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def manejar_sesion_medico(usuario_dao, expediente_dao, usuario_logueado):
    """Maneja la sesión de un médico"""
    while True:
        limpiar_pantalla()
        mostrar_menu_medico()
        sub_opcion = input("\nSeleccione una opción: ").strip()
        
        if sub_opcion == "0":
            print("Cerrando sesión...")
            break
        elif sub_opcion == "1":
            crear_expediente(expediente_dao, usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "2":
            editar_expediente(expediente_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        elif sub_opcion == "3":
            buscar_expediente(expediente_dao)
            input("Presione Enter para continuar...")
        elif sub_opcion == "4":
            ver_expedientes_por_paciente(expediente_dao, usuario_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def manejar_sesion_paciente(expediente_dao, usuario_logueado):
    """Maneja la sesión de un paciente"""
    while True:
        limpiar_pantalla()
        mostrar_menu_paciente()
        sub_opcion = input("\nSeleccione una opción: ").strip()
        
        if sub_opcion == "0":
            print("Cerrando sesión...")
            break
        elif sub_opcion == "1":
            ver_mis_expedientes(expediente_dao, usuario_logueado)
            input("Presione Enter para continuar...")
        else:
            print("Opción no válida.")
            input("Presione Enter para continuar...")


def manejar_inicio_sesion(usuario_dao, centro_dao, expediente_dao, file_manager):
    """Maneja el proceso de inicio de sesión y navegación posterior"""
    limpiar_pantalla()
    usuario_logueado = iniciar_sesion(usuario_dao)
    
    if not usuario_logueado:
        return
    
    # Redireccionar según el tipo de usuario
    if usuario_logueado.es_administrador():
        manejar_sesion_administrador(usuario_dao, centro_dao, expediente_dao, file_manager, usuario_logueado)
    elif usuario_logueado.es_medico():
        manejar_sesion_medico(usuario_dao, expediente_dao, usuario_logueado)
    elif usuario_logueado.es_paciente():
        manejar_sesion_paciente(expediente_dao, usuario_logueado)


def main():
    """Función principal del sistema refactorizada"""
    print("Iniciando Sistema de Gestión de Clínica Médica...")
    
    # Inicializar gestor de archivos
    file_manager = FileManager()
    
    # Inicializar DAOs
    usuario_dao = UsuarioDAO(file_manager)
    centro_dao = CentroDAO(file_manager)
    expediente_dao = ExpedienteDAO(file_manager)
    
    print("Sistema inicializado correctamente.")
    
    # Bucle principal del menú
    while True:
        try:
            limpiar_pantalla()
            mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n¡Gracias por usar el Sistema!")
                break
            elif opcion == "1":
                manejar_modulo_centros(centro_dao)
            elif opcion == "2":
                manejar_modulo_usuarios(usuario_dao, centro_dao)
            elif opcion == "3":
                manejar_inicio_sesion(usuario_dao, centro_dao, expediente_dao, file_manager)
            else:
                limpiar_pantalla()
                print("Opción no válida. Por favor, seleccione una opción del 0 al 3.")
                input("Presione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\nInterrupción detectada. Saliendo del sistema...")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("El sistema continuará ejecutándose...")
            input("Presione Enter para continuar...")


if __name__ == "__main__":
    main()

