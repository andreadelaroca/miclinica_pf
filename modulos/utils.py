# funciones comunes utilizadas en el sistema

# función para leer un archivo de texto
def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            return [linea.strip() for linea in archivo.readlines() if linea.strip()]
    except FileNotFoundError:
        print(f"La información solicitada no se encontró. Verifique la ruta: {ruta_archivo}")
        return []

# función para escribir_archivo
def escribir_archivo(ruta_archivo, contenido):
    try:
        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            for linea in contenido:
                archivo.write(linea + "\n")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")
        
