from Main.PedidosProveedor import *
from Main.VentasMain import *


def pedidoProveedor():
    while True:
        print("Registro de pedidos")
        print("1 - Agregar pedido")
        print("2 - Salir...")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            Proveedores.mostrar()
            nombreProveedor = input("Ingrese el nombre del proveedor: ")
            while not nombreProveedor:
                nombreProveedor = input("Ingrese el nombre del proveedor: ")
            proveedor = Proveedores.validar_provedor(nombreProveedor)
            if proveedor:
                nombreProducto = input("Ingrese el nombre del producto: ")
                while not nombreProducto:
                    nombreProducto = input("Ingrese el nombre del producto registrado: ")
                prodcutoN=Producto.validar_nombre(nombreProducto)
                if prodcutoN:
                    marcaProducto = input("Ingrese la marca del producto: ")
                    while not marcaProducto:
                        marcaProducto = input("Ingrese la marca del producto registrado: ")
                    prodcutoM=Producto.validar_marca(marcaProducto)
                    if prodcutoM:
                        cantidadProducto = (input("Ingrese la cantidad de productos: "))
                        if cantidadProducto.isdigit():
                            if int(cantidadProducto) > 0:
                                precio= VentasMain.total_venta_actual(nombreProducto,int(cantidadProducto))
                                guarda = PedidosProveedor(nombreProveedor, nombreProducto, marcaProducto,cantidadProducto,precio)
                                guarda.guardar()
                            else:
                                print("No se pueden pedir menos de 0  cosas")
                        else:
                            print("Cantidad de productos invalido")
                    else:
                        print("Marca de producto no registrada")
                else:
                    print("Nombre de producto no registrado")
            else:
                print("Nombre de producto no registrado")
        elif opcion == "2":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida")





def menuComprasProveedor():
    while True:
        print("--------Menu de compras a proveedores--------")
        print("1. Realizar pedido de compra")
        print("2. Validacion de entregas")
        print("3. Registrar devoluciones")
        print("4. Generar Historiales de compra")
        print("5. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            pedidoProveedor()
        elif opcion == "2":
            try:
                id = input("Ingrese el id del pedido: ")
                cantidad = int(input("Ingrese la cantidad de productos: "))
                PedidosProveedor.pedidos_proveedorID(id, cantidad)

            except ValueError as e:
                print("Ingrese datos correctos ")
        elif opcion == "3":
            Inventario.informeStockC()
            productos = input("Ingrese el producto para la devolucion: ")
            while not productos:
                productos = input("Ingrese el producto para la devolucion: ")
            try:
                cantidad = int(input("Ingrese la cantidad de productos: "))
                inventario = Inventario()
                if inventario.actualizarSalidas(productos, cantidad):
                    print("Devolucion realizada")
            except ValueError as e:
                print("Ingrese cantidad numerica ")



        elif opcion == "4":
            while True:
                print("----Menu Historiales----")
                print("1. Historial de compras")
                print("2. Historial de compras por proveedor")
                print("3. salir..")
                opcion2 = input("Ingrese una opcion: ")
                if opcion2 == "1":
                    PedidosProveedor.mostrar_pedidos()
                elif opcion2 == "2":
                    print("2. Historial de compras por proveedor")
                    nombreProveedor = input("Ingrese el nombre del proveedor: ")
                    proveedor = Proveedores.validar_provedor(nombreProveedor)
                    if proveedor:
                        PedidosProveedor.pedidos_proveedor(nombreProveedor)
                    else:
                        print("Nombre de proveedor no registrado")
                elif opcion2 == "3":
                    print("Saliendo...")
                    break
                else:
                    print("Opcion no valida")
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")