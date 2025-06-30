#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Sistema de Gestión de Clínica Médica
Archivo principal del sistema usando archivos DAT
"""

import sys
import os

# Agregar directorios al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modulos'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'dao'))

from modulos.usuario import Usuario
from modulos.centro import CentroMedico
from modulos.expediente import Expediente
from modulos.utils import FileManager, obtener_fecha_actual
from dao.usuario_dao import UsuarioDAO
from dao.centro_dao import CentroDAO
from dao.expediente_dao import ExpedienteDAO


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
    print("3. Buscar Usuario")
    print("4. Editar Usuario")
    print("5. Eliminar Usuario")
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
    print("4. Editar Centro")
    print("5. Eliminar Centro")
    print("0. Volver al menú principal")
    print("-"*40)


def mostrar_menu_expedientes():
    os.system("cls")
    """Muestra el menú de gestión de expedientes"""
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


def listar_usuarios(usuario_dao):
    """Lista todos los usuarios"""
    usuarios = usuario_dao.obtener_todos_usuarios()
    
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\n--- LISTA DE USUARIOS ---")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
    print()
    print("-" * 64)


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


def crear_expediente(expediente_dao, usuario_dao, centro_dao):
    """Crea un nuevo expediente médico"""
    print("\n--- CREAR EXPEDIENTE MÉDICO ---")
    
    # Mostrar pacientes disponibles
    pacientes = usuario_dao.obtener_pacientes()
    if not pacientes:
        print("No hay pacientes registrados.")
        return
    
    print("\nPacientes disponibles:")
    for paciente in pacientes:
        print(f"ID: {paciente.id_usuario} | {paciente.nombre} {paciente.apellido}")
    
    try:
        id_paciente = int(input("\nID del paciente: "))
    except ValueError:
        print("ID inválido.")
        return
    
    # Mostrar médicos disponibles
    medicos = usuario_dao.obtener_medicos()
    if not medicos:
        print("No hay médicos registrados.")
        return
    
    print("\nMédicos disponibles:")
    for medico in medicos:
        print(f"ID: {medico.id_usuario} | {medico.nombre} {medico.apellido}")
    
    try:
        id_medico = int(input("\nID del médico: "))
    except ValueError:
        print("ID inválido.")
        return
    
    # Mostrar centros disponibles
    centros = centro_dao.obtener_todos_centros()
    if not centros:
        print("No hay centros registrados.")
        return
    
    print("\nCentros disponibles:")
    for centro in centros:
        print(f"ID: {centro.id_centro} | {centro.nombre}")
    
    try:
        id_centro = int(input("\nID del centro: "))
    except ValueError:
        print("ID inválido.")
        return
    
    # Datos del expediente
    diagnostico = input("\nDiagnóstico: ")
    tratamiento = input("Tratamiento: ")
    observaciones = input("Observaciones: ")
    referencia = input("Referencias: ")
    contrarreferencia = input("Contrarreferencia: ")
    interconsulta = input("Interconsulta: ")
    enfermeria = input("Enfermería: ")
    historia_clinica = input("Historia clínica: ")
    consentimientos = input("Consentimientos: ")
    hoja_identificacion = input("Hoja de identificación: ")
    reporte_examenes = input("Reporte de exámenes: ")
    
    expediente = Expediente(
        id_paciente=id_paciente,
        id_medico=id_medico,
        id_centro=id_centro,
        diagnostico=diagnostico,
        tratamiento=tratamiento,
        observaciones=observaciones,
        referencia=referencia,
        contrarreferencia=contrarreferencia,
        interconsulta=interconsulta,
        enfermeria=enfermeria,
        historia_clinica=historia_clinica,
        consentimientos=consentimientos,
        hoja_identificacion=hoja_identificacion,
        reporte_examenes=reporte_examenes
    )
    
    try:
        id_expediente = expediente_dao.crear_expediente(expediente)
        print(f"Expediente creado exitosamente con ID: {id_expediente}")
    except Exception as e:
        print(f"Error al crear expediente: {e}")


def listar_expedientes(expediente_dao):
    """Lista todos los expedientes"""
    expedientes = expediente_dao.obtener_todos_expedientes()
    
    if not expedientes:
        print("No hay expedientes registrados.")
        return
    
    print("\n--- LISTA DE EXPEDIENTES ---")
    for expediente in expedientes:
        print(f"ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Médico: {expediente.id_medico}")
        print(f"   Diagnóstico: {expediente.diagnostico}")
        print(f"   Tratamiento: {expediente.tratamiento}")
        print(f"   Observaciones: {expediente.observaciones}")
        print(f"   Fecha: {expediente.fecha_creacion}")
        print("-" * 50)


def editar_usuario(usuario_dao):
    """Edita un usuario existente"""
    print("\n--- EDITAR USUARIO ---")
    
    # Mostrar usuarios disponibles
    usuarios = usuario_dao.obtener_todos_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\nUsuarios disponibles:")
    print("\nUsuarios disponibles:")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.tipo_usuario}")
    
    try:
        id_usuario = int(input("\nID del usuario a editar: "))
        usuario = usuario_dao.obtener_usuario_por_id(id_usuario)
        
        # Pésima forma de solucionar el problema, pero hey, funciona!
        if not usuario or id_usuario == 0:
            print("Usuario no encontrado.")
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


def eliminar_usuario(usuario_dao):
    """Elimina (desactiva) un usuario"""
    print("\n--- ELIMINAR USUARIO ---")
    
    # Mostrar usuarios disponibles
    usuarios = usuario_dao.obtener_todos_usuarios()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    
    print("\nUsuarios disponibles:")
    for usuario in usuarios:
        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.tipo_usuario}")
    
    try:
        id_usuario = int(input("\nID del usuario a eliminar: "))
        usuario = usuario_dao.obtener_usuario_por_id(id_usuario)
        
        if not usuario:
            print("Usuario no encontrado.")
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


def editar_centro(centro_dao):
    """Edita un centro médico existente"""
    print("\n--- EDITAR CENTRO MÉDICO ---")
    
    # Mostrar centros disponibles
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


def listar_medicos(usuario_dao):
    """Lista todos los médicos"""
    medicos = usuario_dao.obtener_medicos()
    
    if not medicos:
        print("No hay médicos registrados.")
        return
    
    print("\n--- LISTA DE MÉDICOS ---")
    for medico in medicos:
        print(f"ID: {medico.id_usuario} | {medico.nombre} {medico.apellido} | {medico.email}")


def listar_pacientes(usuario_dao):
    """Lista todos los pacientes"""
    pacientes = usuario_dao.obtener_pacientes()
    
    if not pacientes:
        print("No hay pacientes registrados.")
        return
    
    print("\n--- LISTA DE PACIENTES ---")
    for paciente in pacientes:
        print(f"ID: {paciente.id_usuario} | {paciente.nombre} {paciente.apellido} | {paciente.email}")


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


def mostrar_menu_administrador():
    """Muestra el menú específico para administradores"""
    print("\n" + "-"*40)
    print("    MÓDULO ADMINISTRADOR")
    print("-"*40)
    print("1. Visualizar usuarios")
    print("2. Buscar usuario")
    print("3. Editar usuario")
    print("4. Archivar usuario")
    print("5. Editar centro médico")
    print("6. Archivar centro médico")
    print("7. Ver expedientes por médico")
    print("8. Listar médicos")
    print("9. Listar pacientes")
    print("10. Reportes y estadísticas")
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


def mostrar_estadisticas(file_manager):
    """Muestra estadísticas del sistema"""
    stats = file_manager.obtener_estadisticas()
    print("\n" + "="*40)
    print("    ESTADÍSTICAS DEL SISTEMA")
    print("="*40)
    print(f"Total de Centros Médicos: {stats['total_centros']}")
    print(f"Total de Usuarios: {stats['total_usuarios']}")
    print(f"  - Médicos: {stats['total_medicos']}")
    print(f"  - Pacientes: {stats['total_pacientes']}")
    print(f"Total de Expedientes: {stats['total_expedientes']}")
    print("="*40)


def main():
    """Función principal del sistema"""
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
            os.system('cls || clear')
            mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n¡Gracias por usar el Sistema de Gestión de Clínica Médica!")
                break
            
            elif opcion == "1":
                # Módulo de centros médicos
                while True:
                    os.system('cls || clear')
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
                        termino = input("Término de búsqueda: ")
                        centros = centro_dao.buscar_centros(termino)
                        if centros:
                            print("\n--- RESULTADOS DE BÚSQUEDA ---")
                            for centro in centros:
                                print(f"ID: {centro.id_centro} | {centro.nombre} | {centro.direccion} | {centro.telefono}")
                        else:
                            print("No se encontraron centros.")
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
            
            elif opcion == "2":
                # Módulo de usuarios
                while True:
                    os.system('cls || clear')
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
                        termino = input("Término de búsqueda: ")
                        usuarios = usuario_dao.buscar_usuarios(termino)
                        if usuarios:
                            print("\n--- RESULTADOS DE BÚSQUEDA ---")
                            for usuario in usuarios:
                                print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
                        else:
                            print("No se encontraron usuarios.")
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
            
            elif opcion == "3":
                # Iniciar sesión
                os.system('cls || clear')
                usuario_logueado = iniciar_sesion(usuario_dao)
                
                if usuario_logueado:
                    while True:
                        os.system('cls || clear')
                        
                        if usuario_logueado.es_administrador():
                            mostrar_menu_administrador()
                            sub_opcion = input("\nSeleccione una opción: ").strip()
                            
                            if sub_opcion == "0":
                                print("Cerrando sesión...")
                                break
                            elif sub_opcion == "1":
                                listar_usuarios(usuario_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "2":
                                termino = input("Término de búsqueda: ")
                                usuarios = usuario_dao.buscar_usuarios(termino)
                                if usuarios:
                                    print("\n--- RESULTADOS DE BÚSQUEDA ---")
                                    for usuario in usuarios:
                                        print(f"ID: {usuario.id_usuario} | {usuario.nombre} {usuario.apellido} | {usuario.email} | {usuario.tipo_usuario}")
                                else:
                                    print("No se encontraron usuarios.")
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "3":
                                editar_usuario(usuario_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "4":
                                eliminar_usuario(usuario_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "5":
                                editar_centro(centro_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "6":
                                eliminar_centro(centro_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "7":
                                try:
                                    id_medico = int(input("ID del médico: "))
                                    expedientes = expediente_dao.obtener_expedientes_por_medico(id_medico)
                                    if expedientes:
                                        print(f"\n--- EXPEDIENTES DEL MÉDICO {id_medico} ---")
                                        for expediente in expedientes:
                                            print(f"ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Diagnóstico: {expediente.diagnostico}")
                                    else:
                                        print("No se encontraron expedientes para este médico.")
                                except ValueError:
                                    print("ID inválido.")
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "8":
                                listar_medicos(usuario_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "9":
                                listar_pacientes(usuario_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "10":
                                mostrar_estadisticas(file_manager)
                                input("Presione Enter para continuar...")
                            else:
                                print("Opción no válida.")
                                input("Presione Enter para continuar...")
                        
                        elif usuario_logueado.es_medico():
                            mostrar_menu_medico()
                            sub_opcion = input("\nSeleccione una opción: ").strip()
                            
                            if sub_opcion == "0":
                                print("Cerrando sesión...")
                                break
                            elif sub_opcion == "1":
                                crear_expediente(expediente_dao, usuario_dao, centro_dao)
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "2":
                                termino = input("Término de búsqueda: ")
                                expedientes = expediente_dao.buscar_expedientes(termino)
                                if expedientes:
                                    print("\n--- RESULTADOS DE BÚSQUEDA ---")
                                    for expediente in expedientes:
                                        print(f"ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Diagnóstico: {expediente.diagnostico[:30]}...")
                                else:
                                    print("No se encontraron expedientes.")
                                input("Presione Enter para continuar...")
                            elif sub_opcion == "3":
                                try:
                                    id_paciente = int(input("ID del paciente: "))
                                    expedientes = expediente_dao.obtener_expedientes_por_paciente(id_paciente)
                                    if expedientes:
                                        print(f"\n--- EXPEDIENTES DEL PACIENTE {id_paciente} ---")
                                        for expediente in expedientes:
                                            print(f"ID: {expediente.id_expediente} | Médico: {expediente.id_medico} | Diagnóstico: {expediente.diagnostico}")
                                    else:
                                        print("No se encontraron expedientes para este paciente.")
                                except ValueError:
                                    print("ID inválido.")
                                input("Presione Enter para continuar...")
                            else:
                                print("Opción no válida.")
                                input("Presione Enter para continuar...")
                        
                        elif usuario_logueado.es_paciente():
                            mostrar_menu_paciente()
                            sub_opcion = input("\nSeleccione una opción: ").strip()
                            
                            if sub_opcion == "0":
                                print("Cerrando sesión...")
                                break
                            elif sub_opcion == "1":
                                expedientes = expediente_dao.obtener_expedientes_por_paciente(usuario_logueado.id_usuario)
                                if expedientes:
                                    print(f"\n--- MIS EXPEDIENTES ---")
                                    for expediente in expedientes:
                                        print(f"ID: {expediente.id_expediente} | Médico: {expediente.id_medico} | Diagnóstico: {expediente.diagnostico}")
                                        print(f"   Tratamiento: {expediente.tratamiento}")
                                        print(f"   Fecha: {expediente.fecha_creacion}")
                                        print("-" * 50)
                                else:
                                    print("No tienes expedientes registrados.")
                                input("Presione Enter para continuar...")
                            else:
                                print("Opción no válida.")
                                input("Presione Enter para continuar...")
            
            else:
                os.system('cls || clear')
                print("Opción no válida. Por favor, seleccione una opción del 0 al 3.")
        
        except KeyboardInterrupt:
            print("\n\nInterrupción detectada. Saliendo del sistema...")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}")
            print("El sistema continuará ejecutándose...")


if __name__ == "__main__":
    main()

