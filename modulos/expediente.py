#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiClinica - Módulo Expediente
Clase para gestionar expedientes médicos
"""

from datetime import datetime
from typing import List


class Expediente:
    """Clase que representa un expediente médico"""
    
    def __init__(self, id_expediente: int = 0,
                 id_paciente: int = 0,
                 id_medico: int = 0,
                 id_centro: int = 0,
                 diagnostico: str = "",
                 tratamiento: str = "", 
                 observaciones: str = "",
                 referencia: str = "",
                 contrarreferencia: str="",
                 interconsulta: str="",
                 enfermeria: str="",
                 historia_clinica: str="",
                 consentimientos: str="",
                 hoja_identificacion: str="",
                 reporte_examenes: str="",
                 activo: bool = True,
                 fecha_creacion: str = "",
                 fecha_modificacion: str = ""):
        self.id_expediente = id_expediente
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.id_centro = id_centro
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.referencia = referencia
        self.contrarreferencia = contrarreferencia
        self.interconsulta = interconsulta
        self.enfermeria = enfermeria
        self.historia_clinica = historia_clinica
        self.consentimientos = consentimientos
        self.hoja_identificacion = hoja_identificacion
        self.reporte_examenes = reporte_examenes
        self.activo = activo
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.fecha_creacion = fecha_creacion if fecha_creacion else fecha_actual
        self.fecha_modificacion = fecha_modificacion if fecha_modificacion else fecha_actual
    
    def __str__(self):
        return f"Expediente #{self.id_expediente} - {self.diagnostico[:30]}..."
    
    def to_list(self) -> List[str]:
        """Convierte el expediente a lista para guardar en archivo DAT"""
        return [
            str(self.id_paciente),
            str(self.id_medico),
            str(self.id_centro),
            self.diagnostico,
            self.tratamiento,
            self.observaciones,
            self.referencia,
            self.contrarreferencia,
            self.interconsulta,
            self.enfermeria,
            self.historia_clinica,
            self.consentimientos,
            self.hoja_identificacion,
            self.reporte_examenes,
            str(self.activo),
            self.fecha_creacion,
            self.fecha_modificacion
        ]
    
    @classmethod
    def from_list(cls, datos: List[str]):
        """Crea un expediente desde una lista de datos del archivo DAT"""
        if len(datos) >= 18:  # ID + 17 campos
            return cls(
                id_expediente=int(datos[0]),
                id_paciente=int(datos[1]),
                id_medico=int(datos[2]),
                id_centro=int(datos[3]),
                diagnostico=datos[4],
                tratamiento=datos[5],
                observaciones=datos[6],
                referencia=datos[7],
                contrarreferencia=datos[8],
                interconsulta=datos[9],
                enfermeria=datos[10],
                historia_clinica=datos[11],
                consentimientos=datos[12],
                hoja_identificacion=datos[13],
                reporte_examenes=datos[14],
                activo=datos[15].lower() == 'true',
                fecha_creacion=datos[16],
                fecha_modificacion=datos[17]
            )
        return None
    
    def actualizar_fecha_modificacion(self):
        """Actualiza la fecha de modificación al momento actual"""
        self.fecha_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

