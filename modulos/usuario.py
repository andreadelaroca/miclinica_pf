import os
from . import utils

USUARIOS_FILE = os.path.join(os.path.dirname(__file__), '..', 'dao', 'usuarios.dat')

# Clase para usuario (puede ser ordinario, admin op, medico, paciente)
class Usuario:
    def __init__(self, id_usuario, nombre_usuario, nombre_completo, contrasena_usuario, rol_usuario, estado_usuario, id_medico=None):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo
        self.contrasena_usuario = contrasena_usuario
        self.rol_usuario = rol_usuario
        self.estado_usuario = estado_usuario
        self.id_medico = id_medico or ''

    def to_record(self):
        # id_usuario|nombre_usuario|nombre_completo|contrasena_usuario|rol_usuario|estado_usuario|id_medico\n
        return f"{self.id_usuario}|{self.nombre_usuario}|{self.nombre_completo}|{self.contrasena_usuario}|{self.rol_usuario}|{self.estado_usuario}|{self.id_medico}\n"

    @staticmethod
    def from_record(record):
        parts = record.strip().split('|')
        while len(parts) < 7:  # Aseguramos que haya al menos 7 columnas
            parts.append('')
        return Usuario(*parts[:7])

# REGISTRO DE USUARIO ORDINARIO (rol: ordinario, estado: activo)
def registrar_usuario_ordinario(nombre_usuario, nombre_completo, contrasena_usuario):
    id_usuario = utils.generar_id()
    usuario = Usuario(id_usuario, nombre_usuario, nombre_completo, contrasena_usuario, 'ordinario', 'activo')
    utils.escribir_linea(USUARIOS_FILE, usuario.to_record())
    return id_usuario

# REGISTRO DE ADMIN OPERATIVO (requiere id_admin_op ya valido)
def registrar_admin_operativo(nombre_usuario, nombre_completo, contrasena_usuario, id_admin_op):
    id_usuario = id_admin_op  # mismo id que centro, por requerimiento
    if utils.existe_por_id(USUARIOS_FILE, id_usuario):
        return None  # ya existe ese admin
    usuario = Usuario(id_usuario, nombre_usuario, nombre_completo, contrasena_usuario, 'admin_op', 'activo')
    utils.escribir_linea(USUARIOS_FILE, usuario.to_record())
    return id_usuario

# ASIGNAR ROL A USUARIO ORDINARIO (a medico o a paciente)
def asignar_rol_usuario(id_usuario, nuevo_rol):
    linea = utils.buscar_por_id(USUARIOS_FILE, id_usuario)
    if not linea:
        return False
    usuario = Usuario.from_record(linea)
    if usuario.rol_usuario != 'ordinario':
        return False  # Solo ordinarios pueden cambiar
    if nuevo_rol == 'medico':
        usuario.rol_usuario = 'medico'
        usuario.id_medico = utils.generar_id()  # asignar nuevo ID medico
    elif nuevo_rol == 'paciente':
        usuario.rol_usuario = 'paciente'
    else:
        return False
    utils.actualizar_linea(USUARIOS_FILE, id_usuario, usuario.to_record())
    return True

# INACTIVAR (ESTADO = INACTIVO, no elimina)
def inactivar_usuario(id_usuario):
    linea = utils.buscar_por_id(USUARIOS_FILE, id_usuario)
    if not linea:
        return False
    usuario = Usuario.from_record(linea)
    usuario.estado_usuario = 'inactivo'
    utils.actualizar_linea(USUARIOS_FILE, id_usuario, usuario.to_record())
    return True

# MODIFICAR USUARIO (Solo admin operativo, puede modificar nombre_usuario, nombre_completo, contrasena_usuario)
def modificar_usuario(id_admin_op, id_usuario, nuevo_nombre_usuario, nuevo_nombre_completo, nueva_contrasena):
    linea = utils.buscar_por_id(USUARIOS_FILE, id_admin_op)
    if not linea:
        return False  # admin no existe
    admin = Usuario.from_record(linea)
    if admin.rol_usuario != 'admin_op' or admin.estado_usuario != 'activo':
        return False
    linea_obj = utils.buscar_por_id(USUARIOS_FILE, id_usuario)
    if not linea_obj:
        return False
    usuario = Usuario.from_record(linea_obj)
    usuario.nombre_usuario = nuevo_nombre_usuario
    usuario.nombre_completo = nuevo_nombre_completo
    usuario.contrasena_usuario = nueva_contrasena
    utils.actualizar_linea(USUARIOS_FILE, id_usuario, usuario.to_record())
    return True

# ACCEDER/LOGIN
# Devuelve el diccionario de usuario si credenciales OK y estado activo
usuario_sesion = None  # Global local a este módulo para simular sesión

def login_usuario(nombre_usuario, contrasena_usuario):
    global usuario_sesion
    usuarios = utils.leer_archivo(USUARIOS_FILE)
    for l in usuarios:
        usu = Usuario.from_record(l)
        if usu.nombre_usuario == nombre_usuario and usu.contrasena_usuario == contrasena_usuario:
            if usu.estado_usuario == 'activo':
                usuario_sesion = usu
                return usu
            else:
                return None
    return None

def cerrar_sesion():
    global usuario_sesion
    usuario_sesion = None

# Función de acceso de ejemplo (devuelve el usuario logueado, en los sistemas reales debe usarse Auth!
def usuario_actual():
    global usuario_sesion
    return usuario_sesion
