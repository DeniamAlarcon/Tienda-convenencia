from ProductosOp import *
from ProveedoresOp import *
from ComprasProveedores import *

usuarios = {
    "Montserrat": "montse123",
    "usuario": "TDS1"
}

def solicitar_credenciales():
    while True:
        usuario = input("Ingrese usuario: ").strip()
        contraseña = input("Ingrese contraseña: ").strip()

        if not usuario or not contraseña:
            print("Ingrese los campos solicitados.")
        elif usuario in usuario and usuario[usuario] == contraseña:
            return True
        else:
            print("Usuario o contraseña no válidos.")

def menu():
    while True:
        print("\n--- Registro de Ventas ---")
        print("Ingrese una opcion")
        print("1.- Proveedores")
        print("2.- Productos")
        print("3.- Compras")
        print("4.- Usuarios")
        print("5.- Salir")
        opcion = input("Ingrese una opcion: ")


        if opcion == "1":
            menuProveedor()
        elif opcion == "2":
            menuProductos()
        elif opcion == "3":
            menuComprasProveedor()
        elif opcion == "4":
            solicitar_credenciales()
            print("Accediendo a Usuarios")
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Ingrese una opcion valida")
menu()

def main():
    if solicitar_credenciales():
        menu()

if __name__ == "__main__":
    main()














