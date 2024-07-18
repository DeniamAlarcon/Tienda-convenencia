from Productos import *
from Inventario import *

class VentasMain:
    lista_ventas= []
    lista_venta_actual =[]
    def __init__(self,cantidad, nombre):
        self.cantidad = cantidad
        self.nombre = nombre


    def guardar_venta(self):
        VentasMain.lista_ventas.append(self)
        VentasMain.lista_venta_actual.clear()
        return True

    @classmethod
    def total_venta_actual(self, nombre, cantidad):
        for procuto in Producto.lista_productos:
            if procuto.nombre == nombre:
                cantidad = int(cantidad) + (int(cantidad) * int(procuto.precio))
        return cantidad

    def venta_actual(self):
        VentasMain.lista_venta_actual.append(self)
        return VentasMain.lista_venta_actual


    def generar_reporte(self):
        for producto in self.productos:
            print("reporte")

    def corteCaja(self):
        total = 0
        VentasMain.generar_reporte(self)
        for venta in self.lista_ventas:
            for producto in Producto.lista_productos:
                if venta.nombre == producto.nombre:
                    total = total +(int(venta.cantidad) * int(producto.precio))
        self.lista_ventas.clear()
        return total
