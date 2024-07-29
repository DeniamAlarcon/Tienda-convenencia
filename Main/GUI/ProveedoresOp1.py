import re
import tkinter as tk
from tkinter import ttk

from Main.Proveedores import *


class ProveedorApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Gestión de Proveedores")
        self.center_window(500,500)
        self.resizable(False, False)
        self.overrideredirect(True)
        self.create_widgets()
        self.main_app = main_app

    def center_window(self, width, height):
        # Obtener el tamaño de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular las coordenadas x e y para centrar la ventana
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Establecer la geometría de la ventana
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Proveedor ---", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Registrar Proveedor", width=30, command=self.registrar_proveedor).pack(pady=5)
        tk.Button(self, text="Actualizar Proveedor", width=30, command=self.actualizar_proveedores).pack(pady=5)
        tk.Button(self, text="Mostrar Proveedor", width=30, command=self.mostrar_proveedor).pack(pady=5)
        tk.Button(self, text="Eliminar Proveedor", width=30, command=self.eliminar_proveedor).pack(pady=5)
        tk.Button(self, text="Crear Archivos", width=30, command=self.menu_archivos).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

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
            messagebox.showerror("Error", "El  telefono debe ser numerico con una longitud mayor a 10 y menor a 15")
            return

        registro = Proveedores(nombre, correo, telefono)

        if registro.comprobarExistencia(nombre, correo, telefono):
            messagebox.showinfo("Información", "El proveedor ya existe")
        else:
            if registro.guardar():
                messagebox.showinfo("Éxito", "Proveedor registrado")
                Proveedores.escribir_archivo_csv_principal()
                self.create_widgets()
            else:
                messagebox.showerror("Error", "Ocurrió un error al registrar proveedor")

    def actualizar_proveedores(self):
        self.clear_frame()
        tk.Label(self, text="Actualizar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Proveedor").pack()
        self.id_entry = tk.Entry(self)
        self.id_entry.pack()
        self.boton_buscar=tk.Button(self, text="Buscar", command=self.mostrar_proveedoresAct)
        self.boton_buscar.pack(pady=10)

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
            self.id_entry.config(state=tk.DISABLED)
            self.boton_buscar.config(state="disabled")
        else:
            messagebox.showerror("Error", "No se encontro al proveedor")

    def procesar_actualizacion(self):
        try:
            id = self.id_entry.get()
            if Proveedores.mostrar_nombre(id):
                n_nombre = self.n_nombre_entry.get()
                n_correo = self.n_correo_entry.get()
                n_telefono = self.n_telefono_entry.get()

                if not n_nombre and not n_correo and not n_telefono:
                    messagebox.showerror("Error", "Favor de ingresar todos los campos requeridos")

                if n_correo and not re.match(re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"), n_correo):
                    messagebox.showerror("Error", "Correo no válido")
                    return

                if not n_telefono.isnumeric():
                    messagebox.showerror("Error","Ingrese un numero valido")
                    return

                if n_telefono and not self.validar_telefono(n_telefono):
                    messagebox.showerror("Error", "El  telefono debe ser numerico con una longitud mayor a 10 y menor a 15")
                    return
                Proveedores.actualizarGUI(id, n_nombre, n_correo, n_telefono)
                Proveedores.escribir_archivo_csv_principal()
                self.create_widgets()


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

        # Frame para el Treeview y Scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=(
            'ID', 'Nombre', 'Correo', 'Teléfono'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars para el Treeview
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Asegurarse de que el Treeview se expanda para llenar el frame
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

    def procesar_busqueda_nombre(self):
        # Configurar los encabezados de las columnas
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Limpiar las filas existentes
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Obtener resultados y llenar la tabla
        nombre = self.nombre_busqueda_entry.get()
        resultados = Proveedores.mostrar_nombre(nombre)

        if resultados:
            self.tree_frame.pack(fill=tk.BOTH, expand=True)  # Mostrar la tabla
            for proveedor in resultados:
                if proveedor.nombre == nombre:
                    self.tree.insert('', tk.END, values=(
                        proveedor.id, proveedor.nombre, proveedor.correo, proveedor.telefono))
        else:
            messagebox.showerror("Error","No se encontraron proveedores con ese nombre")
            self.tree_frame.forget()  # Ocultar la tabla

    def gestion_proveedores(self):
        self.clear_frame()
        tk.Label(self, text="Gestion de Proveedores", font=("Arial", 16)).pack(pady=10)
        # Frame para el Treeview y Scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=(
            'ID', 'Nombre', 'Correo', 'Teléfono'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars para el Treeview
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Asegurarse de que el Treeview se expanda para llenar el frame
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar los encabezados de las columnas
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Limpiar las filas existentes
        for row in self.tree.get_children():
            self.tree.delete(row)

        proveedores = Proveedores.mostrar()
        if proveedores:
            self.tree_frame.pack(fill=tk.BOTH, expand=True)
            for proveedor in proveedores:
                self.tree.insert('', tk.END, values=(
                    proveedor.id, proveedor.nombre, proveedor.correo, proveedor.telefono))
        else:
            messagebox.showerror("Error","No hay proveedores registrados")
            self.tree_frame.forget()  # Ocultar la tabla


        tk.Button(self, text="Volver", command=self.mostrar_proveedor).pack(pady=10)

    def eliminar_proveedor(self):
        self.clear_frame()
        tk.Label(self, text="Eliminar Proveedor", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="ID del Proveedor").pack()
        self.id_eliminar_entry = tk.Entry(self)
        self.id_eliminar_entry.pack()
        tk.Button(self, text="Eliminar", command=self.procesar_eliminacion).pack(pady=10)

        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)
        # Frame para el Treeview y Scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Crear el Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=(
            'ID', 'Nombre', 'Correo', 'Teléfono'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars para el Treeview
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Asegurarse de que el Treeview se expanda para llenar el frame
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # Configurar los encabezados de las columnas
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Limpiar las filas existentes
        for row in self.tree.get_children():
            self.tree.delete(row)

        proveedores = Proveedores.mostrar()
        if proveedores:
            self.tree_frame.pack(fill=tk.BOTH, expand=True)
            for proveedor in proveedores:
                self.tree.insert('', tk.END, values=(
                    proveedor.id, proveedor.nombre, proveedor.correo, proveedor.telefono))
        else:
            messagebox.showerror("Error", "No hay proveedores registrados")
            self.tree_frame.forget()  # Ocultar la tabla

    def procesar_eliminacion(self):
        try:
            id = int(self.id_eliminar_entry.get())
            if Proveedores.eliminarProveedor(id):
                messagebox.showinfo("Éxito", "Proveedor eliminado")
                Proveedores.escribir_archivo_csv_principal()
                self.create_widgets()
                #self.id_eliminar_entry.delete(0, tk.END)
            else:
                self.id_eliminar_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID de proveedor válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar proveedor: {e}")

    def validar_telefono(self, telefono):
        return len(telefono) > 9 and len(telefono) < 16 and telefono.isdigit()

    def menu_archivos(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Archivos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Crear Archivo CSV", width=30, command=Proveedores.escribir_archivo_csv).pack(pady=5)
        tk.Button(self, text="Crear Archivo JSON", width=30, command=Proveedores.escribir_archivo_json).pack(pady=5)
        tk.Button(self, text="Crear Archivo PDF", width=30, command=Proveedores.escribir_archivo_pdf).pack(pady=5)
        tk.Button(self, text="Crear Archivo XLSX", width=30, command=Proveedores.escribir_archivo_xlsx).pack(pady=5)
        tk.Button(self, text="Volver", width=30, command=self.create_widgets).pack(pady=20)

    def salir(self):
        self.destroy()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ProveedorApp()
    app.mainloop()
