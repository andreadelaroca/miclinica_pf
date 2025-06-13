# funciones comunes utilizadas en el sistema

# función para leer un archivo de texto
def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        return [linea.strip() for linea in archivo.readlines() if linea.strip()]
    except FileNotFoundError:
        print(f"La información solicitada no se encontró. Verifique la ruta: {ruta_archivo}")
        return None

