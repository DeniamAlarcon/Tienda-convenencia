from collections import defaultdict
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from reportlab.platypus import Image
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
        #archivo_ventas_historial = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_ventas_historial = os.path.join(base_dir, 'Archivos', 'Archivos_ventas', 'ventas_historial.csv')
        try:
            with open(archivo_ventas_historial, encoding='utf8') as archivo:
                reader = csv.DictReader(archivo)
                filas = list(reader)

                if not filas or all(not any(row.values()) for row in filas):
                    print('No hay datos que leer.')
                    return
                # Leer datos
                for row in filas:
                    Ventas.ventas_historial.append({"fecha":row["fecha"],"cantidad":row["cantidad"]})
                print('Datos cargados exitosamente.')
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_ventas_historial}. Creando archivo nuevo...')
            os.makedirs(os.path.dirname(archivo_ventas_historial), exist_ok=True)
            with open(archivo_ventas_historial, mode='w', newline='', encoding='utf8') as archivo:
                fieldnames = ["fecha", "cantidad"]
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
            print(f'Archivo creado: {archivo_ventas_historial}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {archivo_ventas_historial}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def escribir_ventas_historial_csv(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_ventas\\ventas_historial.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_ventas', 'ventas_historial.csv')
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
        except FileNotFoundError:
            print(f'Archivo no encontrado: {ruta_csv}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {ruta_csv}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {ruta_csv}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def crear_grafico_ventas(cls):
        try:
            # Agrupar datos por mes y sumar cantidades
            ventas_agrupadas = defaultdict(int)
            for venta in cls.ventas_historial:
                fecha = datetime.strptime(venta["fecha"], '%d/%m/%Y')  # Convertir la fecha a datetime
                mes_anio = fecha.strftime('%Y-%m')  # Obtener año y mes
                ventas_agrupadas[mes_anio] += int(venta["cantidad"])

            # Ordenar las fechas
            fechas = sorted(datetime.strptime(fecha, '%Y-%m') for fecha in ventas_agrupadas.keys())
            cantidades = [ventas_agrupadas[fecha.strftime('%Y-%m')] for fecha in fechas]

            plt.figure(figsize=(12, 6))
            plt.plot(fechas, cantidades, marker='o', linestyle='-', color='b')
            plt.title('Reporte de ventas por mes')
            plt.xlabel('Fecha')
            plt.ylabel('Cantidad')
            plt.grid(True)

            # Formato del eje X para mostrar fechas correctamente
            plt.gca().xaxis.set_major_locator(MonthLocator())  # Mostrar un tick por mes
            plt.gca().xaxis.set_major_formatter(DateFormatter('%m-%Y'))
            plt.xticks(rotation=45)

            if len(fechas) > 1:
                plt.xlim([fechas[0], fechas[-1]])
            else:
                # Crear un rango de fechas alrededor de la única fecha existente
                fecha_unica = fechas[0]
                fecha_inicio = fecha_unica - timedelta(days=15)  # 15 días antes
                fecha_fin = fecha_unica + timedelta(days=45)  # 45 días después
                plt.xlim([fecha_inicio, fecha_fin])
                # Agregar fechas ficticias al gráfico
                fechas = [fecha_inicio, fecha_unica, fecha_fin]
                cantidades = [0, cantidades[0], 0]

            # Agregar etiquetas a los puntos
            for fecha, cantidad in zip(fechas, cantidades):
                plt.annotate(
                    f'{fecha.strftime("%d/%m/%Y")}\n{cantidad}',
                    (fecha, cantidad),
                    textcoords="offset points",
                    xytext=(0, 10),  # Desplazamiento de la etiqueta
                    ha='center'
                )

            plt.tight_layout()

            base_dir = os.path.dirname(os.path.abspath(__file__))
            grafico_path = os.path.join(base_dir, 'Archivos', 'Archivos_ventas', 'grafico_ventas.png')
            plt.savefig(grafico_path)
            plt.close()
            return grafico_path
        except FileNotFoundError:
            print('Archivo no encontrado:')
        except PermissionError:
            print('Permiso denegado al intentar escribir en el archivo:')
        except IOError:
            print('Error de entrada/salida al intentar abrir el archivo:')
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
    def guardar_historial_grafico(cls):
        Ventas.escribir_ventas_historial_csv()
        Ventas.crear_archivo_pdf_con_grafico()

def corte_caja():
    cantidad = 0
    if Ventas.ventas_list.__len__() != 0:
        for i in Ventas.ventas_list:
            cantidad += int(i.total)
        return cantidad
    else:
        return cantidad


