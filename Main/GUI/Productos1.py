import re
from datetime import datetime
from tkinter import messagebox, ttk

from PIL._tkinter_finder import tk

from Main.Productos import *
from Main.Proveedores import *
from login1 import *



def validar_tamanio(tamanio):
    # Unidades válidas
    unidades_validas = ["kg", "g", "L", "ml", "pcs", "m", "cm", "in"]

    # Patrón para verificar que el tamaño sea un número seguido de una unidad válida
    pattern = re.compile(r'^(\d+(\.\d+)?)(kg|g|L|ml|pcs|m|cm|in)$')
    match = pattern.match(tamanio)

    if match:
        # Extraer el valor numérico y la unidad
        valor = match.group(1)
        unidad = match.group(3)

        # Verificar que la unidad sea válida y que el valor sea mayor a 0
        if unidad in unidades_validas and int(valor) > 0:
            # Verificar que el valor no comience con ceros innecesarios
            if valor == str(int(valor)):  # Esto convierte el valor a flotante y lo compara como cadena
                return True
    return False

def validar_fecha(fecha):
    formato = "%d/%m/%Y"
    try:
        datetime.strptime(fecha, formato)
        return True
    except ValueError:
        return False

def validar_caducidad(fecha):
    if fecha:
        formato = "%d/%m/%Y"
        fecha_actual = datetime.now()
        fecha_dada = datetime.strptime(fecha, formato)
        return fecha_dada < fecha_actual

def validar_cantidad(cantidad):
    return cantidad.isdigit() and int(cantidad) > 0 and not (cantidad.startswith('0') and len(cantidad) > 1)

def validar_precio(precio):
    if precio.isdigit() and int(precio) > 0 and not(precio.startswith('0') and len(precio) > 1):
        if int(precio) >= 1000:
            root = tk.Tk()
            root.withdraw()
            respuesta = messagebox.askyesno("Confirmar Precio",
                                            f"El precio ingresado es: {precio}\n¿Desea continuar?")
            if respuesta:
                # El usuario hizo clic en "Aceptar"
                print("Usuario aceptó la cantidad.")
                return True
            else:
                # El usuario hizo clic en "Cancelar"
                print("Usuario canceló la operación.")
                return False
        else:
            return True
    else:
        return False

def validar_codigo_formato(codigo):
    # Patrón que asegura que el código inicie con "P" seguido de 12 dígitos
    pattern = re.compile(r'^P\d{12}$')
    return bool(pattern.match(codigo))


def validar_longitud(cantidad):
    # Verificar la longitud de la cantidad
    if cantidad.isdigit() and 0 <= int(cantidad) < 1000:
        return True
    else:
        # Crear una ventana raíz oculta
        root = tk.Tk()
        root.withdraw()
        # Mostrar la ventana emergente con los botones Aceptar y Cancelar
        respuesta = messagebox.askyesno("Confirmar Cantidad",
                                        f"La cantidad ingresada es: {cantidad}\n¿Desea continuar?")
        if respuesta:
            # El usuario hizo clic en "Aceptar"
            print("Usuario aceptó la cantidad.")
            return True
        else:
            # El usuario hizo clic en "Cancelar"
            print("Usuario canceló la operación.")
            return False


class ProductosApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Gestión de Productos")
        self.center_window(600,500)
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
        tk.Label(self, text="--- Menu de Productos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Registrar Producto", width=30, command=self.registrar_producto).pack(pady=5)
        tk.Button(self, text="Detalles de Producto", width=30, command=self.detalles_producto).pack(pady=5)
        tk.Button(self, text="Actualizar Producto", width=30, command=self.actualizar_producto).pack(pady=5)
        tk.Button(self, text="Eliminar Producto", width=30, command=self.eliminar_producto).pack(pady=5)
        tk.Button(self, text="Crear Archivos", width=30, command=self.menu_archivos).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

    def registrar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Registrar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Código").pack()
        self.codigo_entry = tk.Entry(self)
        self.codigo_entry.pack()

        tk.Label(self, text="Nombre").pack()
        self.nombre_entry = tk.Entry(self)
        self.nombre_entry.pack()

        tk.Label(self, text="Marca").pack()
        self.marca_entry = tk.Entry(self)
        self.marca_entry.pack()

        tk.Label(self, text="Proveedor").pack()
        self.proveedor_entry = tk.Entry(self)
        self.proveedor_entry.pack()

        tk.Label(self, text="Cantidad").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        tk.Label(self, text="Tamaño (ej. 10kg, 250ml, 30pcs)").pack()
        self.tamanio_entry = tk.Entry(self)
        self.tamanio_entry.pack()

        tk.Label(self, text="Precio").pack()
        self.precio_entry = tk.Entry(self)
        self.precio_entry.pack()

        tk.Label(self, text="Fecha de Vencimiento (dd/mm/yyyy)").pack()
        self.fecha_vencimiento_entry = tk.Entry(self)
        self.fecha_vencimiento_entry.pack()

        tk.Button(self, text="Registrar", command=self.procesar_registro).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_registro(self):
        codigo = self.codigo_entry.get()
        nombre = self.nombre_entry.get()
        marca = self.marca_entry.get()
        proveedor = self.proveedor_entry.get()
        cantidad = self.cantidad_entry.get()
        tamanio = self.tamanio_entry.get()
        precio = self.precio_entry.get()
        fecha_vencimiento = self.fecha_vencimiento_entry.get()

        if not codigo or not nombre or not marca or not proveedor or not cantidad or not tamanio or not precio or not fecha_vencimiento:
            messagebox.showerror("Error", "Favor de llenar todos los campos requeridos")
            return

        if not validar_codigo_formato(codigo):
            messagebox.showerror("Error","Ingrese el codigo con el formato adecuado(P00000000000)")
            return

        if Producto.validar_codigo(codigo):
            messagebox.showerror("Error", "Código de producto ya registrado")
            return

        if Producto.buscar_nombre(nombre):
            messagebox.showerror("Error", "Nombre de producto ya registrado")
            return

        if  not Proveedores.validar_provedor(proveedor):
            messagebox.showerror("Error", "Proveedor no encontrado")
            return

        if not validar_longitud(cantidad):
            messagebox.showerror("Error","Cantidad a ingresar es muy grande")
            return

        if not validar_cantidad(cantidad):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        if not validar_tamanio(tamanio):
            messagebox.showerror("Error", "Tamaño no válido")
            return

        if not validar_precio(precio):
            messagebox.showerror("Error", "Precio no válido")
            return

        if not validar_fecha(fecha_vencimiento):
            messagebox.showerror("Error", "Fecha no válida")
            return

        if validar_caducidad(fecha_vencimiento):
            messagebox.showerror("Error", "El producto está caduco")
            return

        registro = Producto(codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_vencimiento)
        if registro.registrar():
            messagebox.showinfo("Éxito", "Producto registrado exitosamente")
            Producto.escribir_archivo_csv_productos_principal()
            self.create_widgets()
        else:
            messagebox.showerror("Error", "Producto no registrado")

    def detalles_producto(self):
        self.clear_frame()
        tk.Label(self, text="Detalles de Producto", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Busqueda por Nombre", width=30, command=self.buscar_por_nombre).pack(pady=5)
        tk.Button(self, text="Gestión de Productos", width=30, command=self.gestion_productos).pack(pady=5)
        tk.Button(self, text="Volver", width=30, command=self.create_widgets).pack(pady=10)

    def buscar_por_nombre(self):
        self.clear_frame()
        self.center_window(650,500)
        tk.Label(self, text="Buscar Producto por Nombre", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="Nombre del Producto").pack()
        self.nombre_busqueda_entry = tk.Entry(self)
        self.nombre_busqueda_entry.pack()
        tk.Button(self, text="Buscar", command=self.procesar_busqueda_nombre).pack(pady=10)
        tk.Button(self, text="Volver", command=self.detalles_producto).pack(pady=10)

        # Frame for Treeview and Scrollbars
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=(
        'Codigo', 'Nombre', 'Marca', 'Proveedor', 'Cantidad', 'Tamaño', 'Precio', 'Vencimiento'), show='headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars for the Treeview
        scrollbar_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)


    def procesar_busqueda_nombre(self):
        nombre = self.nombre_busqueda_entry.get()
        resultados = Producto.detalles_nombre(nombre)
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        for row in self.tree.get_children():
            self.tree.delete(row)
        if nombre != "":
            if resultados:
                self.tree_frame.pack(fill=tk.BOTH, expand=True)
                # Configurar los encabezados de las columnas
                for col in self.tree['columns']:
                    self.tree.heading(col, text=col)
                for producto in resultados:
                    if producto.nombre == nombre:

                        self.tree.insert('', tk.END, values=(
                            producto.codigo, producto.nombre, producto.marca, producto.proveedor,
                            producto.cantidad, producto.tamanio, producto.precio, producto.fecha_caducidad
                        ))
            else:
                messagebox.showerror("Error","No se encontraron productos con ese nombre")
                self.tree_frame.forget()  # Ocultar la tabla
        else:
            self.tree_frame.pack(fill=tk.BOTH, expand=True)
            for producto in resultados:
                self.tree.insert('', tk.END, values=(
                    producto.codigo, producto.nombre, producto.marca, producto.proveedor,
                    producto.cantidad, producto.tamanio, producto.precio, producto.fecha_caducidad))

    def gestion_productos(self):
        self.clear_frame()
        tk.Label(self, text="Gestión de Productos", font=("Arial", 16)).pack(pady=10)

        # Frame for Treeview and Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            'Codigo', 'Nombre', 'Marca', 'Proveedor', 'Cantidad', 'Tamaño', 'Precio', 'Vencimiento'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars for the Treeview
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Configure column headings
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Load product data
        productos = Producto.detalles()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if productos:
            for producto in productos:
                self.tree.insert('', tk.END, values=(
                    producto.codigo, producto.nombre, producto.marca, producto.proveedor,
                    producto.stock, producto.tamanio, producto.precio, producto.fecha_caducidad
                ))
        else:
            messagebox.showerror("Error","No hay productos registrados")

        # Button to return
        tk.Button(self, text="Volver", command=self.detalles_producto).pack(pady=10)

        # Configure the tree frame to expand with the window
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def actualizar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Actualizar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Código del Producto").pack()
        self.codigo_actualizar_entry = tk.Entry(self)
        self.codigo_actualizar_entry.pack()
        self.boton_buscar=(tk.Button(self, text="Buscar", command=self.mostar_datos_productos))
        self.boton_buscar.pack(pady=10)


        tk.Label(self, text="Nuevo Nombre").pack()
        self.nombre_actualizar_entry = tk.Entry(self)
        self.nombre_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Proveedor").pack()
        self.proveedor_actualizar_entry = tk.Entry(self)
        self.proveedor_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Tamaño").pack()
        self.tamanio_actualizar_entry = tk.Entry(self)
        self.tamanio_actualizar_entry.pack()

        tk.Label(self, text="Nuevo Precio").pack()
        self.precio_actualizar_entry = tk.Entry(self)
        self.precio_actualizar_entry.pack()

        tk.Label(self, text="Nueva fecha de caducidad (dd/mm/yyyy)").pack()
        self.fecha_actualizar_entry = tk.Entry(self)
        self.fecha_actualizar_entry.pack()

        tk.Button(self, text="Actualizar", command=self.procesar_actualizacion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def mostar_datos_productos(self):
        resultados = Producto.buscarProducto(self.codigo_actualizar_entry.get())
        if resultados:
            precio=int(resultados.precio)
            self.nombre_actualizar_entry.insert(tk.END, resultados.nombre)
            self.proveedor_actualizar_entry.insert(tk.END, resultados.proveedor)
            self.tamanio_actualizar_entry.insert(tk.END, resultados.tamanio)
            self.precio_actualizar_entry.insert(tk.END, precio)
            self.fecha_actualizar_entry.insert(tk.END, resultados.fecha_caducidad)
            self.codigo_actualizar_entry.config(state=tk.DISABLED)
            self.boton_buscar.config(state="disabled")
        else:
            messagebox.showerror("Error", "No se encontro el producto")


    def procesar_actualizacion(self):
        codigo = self.codigo_actualizar_entry.get()
        nombre = self.nombre_actualizar_entry.get()
        proveedor = self.proveedor_actualizar_entry.get()
        tamanio = self.tamanio_actualizar_entry.get()
        precio = self.precio_actualizar_entry.get()
        fecha_caducidad = self.fecha_actualizar_entry.get()

        if not codigo:
            messagebox.showerror("Error","ingrese el campo codigo para actualizar")
            return

        if codigo and not Producto.validar_codigo(codigo):
            messagebox.showerror("Error", "Producto no encontrado")
            return

        if not nombre or not proveedor or not tamanio or not precio or not fecha_caducidad:
            messagebox.showerror("Error", "Ingrese todos los campos")
            return

        if not validar_codigo_formato(codigo):
            messagebox.showerror("Error","Ingrese el codigo con el formato adecuado(P00000000000)")
            return

        if nombre and not Producto.buscar_nombre_GUI(nombre,codigo):
            if nombre and Producto.buscar_nombre(nombre):
                messagebox.showerror("Error", "Nombre de producto ya registrado")
                return

        if proveedor and not Proveedores.validar_provedor(proveedor):
            messagebox.showerror("Error", "Proveedor no encontrado")
            return

        if tamanio and not validar_tamanio(tamanio):
            messagebox.showerror("Error", "Tamaño no válido")
            return

        if precio and not validar_precio(precio):
            messagebox.showerror("Error", "Precio no válido")
            return

        if fecha_caducidad and not validar_fecha(fecha_caducidad):
            messagebox.showerror("Error","Fecha no válida")
            return

        if validar_caducidad(fecha_caducidad):
            messagebox.showerror("Error", "El producto está caduco")
            return

        print(codigo,nombre,tamanio,precio,fecha_caducidad, " esto me importa demasiado")
        Producto.actualizar(codigo, nombre, proveedor, tamanio, precio, fecha_caducidad)
        messagebox.showinfo("Éxito", "Producto actualizado exitosamente")
        Producto.escribir_archivo_csv_productos_principal()
        self.create_widgets()

    def eliminar_producto(self):
        self.clear_frame()
        tk.Label(self, text="Eliminar Producto", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Codigo del Producto").pack()
        self.id_eliminar_entry = tk.Entry(self)
        self.id_eliminar_entry.pack()
        tk.Button(self, text="Eliminar", command=self.procesar_eliminacion).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)
        # Frame for Treeview and Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            'Codigo', 'Nombre', 'Marca', 'Proveedor', 'Cantidad', 'Tamaño', 'Precio', 'Vencimiento'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars for the Treeview
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Configure column headings
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Load product data
        productos = Producto.detalles()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if productos:
            for producto in productos:
                self.tree.insert('', tk.END, values=(
                    producto.codigo, producto.nombre, producto.marca, producto.proveedor,
                    producto.cantidad, producto.tamanio, producto.precio, producto.fecha_caducidad
                ))
        else:
            messagebox.showerror("Error", "No hay productos registrados")
        # Configure the tree frame to expand with the window
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)



    def procesar_eliminacion(self):
        try:
            id = self.id_eliminar_entry.get()
            if Producto.eliminar_producto(id):
                messagebox.showinfo("Éxito", "Producto eliminado")
                Producto.escribir_archivo_csv_productos_principal()
                self.create_widgets()
                #self.id_eliminar_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Producto no encontrado")
                self.id_eliminar_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un codigo de producto válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el producto: {e}")

    def menu_archivos(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Archivos ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Crear Archivo CSV", width=30, command=Producto.crear_archivo_csv).pack(pady=5)
        tk.Button(self, text="Crear Archivo JSON", width=30, command=Producto.crear_archivo_json).pack(pady=5)
        tk.Button(self, text="Crear Archivo PDF", width=30, command=Producto.crear_archivo_pdf).pack(pady=5)
        tk.Button(self, text="Crear Archivo XLSX", width=30, command=Producto.crear_archivo_xlsx).pack(pady=5)
        tk.Button(self, text="Volver", width=30, command=self.create_widgets).pack(pady=20)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = ProductosApp()
    app.mainloop()
