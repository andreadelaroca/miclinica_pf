#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - DAO Expediente
Data Access Object para expedientes médicos usando archivos DAT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Optional
from modulos.expediente import Expediente
from modulos.utils import FileManager


class ExpedienteDAO:
    """DAO para manejo de expedientes en archivos DAT"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.archivo = "expedientes"
    
    def crear_expediente(self, expediente: Expediente) -> int:
        """Crea un nuevo expediente"""
        return self.file_manager.insertar_registro(self.archivo, expediente.to_list())
    
    def obtener_expediente_por_id(self, id_expediente: int) -> Optional[Expediente]:
        """Obtiene un expediente por su ID"""
        registro = self.file_manager.obtener_registro_por_id(self.archivo, id_expediente)
        if registro:
            return Expediente.from_list(registro)
        return None
    
    def obtener_todos_expedientes(self) -> List[Expediente]:
        """Obtiene todos los expedientes activos"""
        registros = self.file_manager.obtener_registros(self.archivo)
        expedientes = []
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo:
                expedientes.append(expediente)
        return expedientes
    
    def obtener_expedientes_por_paciente(self, id_paciente: int) -> List[Expediente]:
        """Obtiene todos los expedientes de un paciente"""
        registros = self.file_manager.buscar_registros(self.archivo, 1, str(id_paciente))
        expedientes = []
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo and expediente.id_paciente == id_paciente:
                expedientes.append(expediente)
        return expedientes
    
    def obtener_expedientes_por_medico(self, id_medico: int) -> List[Expediente]:
        """Obtiene todos los expedientes de un médico"""
        registros = self.file_manager.buscar_registros(self.archivo, 2, str(id_medico))
        expedientes = []
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo and expediente.id_medico == id_medico:
                expedientes.append(expediente)
        return expedientes
    
    def obtener_expedientes_por_centro(self, id_centro: int) -> List[Expediente]:
        """Obtiene todos los expedientes de un centro"""
        registros = self.file_manager.buscar_registros(self.archivo, 3, str(id_centro))
        expedientes = []
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo and expediente.id_centro == id_centro:
                expedientes.append(expediente)
        return expedientes
    
    def actualizar_expediente(self, expediente: Expediente) -> bool:
        """Actualiza un expediente existente"""
        expediente.actualizar_fecha_modificacion()
        return self.file_manager.actualizar_registro(self.archivo, expediente.id_expediente, expediente.to_list())
    
    def mostrar_expediente(self, expediente: Expediente) -> bool:
        """Actualiza un expediente existente"""
        datos = expediente.to_list()
        
        os.system('cls || clear')
        print("Expediente")
        print("-" * 64)
        print(f"Paciente:\n{int(datos[0])}\n\n")
        print(f"Médico:\n{int(datos[1])}\n\n")
        print(f"Centro:\n{datos[2]}\n\n")
        print(f"Diagnostico:\n{datos[3]}\n\n")
        print(f"Tratamiento:\n{datos[4]}\n\n")
        print(f"Observaciones:\n{datos[5]}\n\n")
        print(f"Referencia:\n{datos[6]}\n\n")
        print(f"Contrarreferencia:\n{datos[7]}\n\n")
        print(f"Interconsulta:\n{datos[8]}\n\n")
        print(f"Enfermería:\n{datos[9]}\n\n")
        print(f"Historia clinica:\n{datos[10]}\n\n")
        print(f"Consentimientos:\n{datos[11]}\n\n")
        print(f"Hoja de identificación:\n{datos[12]}\n\n")
        print(f"Reporte exámenes:\n{datos[13]}\n\n")
        print(f"Activo:\n{datos[14].lower() == 'true'}\n\n")
        print(f"Fecha de creación:\n{datos[15]}\n\n")
        print(f"Fecha de modificación:\n{datos[16]}\n\n")

        print("-" * 64)

    def eliminar_expediente(self, id_expediente: int) -> bool:
        """Elimina (desactiva) un expediente"""
        expediente = self.obtener_expediente_por_id(id_expediente)
        if expediente:
            expediente.activo = False
            return self.actualizar_expediente(expediente)
        return False

    def buscar_expedientes(self, termino: str) -> List[Expediente]:
        """Busca expedientes por diagnóstico, tratamiento u observaciones"""
        expedientes_encontrados = []
        
        # Buscar por diagnóstico
        registros = self.file_manager.buscar_registros(self.archivo, 4, termino)
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo:
                expedientes_encontrados.append(expediente)
        
        # Buscar por tratamiento
        registros = self.file_manager.buscar_registros(self.archivo, 5, termino)
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo and expediente not in expedientes_encontrados:
                expedientes_encontrados.append(expediente)
        
        # Buscar por observaciones
        registros = self.file_manager.buscar_registros(self.archivo, 6, termino)
        for registro in registros:
            expediente = Expediente.from_list(registro)
            if expediente and expediente.activo and expediente not in expedientes_encontrados:
                expedientes_encontrados.append(expediente)
        
        return expedientes_encontrados

