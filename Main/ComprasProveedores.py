from Productos import *
from Proveedores import *
listaPedido=[]
def pedidoProveedor():

    while True:
        print("Registro de pedidos")
        print("1 - Agregar pedido")
        print("2 - Salir...")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            id = input("Ingrese el nombre del proveedor: ")
            proveedor = Proveedores.buscar_proveedor(id)
            if proveedor:
                nombreProducto = input("Ingrese el nombre del producto: ")
                prodcutoN=Producto.buscarProductoNombre(nombreProducto)
                if prodcutoN:
                    marcaProducto = input("Ingrese la marca del producto: ")
                    prodcutoM=Producto.buscarProductoMarca(marcaProducto)
                    if prodcutoM:
                        cantidadProducto = int(input("Ingrese la cantidad de productos: "))
                        if cantidadProducto>0:
                            listaPedido.append([nombreProducto,prodcutoN,cantidadProducto])
                    else:
                        print("Marca de producto no registrada")
                else:
                    print("Nombre de producto no registrado")
            else:
                print("El proveedor no existe")
        elif opcion == "2":
            print("Saliendo...")
            break
        else:
            print("Opcion no valida")


def mostrarPedidos():
    for i in listaPedido:
        print(i)

def menuComprasProveedor():
    while True:
        print("--------Menu de compras a proveedores--------")
        print("1. Realizar pedido de compra")
        print("2. Validacion de entregas")
        print("3. Registrar devoluciones")
        print("4. Generar historiles")
        print("5. Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            pedidoProveedor()
        elif opcion == "2":
            print("2. Validacion de entregas")
        elif opcion == "3":
            print("Registrar devoluciones")
        elif opcion == "4":
            while True:
                print("----Menu historiales----")
                print("1. Historial de compras")
                print("2. Historial de compras por proveedor")
                print("3. salir..")
                opcion2 = input("Ingrese una opcion: ")
                if opcion2 == "1":
                    print("1. Historial de compras")
                    mostrarPedidos()
                elif opcion == "2":
                    print("2. Historial de compras por proveedor")
                elif opcion2 == "3":
                    print("Saliendo...")
                    break
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opcion invalida")


menuComprasProveedor()
