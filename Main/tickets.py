from Main.Productos import *
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
class Ticket:
    lista_ticket=[]
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad
        self.total = 0


    def guardar_producto(self):
        for product in self.lista_ticket:
            if product.nombre == self.nombre:
                product.cantidad = int(product.cantidad) + int(self.cantidad)
                Ticket.calcular_total()
                return True
        self.lista_ticket.append(self)
        Ticket.calcular_total()
        return True


    @classmethod
    def calcular_total(self):
        for product in Producto.lista_productos:
            for ticket in Ticket.lista_ticket:
                if product.nombre == ticket.nombre:
                    ticket.total = int(product.precio) * int(ticket.cantidad)

    @classmethod
    def crear_archivo_pdf_ticket(cls):
        #archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_tickets\\ticket.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_tickets', 'ticket.pdf')
        try:
            # Crear el documento PDF
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
            titulo = Paragraph('Ticket de Compra', estilo_titulo)
            elementos.append(titulo)
            elementos.append(Spacer(1, 12))

            # Agregar fecha de emisión
            fecha_emision = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            fecha_parrafo = Paragraph(f'Fecha de emisión: {fecha_emision}', estilo_normal)
            elementos.append(fecha_parrafo)
            elementos.append(Spacer(1, 12))

            # Datos del ticket
            data = [
                ['Nombre', 'Cantidad', 'Total']
            ]
            total_final = 0
            for producto in Ticket.lista_ticket:
                data.append([
                    producto.nombre,
                    producto.cantidad,
                    producto.total
                ])
                total_final += producto.total

            # Crear la tabla
            tabla = Table(data, colWidths=[2 * inch, 2 * inch, 2 * inch])

            # Estilos para la tabla
            estilo_tabla = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),  # Añadir relleno izquierdo
                ('RIGHTPADDING', (0, 0), (-1, -1), 12)  # Añadir relleno derecho
            ])
            tabla.setStyle(estilo_tabla)

            elementos.append(tabla)
            elementos.append(Spacer(1, 12))

            # Agregar total final
            total_parrafo = Paragraph(f'Total: ${total_final:.2f}', estilo_normal)
            elementos.append(total_parrafo)
            elementos.append(Spacer(1, 12))

            # Agregar agradecimiento
            agradecimiento = Paragraph('¡Gracias por su compra!', estilo_normal)
            elementos.append(agradecimiento)

            # Construir el documento PDF
            doc.build(elementos)

            print(f'Ticket PDF generado correctamente: {archivo_pdf}')
            os.startfile(archivo_pdf)
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
    def mostar_ticket(self):
        total_pagar = 0
        print("Compra generada el: ", datetime.now())
        print(f"{'nombre':<10} {'cantidad':<20} {'monto':<15}")
        print("=" * 60)
        for ticket in Ticket.lista_ticket:
            print(f"{ticket.nombre:<20} {ticket.cantidad:<10} {ticket.total:<10}")
            total_pagar += int(ticket.total)
        print("=" * 60)
        print("Total a pagar: ", total_pagar)
        return int(total_pagar)

    @classmethod
    def quitar_producto(cls,nombre, cantidad):
        if Ticket.lista_ticket:
            for ticket in Ticket.lista_ticket:
                if ticket.nombre == nombre and int(ticket.cantidad) >= int(cantidad):
                    for producto in Producto.lista_productos:
                        if ticket.nombre == producto.nombre:
                            producto.salidas = int(producto.salidas) - int(cantidad)
                            producto.stock = int(producto.stock) + int(cantidad)
                            ticket.cantidad = int(ticket.cantidad) - int(cantidad)
                            if int(ticket.cantidad) == 0:
                                Ticket.lista_ticket.remove(ticket)
                            Ticket.calcular_total()
                            return True
            return False

    @classmethod
    def limpiar_ticket(cls):
        Ticket.lista_ticket.clear()

