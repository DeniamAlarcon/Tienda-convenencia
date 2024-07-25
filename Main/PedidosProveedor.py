import csv
import os

from Main.Inventario import *
from datetime import datetime
from tkinter import messagebox

class PedidosProveedor:
    idAuto=0
    estatus=""
    pedidos = []

    def __init__(self, proveedor, nombre, marca, cantidad, precio):
        PedidosProveedor.idAuto += 1
        self.id = PedidosProveedor.idAuto
        self.proveedor = proveedor
        self.nombre = nombre
        self.marca = marca
        self.cantidad = cantidad
        self.precio = precio
        self.estatus = PedidosProveedor.estatus="Pendiente"

    @classmethod
    def leer_archivo(cls):
        #archivo_compras = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_compras\\compras.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_compras = os.path.join(base_dir, 'Archivos', 'Archivos_compras', 'compras.csv')
        try:
            with open(archivo_compras, encoding='utf8') as archivo:
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
            PedidosProveedor.idAuto = max_id + 1

            # Leer datos y crear objetos Proveedores
            for row in filas:
                compras = cls(row["proveedor"], row["nombre"], row["marca"], row["cantidad"], row["precio"])
                compras.id = int(row["id"])  # Asignar el ID del archivo
                compras.estatus = row["estatus"]
                cls.pedidos.append(compras)
            print('Datos cargados exitosamente.')
        except FileNotFoundError:
            print(f'Archivo no encontrado: {archivo_compras}. Creando archivo nuevo...')
            os.makedirs(os.path.dirname(archivo_compras), exist_ok=True)
            with open(archivo_compras, mode='w', newline='', encoding='utf8') as archivo:
                fieldnames = ["id", "proveedor", "nombre", "marca", "cantidad", "precio", "estatus"]
                writer = csv.DictWriter(archivo, fieldnames=fieldnames)
                writer.writeheader()
            print(f'Archivo creado: {archivo_compras}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {archivo_compras}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')
    @classmethod
    def escribir_archivo_csv_principal_compras(cls):
        #ruta_csv = 'C:\\Users\\Deniam\\OneDrive\\Documentos\\GitHub\\Tienda-convenencia\\Archivos\\Archivos_compras\\compras.csv'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(base_dir, 'Archivos', 'Archivos_compras', 'compras.csv')
        try:
            with open(ruta_csv, mode="w", encoding='utf8', newline='') as archivo_csv:
                fieldnames = ["id", "proveedor", "nombre", "marca", "cantidad", "precio","estatus"]
                writer = csv.DictWriter(archivo_csv, fieldnames=fieldnames)
                writer.writeheader()

                for compras in PedidosProveedor.pedidos:
                    writer.writerow({
                        "id": compras.id,
                        "proveedor": compras.proveedor,
                        "nombre": compras.nombre,
                        "marca": compras.marca,
                        "cantidad": compras.cantidad,
                        "precio": compras.precio,
                        "status": compras.estatus
                    })
        except FileNotFoundError:
            print(f'Archivo no encontrado: {ruta_csv}')
        except IOError:
            print(f'Error de entrada/salida al intentar abrir el archivo: {ruta_csv}')
        except KeyError as e:
            print(f'Llave no encontrada en los datos del archivo: {e}')
        except ValueError as e:
            print(f'Valor incorrecto encontrado en los datos del archivo: {e}')
        except Exception as e:
            print(f'Ocurrió un error inesperado: {e}')

    def guardar(self):
        PedidosProveedor.pedidos.append(self)
        return True

    @classmethod
    def mostrar_pedidos(cls):
        if not cls.pedidos:
            print("No hay pedidos guardados.")
        else:
            for pedido in cls.pedidos:
                print(
                    f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad},Precio de Compra: {pedido.precio}, Estatus: {pedido.estatus}")
            return cls.pedidos

    @classmethod
    def pedidos_proveedor(self,proveedor):
        if not self.pedidos:
            print("No hay pedidos guardados con este proveedor.")
        else:
            for pedido in self.pedidos:
                if pedido.proveedor == proveedor:
                    print(
                        f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad}, Precio de Compra: {pedido.precio},  Estatus: {pedido.estatus}")

            return self.pedidos

    @classmethod
    def actualizar_estatus_a_entregado(cls, idp):
        pedido = cls.buscarID(idp)
        if pedido:
            pedido.estatus = "Entregado"
            print(f"Estatus del pedido ID {idp} actualizado a 'Entregado'.")
        else:
            print("Pedido no encontrado")

    @classmethod
    def pedidos_proveedorID(self, idp,cantidad):
        if not self.pedidos:
            messagebox.showerror("Error","No hay pedidos guardados con este proveedor.")
        else:
            for pedido in self.pedidos:
                if pedido.id == int(idp):
                    if pedido.estatus=="Pendiente":
                        print(
                            f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad},Precio de Compra: {pedido.precio},  Estatus: {pedido.estatus}")

                        if int(pedido.cantidad) < int(cantidad):
                             messagebox.showerror("Eroro","Se exedio la cantidad de producto")
                        elif int(pedido.cantidad) > int(cantidad):
                            messagebox.showerror("Error","Entrega Incompleta")
                        else:
                            inventario = Inventario()
                            inventario.actualizarEntradas(pedido.nombre, cantidad)
                            PedidosProveedor.actualizar_estatus_a_entregado(int(idp))
                            Producto.escribir_archivo_csv_productos_principal()
                            PedidosProveedor.escribir_archivo_csv_principal_compras()
                            messagebox.showinfo("Éxito","Entrega completa")
                        return True
                    else:
                        messagebox.showerror("Error","No existen pedidos pendientes para validar")
                else:
                    messagebox.showerror("Error","Pedido no encontrado con este ID")

    @classmethod
    def buscarID(self,idp):
        for pedido in self.pedidos:
            if pedido.id == idp:
                return pedido
        return
