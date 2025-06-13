class Usuario:
    def __init__(self, nombre, contraseña, rol):
        self.nombre_usuario = nombre
        self.contraseña_usuario = contraseña
        self.rol_usuario = rol

class UsuarioDAO:
    def __init__(self):
        self.usuarios = []

    def registrar_usuario(self, nombre, contraseña, tipo):
        # To do: Mejorar esta comprobación de que el usuario ya exista
        if nombre in self.usuarios:
            return
        
        self.usuarios.append(Usuario(nombre, contraseña, tipo))
        pass

    def asignar_rol(self, rol):
        
        pass
    def modificar_usuario(self):

        pass

    def inactivar_usuario(self):

        pass

    def acceder(self, nombre_usuario, contraseña_usuario):
        usuario = [usuario for usuario in self.usuarios if nombre_usuario in usuario.nombre_usuario]
        if usuario == None:
            return None
        
        if(contraseña_usuario == usuario.contraseña_usuario):
            return usuario
        else:
            return None
        
    def cerrar_sesion():
        
        pass