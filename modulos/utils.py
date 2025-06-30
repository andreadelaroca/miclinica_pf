# funciones comunes utilizadas en el sistema

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class FileManager:
    # gestor de archivos DAT
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.separador = "|"
        self._crear_directorio()
        
    def _crear_directorio(self):
        # crea el directorio de datos si no existe
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _obtener_ruta_archivo(self, nombre_archivo: str) -> str:
        # obtiene la ruta completa del archivo
        return os.path.join(self.data_dir, f"{nombre_archivo}.dat")
    
    def _obtener_siguiente_id(self, archivo: str) -> int:
        # obtiene el siguiente ID disponible
        try:
            with open(self._obtener_ruta_archivo(archivo), 'r', encoding='utf-8') as f:
                lineas = f.readlines()
                if not lineas:
                    return 1
                # el ID está en la primera columna
                ultimo_id = max(int(linea.split(self.separador)[0]) for linea in lineas if linea.strip())
                return ultimo_id + 1
        except FileNotFoundError:
            return 1
        
    def obtener_registros(self, archivo: str) -> List[List[str]]:
        # obtiene todos los registros de un archivo
        try:
            with open(self._obtener_ruta_archivo(archivo), 'r', encoding='utf-8') as f:
                registros = []
                for linea in f:
                    if linea.strip():
                        registros.append(linea.strip().split(self.separador))
                return registros
        except FileNotFoundError:
            return []
    
    def obtener_registro_por_id(self, archivo: str, id_registro: int) -> Optional[List[str]]:
        # obtiene un registro específico por ID
        registros = self.obtener_registros(archivo)
        for registro in registros:
            if int(registro[0]) == id_registro:
                return registro
        return None
    
    def actualizar_registro(self, archivo: str, id_registro: int, nuevos_datos: List[str]) -> bool:
        # actualiza un registro existente
        registros = self.obtener_registros(archivo)
        encontrado = False
        for i, registro in enumerate(registros):
            if int(registro[0]) == id_registro:
                registros[i] = [str(id_registro)] + nuevos_datos
                encontrado = True
                break
        if encontrado:
            with open(self._obtener_ruta_archivo(archivo), 'w', encoding='utf-8') as f:
                for registro in registros:
                    f.write(self.separador.join(registro) + "\n")
        return encontrado
    
    def buscar_registros(self, archivo: str, columna: int, valor: str) -> List[List[str]]:
        # busca registros por valor en una columna específica
        registros = self.obtener_registros(archivo)
        resultados = []
        for registro in registros:
            if len(registro) > columna and valor.lower() in registro[columna].lower():
                resultados.append(registro)
        return resultados