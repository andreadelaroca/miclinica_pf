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