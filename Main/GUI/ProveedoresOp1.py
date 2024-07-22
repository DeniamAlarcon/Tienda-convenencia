import tkinter as tk
from tkinter import messagebox
from Main.Proveedores import *
import re

class ProveedorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Proveedores")
        self.geometry("500x500")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Proveedor ---", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Registrar Proveedor", width=30, command=self.registrar_proveedor).pack(pady=5)
        tk.Button(self, text="Actualizar Proveedor", width=30, command=self.actualizar_proveedores).pack(pady=5)
        tk.Button(self, text="Mostrar Proveedor", width=30, command=self.mostrar_proveedor).pack(pady=5)
        tk.Button(self, text="Eliminar Proveedor", width=30, command=self.eliminar_proveedor).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.destroy).pack(pady=20)

    def registrar_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Registrar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Correo Electrónico").pack()
        self.correo_entry = tk.Entry(self)
        self.correo_entry.pack()

        tk.Label(self, text="Teléfono").pack()
        self.telefono_entry = tk.Entry(self)
        self.telefono_entry.pack()

        tk.Button(self, text="Registrar", command=self.procesar_registro).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_registro(self):
        nombre = self.nombre_entry.get()
        correo = self.correo_entry.get()
        telefono = self.telefono_entry.get()

        if not nombre or not correo or not telefono:
            messagebox.showerror("Error", "Favor de llenar todos los campos requeridos")
            return

        pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
        if not re.match(pattern, correo):
            messagebox.showerror("Error", "Correo no válido")
            return

        if not self.validar_telefono(telefono):
            messagebox.showerror("Error", "El numero debe ser mayor a 10 y menoar a 15")
            return

        registro = Proveedores(nombre, correo, telefono)

        if registro.comprobarExistencia(nombre, correo, telefono):
            messagebox.showinfo("Información", "El proveedor ya existe")
        else:
            if registro.guardar():
                messagebox.showinfo("Éxito", "Proveedor registrado")
                self.create_widgets()
            else:
                messagebox.showerror("Error", "Ocurrió un error al registrar proveedor")

    def actualizar_proveedores(self):
        self.clear_frame()
        tk.Label(self, text="Actualizar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Proveedor").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()
        tk.Button(self, text="Buscar", command=self.mostrar_proveedoresAct).pack(pady=10)

        tk.Label(self, text="Nuevo Nombre").pack()
        self.n_nombre_entry = tk.Entry(self)
        self.n_nombre_entry.pack()

        tk.Label(self, text="Nuevo Correo Electrónico").pack()
        self.n_correo_entry = tk.Entry(self)
        self.n_correo_entry.pack()

        tk.Label(self, text="Nuevo Teléfono").pack()
        self.n_telefono_entry = tk.Entry(self)
        self.n_telefono_entry.pack()

        tk.Button(self, text="Actualizar", command=self.procesar_actualizacion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def mostrar_proveedoresAct(self):
        resultados=Proveedores.mostrar_nombre(self.id_entry.get())
        if resultados:
            for i in resultados:
                if i.nombre==self.id_entry.get():
                    self.n_nombre_entry.insert(tk.END, i.nombre)
                    self.n_correo_entry.insert(tk.END, i.correo)
                    self.n_telefono_entry.insert(tk.END, i.telefono)
                messagebox.showerror("Si se encotro el ID", i.id)
        else:
            messagebox.showerror("Error", "No se encontro al proveedor")


    def procesar_actualizacion(self):
        try:
            id = self.id_entry.get()
            if Proveedores.mostrar_nombre(id):
                n_nombre = self.n_nombre_entry.get()
                n_correo = self.n_correo_entry.get()
                n_telefono = self.n_telefono_entry.get()

                if n_correo and not re.match(re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"), n_correo):
                    messagebox.showerror("Error", "Correo no válido")
                    return

                if n_telefono and not self.validar_telefono(n_telefono):
                    messagebox.showerror("Error", "El numero debe ser mayor a 10 y menoar a 15")
                    return

                if n_nombre != "" and n_correo != "" and n_telefono != "":
                    Proveedores.actualizarGUI(id, n_nombre, n_correo, n_telefono)
                    messagebox.showinfo("Éxito", "Proveedor actualizado")
                    self.create_widgets()
                else:
                    messagebox.showerror("Error", "Favor de ingresar todos los campos requeridos")
            else:
                messagebox.showerror("Error","Proveedor no encontrado")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID de proveedor válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar proveedor: {e}")

    def mostrar_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Mostrar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Busqueda por nombre", width=30, command=self.buscar_por_nombre).pack(pady=5)
        tk.Button(self, text="Gestion de proveedores", width=30, command=self.gestion_proveedores).pack(pady=5)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=20)

    def buscar_por_nombre(self):
        self.clear_frame()
        tk.Label(self, text="Buscar Proveedor por Nombre", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Nombre del Proveedor").pack()
        self.nombre_busqueda_entry = tk.Entry(self)
        self.nombre_busqueda_entry.pack()
        tk.Button(self, text="Buscar", command=self.procesar_busqueda_nombre).pack(pady=10)
        tk.Button(self, text="Volver", command=self.mostrar_proveedor).pack(pady=10)
        self.resultado_text = tk.Text(self, height=10, width=50, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)

    def procesar_busqueda_nombre(self):
        nombre = self.nombre_busqueda_entry.get()
        resultados = Proveedores.mostrar_nombre(nombre)
        self.resultado_text.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        self.resultado_text.delete(1.0, tk.END)  # Limpiar el cuadro de texto

        if resultados:
            for proveedor in resultados:
                if proveedor.nombre==nombre:
                    self.resultado_text.insert(tk.END, f"{'ID': <5}{'NOMBRE': <10}{'CORREO': <15}{'TELEFONO': <10}\n"
                                                       f"{proveedor.id: <5}{proveedor.nombre: <10}{proveedor.correo: <15}{proveedor.telefono: <10}\n")
        else:
            self.resultado_text.insert(tk.END, "No se encontraron proveedores con ese nombre")

        self.resultado_text.config(state=tk.DISABLED)  # Deshabilitar edición nuevamente

    def gestion_proveedores(self):
        self.clear_frame()
        tk.Label(self, text="Gestion de Proveedores", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=60, state=tk.DISABLED)
        self.resultado_text.pack(pady=10)
        proveedores = Proveedores.mostrar()
        self.resultado_text.config(state=tk.NORMAL)  # Habilitar edición temporalmente
        if proveedores:
            self.resultado_text.insert(tk.END,f"{'ID': <10}{'NOMBRE': <15}{'CORREO': <20}{'TELEFONO': <10}\n")
            for proveedor in proveedores:
                self.resultado_text.insert(tk.END,f"{proveedor.id: <10}{proveedor.nombre: <15}{proveedor.correo: <20}{proveedor.telefono: <10}\n")
        else:
            self.resultado_text.insert(tk.END, "No hay proveedores registrados")
        self.resultado_text.config(state=tk.DISABLED)  # Deshabilitar edición nuevamente

        tk.Button(self, text="Volver", command=self.mostrar_proveedor).pack(pady=10)

    def eliminar_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Eliminar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="ID del Proveedor").pack()
        self.id_eliminar_entry = tk.Entry(self)
        self.id_eliminar_entry.pack()
        tk.Button(self, text="Eliminar", command=self.procesar_eliminacion).pack(pady=10)

        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_eliminacion(self):
        try:
            id = int(self.id_eliminar_entry.get())
            if Proveedores.eliminarProveedor(id):
                messagebox.showinfo("Éxito", "Proveedor eliminado")
                self.create_widgets()
                #self.id_eliminar_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Proveedor no encontrado")
                self.id_eliminar_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID de proveedor válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar proveedor: {e}")

    def validar_telefono(self, telefono):
        return len(telefono) > 9 and len(telefono) < 16 and telefono.isdigit()

    def salir(self):
        self.destroy()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ProveedorApp()
    app.mainloop()
