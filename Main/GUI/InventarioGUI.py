import tkinter as tk
from tkinter import ttk
from Main.Inventario import *


class InventarioApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Inventario de Productos")
        self.center_window(600,400)
        self.resizable(False, False)
        self.overrideredirect(True)
        self.inventario = Inventarios()
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
        self.center_window(600,400)
        tk.Label(self, text="--- Menú Principal ---", font=("Arial", 16)).pack(pady=10)
        tk.Button(self, text="Generar informe de inventario", width=30, command=self.generar_informe_inventario).pack(pady=5)
        tk.Button(self, text="Generar informe de stock", width=30, command=self.generar_informe_stock).pack(pady=5)
        tk.Button(self, text="Ajuste de inventario", width=30, command=self.ajuste_inventario).pack(pady=5)
        tk.Button(self, text="Revisión de fechas de caducidad", width=30, command=self.revision_fechas_caducidad).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

    def generar_informe_inventario(self):
        self.clear_frame()
        self.center_window(1250, 600)
        tk.Label(self, text="Reporte de Inventario", font=("Arial", 16)).pack(pady=10)

        # Frame for Treeview and Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            'Codigo', 'Nombre', 'Marca', 'Precio', 'Proveedor', 'Entradas', 'Salidas', 'Stock',
            'Existencias_anteriores', 'Ajustes'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars for the Treeview
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Make sure the Treeview expands to fill the frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configure column headings
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Load product data
        productos = self.inventario.obtenerInventario()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if productos:
            for producto in productos:
                self.tree.insert('', tk.END, values=(
                    producto.codigo, producto.nombre, producto.marca, producto.precio, producto.proveedor,
                    producto.entradas, producto.salidas, producto.stock, producto.existenciasAnteriores,
                    producto.ajuste))
                producto.existenciasAnteriores = producto.stock
            Producto.escribir_archivo_csv_productos_principal()
            # Frame para los botones de generación de archivos en la misma línea
            archivo_frame = tk.Frame(self)
            archivo_frame.pack(pady=5)

            tk.Button(archivo_frame, text="Generar archivo CSV", command=Inventario.escribir_archivo_csv).pack(
                side=tk.LEFT,
                padx=5)
            tk.Button(archivo_frame, text="Generar archivo JSON", command=Inventario.escribir_archivo_json).pack(
                side=tk.LEFT, padx=5)
            tk.Button(archivo_frame, text="Generar archivo PDF", command=Inventario.escribir_archivo_pdf).pack(
                side=tk.LEFT,
                padx=5)
            tk.Button(archivo_frame, text="Generar archivo XLSX", command=Inventario.escribir_archivo_xlsx).pack(
                side=tk.LEFT, padx=5)

            # Botones adicionales
            tk.Button(self, text="Limpiar entradas, salidas y ajuste", command=self.procesar_limpieza).pack(pady=5)
            tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=5)
        else:
            self.tree.insert('', tk.END, values=("No hay productos registrados",))


        #self.inventario.obtenerInventario()
    def procesar_limpieza(self):
        if self.inventario.limpiar():
            messagebox.showinfo("Limpieza", "Limpieza de entradas, salidas y ajustes realizado")
        else:
            messagebox.showinfo("Sin datos","no hay productos registrados")

    def generar_informe_stock(self):
        self.clear_frame()
        self.center_window(600, 600)
        tk.Label(self, text="Reporte de Stock", font=("Arial", 16)).pack(pady=10)

        # Frame para el Treeview y Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Crear el Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            'Código', 'Nombre', 'Marca', 'Precio', 'Stock'), show='headings')

        self.tree.grid(row=0, column=0, sticky='nsew')

        # Scrollbars para el Treeview
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky='ns')

        scrollbar_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Configurar los encabezados de las columnas
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')

        # Cargar los datos del inventario
        productos = self.inventario.informeStock()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if productos:
            for producto in productos:
                self.tree.insert('', tk.END, values=(
                    producto.codigo, producto.nombre, producto.marca, producto.precio, producto.stock))
        else:
            self.tree.insert('', tk.END, values=("No hay productos registrados",))

        # Frame para los botones de generación de archivos en la misma línea
        archivo_frame = tk.Frame(self)
        archivo_frame.pack(pady=5)

        tk.Button(archivo_frame, text="Generar archivo CSV", command=Inventario.escribir_archivo_stock_csv).pack(
            side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo JSON", command=Inventario.escribir_archivo_stock_json).pack(
            side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo PDF", command=Inventario.escribir_archivo_stock_pdf).pack(
            side=tk.LEFT, padx=5)
        tk.Button(archivo_frame, text="Generar archivo XLSX", command=Inventario.escribir_archivo_stock_xlsx).pack(
            side=tk.LEFT, padx=5)

        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

        # Asegurarse de que el Treeview se expanda para llenar el frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def ajuste_inventario(self):
        self.clear_frame()

        tk.Label(self, text="--- Ajuste de Inventario ---", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Producto").pack()
        self.nombre_ajuste_entry = tk.Entry(self)
        self.nombre_ajuste_entry.pack()

        tk.Label(self, text="Cantidad Dañada").pack()
        self.cantidad_ajuste_entry = tk.Entry(self)
        self.cantidad_ajuste_entry.pack()

        tk.Label(self, text="Precio del Producto").pack()
        self.precio_ajuste_entry = tk.Entry(self)
        self.precio_ajuste_entry.pack()

        tk.Button(self, text="Realizar Ajuste", command=self.procesar_ajuste).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_ajuste(self):
        nombre = self.nombre_ajuste_entry.get()
        cantidad = self.cantidad_ajuste_entry.get()
        precio = self.precio_ajuste_entry.get()

        if not nombre or not cantidad or not precio:
            messagebox.showerror("Error","Ingrese todos los campos requeridos")
            return

        if not nombre or not Producto.validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre del producto no existe")
            return

        if not cantidad.isdigit() or int(cantidad) < 0 or int(cantidad) > Producto.validar_stock(nombre):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        try:
            precio = float(precio)
            if precio < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio no válido")
            return

        total = self.inventario.calculoAjuste(int(cantidad), nombre, precio)
        Inventario.actualizarSalidas(nombre, int(cantidad))
        mensaje_stock=Inventario.mensajes_stock(nombre)
        messagebox.showinfo("Éxito", f"Ajuste realizado exitosamente\ntotal a reponer {total}\n{mensaje_stock}")
        Producto.escribir_archivo_csv_productos_principal()
        self.create_widgets()

    def revision_fechas_caducidad(self):
        lista_proximos,lista_cambios=self.inventario.fechas_caducidad()
        self.clear_frame()
        self.center_window(600,600)
        tk.Label(self, text="Reporte de fechas de caducidad", font=("Arial", 16)).pack(pady=10)

        # Crear un frame para el Text y el Scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=20, width=200, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)


        self.resultado_text.config(state=tk.NORMAL)
        if lista_proximos or lista_cambios:
            for cambios in lista_cambios:
                self.resultado_text.insert(tk.END,cambios+"\n")
            for proximos in lista_proximos:
                self.resultado_text.insert(tk.END,proximos+"\n")
        else:
            self.resultado_text.insert(tk.END, "No hay productos proximos a caducar")
        self.resultado_text.config(state=tk.DISABLED)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

class Inventarios:
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores

    def obtenerInventario(self):
        if Proveedores.proveedores:
            if Producto.lista_productos:
                print("INFORME DE INVENTARIO CREADO EL: ", datetime.now())
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Existencias_anteriores'} {'Ajustes':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10} {product.existenciasAnteriores} {product.ajuste:<10}")
                    print("=" * 105)
                return self.producto
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def limpiar(self):
        if self.producto:
            for product in self.producto:
                product.entradas = 0
                product.salidas = 0
                product.ajuste = 0
            return True
        else:
            return False


    def informeStock(self):
        if self.producto:
            if self.proveedor:
                Inventario.escribir_archivo_stock_csv()
                Inventario.escribir_archivo_stock_json()
                Inventario.escribir_archivo_stock_pdf()
                Inventario.escribir_archivo_stock_xlsx()
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                #for product in self.producto:
                    #Inventario.mensajes_stock(product.nombre)
                return self.producto
            else:
                print('No hay proveedores registrados')
                return None
        else:
            print('No hay productos registrados')
            return None

    def calculoAjuste(self,cantidad,nombre,precio):
        for product in self.producto:
            if product.nombre == nombre:
                total_reponer = int(cantidad) * int(precio)
                print("Ajuste realizada")
                print("Total a reponer: ", total_reponer)
                product.ajuste = cantidad
                return total_reponer

    def fechas_caducidad(self):
        lista_proximos = []
        lista_cambios = []
        formato = "%d/%m/%Y"
        for product in self.producto:
            fecha_caducidad = datetime.strptime(product.fecha_caducidad, formato)
            fecha_actual = datetime.now()
            diferencia_dias = (fecha_caducidad - fecha_actual).days
            if diferencia_dias <= 10:
                if diferencia_dias <= 2:
                    print("Realizar cambio de: ", product.nombre)
                    lista_cambios.append(f"Realizar cambio de {product.nombre}")
                else:
                    print(product.nombre, "Próximo a caducar")
                    lista_proximos.append(f"{product.nombre} próximo a caducar")
            else:
                print("Sin productos próximos a caducar")
                break
        return lista_proximos, lista_cambios

if __name__ == "__main__":
    app = InventarioApp()
    app.mainloop()
