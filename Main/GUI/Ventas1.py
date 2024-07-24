from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from reportlab.platypus import Image

from Main.VentaP import corte_caja, Ventas
from Main.VentasMain import *
from Main.tickets import *
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re



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

def validar_pago(total_dado,total_pagar):
    total_dado = int(total_dado)
    if total_dado < int(total_pagar):
        messagebox.showerror("Error", "Efectivo incompleto")
        return False
    else:
        cambio = total_dado - total_pagar
        messagebox.showinfo("Pago realizado", f"Cambio: {cambio}")
        return True


class VentasApp(tk.Tk):
    def __init__(self,main_app):
        super().__init__()
        self.title("Gestión de Ventas")
        self.geometry("600x400")
        self.resizable(False, False)
        self.create_widgets()
        self.main_app = main_app

    def on_closing(self):
        # Opcionalmente, puedes mostrar un mensaje o simplemente hacer nada.
        messagebox.showinfo("Información", "No puedes cerrar esta ventana ocupe el boton salir.")

    def create_widgets(self):
        self.clear_frame()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        tk.Label(self, text="Agregar Venta", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Producto").pack()
        self.producto_entry = tk.Entry(self)
        self.producto_entry.pack()

        tk.Label(self, text="Cantidad").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        archivo_frame = tk.Frame(self)
        archivo_frame.pack(pady=5)
        tk.Button(archivo_frame, text="Agregar", command=self.procesar_agregar_venta).pack(side=tk.LEFT,pady=10)
        tk.Button(archivo_frame, text="Quitar producto", command=self.procesar_quitar).pack(side=tk.LEFT,pady=5)

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
        if cantidad != "" and producto != "":
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
                self.producto_entry.delete(0, tk.END)
                self.cantidad_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error","Ingrese todos los campos")

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
            Ticket.crear_archivo_pdf_ticket()
            self.resultado_text.insert(tk.END,f"Total a pagar: ${total_pagar}")

            #mostrar en la misma linea
            cantidad_frame = tk.Frame(self)
            cantidad_frame.pack(pady=5)
            tk.Label(cantidad_frame, text="Cantidad").pack(side=tk.LEFT, padx=5)
            self.cantidad_entry = tk.Entry(cantidad_frame)
            self.cantidad_entry.pack(side=tk.LEFT, padx=5)
            tk.Button(self,text="Aceptar",command=lambda:self.procesar_pago(total_pagar)).pack(pady=5)


        else:
            self.resultado_text.insert(tk.END, "No hay productos registrados para venta")
            tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=5)
        self.resultado_text.config(state=tk.DISABLED)

    def procesar_pago(self,total_pagar):
        try:
            valor = self.cantidad_entry.get()
            if valor.isdigit():
                if validar_pago(int(valor),total_pagar):
                    for venta in Ticket.lista_ticket:
                        venta = Ventas(venta.nombre,venta.cantidad,venta.total)
                        venta.guardar_venta()
                    self.create_widgets()
                    Producto.escribir_archivo_csv_productos_principal()
                    Ticket.limpiar_ticket()
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

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Cantidad no válida")
            return

        if not seleccionar_cantidad_producto(producto, cantidad):
            messagebox.showerror("Error", "La cantidad excede el stock o es inválida")
            return

        ticket = Ticket(producto, cantidad)
        ticket.guardar_producto()

        messagebox.showinfo("Éxito", "Producto agregado correctamente")
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

        #self.create_widgets()

    def mostrar_historial_ventas(self):
        self.clear_frame()
        self.geometry("600x600")
        tk.Label(self, text="Historial de Ventas", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80)
        self.resultado_text.pack(pady=10)
        ventas = Ventas.ventas_list
        if ventas:
            for venta in ventas:
                self.resultado_text.insert(tk.END, f"Nombre: {venta.producto}, Cantidad: {venta.cantidad}, Total: {venta.total}\n")
        else:
            self.resultado_text.insert(tk.END, "No hay ventas registradas")
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

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
            monto = int(self.monto_entry.get())
            if monto > monto_pagar:
                messagebox.showerror("Error", "Tiene sobrante, verifique la cantidad")
            elif monto < monto_pagar:
                messagebox.showerror("Error", "Tiene faltante, verifique la cantidad")
            else:
                cantidad = monto_pagar
                fecha_actual = datetime.now().strftime("%d/%m/%Y")
                Ventas.ventas_historial.append({"fecha": fecha_actual, "cantidad": cantidad})
                Ventas.guardar_historial_grafico()
                Ventas.ventas_list.clear()
                messagebox.showinfo("Éxito", "Corte de caja exitoso, buen día")
                self.create_widgets()
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




