#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - DAO Centro Médico
Data Access Object para centros médicos usando archivos DAT
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from typing import List, Optional
from modulos.centro import CentroMedico
from modulos.utils import FileManager


class CentroDAO:
    """DAO para manejo de centros médicos en archivos DAT"""
    
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.archivo = "centros"
    
    def crear_centro(self, centro: CentroMedico) -> int:
        """Crea un nuevo centro médico"""
        return self.file_manager.insertar_registro(self.archivo, centro.to_list())
    
    def obtener_centro_por_id(self, id_centro: int) -> Optional[CentroMedico]:
        """Obtiene un centro por su ID"""
        registro = self.file_manager.obtener_registro_por_id(self.archivo, id_centro)
        if registro:
            return CentroMedico.from_list(registro)
        return None
    
    def obtener_todos_centros(self) -> List[CentroMedico]:
        """Obtiene todos los centros activos"""
        registros = self.file_manager.obtener_registros(self.archivo)
        centros = []
        for registro in registros:
            centro = CentroMedico.from_list(registro)
            if centro and centro.activo:
                centros.append(centro)
        return centros
    
    def actualizar_centro(self, centro: CentroMedico) -> bool:
        """Actualiza un centro existente"""
        return self.file_manager.actualizar_registro(self.archivo, centro.id_centro, centro.to_list())
    
    def eliminar_centro(self, id_centro: int) -> bool:
        """Elimina (desactiva) un centro"""
        centro = self.obtener_centro_por_id(id_centro)
        if centro:
            centro.activo = False
            return self.actualizar_centro(centro)
        return False
    
    def buscar_centros(self, termino: str) -> List[CentroMedico]:
        """Busca centros por nombre o dirección"""
        centros_encontrados = []
        
        # Buscar por nombre
        registros = self.file_manager.buscar_registros(self.archivo, 1, termino)
        for registro in registros:
            centro = CentroMedico.from_list(registro)
            if centro and centro.activo:
                centros_encontrados.append(centro)
        
        # Buscar por dirección
        registros = self.file_manager.buscar_registros(self.archivo, 2, termino)
        for registro in registros:
            centro = CentroMedico.from_list(registro)
            if centro and centro.activo and centro not in centros_encontrados:
                centros_encontrados.append(centro)
        
        return centros_encontrados

