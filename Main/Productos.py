import csv
import json
import os
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
from datetime import datetime


class Producto:
    lista_productos = []
    def __init__(self ,codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.proveedor = proveedor
        self.tamanio = tamanio
        self.precio = precio
        self.fecha_caducidad = fecha_caducidad
        self.entradas = cantidad
        self.salidas = 0
        self.stock = cantidad
        self.existenciasAnteriores = cantidad
        self.ajuste = 0

    @classmethod
    def leer_archivo(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_proveedores = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'productos.csv')

        codigos_procesados = set()
        nombres_procesados = set()
        codigo_pattern = re.compile(r'^P\d{2}$')
        fecha_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')

        try:
            with open(archivo_proveedores, encoding='utf8') as archivo_productos:
                reader = csv.DictReader(archivo_productos)
                filas = list(reader)
                if not filas or all(not any(row.values()) for row in filas):
                    print('No hay datos que leer')
                    return
                for row in filas:
                    codigo = row["codigo"]
                    nombre = row["nombre"]

                    if not codigo_pattern.match(codigo):
                        print(f'Código inválido en la fila: {row}')
                        continue

                    if codigo in codigos_procesados or nombre in nombres_procesados:
                        print(f'Fila ignorada por código o nombre duplicado: {row}')
                        continue

                    try:
                        stock = int(row["stock"])
                        precio = float(row["precio"])

                        # Validar entradas, salidas, stock, existencias_anteriores, ajuste
                        if not re.match(r'^(0|[1-9]\d*)$', row["entradas"]) or \
                                not re.match(r'^(0|[1-9]\d*)$', row["salidas"]) or \
                                not re.match(r'^(0|[1-9]\d*)$', row["stock"]) or \
                                not re.match(r'^(0|[1-9]\d*)$', row["existencias_anteriores"]) or \
                                not re.match(r'^(0|[1-9]\d*)$', row["ajuste"]):
                            print(f'Datos inválidos en la fila: {row}')
                            continue

                        entradas = int(row["entradas"])
                        salidas = int(row["salidas"])
                        stock = int(row["stock"])

                        if not (stock >= 0 and precio > 0 and entradas >= 0 and salidas >= 0 and stock >= 0):
                            print(f'Datos inválidos en la fila: {row}')
                            continue

                        if not re.match(r'^\d+(kg|g|L|ml|pcs|m|cm|in)$', row["tamanio"]):
                            print(f'Formato de tamaño inválido en la fila: {row}')
                            continue

                        fecha_caducidad = row["fecha_caducidad"]
                        if not fecha_pattern.match(fecha_caducidad):
                            print(f'Formato de fecha inválido en la fila: {row}')
                            continue
                        try:
                            datetime.strptime(fecha_caducidad, "%d/%m/%Y")
                        except ValueError:
                            print(f'Fecha inválida en la fila: {row}')
                            continue

                        producto = Producto(
                            codigo,
                            nombre,
                            row["marca"],
                            row["proveedor"],
                            stock,
                            row["tamanio"],
                            precio,
                            fecha_caducidad
                        )
                        producto.entradas = entradas
                        producto.salidas = salidas
                        producto.stock = stock
                        producto.existenciasAnteriores = int(row["existencias_anteriores"])
                        producto.ajuste = int(row["ajuste"])

                        Producto.lista_productos.append(producto)
                        codigos_procesados.add(codigo)
                        nombres_procesados.add(nombre)
                    except ValueError as e:
                        print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
                        continue

            print("Datos cargados correctamente")
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_proveedores}. Creando archivo nuevo...')
            os.makedirs(os.path.dirname(archivo_proveedores), exist_ok=True)
            with open(archivo_proveedores, mode='w', newline='', encoding='utf8') as archivo:
                fieldnames = ["codigo", "nombre", "marca", "proveedor", "tamanio", "precio",
                              "fecha_caducidad", "entradas", "salidas", "stock", "existencias_anteriores", "ajuste"]
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
            print(f'Archivo creado: {archivo_proveedores}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {archivo_proveedores}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    @classmethod
    def crear_archivos_eliminaciones(cls,fecha_eliminacion,codigo):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'productos_eliminados.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "proveedor","fecha_eliminacion"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for producto in Producto.lista_productos:
                    if producto.codigo == codigo:
                        writer.writerow({
                            "codigo": producto.codigo,
                            "nombre": producto.nombre,
                            "marca": producto.marca,
                            "precio": producto.precio,
                            "proveedor": producto.proveedor,
                            "fecha_eliminacion": fecha_eliminacion
                        })
            print("Archivo creado correctamente")
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
    def escribir_archivo_csv_productos_principal(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\productos.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'productos.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "proveedor", "tamanio",
                              "fecha_caducidad","entradas","salidas","stock","existencias_anteriores","ajuste"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for producto in Producto.lista_productos:
                    writer.writerow({
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "marca": producto.marca,
                        "precio": int(producto.precio),
                        "proveedor": producto.proveedor,
                        "tamanio": producto.tamanio,
                        "fecha_caducidad": producto.fecha_caducidad,
                        "entradas": producto.entradas,
                        "salidas": producto.salidas,
                        "stock": producto.stock,
                        "existencias_anteriores": producto.existenciasAnteriores,
                        "ajuste": producto.ajuste
                    })
            print("Archivo creado correctamente")
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
    def crear_archivo_csv(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_csv.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'reporte_productos_csv.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "proveedor", "cantidad", "tamanio",
                              "fecha_caducidad"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for producto in Producto.lista_productos:
                    writer.writerow({
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "marca": producto.marca,
                        "precio": producto.precio,
                        "proveedor": producto.proveedor,
                        "cantidad": producto.stock,
                        "tamanio": producto.tamanio,
                        "fecha_caducidad": producto.fecha_caducidad
                    })
            print("Archivo creado correctamente")
            os.startfile(ruta_csv)
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
    def crear_archivo_json(cls):
        #ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_json.json'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'reporte_productos_json.json')
        try:

            lista_productos_json = [
                {
                    "codigo": producto.codigo,
                    "nombre": producto.nombre,
                    "marca": producto.marca,
                    "precio": producto.precio,
                    "proveedor": producto.proveedor,
                    "cantidad": producto.stock,
                    "tamanio": producto.tamanio,
                    "fecha_caducidad": producto.fecha_caducidad
                }
                for producto in Producto.lista_productos
            ]
            json_object = json.dumps(lista_productos_json, indent=4)

            with open(ruta_json, "w", encoding='utf8') as json_file:
                json_file.write(json_object)
            print("Archivo creado correctamente")
            os.startfile(ruta_json)
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
    def crear_archivo_pdf(cls):
        #archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_pdf.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'reporte_productos_pdf.pdf')
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
            fieldnames = ["Código", "Nombre", "Marca", "Precio", "Proveedor", "Cantidad", "Tamanio", "FechaCaducidad"]
            data = [fieldnames]

            for product in Producto.lista_productos:
                data.append([
                    product.codigo,
                    product.nombre,
                    product.marca,
                    product.precio,
                    product.proveedor,
                    product.stock,
                    product.tamanio,
                    product.fecha_caducidad
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
            print("Archivo creado correctamente")
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
    def crear_archivo_xlsx(cls):
        #archivo_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_producto_xlsx.xlsx'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_xlsx = os.path.join(base_dir, 'Archivos', 'Archivos_productos', 'reporte_productos_xlsx.xlsx')
        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Inventario"

            # Escribir encabezados
            encabezados = ["Código", "Nombre", "Marca", "Precio", "Proveedor", "Cantidad", "Tamanio", "FechaCaducidad"]
            sheet.append(encabezados)

            # Escribir datos
            for producto in Producto.lista_productos:
                sheet.append([
                    producto.codigo,
                    producto.nombre,
                    producto.marca,
                    producto.precio,
                    producto.proveedor,
                    producto.stock,
                    producto.tamanio,
                    producto.fecha_caducidad
                ])

            workbook.save(archivo_xlsx)
            print("Archivo creado correctamente")
            os.startfile(archivo_xlsx)
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


    def registrar(self):
        Producto.lista_productos.append(self)
        return True

    @classmethod
    def buscar_nombre(self, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    print("Nombre de producto ya registrado")
                    return True
            return False

    @classmethod
    def buscar_nombre_GUI(self,nombre,id):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre and product.codigo == id:
                    return True
            return False


    @classmethod
    def detalles_nombre(cls, nombre):
        if Producto.lista_productos.__len__() == 0:
            print("no hay productos existentes")
        elif not nombre:
            for product in Producto.lista_productos:
                print("Codigo: ", product.codigo, "Nombre: ", product.nombre, "Marca: ", product.marca, "Proveedor: ",
                      product.proveedor, "Cantidad: ", product.cantidad, "Unidad de medida: ", product.tamanio,
                      "Precio: ", product.precio, "Fecha de caducidad:", product.fecha_caducidad)
            return Producto.lista_productos
        else:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    print("Codigo: ",product.codigo, "Nombre: ",product.nombre, "Marca: ",product.marca, "Proveedor: ", product.proveedor, "Cantidad: ",product.cantidad, "Unidad de medida: ",product.tamanio, "Precio: ",product.precio, "Fecha de caducidad:",product.fecha_caducidad)
                    return Producto.lista_productos
            print("producto no encontrado")

    @classmethod
    def detalles(self):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                print("Codigo: ",product.codigo, "Nombre: ",product.nombre, "Marca: ",product.marca, "Proveedor: ",product.proveedor, "Cantidad: ",product.stock, "Unidad de medida: ",product.tamanio, "Precio: ",product.precio, "Fecha de caducidad:",product.fecha_caducidad)
            return Producto.lista_productos
        else:
            print("No hay registro de productos")

    @classmethod
    def buscarProducto(self, id):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.codigo == id:
                    return product
            return None
        else:
            print("producto no encontrado")

    @classmethod
    def buscar_Producto_Nombre_Proveedor(self, nombre,proveedor,marca):
        for product in Producto.lista_productos:
            if product.nombre == nombre and product.proveedor == proveedor and product.marca == marca:
                return product

    @classmethod
    def actualizar(self, id, nombre, proveedor, tamanio, precio, fecha_caducidad):
        producto = Producto.buscarProducto(id)
        if producto:
            if nombre =="" and proveedor == "" and tamanio == "" and precio == "" and fecha_caducidad == "":
                producto.nombre = producto.nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = producto.tamanio
                producto.precio = producto.precio
                producto.fecha_caducidad = producto.fecha_caducidad
            elif nombre == "":
                producto.nombre = producto.nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio
                producto.fecha_caducidad = fecha_caducidad
            elif proveedor == "":
                producto.nombre = nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = tamanio
                producto.precio = precio
                producto.fecha_caducidad = fecha_caducidad
            elif tamanio == "":
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = producto.tamanio
                producto.precio = precio
                producto.fecha_caducidad = fecha_caducidad
            elif precio == "":
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = producto.precio
                producto.fecha_caducidad = fecha_caducidad
            elif fecha_caducidad == "":
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio
                producto.fecha_caducidad = producto.fecha_caducidad
            else:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio
                producto.fecha_caducidad = fecha_caducidad
            print("Prodcuto actualizado")
        else:
            print("Producto no encontrado")

    @classmethod
    def eliminar_producto(cls, id):
        try:
            producto = cls.buscarProducto(id)
            print(producto)
            if producto:
                Producto.crear_archivos_eliminaciones(datetime.now(),producto.codigo)
                cls.lista_productos.remove(producto)
                print("Producto eliminado con exito.")
                return True
            else:
                print("Producto no encontrado.")
        except Exception as e:
            print("Intentelo nuevamente, no ha sido eliminado")

    @classmethod
    def validar_codigo(cls, codigo):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.codigo == codigo:
                    return True
            return False
        else:
           return False

    @classmethod
    def validar_marca(cls, marca):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.marca == marca:
                    return True
            return False
        else:
            return False

    @classmethod
    def validar_nombre(cls, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    return True
            return False
        else:
            return False

    @classmethod
    def validar_proveedor_prod(cls, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.proveedor == nombre:
                    return True
            return False
        else:
            return False

    @classmethod
    def validar_stock(cls, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    #print(product.stock)
                    return int(product.stock)