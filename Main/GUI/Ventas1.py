from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from reportlab.platypus import Image

from Main.VentaP import corte_caja
from Main.VentasMain import *
from Main.tickets import *


class Ventas:
    ventas_list = []
    ventas_historial=[]
    def __init__(self, producto, cantidad,total):
        self.producto = producto
        self.cantidad = cantidad
        self.total = total


    def guardar_venta(self):
        Ventas.ventas_list.append(self)
        return True

    @classmethod
    def leer_ventas_historial_csv(cls):
        archivo_ventas_historial = 'D:\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
        try:
            with open(archivo_ventas_historial, encoding='utf8') as archivo:
                reader = csv.DictReader(archivo)
                filas = list(reader)

                if not filas or all(not any(row.values()) for row in filas):
                    print('No hay datos que leer.')
                    return
                # Leer datos y crear objetos Proveedores
                for row in filas:
                    Ventas.ventas_historial.append({"fecha":row["fecha"],"cantidad":row["cantidad"]})
                print('Datos cargados exitosamente.')
        except csv.Error as e:
            print(f'Error al leer el archivo CSV')

    @classmethod
    def escribir_ventas_historial_csv(cls):
        ruta_csv = 'D:\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["fecha", "cantidad"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for venta in Ventas.ventas_historial:
                    writer.writerow({
                        "fecha":venta["fecha"],
                        "cantidad":venta["cantidad"]
                    })
            print(f'Archivo CSV actualizado correctamente: {ruta_csv}')
        except PermissionError:
            print(f'Error de permisos al crear o escribir el archivo CSV')
        except csv.Error as e:
            print(f'Error al escribir el archivo CSV: {e}')

    @classmethod
    def crear_grafico_ventas(cls):
        try:
            # Agrupar datos por fecha y sumar cantidades
            ventas_agrupadas = defaultdict(int)
            for venta in cls.ventas_historial:
                fecha = datetime.strptime(venta["fecha"], '%d/%m/%Y')  # Convertir la fecha a datetime
                ventas_agrupadas[fecha] += int(venta["cantidad"])

            # Ordenar las fechas
            fechas = sorted(ventas_agrupadas.keys())
            cantidades = [ventas_agrupadas[fecha] for fecha in fechas]

            plt.figure(figsize=(12, 6))
            plt.plot(fechas, cantidades, marker='o', linestyle='-', color='b')
            plt.title('Reporte de ventas por mes')
            plt.xlabel('Fecha')
            plt.ylabel('Cantidad')
            plt.grid(True)

            # Formato del eje X para mostrar fechas correctamente
            plt.gca().xaxis.set_major_locator(MonthLocator())  # Mostrar un tick por mes
            plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%Y'))
            plt.xticks(rotation=45)

            # Agregar etiquetas a los puntos
            for fecha, cantidad in zip(fechas, cantidades):
                plt.annotate(
                    f'{fecha.strftime("%d/%m/%Y")}',
                    (fecha, cantidad),
                    textcoords="offset points",
                    xytext=(0, 10),  # Desplazamiento de la etiqueta
                    ha='center'
                )

            plt.tight_layout()

            grafico_path = 'D:\\Tienda-convenencia\\Archivos\\Archivos_ventas\\grafico_ventas.png'
            plt.savefig(grafico_path)
            plt.close()

            return grafico_path
        except Exception as e:
            print(f'Error al generar el gráfico: {e}')
            return None

    @classmethod
    def crear_archivo_pdf_con_grafico(cls):
        try:
            archivo_pdf = 'D:\\Tienda-convenencia\\Archivos\\Archivos_ventas\\reporte_ventas.pdf'
            doc = SimpleDocTemplate(
                archivo_pdf,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            elementos = []

            # Estilos
            estilos = getSampleStyleSheet()
            estilo_titulo = estilos['Title']
            estilo_normal = estilos['Normal']

            # Agregar título
            titulo = Paragraph('Reporte de ventas por mes', estilo_titulo)
            elementos.append(titulo)
            elementos.append(Spacer(1, 12))

            # Agregar fecha de emisión
            fecha_emision = datetime.now().strftime('%d-%m-%Y')
            fecha_parrafo = Paragraph(f'Fecha de emisión: {fecha_emision}', estilo_normal)
            elementos.append(fecha_parrafo)
            elementos.append(Spacer(1, 12))

            # Crear y agregar gráfico
            grafico_path = cls.crear_grafico_ventas()
            if grafico_path:
                img = Image(grafico_path)
                img.drawHeight = 4 * inch
                img.drawWidth = 6 * inch
                elementos.append(img)
                elementos.append(Spacer(1, 12))
            else:
                elementos.append(Paragraph('No se pudo generar el gráfico.', estilo_normal))

            # Agregar agradecimiento
            agradecimiento = Paragraph('¡Gracias por su trabajo!', estilo_normal)
            elementos.append(agradecimiento)

            # Construir el documento PDF
            doc.build(elementos)

            print(f'Reporte de ventas PDF generado correctamente: {archivo_pdf}')
        except Exception as e:
            print(f'Ha ocurrido un error al generar el reporte de ventas: {e}')

    @classmethod
    def guardar_historial_grafico(cls):
        Ventas.leer_ventas_historial_csv()
        Ventas.escribir_ventas_historial_csv()
        Ventas.crear_archivo_pdf_con_grafico() #sacar de aqui va al menu para crear reporte



    @staticmethod
    def mostrar_ventas():
        for venta in Ventas.ventas_list:
            print(f"Producto: {venta.producto}, Cantidad: {venta.cantidad}, Total: {venta.total}")


import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import re

# Assuming Producto, Proveedores, Inventario, Ticket, Ventas classes are defined in the Main module

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

def metodo_pago(total_pagar):
    def procesar_pago():
        opcion = metodo_pago_var.get()
        if opcion == "1":
            total_dado = int(efectivo_entry.get())
            if total_dado < total_pagar:
                messagebox.showerror("Error", "Efectivo incompleto")
            else:
                cambio = total_dado - total_pagar
                messagebox.showinfo("Pago realizado", f"Cambio: {cambio}")
                metodo_pago_window.destroy()
        elif opcion == "2":
            messagebox.showinfo("Pago realizado", "Pago con tarjeta")
            metodo_pago_window.destroy()

    metodo_pago_window = tk.Toplevel()
    metodo_pago_window.title("Método de Pago")

    metodo_pago_var = tk.StringVar(value="1")

    tk.Radiobutton(metodo_pago_window, text="Efectivo", variable=metodo_pago_var, value="1").pack(anchor=tk.W)
    tk.Radiobutton(metodo_pago_window, text="Tarjeta", variable=metodo_pago_var, value="2").pack(anchor=tk.W)

    efectivo_frame = tk.Frame(metodo_pago_window)
    tk.Label(efectivo_frame, text="Ingrese el efectivo dado:").pack(side=tk.LEFT)
    efectivo_entry = tk.Entry(efectivo_frame)
    efectivo_entry.pack(side=tk.LEFT)
    efectivo_frame.pack(anchor=tk.W)

    tk.Button(metodo_pago_window, text="Pagar", command=procesar_pago).pack()

class VentasApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Ventas")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        self.clear_frame()
        tk.Label(self, text="--- Menu de Ventas ---", font=("Arial", 16)).pack(pady=10)

        tk.Button(self, text="Agregar Venta", width=30, command=self.agregar_venta).pack(pady=5)
        tk.Button(self, text="Mostrar Historial Ventas", width=30, command=self.mostrar_historial_ventas).pack(pady=5)
        tk.Button(self, text="Corte de Caja", width=30, command=self.corte_caja).pack(pady=5)
        tk.Button(self, text="Generar Reporte de Ventas", width=30, command=self.generar_reporte_ventas).pack(pady=5)
        tk.Button(self, text="Salir", width=30, command=self.destroy).pack(pady=20)

    def agregar_venta(self):
        self.clear_frame()
        tk.Label(self, text="Agregar Venta", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Nombre del Producto").pack()
        self.producto_entry = tk.Entry(self)
        self.producto_entry.pack()

        tk.Label(self, text="Cantidad").pack()
        self.cantidad_entry = tk.Entry(self)
        self.cantidad_entry.pack()

        tk.Button(self, text="Agregar", command=self.procesar_agregar_venta).pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

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
        self.create_widgets()

    def mostrar_historial_ventas(self):
        self.clear_frame()
        tk.Label(self, text="Historial de Ventas", font=("Arial", 16)).pack(pady=10)
        self.resultado_text = tk.Text(self, height=20, width=80)
        self.resultado_text.pack(pady=10)
        ventas = Ventas.ventas_list
        if ventas:
            for venta in ventas:
                self.resultado_text.insert(tk.END, f"Nombre: {venta.nombre}, Cantidad: {venta.cantidad}, Total: {venta.total}\n")
        else:
            self.resultado_text.insert(tk.END, "No hay ventas registradas")
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def corte_caja(self):
        self.clear_frame()
        tk.Label(self, text="Corte de Caja", font=("Arial", 16)).pack(pady=10)
        monto = corte_caja()
        if monto >= 0:
            tk.Label(self, text=f"Total en caja: {monto}").pack(pady=10)
            self.monto_entry = tk.Entry(self)
            self.monto_entry.pack(pady=10)
            tk.Button(self, text="Realizar Corte", command=self.procesar_corte_caja).pack(pady=10)
        else:
            tk.Label(self, text="No hay ventas realizadas").pack(pady=10)
        tk.Button(self, text="Volver", command=self.create_widgets).pack(pady=10)

    def procesar_corte_caja(self):
        monto = int(self.monto_entry.get())
        if monto > corte_caja():
            messagebox.showerror("Error", "Tiene sobrante, verifique la cantidad")
        elif monto < corte_caja():
            messagebox.showerror("Error", "Tiene faltante, verifique la cantidad")
        else:
            cantidad = corte_caja()
            messagebox.showinfo("Éxito", "Corte de caja exitoso, buen día")
            fecha_actual = datetime.now().strftime("%d/%m/%Y")
            Ventas.ventas_historial.append({"fecha": fecha_actual, "cantidad": cantidad})
            Ventas.guardar_historial_grafico()
            Ventas.ventas_list.clear()
            self.create_widgets()

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




