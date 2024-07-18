from ProductosOp import *
from ProveedoresOp import *
from ComprasProveedores import *
from VentaP import menuVentas

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
            menuComprasProveedor()
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


def main():
    if solicitar_credenciales():
        menu()

if __name__ == "__main__":
    main()














