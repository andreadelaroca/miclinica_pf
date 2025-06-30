# funciones comunes utilizadas en el sistema

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class FileManager:
    # gestor simple de archivos DAT
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.separador = "|"
        self._crear_directorio()
        
    