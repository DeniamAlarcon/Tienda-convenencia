from Inventario import *
from VentasMain import *
from Productos import *
from tickets import *

class Ventas:
    ventas_list = []
    def __init__(self, producto, cantidad,total):
        self.producto = producto
        self.cantidad = cantidad
        self.total = total


    def guardar_venta(self):
        Ventas.ventas_list.append(self)
        return True


    @staticmethod
    def mostrar_ventas():
        for venta in Ventas.ventas_list:
            print(f"Producto: {venta.producto}, Cantidad: {venta.cantidad}, Total: {venta.total}")


def buscar_producto(producto):
    print(producto)
    while not producto:
        producto = input("Ingrese el nombre del producto: ")
        print(f"Buscando el producto '{producto}'...")
        for i in Producto.lista_productos:
            if i.nombre == producto:
                return producto
            else:
                print("Producto no encontrado")
                producto = ""

def seleccionar_cantidad_producto(producto, cantidad):
    for i in Producto.lista_productos:
        if i.nombre == producto:
            if int(cantidad) > int(i.stock):
                print("La cantidad excede el stock")
                return False
            elif i.stock == 0:
                print("No hay stock de ", producto)
                print("Cancelando compra...")
                Ticket.limpiar_ticket()
                menuVentas()
            elif int(cantidad) == 0:
                print("La cantidad debe ser mayor a 0")
                return False
            else:
                print(f"Seleccionando {cantidad} unidades...")
                return True

def metodo_pago(total_pagar):
    while True:
        print("1. Efectivo")
        print("2. tarjeta")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            while True:
                total_dado = int(input("Ingrese el efectivo dado: "))
                if total_dado < total_pagar:
                    print("Efectivo incompleto")
                elif total_dado > total_pagar:
                    print("Cambio: ", total_dado - total_pagar)
                    break
                elif total_dado == total_pagar:
                    print("Cambio: 0")
                    break
            break
        elif opcion == "2":
            print("tarjeta")
            print("Cambio: 0")
            break

def corte_caja():
    cantidad = 0
    if Ventas.ventas_list.__len__() != 0:
        for i in Ventas.ventas_list:
            cantidad += int(i.total)
        return cantidad
    else:
        return cantidad

def venta():
    global venta
    while True:
        print("1.- Agregar producto")
        print("2.- Finalizar venta")
        print("3.- salir")
        opcion2 = input("Seleccione una opcion: ")
        if opcion2 == "1":
            producto = input("Ingrese el nombre del producto: ")
            validaNP = Producto.validar_nombre(producto)
            if validaNP:
                cant = ""
                while not cant:
                    cant = input("Ingrese la cantidad")
                    if cant.isdigit():
                        if int(cant) > 0:
                            break
                        else:
                            print("Cantidad debe ser mayor a 0")
                            cant = ""
                    else:
                        print("No se admite texto en la cantidad")
                        cant = ""
                while not seleccionar_cantidad_producto(producto,cant):
                    cant = input("Ingrese la cantidad")
                ticket = Ticket(producto, cant)
                ticket.guardar_producto()

            else:
                print("Producto no encontrado")
        elif opcion2 == "2":
            metodo_pago(Ticket.mostar_ticket())
            for i in Ticket.lista_ticket:
                venta = Ventas(i.nombre, i.cantidad, i.total)
                venta.guardar_venta()
                Inventario.actualizarSalidas(i.nombre, i.cantidad)
            break
        elif opcion2 == "3":
            Ticket.limpiar_ticket()
            print("Saliendo...")
            break

def menuVentas():
    if Proveedores.proveedores:
        if Producto.lista_productos:
            while True:
                print("----Ventas---")
                print("1 - Agregar Venta")
                print("2 - Mostrar Historial Ventas")
                print("3 - Corte de caja")
                print("4 - Salir")
                opcion= input("Seleccione una opcion: ")
                if opcion == "1":
                    venta()
                elif opcion == "2":
                    Ventas.mostrar_ventas()
                elif opcion == "3":
                    if corte_caja() != 0:
                        monto = ""
                        while not monto:
                            monto = input("Ingrese el total que se tiene en la caja: ")
                            if int(monto) > corte_caja():
                                print("Tiene sobrante verifique la cantidad")
                                print("La cantidad que debe tener es: ", corte_caja())
                                monto = ""
                            elif int(monto) < corte_caja():
                                print("Tiene faltante verifique la cantidad")
                                print("La cantidad que debe tener es: ", corte_caja())
                                monto = ""
                            elif int(monto) == corte_caja():
                                print("Corte de caja exitoso buen dia")
                                Ventas.ventas_list.clear()
                                break
                        break
                    else:
                        print("No hay ventas realizadas")
                        break
                elif opcion == "4":
                    break
        else:
            print("no hay productos registrados")
    else:
        print("No hay proveedores registrados")




