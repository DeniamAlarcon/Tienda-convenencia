class Proveedores:
    idAuto=0
    proveedores = []
    def __init__(self,nombre,correo,telefono):
        Proveedores.idAuto+=1
        self.id = Proveedores.idAuto
        self.nombre=nombre
        self.correo=correo
        self.telefono=telefono
    def guardar(self):
        Proveedores.proveedores.append(self)
        return True

    @classmethod
    def mostrar(cls):
        if not cls.proveedores:
            print("No hay proveedores registrados")
        else:
            for proveedor in cls.proveedores:
               print(
                f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")

    @classmethod
    def mostrar_nombre(cls,nombre):
        if not cls.proveedores:
            print("No hay proveedores")
        else:
            for proveedor in cls.proveedores:
                if nombre.upper() == proveedor.nombre.upper():
                    print(
                        f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")
                else:
                    print("Proveedor no encontrado")

    @classmethod
    def buscar_proveedor(cls, id):
        for proveedor in cls.proveedores:
            if proveedor.id == id:
                return proveedor
        return None
    @classmethod
    def actualizar(cls,id,nombre,correo,telefono):
        proveedor = cls.buscar_proveedor(id)
        if proveedor:
            if Proveedores.comprobarExistencia(nombre,correo,telefono):
                print("Ya existe un proveedor con esos datos")
            else:
                if nombre == "" and correo == "" and telefono == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = proveedor.correo
                    proveedor.telefono = proveedor.telefono
                elif nombre == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = correo
                    proveedor.telefono = telefono
                elif correo == "":
                    proveedor.correo = proveedor.correo
                    proveedor.nombre = nombre
                    proveedor.telefono = telefono
                elif telefono == "":
                    proveedor.telefono = proveedor.telefono
                    proveedor.nombre = nombre
                    proveedor.correo = correo
                else:
                    proveedor.nombre = nombre
                    proveedor.correo = correo
                    proveedor.telefono = telefono
                print("Proveedor actualizado exitosamente.")
        else:
            print("Proveedor no encontrado.")

    @classmethod
    def eliminarProveedor(cls, id):
        try:
            proveedor = cls.buscar_proveedor(id)
            if proveedor:
                cls.proveedores.remove(proveedor)
                print("Proveedor eliminado con exito.")
            else:
                print("Proveedor no encontrado.")
        except Exception as e:
            print("Intentelo nuevamente, no ha sido eliminado")
    @classmethod
    def comprobarExistencia(self,nombre,correo,telefono):
        for proveedor in Proveedores.proveedores:
            if proveedor.nombre==nombre or proveedor.correo==correo or  proveedor.telefono==telefono:
                return True

    @classmethod
    def validar_provedor(cls,nombre):
        if Proveedores.proveedores.__len__() != 0:
            for proveedor in Proveedores.proveedores:
                if proveedor.nombre == nombre:
                    return True
                else:
                    print("Proveedor no encontrado.")
        else:
            print("No hay proveedores registrado.")
