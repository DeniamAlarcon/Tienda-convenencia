import csv
from datetime import datetime
from Productos import *
from ProductosOp import *

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio


# Función para cargar productos desde un archivo CSV
def cargar_productos(archivo):
    productos = []
    try:
        with open(archivo, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                nombre, precio = row
                productos.append(Producto(nombre, float(precio)))
    except FileNotFoundError:
        pass
    return productos


# Función para cargar ventas desde un archivo CSV
def cargar_ventas(archivo):
    ventas = []
    try:
        with open(archivo, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                ventas.append(row)
    except FileNotFoundError:
        pass
    return ventas


# Función para guardar productos en un archivo CSV
def guardar_productos(archivo, productos):
    with open(archivo, mode='w', newline='') as file:
        writer = csv.writer(file)
        for producto in productos:
            writer.writerow([producto.nombre, producto.precio])


# Función para guardar una venta en un archivo CSV
def guardar_venta(archivo, venta):
    with open(archivo, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(venta)


# Función para agregar un producto nuevo
def agregar_producto(productos):
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto: "))
    productos.append(Producto(nombre, precio))
    print("Producto agregado con éxito.")


# Función para registrar una venta
def registrar_venta(productos):
    ventas = []
    while True:
        nombre_producto = input("Ingrese el nombre del producto a vender: ")
        producto = next((p for p in productos if p.nombre.lower() == nombre_producto.lower()), None)

        if producto:
            cantidad = int(input(f"Ingrese la cantidad de {producto.nombre} a vender: "))
            total = cantidad * producto.precio
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            venta = [producto.nombre, cantidad, producto.precio, total, fecha]
            ventas.append(venta)
            print("Producto agregado a la venta.")
        else:
            print("Producto no encontrado.")

        otra_venta = input("¿Desea agregar otro producto a la venta? (s/n): ").lower()
        if otra_venta != 's':
            break

    return ventas


# Función principal
def main():
    archivo_productos = 'productos.csv'
    archivo_ventas = 'ventas.csv'
    productos = cargar_productos(archivo_productos)

    while True:
        print("\n--- Registro de ventas ---")
        print("1. Agregar Producto")
        print("2. Registrar Venta")
        print("3. Listar Productos")
        print("4. Listar Ventas")
        print("5.Procesar Pago")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto(productos)
            guardar_productos(archivo_productos, productos)
        elif opcion == '2':
            intput = input("Ingrese el nombre del producto: ")
            Producto.buscar_nombre(intput)
            ventas = registrar_venta(productos)
            for venta in ventas:
                guardar_venta(archivo_ventas, venta)
        elif opcion == '3':
            print("\nProductos Registrados:")
            for producto in productos:
                print(f"Nombre: {producto.nombre}, Precio: {producto.precio}")
        elif opcion == '4':
            ventas = cargar_ventas(archivo_ventas)
            print("\nVentas Registradas:")
            for venta in ventas:
                print(
                    f"Producto: {venta[0]}, Cantidad: {venta[1]}, Precio Unitario: {venta[2]}, Total: {venta[3]}, Fecha: {venta[4]}")
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()
