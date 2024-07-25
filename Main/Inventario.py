import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
from Main.Productos import *
from Main.Proveedores import *
from datetime import datetime

class Inventario:
    #listaStock=[]
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores

    @classmethod
    def escribir_archivo_csv(self):
        #ruta_csv = 'D:\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_inventarios', 'reporte_inventario.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "proveedor", "entradas", "salidas", "stock",
                              "existencias_anteriores", "ajuste"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for producto in Producto.lista_productos:
                    writer.writerow({
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "marca": producto.marca,
                        "precio": producto.precio,
                        "proveedor": producto.proveedor,
                        "entradas": producto.entradas,
                        "salidas": producto.salidas,
                        "stock": producto.stock,
                        "existencias_anteriores": producto.existenciasAnteriores,
                        "ajuste": producto.ajuste
                    })
                print("archivo CSV creado correctamente ")
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
    def escribir_archivo_json(self):
        #ruta_json = 'D:\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.json'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(base_dir, 'Archivos', 'Archivos_inventarios', 'reporte_inventario.json')
        try:
            lista_productos_json = [
                {
                    "codigo": producto.codigo,
                    "nombre": producto.nombre,
                    "marca": producto.marca,
                    "precio": producto.precio,
                    "proveedor": producto.proveedor,
                    "entradas": producto.entradas,
                    "salidas": producto.salidas,
                    "stock": producto.stock,
                    "existencias_anteriores": producto.existenciasAnteriores,
                    "ajuste": producto.ajuste
                }
                for producto in Producto.lista_productos
            ]
            json_object = json.dumps(lista_productos_json, indent=4)

            with open(ruta_json, "w", encoding='utf8') as json_file:
                json_file.write(json_object)
            print("archivo JSON creado correctamente ")
        except FileNotFoundError:
            print(f'Archivo no encontrado: {ruta_json}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {ruta_json}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {ruta_json}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def escribir_archivo_pdf(self):
        #archivo_pdf = 'D:\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_inventarios', 'reporte_inventario.pdf')
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

            # Crear la tabla
            fieldnames = ["Código", "Nombre", "Marca", "Precio", "Proveedor", "Entradas", "Salidas", "Stock",
                          "Existencias Anteriores", "Ajuste"]
            data = [fieldnames]

            for product in Producto.lista_productos:
                data.append([
                    product.codigo,
                    product.nombre,
                    product.marca,
                    product.precio,
                    product.proveedor,
                    product.entradas,
                    product.salidas,
                    product.stock,
                    product.existenciasAnteriores,
                    product.ajuste
                ])

            tabla = Table(data)

            # Estilos para la tabla
            estilo = TableStyle([
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
            tabla.setStyle(estilo)

            # Agregar espacio antes y después de la tabla
            elementos.append(Spacer(1, 12))
            elementos.append(tabla)
            elementos.append(Spacer(1, 12))

            doc.build(elementos)
            print("archivo PDF creado correctamente ")
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
    def escribir_archivo_xlsx(self):
        #archivo_xlsx = 'D:\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.xlsx'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_xlsx = os.path.join(base_dir, 'Archivos', 'Archivos_inventarios', 'reporte_inventario.xlsx')
        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Inventario"

            # Escribir encabezados
            encabezados = ["codigo", "nombre", "marca", "precio", "proveedor", "entradas", "salidas", "stock",
                           "existencias_anteriores", "ajuste"]
            sheet.append(encabezados)

            # Escribir datos
            for producto in Producto.lista_productos:
                sheet.append([
                    producto.codigo,
                    producto.nombre,
                    producto.marca,
                    producto.precio,
                    producto.proveedor,
                    producto.entradas,
                    producto.salidas,
                    producto.stock,
                    producto.existenciasAnteriores,
                    producto.ajuste
                ])

            workbook.save(archivo_xlsx)
            print("archivo xlsx creado correctamente ")
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_xlsx}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {archivo_xlsx}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {archivo_xlsx}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def mensajes_stock(self,nombre):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                if int(product.stock) < 5 and int(product.stock) >0:
                    print("Stock bajo de ",product.nombre)
                    return "Stock bajo de ",product.nombre
                elif int(product.stock) == 0:
                    print("No hay stock de ",product.nombre)
                    return "No hay stock de ", product.nombre
        return None

    def actualizarEntradas(self,nombre, cantidad):
        for product in self.producto:
            if product.nombre == nombre:
                product.entradas = int(product.entradas) + int(cantidad)
                product.stock = int(product.stock) + int(cantidad)
                Inventario.mensajes_stock(nombre)
                return True

    @classmethod
    def actualizarSalidas(self, nombre, cantidad):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                if int(product.stock) >= int(cantidad):
                    product.salidas = int(product.salidas) + int(cantidad)
                    product.stock = int(product.stock) - int(cantidad)
                    Inventario.mensajes_stock(nombre)
                    return True
                else:
                    return False
        print("Producto no encontrado")
        return False

    @classmethod
    def escribir_archivo_stock_csv(self):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_Stock', 'reporte_stock.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "stock"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()
                for producto in Producto.lista_productos:
                    writer.writerow({
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "marca": producto.marca,
                        "precio": producto.precio,
                        "stock": producto.stock
                    })
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
    def escribir_archivo_stock_pdf(self):
        #archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_Stock', 'reporte_stock.pdf')
        try:
            # Ajustar márgenes
            doc = SimpleDocTemplate(
                archivo_pdf,
                pagesize=letter,
                rightMargin=inch,
                leftMargin=inch,
                topMargin=inch,
                bottomMargin=inch
            )
            elementos = []

            # Crear la tabla
            fieldnames = ["Código", "Nombre", "Marca", "Precio", "Stock"]
            data = [fieldnames]

            for producto in Producto.lista_productos:
                data.append([
                    producto.codigo,
                    producto.nombre,
                    producto.marca,
                    producto.precio,
                    producto.stock
                ])

            tabla = Table(data, colWidths=[1.2 * inch] * len(fieldnames))

            estilo = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Espacio interno izquierdo
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Espacio interno derecho
            ])
            tabla.setStyle(estilo)
            elementos.append(tabla)
            doc.build(elementos)
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
    def escribir_archivo_stock_json(cls):
        #ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.json'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(base_dir, 'Archivos', 'Archivos_Stock', 'reporte_stock.json')
        lista_productos_json = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "marca": producto.marca,
                "precio": producto.precio,
                "stock": producto.stock
            }
            for producto in Producto.lista_productos
        ]

        try:
            with open(ruta_json, "w", encoding='utf8') as archivo_json:
                json.dump(lista_productos_json, archivo_json, indent=4, ensure_ascii=False)
        except FileNotFoundError:
            print(f'Archivo no encontrado: {ruta_json}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {ruta_json}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {ruta_json}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def escribir_archivo_stock_xlsx(cls):
        #ruta_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.xlsx'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_xlsx = os.path.join(base_dir, 'Archivos', 'Archivos_Stock', 'reporte_stock.xlsx')
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Stock"

        # Escribir encabezados
        encabezados = ["codigo", "nombre", "marca", "precio", "stock"]
        sheet.append(encabezados)

        # Escribir datos
        for producto in Producto.lista_productos:
            sheet.append([
                producto.codigo,
                producto.nombre,
                producto.marca,
                producto.precio,
                producto.stock
            ])

        try:
            workbook.save(ruta_xlsx)
        except FileNotFoundError:
            print(f'Archivo no encontrado: {ruta_xlsx}')
        except PermissionError:
            print(f'Permiso denegado al intentar escribir en el archivo: {ruta_xlsx}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {ruta_xlsx}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def informeStockC(cls):
        if Producto.lista_productos:
            if Proveedores.proveedores:
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in Producto.lista_productos:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                for product in Producto.lista_productos:
                    Inventario.mensajes_stock(product.nombre)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')
