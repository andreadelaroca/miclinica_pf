# funciones comunes utilizadas en el sistema

# función para leer archivo de texto
def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            return [linea.strip() for linea in archivo.readlines() if linea.strip()]
    except FileNotFoundError:
        print(f"La información solicitada no se encontró. Verifique la ruta: {ruta_archivo}")
        return []

# función para escribir archivo de texto
def escribir_archivo(nombre_archivo, contenido):
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            for linea in contenido:
                archivo.write(linea + "\n")
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")
        
# función para actualizar registro en archivo de texto
def actualizar_registro(nombre_archivo, id, contenido_nuevo):
    