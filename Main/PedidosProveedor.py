
class PedidosProveedor:
    idAuto=0
    pedidos = []

    def __init__(self, proveedor, nombre, marca, cantidad):
        PedidosProveedor.idAuto += 1
        self.id = PedidosProveedor.idAuto
        self.proveedor = proveedor
        self.nombre = nombre
        self.marca = marca
        self.cantidad = cantidad

    def guardar(self):
        PedidosProveedor.pedidos.append(self)

    @classmethod
    def mostrar_pedidos(cls):
        if not cls.pedidos:
            print("No hay pedidos guardados.")
        else:
            for pedido in cls.pedidos:
                print(
                    f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad}")

    @classmethod
    def pedidos_proveedor(self,proveedor):
        if not self.pedidos:
            print("No hay pedidos guardados con este proveedor.")
        else:
            for pedido in self.pedidos:
                if pedido.proveedor == proveedor:
                    print(
                        f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad}")
                else:
                    print("Pedido no encontrado")

    @classmethod
    def pedidos_proveedorID(self, i,cantidad):
        if not self.pedidos:
            print("No hay pedidos guardados con este proveedor.")
        else:
            for pedido in self.pedidos:
                if pedido.nombre == i:
                    print(
                        f"ID: {pedido.id}, Proveedor: {pedido.proveedor}, Nombre: {pedido.nombre}, Marca: {pedido.marca}, Cantidad: {pedido.cantidad}")
                    if int(pedido.cantidad) < int(cantidad):
                        print("Se exedio la cantidad de producto")
                    elif int(pedido.cantidad) > int(cantidad):
                        print("Entrega Incompleta")
                    else:
                        print("Entrega correcta")
                else:
                    print("Pedido no encontrado")


