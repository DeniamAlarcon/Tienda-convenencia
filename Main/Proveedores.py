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
            print("No hay proveedores")
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
            if nombre == "" and correo== "" and telefono== "":
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
    def eliminar_proveedor(cls, id):
        proveedor = cls.buscar_proveedor(id)
        if proveedor:
            cls.proveedores.remove(proveedor)
            print("Proveedor eliminado exitosamente.")
        else:
            print("Proveedor no encontrado.")