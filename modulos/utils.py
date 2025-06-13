# funciones comunes utilizadas en el sistema

# función para leer un archivo de texto
def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        return contenido

