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