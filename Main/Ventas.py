
from Inventario import *
from VentasMain import *
from Productos import *

def acceder_apartado_ventas():
    print("Accediendo al apartado de ventas")


def buscar_producto():
    producto = ""
    while not producto:
        producto = input("Ingrese el nombre del producto: ")
        print(f"Buscando el producto '{producto}'...")
        for i in Producto.lista_productos:
            if i.nombre == producto:
                return producto
            else:
                print("Producto no encontrado")
                producto = ""


def agregar_producto_a_venta(producto):
    print(f"Agregando '{producto}' a la venta...")


def seleccionar_cantidad_producto(producto):
    cantidad = input("Ingrese la cantidad del producto: ")
    for i in Producto.lista_productos:
        if i.nombre == producto:
            if int(cantidad) > int(i.stock):
                print("La cantidad excede el stock")
                cantidad = ""
            elif int(cantidad) == 0:
                print("La cantidad debe ser mayor a 0")
                cantidad = ""
            else:
                print(f"Seleccionando {cantidad} unidades...")
                return cantidad


def seleccionar_metodo_pago():
    metodo_pago = input("Seleccione el método de pago (tarjeta/efectivo): ")
    print(f"Método de pago seleccionado: {metodo_pago}")
    return metodo_pago


def verificar_pago(monto_venta):
    pago_cliente = float(input("Ingrese el monto pagado por el cliente: "))
    if pago_cliente >= monto_venta:
        print("Accediendo a emisión de tickets...")
    else:
        print("Dinero insuficiente")

def cantidad_pagar(venta_actual):
    incremental = 0
    for i in venta_actual:
        incremental += 1
        print(f"{incremental} {i.nombre} {i.cantidad} {VentasMain.total_venta_actual(i.nombre,i.cantidad)}")


def menuVentas():
    if Proveedores.proveedores:
        if Producto.lista_productos:
            acceder_apartado_ventas()
            n = int(input("¿Cuántos productos desea vender? "))
            productos = []
            venta_actual=[]
            for i in range(n):
                producto = buscar_producto()
                agregar_producto_a_venta(producto)
                cantidad = seleccionar_cantidad_producto(producto)
                venta = VentasMain(cantidad,producto)
                venta.guardar_venta()
                Inventario.actualizarSalidas(producto, cantidad)
                venta_actual=venta.venta_actual()
                productos.append((producto, cantidad))

            metodo_pago = seleccionar_metodo_pago()
            cantidad_pagar(venta_actual)
            monto_venta = sum(cantidad for _, cantidad in productos)  # Asume que el precio de cada producto es 1 unidad

            print(f"El monto total de la venta es: {monto_venta}")
            verificar_pago(monto_venta)
        else:
            print("No hay productos registrados")
    else:
        print("No hay proveedores registrados")