from tkinter import ttk, messagebox

from PIL._tkinter_finder import tk

from Main.VentaP import Ventas
from Main.tickets import *
from login1 import *


def validar_tamanio(tamanio):
    unidades_validas = ["kg", "g", "L", "ml", "pcs", "m", "cm", "in"]
    pattern = re.compile(r'^(\d+(\.\d+)?)(kg|g|L|ml|pcs|m|cm|in)$')
    match = pattern.match(tamanio)
    if match:
        unidad = match.group(3)
        return unidad in unidades_validas
    return False

def validar_stock(producto):
    for i in Producto.lista_productos:
        if i.nombre == producto:
            if i.stock == 0:
                return False
            else:
                return True

def seleccionar_cantidad_producto(producto, cantidad):
    for i in Producto.lista_productos:
        if i.nombre == producto:
            if int(cantidad) > int(i.stock):
                return False
            elif int(cantidad) == 0:
                return False
            else:
                Inventario.actualizarSalidas(producto, cantidad)
                return True

def validar_pago(total_dado, total_pagar):
    total_dado = int(total_dado)
    total_pagar = int(total_pagar)

    if total_dado < total_pagar:
        messagebox.showerror("Error", "Efectivo incompleto")
        return False
    elif total_dado > total_pagar * 10:  # Aquí defines la condición para un pago significativamente mayor
        respuesta = messagebox.askokcancel("Pago muy grande", f"El pago es mucho mayor que el total a pagar.\n\nTotal dado: {total_dado}\nTotal a pagar: {total_pagar}\n\n¿Desea continuar?")
        if not respuesta:
            return False

    cambio = total_dado - total_pagar
    messagebox.showinfo("Pago realizado", f"Cambio: {cambio}")
    return True

def validar_cantidad_venta(cantidad):
    return cantidad.isdigit() and int(cantidad) >= 0 and not (cantidad.startswith('0') and len(cantidad) > 1)


class VentasApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Gestión de Ventas")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.center_window(600, 400)
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
        tk.Label(self, text="--- Menu de Ventas ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Agregar Venta", width=30, command=self.agregar_venta).pack(pady=5)
        tk.Button(self, text="Mostrar Historial Ventas", width=30, command=self.mostrar_historial_ventas).pack(pady=5)
        tk.Button(self, text="Corte de Caja", width=30, command=self.corte_caja).pack(pady=5)
        tk.Button(self, text="Generar Reporte de Ventas", width=30, command=self.generar_reporte_ventas).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.volver_menu_principal).pack(pady=20)

    def volver_menu_principal(self):
        self.destroy()
        self.main_app.deiconify()

    def agregar_venta(self):
        self.clear_frame()
        tk.Label(self, text="Agregar Venta", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Producto").pack()
        self.producto_entry = tk.Entry(self)
        self.producto_entry.pack()

        tk.Label(self, text="Cantidad").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        archivo_frame = tk.Frame(self)
        archivo_frame.pack(pady=5)
        tk.Button(archivo_frame, text="Agregar", command=self.procesar_agregar_venta).pack(side=tk.LEFT, pady=10)
        tk.Button(archivo_frame, text="Quitar producto", command=self.procesar_quitar).pack(side=tk.LEFT, pady=5)

        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=5, width=50, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)

        tk.Button(self, text="Finalizar venta", command=self.mostrar_ticket_ventas).pack(pady=10)
        tk.Button(self, text="Volver", command=self.borrar_ticket).pack(pady=10)

    def procesar_quitar(self):
        cantidad = self.cantidad_entry.get()
        producto = self.producto_entry.get()
        if Ticket.lista_ticket.__len__() !=0:
            if cantidad != "" and producto != "":
                if re.match(r'^[1-9]\d*|0$', cantidad):
                    if Ticket.quitar_producto(producto, cantidad):
                        productos = Ticket.lista_ticket
                        self.resultado_text.config(state=tk.NORMAL)
                        self.resultado_text.delete('1.0', tk.END)
                        if productos:
                            self.resultado_text.insert(tk.END,
                                                       f"{'Nombre':<10} {'Cantidad':<20} {'Total':<15}\n")
                            for producto in productos:
                                self.resultado_text.insert(tk.END,
                                                           f"{producto.nombre:<10} {producto.cantidad:<20} {producto.total:<15}\n")
                        messagebox.showinfo("Borrado","Producto eliminado de la venta")
                        self.producto_entry.delete(0, tk.END)
                        self.cantidad_entry.delete(0, tk.END)
                    else:
                        messagebox.showerror("Error","El producto no pudo ser eliminado verifique los datos")
                else:
                    messagebox.showerror("Error", "Cantidad no válida")
            else:
                messagebox.showerror("Error","Ingrese todos los campos")
        else:
            messagebox.showerror("Error","No hay productos por eliminar")

    def borrar_ticket(self):
        for i in Ticket.lista_ticket:
            for j in Producto.lista_productos:
                if i.nombre == j.nombre:
                    j.stock = int(j.stock) + int(i.cantidad)
        Ticket.limpiar_ticket()
        self.create_widgets()


    def mostrar_ticket_ventas(self):
        self.clear_frame()
        self.geometry("600x600")
        tk.Label(self, text="Ticket de venta", font=("Arial", 16)).pack(pady=10)

        # Crear un frame para el Text y el Scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(pady=10)

        self.resultado_text = tk.Text(text_frame, height=20, width=200, state=tk.DISABLED, wrap=tk.NONE)
        self.resultado_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.resultado_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.resultado_text.config(yscrollcommand=scrollbar.set)

        productos = Ticket.lista_ticket
        self.resultado_text.config(state=tk.NORMAL)
        if productos:
            self.resultado_text.insert(tk.END,
                                       f"{'Nombre':<10} {'Cantidad':<20} {'Total':<15}\n")
            for producto in productos:
                self.resultado_text.insert(tk.END,
                                           f"{producto.nombre:<10} {producto.cantidad:<20} {producto.total:<15}\n")
            total_pagar = Ticket.mostar_ticket()
            self.resultado_text.insert(tk.END,f"Total a pagar: ${total_pagar}")

            #mostrar en la misma linea
            cantidad_frame = tk.Frame(self)
            cantidad_frame.pack(pady=5)
            tk.Label(cantidad_frame, text="Cantidad").pack(side=tk.LEFT, padx=5)
            self.cantidad_entry = tk.Entry(cantidad_frame)
            self.cantidad_entry.pack(side=tk.LEFT, padx=5)
            tk.Button(self,text="Aceptar",command=lambda:self.procesar_pago(total_pagar)).pack(pady=5)
            tk.Button(self,text="Volver",command=self.procesar_regreso).pack(pady=5) #aqui regreso a la pantalla


        else:
            self.resultado_text.insert(tk.END, "No hay productos registrados para venta")
            tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=5)
        self.resultado_text.config(state=tk.DISABLED)

    def procesar_regreso(self):
        self.agregar_venta()
        self.mostrar_productos()

    def procesar_pago(self,total_pagar):
        try:
            valor = self.cantidad_entry.get()
            if valor.isdigit():
                if validar_cantidad_venta(valor):
                    if validar_pago(int(valor),total_pagar):
                        for venta in Ticket.lista_ticket:
                            venta = Ventas(venta.nombre,venta.cantidad,venta.total)
                            venta.guardar_venta()
                        mensajes_stock = Inventario.messajes_stock_sin_busqueda()
                        if mensajes_stock:
                            messagebox.showinfo("Información de Stock", mensajes_stock)
                        self.create_widgets()
                        Ticket.crear_archivo_pdf_ticket()
                        Producto.escribir_archivo_csv_productos_principal()
                        Ticket.limpiar_ticket()
                        self.main_app.corte_realizado = False
                else:
                    messagebox.showerror("Error","Cantidad invalida")
            else:
                messagebox.showwarning("Advertencia", "Cantidad invalida")
        except ValueError:
            messagebox.showerror("Error","Ingrese los datos requeridos")


    def procesar_agregar_venta(self):
        producto = self.producto_entry.get()
        cantidad = self.cantidad_entry.get()

        if not producto or not cantidad:
            messagebox.showerror("Error", "Favor de llenar todos los campos")
            return

        if not Producto.validar_nombre(producto):
            messagebox.showerror("Error", "Producto no encontrado")
            return

        if not validar_stock(producto):
            messagebox.showerror("Error", f"No hay stock de {producto}")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0 or not re.match(r'^[1-9]\d*|0$', cantidad):
            messagebox.showerror("Error", "Cantidad no válida")
            return

        if not seleccionar_cantidad_producto(producto, cantidad):
            messagebox.showerror("Error", "La cantidad excede el stock o es inválida")
            return

        ticket = Ticket(producto, cantidad)
        ticket.guardar_producto()

        messagebox.showinfo("Éxito", "Producto agregado correctamente")
        self.mostrar_productos()


        #self.create_widgets()
    def mostrar_productos(self):
        productos = Ticket.lista_ticket
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete('1.0', tk.END)
        if productos:
            self.resultado_text.insert(tk.END,
                                       f"{'Nombre':<10} {'Cantidad':<20} {'Total':<15}\n")
            for producto in productos:
                self.resultado_text.insert(tk.END,
                                           f"{producto.nombre:<10} {producto.cantidad:<20} {producto.total:<15}\n")
        self.producto_entry.delete(0, tk.END)
        self.cantidad_entry.delete(0, tk.END)

    def mostrar_historial_ventas(self):
        self.clear_frame()
        self.center_window(600,600)
        tk.Label(self, text="Historial de Ventas", font=("Arial", 16)).pack(pady=10)

        # Frame for Treeview and Scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Create the Treeview
        self.tree = ttk.Treeview(tree_frame, columns=(
            'Nombre', 'Cantidad', 'Total'), show='headings')

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


        ventas = Ventas.ventas_list

        for row in self.tree.get_children():
            self.tree.delete(row)

        if ventas:
            for venta in ventas:
                self.tree.insert('', tk.END, values=(venta.producto,venta.cantidad,venta.total))
            tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=5)
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
        else:
            messagebox.showerror("Error", "No hay ventas registradas")
            self.create_widgets()

    def corte_caja(self):
        self.clear_frame()
        tk.Label(self, text="Corte de Caja", font=("Arial", 16)).pack(pady=10)
        monto = 0
        for total_pagar in Ventas.ventas_list:
            monto += total_pagar.total
        if monto >= 0:
            tk.Label(self, text=f"Total en caja: {monto}").pack(pady=10)
            self.monto_entry = tk.Entry(self)
            self.monto_entry.pack(pady=10)
            tk.Button(self, text="Realizar Corte", command=lambda:self.procesar_corte_caja(monto)).pack(pady=10)
        else:
            tk.Label(self, text="No hay ventas realizadas").pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_corte_caja(self,monto_pagar):
        try:
            monto = self.monto_entry.get()
            if validar_cantidad_venta(monto):
                if int(monto) > int(monto_pagar):
                    messagebox.showerror("Error", "Tiene sobrante, verifique la cantidad")
                elif int(monto) < int(monto_pagar):
                    messagebox.showerror("Error", "Tiene faltante, verifique la cantidad")
                else:
                    cantidad = monto_pagar
                    fecha_actual = datetime.now().strftime("%d/%m/%Y")
                    Ventas.ventas_historial.append({"fecha": fecha_actual, "cantidad": cantidad})
                    #Ventas.guardar_historial_grafico()
                    Ventas.escribir_ventas_historial_csv()
                    Ventas.ventas_list.clear()
                    self.main_app.corte_realizado = True
                    messagebox.showinfo("Éxito", "Corte de caja exitoso, buen día")
                    self.create_widgets()
            else:
                messagebox.showerror("Error", "Cantidad invalida")
        except ValueError:
            messagebox.showerror("Error","Inngrese una cantidad valida")

    def generar_reporte_ventas(self):
        Ventas.guardar_historial_grafico()
        messagebox.showinfo("Éxito", "Reporte generado exitosamente")
        self.create_widgets()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = VentasApp()
    app.mainloop()




