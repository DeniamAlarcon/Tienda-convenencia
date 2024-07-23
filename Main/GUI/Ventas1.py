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
        archivo_ventas_historial = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
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
        ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
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

            #grafico_path = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\grafico_ventas.png'
            base_dir = os.path.dirname(os.path.abspath(__file__))
            grafico_path = os.path.join(base_dir, 'Archivos', 'Archivos_ventas', 'grafico_ventas.png')
            plt.savefig(grafico_path)
            plt.close()

            return grafico_path
        except FileNotFoundError:
            print(f'Archivo no encontrado:')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo:')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo:')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def crear_archivo_pdf_con_grafico(cls):
        #archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\reporte_ventas.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_ventas', 'reporte_ventas.pdf')
        try:
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
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_pdf}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {archivo_pdf}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {archivo_pdf}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

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
        self.create_widgets()
        self.main_app = main_app

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

        tk.Button(self, text="Agregar", command=self.procesar_agregar_venta).pack(pady=10)
        tk.Button(self, text="Finalizar venta", command=self.mostrar_ticket_ventas).pack(pady=10)
        tk.Button(self, text="Volver", command=self.borrar_ticket).pack(pady=10)

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
        valor = int(self.cantidad_entry.get())
        if validar_pago(valor,total_pagar):
            for venta in Ticket.lista_ticket:
                venta = Ventas(venta.nombre,venta.cantidad,venta.total)
                venta.guardar_venta()
            self.create_widgets()
            Producto.escribir_archivo_csv_productos_principal()
            Ticket.limpiar_ticket()


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
        monto = int(self.monto_entry.get())
        if monto > monto_pagar:
            messagebox.showerror("Error", "Tiene sobrante, verifique la cantidad")
        elif monto < monto_pagar:
            messagebox.showerror("Error", "Tiene faltante, verifique la cantidad")
        else:
            cantidad = monto_pagar
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




