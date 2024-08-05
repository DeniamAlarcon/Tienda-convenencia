import csv
import json
import os
import re
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
from openpyxl import Workbook
from datetime import datetime

from Main.Productos import Producto


class Proveedores:
    idAuto=1
    proveedores = []
    def __init__(self,nombre,correo,telefono):
        self.id = Proveedores.idAuto
        self.nombre=nombre
        self.correo=correo
        self.telefono=telefono
        # expeciones

    @classmethod
    def leer_archivo(cls):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_proveedores = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'proveedores.csv')

        ids_procesados = set()
        nombres_procesados = set()
        correos_procesados = set()
        telefonos_procesados = set()

        try:
            with open(archivo_proveedores, encoding='utf8') as archivo:
                reader = csv.DictReader(archivo)
                filas = list(reader)

                if not filas:
                    print('No hay datos que leer.')
                    return

            # Encontrar el ID máximo en el archivo
            max_id = 0
            for row in filas:
                if row["id"].isdigit():
                    id_sin_ceros = str(int(row["id"]))  # Convertir el ID para eliminar ceros a la izquierda
                    max_id = max(max_id, int(id_sin_ceros))

            # Configurar idAuto para continuar desde el ID máximo encontrado
            Proveedores.idAuto = max_id + 1

            # Leer datos y crear objetos Proveedores
            for row in filas:
                if all(row.values()):
                    id_original = row["id"]
                    id_sin_ceros = str(int(id_original))  # Convertir el ID para eliminar ceros a la izquierda
                    nombre = row["nombre"]
                    correo = row["correo"]
                    telefono = row["telefono"]

                    # Validar que el ID no tenga ceros a la izquierda
                    if id_original != id_sin_ceros:
                        print(f'ID con ceros a la izquierda ignorado: {id_original} en la fila {row}')
                        continue

                    # Validar que los campos sean únicos
                    if id_sin_ceros in ids_procesados or nombre in nombres_procesados or correo in correos_procesados or telefono in telefonos_procesados:
                        print(f'Fila ignorada por duplicado: {row}')
                        continue

                    # Validar el número de teléfono
                    if not telefono.isdigit() or not (10 <= len(telefono) <= 15):
                        print(f'Número de teléfono inválido: {telefono} en la fila {row}')
                        continue

                    # Validar el formato del correo
                    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$', correo):
                        print(f'Correo inválido: {correo} en la fila {row}')
                        continue

                    proveedor = cls(nombre, correo, telefono)
                    proveedor.id = int(id_sin_ceros)  # Asignar el ID del archivo sin ceros a la izquierda
                    cls.proveedores.append(proveedor)

                    # Añadir a los conjuntos de procesados
                    ids_procesados.add(id_sin_ceros)
                    nombres_procesados.add(nombre)
                    correos_procesados.add(correo)
                    telefonos_procesados.add(telefono)

            print('Datos cargados exitosamente.')

        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_proveedores}. Creando archivo nuevo...')
            os.makedirs(os.path.dirname(archivo_proveedores), exist_ok=True)
            with open(archivo_proveedores, mode='w', newline='', encoding='utf8') as archivo:
                fieldnames = ["id", "nombre", "correo", "telefono"]
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
    def crear_archivos_eliminaciones(cls, fecha_eliminacion, id2):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'proveedores_eliminados.csv')
        try:
            with open(ruta_csv, mode="a", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["id", "nombre", "correo", "telefono","fecha_eliminacion"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for proveedor in Proveedores.proveedores:
                    if proveedor.id == id2:
                        writer.writerow({
                            "id": proveedor.id,
                            "nombre": proveedor.nombre,
                            "correo": proveedor.correo,
                            "telefono": proveedor.telefono,
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
    def escribir_archivo_csv_principal(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\proveedores.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'proveedores.csv')
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
    def escribir_archivo_csv(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_csv.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'reporte_proveedores_csv.csv')
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
    def escribir_archivo_json(cls):
        #ruta_json = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_json.json'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'reporte_proveedores_json.json')
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
    def escribir_archivo_pdf(cls):
        #archivo_pdf = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_pdf.pdf'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_pdf = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'reporte_proveedores_pdf.pdf')
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
    def escribir_archivo_xlsx(cls):
        #archivo_xlsx = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_proveedores\\reporte_proveedores_xlsx.xlsx'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_xlsx = os.path.join(base_dir, 'Archivos', 'Archivos_proveedores', 'reporte_proveedores_xlsx.xlsx')
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

    def guardar(self):
        Proveedores.idAuto += 1
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

    #Actualizacion en GUI
    @classmethod
    def actualizarGUI(cls, id, nom, correo, telefono):
        buscar=cls.actualizarGUI_Validar(id,nom,correo,telefono)
        print(buscar)
        if buscar:
            for proveedor in cls.proveedores:
                if proveedor.nombre == id:
                    if nom == proveedor.nombre and correo == proveedor.correo and telefono == proveedor.telefono:
                        proveedor.nombre = proveedor.nombre
                        proveedor.correo = proveedor.correo
                        proveedor.telefono = proveedor.telefono
                    elif nom == proveedor.nombre:
                        proveedor.nombre = proveedor.nombre
                        proveedor.correo = correo
                        proveedor.telefono = telefono
                    elif correo == proveedor.correo:
                        proveedor.correo = proveedor.correo
                        for producto in Producto.lista_productos:
                            if producto.proveedor==proveedor.nombre:
                                producto.proveedor=nom
                        proveedor.nombre = nom
                        proveedor.telefono = telefono
                    elif telefono == proveedor.telefono:
                        proveedor.telefono = proveedor.telefono
                        for producto in Producto.lista_productos:
                            if producto.proveedor==proveedor.nombre:
                                producto.proveedor=nom
                        proveedor.nombre = nom
                        proveedor.correo = correo
                    else:
                        for producto in Producto.lista_productos:
                            if producto.proveedor==proveedor.nombre:
                                producto.proveedor=nom
                        proveedor.nombre = nom
                        proveedor.correo = correo
                        proveedor.telefono = telefono
                    messagebox.showinfo("Exito","Proveedor actualizado correctamente")
        else:
            messagebox.showerror("Error","Proveedor ya registrado con esos datos.")

    @classmethod
    def actualizar(cls, id, nombre, correo, telefono):
        proveedor = cls.buscar_nombre_valida(id)
        if proveedor:
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
                messagebox.showinfo("Exito","Proveedor actualizado correctamente")
        else:
            print("Proveedor no encontrado.")
    #No agregado al diagrama de clases
    @classmethod
    def actualizarGUI_ValidarN(cls, nom, nomb):
        if Proveedores.proveedores.__len__()!=0:
            for prov in Proveedores.proveedores:
                if prov.nombre == nom and prov.nombre==nomb:
                    return True
            return False

    @classmethod
    def actualizarGUI_ValidarC(cls, nom, correo):
        if Proveedores.proveedores.__len__() != 0:
            for prov in Proveedores.proveedores:
                if prov.nombre == nom and prov.correo==correo:
                    return True
            return False

    @classmethod
    def actualizarGUI_ValidarT(cls, nom, telefono):
        if Proveedores.proveedores.__len__() != 0:
            for prov in Proveedores.proveedores:
                if prov.nombre == nom and prov.telefono == telefono:
                    return True
            return False

    @classmethod
    def buscar_nombre(self, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Proveedores.proveedores:
                if product.nombre == nombre:
                    print("Nombre de producto ya registrado")
                    return True
            return False

    @classmethod
    def buscar_correo(self, correo):
        if Producto.lista_productos.__len__() != 0:
            for product in Proveedores.proveedores:
                if product.correo == correo:
                    print("Nombre de producto ya registrado")
                    return True
            return False

    @classmethod
    def buscar_telefono(self, telefono):
        if Producto.lista_productos.__len__() != 0:
            for product in Proveedores.proveedores:
                if product.telefono == telefono:
                    print("Nombre de producto ya registrado")
                    return True
            return False

    @classmethod
    def buscar_nombre_valida(self, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Proveedores.proveedores:
                if product.nombre == nombre:
                    return product
            return False

    @classmethod
    def actualizarGUI_verificar(cls, nom, correo, telefono):
        for prov in cls.proveedores:
            if (prov.nombre) != (nom) and prov.telefono != telefono and prov.correo != correo:
                return True
            else:
                return False

    @classmethod
    def eliminarProveedor(cls, id):
        try:
            proveedor = cls.buscar_proveedor(id)
            nom = proveedor.nombre
            if proveedor:
                validacion = Producto.validar_proveedor_prod(nom)
                if not validacion:
                    Proveedores.crear_archivos_eliminaciones(datetime.now(), proveedor.id)
                    cls.proveedores.remove(proveedor)
                    print("Proveedor eliminado con exito.")
                    return True
                else:
                    messagebox.showerror("Error", "Existen productos relacionados con este proveedor")
            else:
                messagebox.showerror("Error", "Proveedor no encontrado")
        except Exception as e:
            print("Intentelo nuevamente, no ha sido eliminado")

    @classmethod
    def comprobarExistencia(self,nombre,correo,telefono):
        for proveedor in Proveedores.proveedores:
            if proveedor.nombre==nombre or proveedor.correo==correo or  proveedor.telefono==telefono:
                return True
        return False

    @classmethod
    def validar_provedor(cls,nombre):
        if Proveedores.proveedores.__len__() != 0:
            for proveedor in Proveedores.proveedores:
                if proveedor.nombre == nombre:
                    return True
            print("Proveedor no encontrado.")
        else:
            print("No hay proveedores registrado.")
