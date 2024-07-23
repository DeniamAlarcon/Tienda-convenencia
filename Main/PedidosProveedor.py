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
    @classmethod
    def eliminar_pedidos(cls,id):
        if cls.pedidos.__len__() != 0:
            if cls.buscarID(id):
                cls.pedidos.remove(id)
                return True
            else:
                print("Pedido no encontrado")
        return False