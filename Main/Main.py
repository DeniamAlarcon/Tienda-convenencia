from  ProductosOp import *
from ProveedoresOp import *
from ComprasProveedores import *
from Inventario import *


def menu():
    while True:
        print("Ingrese una opcion")
        print("1.- Proveedores")
        print("2.- Productos")
        print("3.- Compras")
        print("4.- Inventario")
        print("5.- Salir")
        opcion = input("Ingrese una opcion: ")
        if opcion == "1":
            menuProveedor()
        elif opcion == "2":
            menuProductos()
        elif opcion == "3":
            menuComprasProveedor()
        elif opcion == "4":
            menuInventario()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Ingrese una opcion valida")
menu()