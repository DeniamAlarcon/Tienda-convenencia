from ProductosOp import *
from ProveedoresOp import *
from ComprasProveedores import *
from VentaP import menuVentas
from Proveedores import *
from Productos import *

usuarios = [
    "admin",
    "admin"
]

def solicitar_credenciales():

    while True:
        print("---Inicio de sesion---")
        usuario = input("Ingrese usuario: ")
        contraseña = input("Ingrese contraseña: ")

        if not usuario or not contraseña:
            print("Ingrese los campos solicitados.")
        elif usuarios[0] == usuario and usuarios[1] == contraseña:
            return True
        else:
            print("Usuario o contraseña no válidos.")

def menu():
    Proveedores.leer_archivo()
    Producto.leer_archivo()
    while True:
        print("\n--- Menu principal ---")
        print("Ingrese una opcion")
        print("1.- Proveedores")
        print("2.- Productos")
        print("3.- Compras")
        print("4.- Inventarios")
        print("5.- Ventas")
        print("6.- Salir")
        opcion = input("Ingrese una opcion: ")

        if opcion == "1":
            menuProveedor()
        elif opcion == "2":
            menuProductos()
        elif opcion == "3":
            if Proveedores.mostrar():
                menuComprasProveedor()
            else:
                print("registre un proveedor")
#        elif opcion == "4":
#            solicitar_credenciales()
#            print("Accediendo a Usuarios")
        elif opcion == "4":
            menuInventario()
        elif opcion == "5":
            menuVentas()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Ingrese una opcion valida")



if solicitar_credenciales():
    menu()















