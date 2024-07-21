import csv
import json

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
class Proveedores:
    idAuto=0
    proveedores = []
    def __init__(self,nombre,correo,telefono):
        Proveedores.idAuto+=1
        self.id = Proveedores.idAuto
        self.nombre=nombre
        self.correo=correo
        self.telefono=telefono

    @classmethod
    def leer_archivo(cls):
        archivo_proveedores = 'D:\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\proveedores.csv'
        try:

            with open(archivo_proveedores, encoding='utf8') as archivo:
                reader = csv.DictReader(archivo)
                filas = list(reader)

                if not filas or all(not any(row.values()) for row in filas):
                    print('No hay datos que leer.')
                    return

            # Encontrar el ID máximo en el archivo
            max_id = 0
            for row in filas:
                if row["id"].isdigit():
                    max_id = max(max_id, int(row["id"]))

            # Configurar idAuto para continuar desde el ID máximo encontrado
            Proveedores.idAuto = max_id + 1

            # Leer datos y crear objetos Proveedores
            for row in filas:
                proveedor = cls(row["nombre"], row["correo"], row["telefono"])
                proveedor.id = int(row["id"])  # Asignar el ID del archivo
                cls.proveedores.append(proveedor)
            print('Datos cargados exitosamente.')
        except csv.Error as e:
            print(f'Error al leer el archivo CSV: {e}')

    @classmethod
    def escribir_archivo_csv(cls):
        ruta_csv = 'D:\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_csv.csv'
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["id", "nombre", "correo", "telefono"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for proveedor in Proveedores.proveedores:
                    writer.writerow({
                        "id": proveedor.id,
                        "nombre": proveedor.nombre,
                        "correo": proveedor.correo,
                        "telefono": proveedor.telefono
                    })
        except PermissionError:
            print(f"Error al crear o escribir el archivo CSV")

    @classmethod
    def escribir_archivo_json(cls):
        ruta_json = 'D:\\Tienda-convenencia\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_json.json'

        try:
            lista_proveedores_json = [
                {
                    "id": proveedor.id,
                    "nombre": proveedor.nombre,
                    "correo": proveedor.correo,
                    "telefono": proveedor.telefono
                }
                for proveedor in Proveedores.proveedores
            ]
            json_object = json.dumps(lista_proveedores_json, indent=4)

            with open(ruta_json, "w", encoding='utf8') as json_file:
                json_file.write(json_object)

        except Exception as e:
            print(f"Error al crear o escribir el archivo JSON: ")

    @classmethod
    def escribir_archivo_pdf(cls):
        archivo_pdf = 'D:\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_pdf.pdf'
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
            fieldnames = ["Id", "Nombre", "Correo", "Telefono"]
            data = [fieldnames]

            for proveedor in Proveedores.proveedores:
                data.append([
                    proveedor.id,
                    proveedor.nombre,
                    proveedor.correo,
                    proveedor.telefono
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

    @classmethod
    def escribir_archivo_xlsx(cls):
        archivo_xlsx = 'D:\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_xlsx.xlsx'

        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Proveedores"

            # Escribir encabezados
            encabezados = ["Id", "Nombre", "Correo", "Telefono"]
            sheet.append(encabezados)

            # Escribir datos
            for proveedor in Proveedores.proveedores:
                sheet.append([
                    proveedor.id,
                    proveedor.nombre,
                    proveedor.correo,
                    proveedor.telefono
                ])

            workbook.save(archivo_xlsx)
        except Exception as e:
            print(f"Error al crear o escribor el archivo XLSX")

    def guardar(self):
        Proveedores.proveedores.append(self)
        return True

    @classmethod
    def mostrar(cls):
        if not cls.proveedores:
            print("No hay proveedores registrados")
        else:
            for proveedor in cls.proveedores:
               print(
                f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")
            return cls.proveedores

    @classmethod
    def mostrar_nombre(cls,nomb):
        if not cls.proveedores:
            print("No hay proveedores")
        else:
            for proveedor in cls.proveedores:
                if nomb == proveedor.nombre:
                    print(
                        f"ID: {proveedor.id}, Nombre: {proveedor.nombre}, Correo: {proveedor.correo}, Teléfono: {proveedor.telefono}")
                    return Proveedores.proveedores



    @classmethod
    def buscar_proveedor(cls, id2):
        for proveedor in cls.proveedores:
            if proveedor.id == id2:
                return proveedor
        return None
    @classmethod
    def actualizar(cls,id,nombre,correo,telefono):
        proveedor = cls.buscar_proveedor(id)
        if proveedor:
            if Proveedores.comprobarExistencia(nombre,correo,telefono):
                print("Ya existe un proveedor con esos datos")
            else:
                if nombre == "" and correo == "" and telefono == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = proveedor.correo
                    proveedor.telefono = proveedor.telefono
                elif nombre == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = correo
                    proveedor.telefono = telefono
                elif correo == "":
                    proveedor.correo = proveedor.correo
                    proveedor.nombre = nombre
                    proveedor.telefono = telefono
                elif telefono == "":
                    proveedor.telefono = proveedor.telefono
                    proveedor.nombre = nombre
                    proveedor.correo = correo
                else:
                    proveedor.nombre = nombre
                    proveedor.correo = correo
                    proveedor.telefono = telefono
                print("Proveedor actualizado exitosamente.")
        else:
            print("Proveedor no encontrado.")

    @classmethod
    def actualizarGUI(cls, id, nom, correo, telefono):
        #proveedor = cls.mostrar_nombre(id)
        for proveedor in cls.proveedores:
            if proveedor.nombre == id:
                if nom == "" and correo == "" and telefono == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = proveedor.correo
                    proveedor.telefono = proveedor.telefono
                elif nom == "":
                    proveedor.nombre = proveedor.nombre
                    proveedor.correo = correo
                    proveedor.telefono = telefono
                elif correo == "":
                    proveedor.correo = proveedor.correo
                    proveedor.nombre = nom
                    proveedor.telefono = telefono
                elif telefono == "":
                    proveedor.telefono = proveedor.telefono
                    proveedor.nombre = nom
                    proveedor.correo = correo
                else:
                    proveedor.nombre = nom
                    proveedor.correo = correo
                    proveedor.telefono = telefono

    @classmethod
    def eliminarProveedor(cls, id):
        try:
            proveedor = cls.buscar_proveedor(id)
            if proveedor:
                cls.proveedores.remove(proveedor)
                print("Proveedor eliminado con exito.")
                return True
            else:
                print("Proveedor no encontrado.")
        except Exception as e:
            print("Intentelo nuevamente, no ha sido eliminado")
    @classmethod
    def comprobarExistencia(self,nombre,correo,telefono):
        for proveedor in Proveedores.proveedores:
            if proveedor.nombre==nombre or proveedor.correo==correo or  proveedor.telefono==telefono:
                return True

    @classmethod
    def validar_provedor(cls,nombre):
        if Proveedores.proveedores.__len__() != 0:
            for proveedor in Proveedores.proveedores:
                if proveedor.nombre == nombre:
                    return True
                else:
                    print("Proveedor no encontrado.")
        else:
            print("No hay proveedores registrado.")

    @classmethod
    def mandar_proveedores(cls):
        if Proveedores.proveedores.__len__() != 0:
            return Proveedores.proveedores
        else:
            return None