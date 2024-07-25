from Main.Productos import *
from Main.Inventario import *

class VentasMain:
    lista_ventas= []
    lista_venta_actual =[]

    @classmethod
    def total_venta_actual(self, nombre, cantidad):
        for procuto in Producto.lista_productos:
            if procuto.nombre == nombre:
                cantidad = int(cantidad) + (int(cantidad) * int(procuto.precio))
        return cantidad





