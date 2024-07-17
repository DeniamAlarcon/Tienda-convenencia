def acceder_apartado_ventas():
    print("Accediendo al apartado de ventas")


def buscar_producto():
    producto = input("Ingrese el nombre del producto: ")
    print(f"Buscando el producto '{producto}'...")
    return producto


def agregar_producto_a_venta(producto):
    print(f"Agregando '{producto}' a la venta...")


def seleccionar_cantidad_producto():
    cantidad = int(input("Ingrese la cantidad del producto: "))
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


def main():
    acceder_apartado_ventas()
    n = int(input("¿Cuántos productos desea buscar? "))
    productos = []
    for _ in range(n):
        producto = buscar_producto()
        agregar_producto_a_venta(producto)
        cantidad = seleccionar_cantidad_producto()
        productos.append((producto, cantidad))

    metodo_pago = seleccionar_metodo_pago()

    monto_venta = sum(cantidad for _, cantidad in productos)  # Asume que el precio de cada producto es 1 unidad
    print(f"El monto total de la venta es: {monto_venta}")
    verificar_pago(monto_venta)


if __name__ == "__main__":
    main()