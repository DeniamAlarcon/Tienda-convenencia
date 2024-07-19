import tkinter as tk
from tkinter import messagebox

class Proveedores:
    idAuto = 0
    proveedores = []

    def __init__(self, nombre, correo, telefono):
        Proveedores.idAuto += 1
        self.id = Proveedores.idAuto
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    def guardar(self):
        Proveedores.proveedores.append(self)
        return True

    @classmethod
    def mostrar(cls):
        if not cls.proveedores:
            print("No hay proveedores registrados")
        else:
            for proveedor in cls.proveedores:
                print(f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")

    @classmethod
    def mostrar_nombre(cls, nombre):
        if not cls.proveedores:
            print("No hay proveedores")
        else:
            for proveedor in cls.proveedores:
                if nombre.upper() == proveedor.nombre.upper():
                    print(f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")
                else:
                    print("Proveedor no encontrado")

    @classmethod
    def buscar_proveedor(cls, id):
        for proveedor in cls.proveedores:
            if proveedor.id == id:
                return proveedor
        return None

    @classmethod
    def actualizar(cls, id, nombre, correo, telefono):
        proveedor = cls.buscar_proveedor(id)
        if proveedor:
            if Proveedores.comprobarExistencia(nombre, correo, telefono):
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
    def comprobarExistencia(self, nombre, correo, telefono):
        for proveedor in Proveedores.proveedores:
            if proveedor.nombre == nombre or proveedor.correo == correo or proveedor.telefono == telefono:
                return True

    @classmethod
    def validar_provedor(cls, nombre):
        if Proveedores.proveedores.__len__() != 0:
            for proveedor in Proveedores.proveedores:
                if proveedor.nombre == nombre:
                    return True
                else:
                    print("Proveedor no encontrado.")
        else:
            print("No hay proveedores registrado.")

# Funciones para la interfaz gráfica
def agregar_proveedor():
    def guardar_proveedor():
        nombre = entry_nombre.get()
        correo = entry_correo.get()
        telefono = entry_telefono.get()

        if nombre and correo and telefono:
            proveedor = Proveedores(nombre, correo, telefono)
            proveedor.guardar()
            messagebox.showinfo("Éxito", "Proveedor agregado exitosamente")
            ventana_agregar.destroy()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Proveedor")

    tk.Label(ventana_agregar, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Correo:").grid(row=1, column=0, padx=10, pady=10)
    entry_correo = tk.Entry(ventana_agregar)
    entry_correo.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(ventana_agregar, text="Teléfono:").grid(row=2, column=0, padx=10, pady=10)
    entry_telefono = tk.Entry(ventana_agregar)
    entry_telefono.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(ventana_agregar, text="Guardar", command=guardar_proveedor).grid(row=3, column=0, columnspan=2, pady=10)

def mostrar_proveedores():
    ventana_mostrar = tk.Toplevel()
    ventana_mostrar.title("Mostrar Proveedores")

    if not Proveedores.proveedores:
        tk.Label(ventana_mostrar, text="No hay proveedores registrados").pack(pady=10)
    else:
        for proveedor in Proveedores.proveedores:
            tk.Label(ventana_mostrar, text=f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}").pack(pady=5)

def eliminar_proveedor():
    def eliminar():
        id = int(entry_id.get())
        Proveedores.eliminarProveedor(id)
        messagebox.showinfo("Éxito", "Proveedor eliminado")
        ventana_eliminar.destroy()

    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Proveedor")

    tk.Label(ventana_eliminar, text="ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(ventana_eliminar)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar).grid(row=1, column=0, columnspan=2, pady=10)

# Menú principal
def menu_principal():
    root = tk.Tk()
    root.title("Gestión de Proveedores")

    tk.Button(root, text="Agregar Proveedor", command=agregar_proveedor).pack(pady=10)
    tk.Button(root, text="Mostrar Proveedores", command=mostrar_proveedores).pack(pady=10)
    tk.Button(root, text="Eliminar Proveedor", command=eliminar_proveedor).pack(pady=10)
    tk.Button(root, text="Salir", command=root.destroy).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    menu_principal()
