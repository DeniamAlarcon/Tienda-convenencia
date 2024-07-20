import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
from Productos import *
from Proveedores import *
from datetime import datetime

class Inventario:
    def __init__(self):
        self.producto = Producto.lista_productos
        self.proveedor = Proveedores.proveedores

    def escribir_archivo_csv(self):
        ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.csv'
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "proveedor", "entradas", "salidas", "stock",
                              "existencias_anteriores", "ajuste"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for producto in self.producto:
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
        except PermissionError:
            print(f"Error al crear o escribir el archivo CSV")

    def escribir_archivo_json(self):
        ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.json'

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
                for producto in self.producto
            ]
            json_object = json.dumps(lista_productos_json, indent=4)

            with open(ruta_json, "w", encoding='utf8') as json_file:
                json_file.write(json_object)

        except Exception as e:
            print(f"Error al crear o escribir el archivo JSON: ")

    def escribir_archivo_pdf(self):
        archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.pdf'

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

            for product in self.producto:
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
        except Exception as e:
            print(f"Error al crear o escribir el archivo PDF")

    def escribir_archivo_xlsx(self):
        archivo_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_inventarios\\reporte_inventario.xlsx'

        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Inventario"

            # Escribir encabezados
            encabezados = ["codigo", "nombre", "marca", "precio", "proveedor", "entradas", "salidas", "stock",
                           "existencias_anteriores", "ajuste"]
            sheet.append(encabezados)

            # Escribir datos
            for producto in self.productos:
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
        except Exception as e:
            print(f"Error al crear o escribor el archivo XLSX")

    def menu_archivos(self):
        while True:
            print("1. Crear archivo CSV")
            print("2. Crear archivo JSON")
            print("3. Crear archivo PDF")
            print("4. Crear archivo XLSX")
            print("5 Salir")
            opcion = input("Seleccione una opcion")
            if opcion == "1":
                Inventario.escribir_archivo_csv(self)
            elif opcion == "2":
                Inventario.escribir_archivo_json(self)
            elif opcion == "3":
                Inventario.escribir_archivo_pdf(self)
            elif opcion == "4":
                Inventario.escribir_archivo_xlsx(self)
            elif opcion == "5":
                break

    def obtenerInventario(self):
        if self.proveedor:
            if self.producto:
                while True:
                    print("Desea crear un archivo del informe de inventario?")
                    print("1. Si")
                    print("2. No")
                    opcion = input("Seleccione una opcion")
                    if opcion == "1":
                        Inventario.menu_archivos(self)
                        break
                    elif opcion == "2":
                        break
                print("INFORME DE INVENTARIO CREADO EL: ", datetime.now())
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Proveedor':<20} {'Entradas':<10} {'Salidas':<10} {'Stock':<10} {'Existencias_anteriores'} {'Ajustes':<10}")
                print("=" * 105)
                for product in self.producto:
                    # Imprimir cada producto con su información formateada en columnas
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.proveedor:<20} {product.entradas:<10} {product.salidas:<10} {product.stock:<10} {product.existenciasAnteriores} {product.ajuste:<10}")
                    product.entradas=0
                    product.salidas=0
                    product.ajuste=0
                    print("=" * 105)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')


    @classmethod
    def mensajes_stock(self,nombre):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                if int(product.stock) < 5 and int(product.stock) >0:
                    print("Stock bajo de ",product.nombre)
                elif int(product.stock) == 0:
                    print("No hay stock de ",product.nombre)

    def actualizarEntradas(self,nombre, cantidad):
        for product in self.producto:
            if product.nombre == nombre:
                product.entradas = int(product.entradas) + int(cantidad)
                product.stock = int(product.stock) + int(cantidad)
                Inventario.mensajes_stock(nombre)



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
            else:
                print("Producto no encontrado")
                return False

    def escribir_archivo_stock_csv(self):
        ruta_csv = 'D:\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.csv'
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["codigo", "nombre", "marca", "precio", "stock"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()
                for producto in self.producto:
                    writer.writerow({
                        "codigo": producto.codigo,
                        "nombre": producto.nombre,
                        "marca": producto.marca,
                        "precio": producto.precio,
                        "stock": producto.stock
                    })
        except PermissionError:
            print(f"Error al crear o escribir el archivo CSV")

    def escribir_archivo_stock_pdf(self):
        archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.pdf'

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

            for producto in self.producto:
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
        except Exception as e:
            print(f"Error al crear o escribir el archivo PDF")

    def escribir_archivo_stock_json(cls):
        ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.json'
        lista_productos_json = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "marca": producto.marca,
                "precio": producto.precio,
                "stock": producto.stock
            }
            for producto in cls.producto
        ]

        try:
            with open(ruta_json, "w", encoding='utf8') as archivo_json:
                json.dump(lista_productos_json, archivo_json, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"Error al crear o escribir el archivo JSON")

    def escribir_archivo_stock_xlsx(cls):
        ruta_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_Stock\\reporte_stock.xlsx'
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Stock"

        # Escribir encabezados
        encabezados = ["codigo", "nombre", "marca", "precio", "stock"]
        sheet.append(encabezados)

        # Escribir datos
        for producto in cls.producto:
            sheet.append([
                producto.codigo,
                producto.nombre,
                producto.marca,
                producto.precio,
                producto.stock
            ])

        try:
            workbook.save(ruta_xlsx)
        except PermissionError:
            print(f"Error al crear o escribir el archivo xlsx")

    def informeStock(self):
        if self.producto:
            if self.proveedor:
                Inventario.escribir_archivo_stock_csv(self)
                Inventario.escribir_archivo_stock_json(self)
                Inventario.escribir_archivo_stock_pdf(self)
                Inventario.escribir_archivo_stock_xlsx(self)
                print("INFORME DE STOCK DISPONIBLE")
                print(f"{'Código':<10} {'Nombre':<20} {'Marca':<15} {'Precio':<10} {'Stock':<10}")
                print("=" * 105)
                for product in self.producto:
                    print(f"{product.codigo:<10} {product.nombre:<20} {product.marca:<15} {product.precio:<10} {product.stock:<10}")
                print("=" * 105)
                for product in self.producto:
                    Inventario.mensajes_stock(product.nombre)
            else:
                print('No hay proveedores registrados')
        else:
            print('No hay productos registrados')

    def calculoAjuste(self,cantidad,nombre,precio):
        for product in self.producto:
            if product.nombre == nombre:
                total_reponer = int(cantidad)*int(precio)
                print("Ajuste realizada")
                print("Total a reponer: ",total_reponer)
                product.ajuste = cantidad

    def ajuste_inventario(self):
        if self.proveedor:
            if self.producto:
                nombre = ""
                while not nombre:
                    nombre = input("Ingrese el nombre del producto: ")
                    if nombre:
                        if not Producto.validar_nombre(nombre):
                            print("El nombre del producto no existe")
                            nombre = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                cantidad = ""
                while not cantidad:
                    cantidad = input("Ingrese la cantidad de producto dañado: ")
                    if cantidad:
                        if cantidad.isdigit():
                            if int(cantidad) < Producto.validar_stock(nombre):
                                if int(cantidad) < 0:
                                    print("Ingrese una cantidad mayor a 0")
                                    cantidad = ""
                                else:
                                    cantidad = int(cantidad)
                            else:
                                print("La cantidad ingresada excede el stock")
                                cantidad = ""
                        else:
                            print("Favor de ingresar el dato numerico")
                            cantidad = ""
                    else:
                        print("Favor de ingresar el dato requerido")

                precio = ""
                while not precio:
                    try:
                        precio = input("Ingrese el precio del producto: ")
                        if precio:
                            if int(precio) < 0:
                                print("Ingrese una precio mayor a 0")
                                precio = ""
                            else:
                                Inventario.calculoAjuste(self, cantidad, nombre, precio)
                                Inventario.actualizarSalidas(nombre, cantidad)
                        else:
                            print("Favor de ingresar el dato requerido")
                    except ValueError:
                        print("Precio no valido")
            else:
                print('No hay productos registrados')
        else:
            print('No hay proveedores registrados')

    def fechas_caducidad(self):
        formato = "%d/%m/%Y"
        for product in self.producto:
            fecha_caducidad = datetime.strptime(product.fecha_caducidad,formato)
            fecha_actual = datetime.now().date()
            diferencia_dias = (fecha_caducidad - fecha_actual).days
            if diferencia_dias <= 10:
                if diferencia_dias <= 2:
                    print("Realizar cambio de: ", product.nombre)
                else:
                    print(product.nombre, " Proximo a caducar")



def menuInventario():
    inventario = Inventario()
    while True:
        print("1. Generacion de informe de inventario")
        print("2. Generacion de stock")
        print("3. Ajuste de inventario(robos,perdidas,daños)")
        print("4  Revision fechas caducidad")
        print("5. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            inventario.obtenerInventario()
        elif opcion == "2":
            inventario.informeStock()
        elif opcion == "3":
            inventario.ajuste_inventario()
            while True:
                print("1. Ingresar otro ajuste")
                print("2. Salir")
                opcion1 = input("Ingrese una opcion: ")
                if opcion1 == "1":
                    inventario.ajuste_inventario()
                elif opcion1 == "2":
                    break
        elif opcion == "4":
            inventario.fechas_caducidad()
        elif opcion == "5":
            break

