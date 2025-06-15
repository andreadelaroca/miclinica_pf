from modules.utils import leer_archivo, escribir_archivo, generar_id

def registrar_centro():
    id_centro = generar_id("CTR")
    id_admin = input("ID del administrador operativo: ")
    nombre = input("Nombre del centro: ")
    ubicacion = input("Ubicación del centro: ")
    linea = f"{id_centro}|{id_admin}|{nombre}|{ubicacion}\n"
    escribir_archivo("data/centros.txt", [linea])
    print("Centro registrado exitosamente.")

def acceder_centro():
    id_buscar = input("Ingrese ID o nombre del centro: ").strip().lower()
    centros = leer_archivo("data/centros.txt")
    for c in centros:
        partes = c.strip().split("|")
        if id_buscar == partes[0].lower() or id_buscar == partes[2].lower():
            print(f"ID: {partes[0]}, Admin: {partes[1]}, Nombre: {partes[2]}, Ubicación: {partes[3]}")
            return
    print("Centro no encontrado.")

def modificar_centro():
    id_centro = input("ID del centro a modificar: ")
    centros = leer_archivo("data/centros.txt")
    for i, linea in enumerate(centros):
        datos = linea.strip().split("|")
        if datos[0] == id_centro:
            nuevo_nombre = input(f"Nuevo nombre [{datos[2]}]: ") or datos[2]
            nueva_ubicacion = input(f"Nueva ubicación [{datos[3]}]: ") or datos[3]
            nuevos_datos = f"{datos[0]}|{datos[1]}|{nuevo_nombre}|{nueva_ubicacion}\n"
            centros[i] = nuevos_datos
            with open("data/centros.txt", "w") as file:
                file.writelines(centros)
            print("Centro modificado.")
            return
    print("Centro no encontrado.")

def eliminar_centro():
    id_centro = input("ID del centro a eliminar: ")
    centros = leer_archivo("data/centros.txt")
    nuevos = [c for c in centros if not c.startswith(id_centro)]
    if len(centros) == len(nuevos):
        print("Centro no encontrado.")
    else:
        with open("data/centros.txt", "w") as file:
            file.writelines(nuevos)
        print("Centro eliminado.")
