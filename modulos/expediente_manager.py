#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo de Gestión de Expedientes
Centraliza todas las operaciones CRUD de expedientes médicos
"""

import os
from modulos.expediente import Expediente


def crear_expediente(expediente_dao, usuario_dao, medico_logueado):
    """Crea un nuevo expediente médico"""
    print("\n--- CREAR EXPEDIENTE MÉDICO ---")
    
    # Mostrar pacientes del mismo centro del médico logueado
    pacientes = usuario_dao.obtener_pacientes_por_centro(medico_logueado.id_centro)
    if not pacientes:
        print("No hay pacientes registrados en su centro.")
        return
    
    print("\nPacientes disponibles en su centro:")
    for paciente in pacientes:
        print(f"ID: {paciente.id_usuario} | {paciente.nombre} {paciente.apellido}")
    
    try:
        id_paciente = int(input("\nID del paciente: "))
    except ValueError:
        print("ID inválido.")
        return
    
    # Validar si paciente pertenece al centro
    if not any(paciente.id_usuario == id_paciente for paciente in pacientes):
        print("El paciente seleccionado no pertenece a su centro.")
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
        id_medico=medico_logueado.id_usuario,
        id_centro=medico_logueado.id_centro,
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


def editar_expediente(expediente_dao, medico_logueado):
    """Edita un expediente médico del médico logueado"""
    print("\n--- EDITAR EXPEDIENTE MÉDICO ---")
    
    # Obtener expedientes del médico logueado
    expedientes = expediente_dao.obtener_expedientes_por_medico(medico_logueado.id_usuario)
    if not expedientes:
        print("No tienes expedientes registrados.")
        return
    
    print("\nTus expedientes:")
    for i, expediente in enumerate(expedientes, 1):
        print(f"{i}. ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Diagnóstico: {expediente.diagnostico[:50]}...")
    
    try:
        seleccion = int(input("\nSelecciona el número del expediente a editar: "))
        if seleccion < 1 or seleccion > len(expedientes):
            print("Selección inválida.")
            return
        
        expediente = expedientes[seleccion - 1]
        
        print(f"\nEditando expediente ID: {expediente.id_expediente}")
        print("(Presione Enter para mantener el valor actual)")
        
        # Editar campos del expediente
        _editar_campo_expediente(expediente, "diagnostico", "DIAGNÓSTICO")
        _editar_campo_expediente(expediente, "tratamiento", "TRATAMIENTO")
        _editar_campo_expediente(expediente, "observaciones", "OBSERVACIONES")
        _editar_campo_expediente(expediente, "referencia", "REFERENCIAS")
        _editar_campo_expediente(expediente, "contrarreferencia", "CONTRARREFERENCIA")
        _editar_campo_expediente(expediente, "interconsulta", "INTERCONSULTA")
        _editar_campo_expediente(expediente, "enfermeria", "ENFERMERÍA")
        _editar_campo_expediente(expediente, "historia_clinica", "HISTORIA CLÍNICA")
        _editar_campo_expediente(expediente, "consentimientos", "CONSENTIMIENTOS")
        _editar_campo_expediente(expediente, "hoja_identificacion", "HOJA DE IDENTIFICACIÓN")
        _editar_campo_expediente(expediente, "reporte_examenes", "REPORTE DE EXÁMENES")
        
        expediente.actualizar_fecha_modificacion()
        
        if expediente_dao.actualizar_expediente(expediente):
            print("Expediente actualizado exitosamente.")
        else:
            print("Error al actualizar expediente.")
    
    except ValueError:
        print("Selección inválida.")
    except Exception as e:
        print(f"Error: {e}")


def _editar_campo_expediente(expediente, campo, titulo):
    """Función auxiliar para editar un campo del expediente"""
    valor_actual = getattr(expediente, campo)
    print(f"\n{titulo} ACTUAL:")
    print(f"{valor_actual if valor_actual else '[Vacío]'}")
    nuevo_valor = input(f"\nNuevo {titulo.lower()}: ").strip()
    if nuevo_valor:
        setattr(expediente, campo, nuevo_valor)


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


def buscar_expediente(expediente_dao):
    """Busca expedientes por término"""
    termino = input("Término de búsqueda: ")
    expedientes = expediente_dao.buscar_expedientes(termino)
    if expedientes:
        print("\n--- RESULTADOS DE BÚSQUEDA ---")
        for i, expediente in enumerate(expedientes, 1):
            print(f"{i}. ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Diagnóstico: {expediente.diagnostico[:50]}...")
        
        try:
            seleccion = int(input("\nSeleccione el número del expediente para ver detalles (0 para volver): "))
            if seleccion == 0:
                return
            if seleccion < 1 or seleccion > len(expedientes):
                print("Selección inválida.")
                return
            
            expediente_detallado = expedientes[seleccion - 1]
            ver_expediente_detallado(expediente_detallado)
        except ValueError:
            print("Selección inválida.")
    else:
        print("No se encontraron expedientes.")


def ver_expedientes_por_paciente(expediente_dao, usuario_dao, usuario_logueado):
    """Muestra expedientes de un paciente específico"""
    # Mostrar pacientes del centro del usuario logueado
    pacientes = usuario_dao.obtener_pacientes_por_centro(usuario_logueado.id_centro)
    if not pacientes:
        print("No hay pacientes en su centro.")
        return
    
    print("\nPacientes en su centro:")
    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. ID: {paciente.id_usuario} | {paciente.nombre} {paciente.apellido}")
    
    try:
        seleccion = int(input("\nSeleccione el número del paciente (0 para volver): "))
        if seleccion == 0:
            return
        if seleccion < 1 or seleccion > len(pacientes):
            print("Selección inválida.")
            return
        
        paciente_seleccionado = pacientes[seleccion - 1]
        expedientes = expediente_dao.obtener_expedientes_por_paciente(paciente_seleccionado.id_usuario)
        if expedientes:
            print(f"\n--- EXPEDIENTES DE {paciente_seleccionado.nombre} {paciente_seleccionado.apellido} ---")
            for i, expediente in enumerate(expedientes, 1):
                print(f"{i}. ID: {expediente.id_expediente} | Médico: {expediente.id_medico} | Diagnóstico: {expediente.diagnostico[:50]}...")
            
            try:
                exp_seleccion = int(input("\nSeleccione el número del expediente para ver detalles (0 para volver): "))
                if exp_seleccion == 0:
                    return
                if exp_seleccion < 1 or exp_seleccion > len(expedientes):
                    print("Selección inválida.")
                    return
                
                expediente_detallado = expedientes[exp_seleccion - 1]
                ver_expediente_detallado(expediente_detallado)
            except ValueError:
                print("Selección inválida.")
        else:
            print("Este paciente no tiene expedientes registrados.")
    except ValueError:
        print("Selección inválida.")


def ver_expedientes_por_medico(expediente_dao, usuario_dao, usuario_logueado):
    """Muestra expedientes por médico del centro"""
    medicos = usuario_dao.obtener_medicos_por_centro(usuario_logueado.id_centro)
    if not medicos:
        print("No hay médicos en su centro.")
        return
    
    print(f"\nMédicos en su centro (Centro {usuario_logueado.id_centro}):")
    for i, medico in enumerate(medicos, 1):
        print(f"{i}. ID: {medico.id_usuario} | {medico.nombre} {medico.apellido}")
    
    try:
        seleccion = int(input("\nSeleccione el número del médico (0 para volver): "))
        if seleccion == 0:
            return
        if seleccion < 1 or seleccion > len(medicos):
            print("Selección inválida.")
            return
        
        medico_seleccionado = medicos[seleccion - 1]
        expedientes = expediente_dao.obtener_expedientes_por_medico(medico_seleccionado.id_usuario)
        if expedientes:
            print(f"\n--- EXPEDIENTES DEL DR. {medico_seleccionado.nombre} {medico_seleccionado.apellido} ---")
            for expediente in expedientes:
                print(f"ID: {expediente.id_expediente} | Paciente: {expediente.id_paciente} | Diagnóstico: {expediente.diagnostico}")
        else:
            print("Este médico no tiene expedientes registrados.")
    except ValueError:
        print("Selección inválida.")


def ver_mis_expedientes(expediente_dao, paciente_logueado):
    """Muestra expedientes del paciente logueado"""
    expedientes = expediente_dao.obtener_expedientes_por_paciente(paciente_logueado.id_usuario)
    if expedientes:
        print(f"\n--- MIS EXPEDIENTES ---")
        for i, expediente in enumerate(expedientes, 1):
            print(f"{i}. ID: {expediente.id_expediente} | Médico: {expediente.id_medico} | Diagnóstico: {expediente.diagnostico[:50]}...")
            print(f"   Fecha: {expediente.fecha_creacion}")
        
        try:
            seleccion = int(input("\nSeleccione el número del expediente para ver detalles (0 para volver): "))
            if seleccion == 0:
                return
            if seleccion < 1 or seleccion > len(expedientes):
                print("Selección inválida.")
                return
            
            expediente_detallado = expedientes[seleccion - 1]
            ver_expediente_detallado(expediente_detallado)
        except ValueError:
            print("Selección inválida.")
    else:
        print("No tienes expedientes registrados.")


def ver_expediente_detallado(expediente):
    """Muestra un expediente médico con todos los detalles en formato ordenado"""
    os.system('cls || clear')
    print("\n" + "="*70)
    print(f"    EXPEDIENTE MÉDICO - ID: {expediente.id_expediente}")
    print("="*70)
    
    campos = [
        ("ID MÉDICO", expediente.id_medico),
        ("ID CENTRO", expediente.id_centro),
        ("DIAGNÓSTICO", expediente.diagnostico),
        ("TRATAMIENTO", expediente.tratamiento),
        ("OBSERVACIONES", expediente.observaciones),
        ("REFERENCIAS", expediente.referencia),
        ("CONTRARREFERENCIA", expediente.contrarreferencia),
        ("INTERCONSULTA", expediente.interconsulta),
        ("ENFERMERÍA", expediente.enfermeria),
        ("HISTORIA CLÍNICA", expediente.historia_clinica),
        ("CONSENTIMIENTOS", expediente.consentimientos),
        ("HOJA DE IDENTIFICACIÓN", expediente.hoja_identificacion),
        ("REPORTE DE EXÁMENES", expediente.reporte_examenes)
    ]
    
    for titulo, contenido in campos:
        print(f"\n{titulo}:")
        print(f"{contenido if contenido else '[No especificado]'}")
        print("-" * 50)
    
    print(f"\nFECHA DE CREACIÓN: {expediente.fecha_creacion}")
    print(f"FECHA DE MODIFICACIÓN: {expediente.fecha_modificacion}")
    print("\n" + "="*70)

