import csv
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook


class Producto:
    lista_productos = []
    def __init__(self ,codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.proveedor = proveedor
        self.cantidad = cantidad
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
        archivo_proveedores = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\productos.csv'
        try:
            with open(archivo_proveedores, encoding='utf8') as archivo_productos:
                reader = csv.DictReader(archivo_productos)
                filas = list(reader)
                if not filas or all(not any(row.values()) for row in filas):
                    print('No hay datos que leer')
                    return
                for row in filas:
                    producto = Producto(
                        row["codigo"],
                        row["nombre"],
                        row["marca"],
                        row["proveedor"],
                        row["cantidad"],
                        row["unidad_medida"],
                        row["precio"],
                        row["fecha_caducidad"]
                    )
                    Producto.lista_productos.append(producto)
                    producto.entradas = row["entradas"]
                    producto.salidas = row["salidas"]
                    producto.stock = row["stock"]
                    producto.existenciasAnteriores = row["existencias_anteriores"]
                    producto.ajuste = row["ajuste"]
            print("Archivo creado correctamente")
        except csv.Error as e:
            print(f'Error al leer el archivo CSV')

    @classmethod
    def crear_archivo_csv(cls):
        ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_csv.csv'
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
                        "cantidad": producto.cantidad,
                        "tamanio": producto.tamanio,
                        "fecha_caducidad": producto.fecha_caducidad
                    })
            print("Archivo creado correctamente")
        except PermissionError:
            print(f"Error al crear o escribir el archivo CSV")

    @classmethod
    def crear_archivo_json(cls):
        ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_json.json'

        try:
            lista_productos_json = [
                {
                    "codigo": producto.codigo,
                    "nombre": producto.nombre,
                    "marca": producto.marca,
                    "precio": producto.precio,
                    "proveedor": producto.proveedor,
                    "cantidad": producto.cantidad,
                    "tamanio": producto.tamanio,
                    "fecha_caducidad": producto.fecha_caducidad
                }
                for producto in Producto.lista_productos
            ]
            json_object = json.dumps(lista_productos_json, indent=4)

            with open(ruta_json, "w", encoding='utf8') as json_file:
                json_file.write(json_object)
            print("Archivo creado correctamente")
        except Exception as e:
            print(f"Error al crear o escribir el archivo JSON: ")

    @classmethod
    def crear_archivo_pdf(cls):
        archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_productos_pdf.pdf'

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
                    product.cantidad,
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
        except Exception as e:
            print(f"Error al crear o escribir el archivo PDF")

    @classmethod
    def crear_archivo_xlsx(cls):
        archivo_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_productos\\reporte_producto_xlsx.xlsx'

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
                    producto.cantidad,
                    producto.tamanio,
                    producto.fecha_caducidad
                ])

            workbook.save(archivo_xlsx)
            print("Archivo creado correctamente")
        except Exception as e:
            print(f"Error al crear o escribor el archivo XLSX")


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
                print("Codigo: ",product.codigo, "Nombre: ",product.nombre, "Marca: ",product.marca, "Proveedor: ",product.proveedor, "Cantidad: ",product.cantidad, "Unidad de medida: ",product.tamanio, "Precio: ",product.precio, "Fecha de caducidad:",product.fecha_caducidad)
            return Producto.lista_productos
        else:
            print("No hay registro de productos")

    @classmethod
    def buscarProducto(self, id):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.codigo == id:
                    return product
        else:
            print("producto no encontrado")

    @classmethod
    def buscarProductoNombre(self, nombre):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                return product

    @classmethod
    def buscarProductoMarca(self, marca):
        for product in Producto.lista_productos:
            if product.marca == marca:
                return product


    @classmethod
    def actualizar(self, id, nombre, proveedor, tamanio, precio):
        producto = self.buscarProducto(id)
        if producto:
            if not nombre and not proveedor and not tamanio and not precio:
                producto.nombre = producto.nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = producto.tamanio
                producto.precio = producto.precio
            elif not nombre:
                producto.nombre = producto.nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio
            elif not proveedor:
                producto.nombre = nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = tamanio
                producto.precio = precio
            elif not tamanio:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = producto.tamanio
                producto.precio = precio
            elif not precio:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = producto.precio
            else:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio

            print("Prodcuto actualizado")
        else:
            print("Producto no encontrado")

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
    def validar_stock(cls, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    #print(product.stock)
                    return int(product.stock)