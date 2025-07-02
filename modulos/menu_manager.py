#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo de Gestión de Menús
Centraliza todas las funciones de mostrar menús del sistema
"""

import os


def mostrar_menu_principal():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*50)
    print("    SISTEMA DE GESTIÓN DE CLÍNICA MÉDICA")
    print("="*50)
    print("1. Módulo de centros médicos")
    print("2. Módulo de usuarios")
    print("3. Iniciar sesión")
    print("0. Salir")
    print("="*50)


def mostrar_menu_usuarios():
    """Muestra el menú de gestión de usuarios"""
    print("\n" + "-"*40)
    print("    GESTIÓN DE USUARIOS")
    print("-"*40)
    print("1. Registrar Usuario")
    print("2. Listar Usuarios")
<<<<<<< HEAD
    print("3. Buscar Usuario") 
    print("4. Editar Usuario") 
    print("5. Eliminar Usuario")
=======
    print("3. Buscar Usuario")
>>>>>>> f2c65808598ff72dc24eb8f9e1870288cf9b06b0
    print("0. Volver al menú principal")
    print("-"*40)


def mostrar_menu_centros():
    """Muestra el menú de gestión de centros médicos"""
    print("\n" + "-"*40)
    print("    GESTIÓN DE CENTROS MÉDICOS")
    print("-"*40)
    print("1. Registrar Centro Médico")
    print("2. Listar Centros")
    print("3. Buscar Centro")
    print("0. Volver al menú principal")
    print("-"*40)


def mostrar_menu_expedientes():
    """Muestra el menú de gestión de expedientes"""
    os.system("cls" if os.name == "nt" else "clear")
    print("\n" + "-"*40)
    print("    GESTIÓN DE EXPEDIENTES MÉDICOS")
    print("-"*40)
    print("1. Crear Expediente")
    print("2. Listar Expedientes")
    print("3. Buscar Expediente")
    print("4. Ver Expedientes por Paciente")
    print("5. Ver Expedientes por Médico")
    print("6. Listar Médicos")
    print("7. Listar Pacientes")
    print("0. Volver al menú principal")
    print("-"*40)


def mostrar_menu_administrador():
    """Muestra el menú específico para administradores"""
    print("\n" + "-"*40)
    print("    MÓDULO ADMINISTRADOR")
    print("-"*40)
    print("1. Visualizar usuarios")
    print("2. Buscar usuario")
    print("3. Archivar usuario")
    print("4. Archivar centro médico")
    print("5. Ver expedientes por médico")
    print("6. Listar médicos")
    print("7. Listar pacientes")
    print("8. Reportes y estadísticas")
    print("0. Cerrar sesión")
    print("-"*40)


def mostrar_menu_medico():
    """Muestra el menú específico para médicos"""
    print("\n" + "-"*40)
    print("    MÓDULO MÉDICO")
    print("-"*40)
    print("1. Crear expediente")
    print("2. Buscar expediente")
    print("3. Ver expedientes por paciente")
    print("0. Cerrar sesión")
    print("-"*40)


def mostrar_menu_paciente():
    """Muestra el menú específico para pacientes"""
    print("\n" + "-"*40)
    print("    MÓDULO PACIENTE")
    print("-"*40)
    print("1. Ver mis expedientes")
    print("0. Cerrar sesión")
    print("-"*40)


def limpiar_pantalla():
    """Limpia la pantalla según el sistema operativo"""
    os.system("cls" if os.name == "nt" else "clear")

