from Main.Productos import *
from Main.Proveedores import *
from datetime import datetime

import re

def validar_tamanio(tamanio):
    # Lista de unidades de medida válidas
    unidades_validas = ["kg", "g", "L", "ml", "pcs", "m", "cm", "in"]
    # Crear una expresión regular para verificar el formato
    pattern = re.compile(r'^(\d+(\.\d+)?)(kg|g|L|ml|pcs|m|cm|in)$')
    match = pattern.match(tamanio)
    if match:
        # Extraer la unidad de medida del tamaño validado
        unidad = match.group(3)
        # Verificar si la unidad de medida extraída es válida
        return unidad in unidades_validas
    return False
def validarDigitos(digito):
    if digito.isdigit():
        return True

def validar_fecha(fecha):
    formato = "%d/%m/%Y"
    try:
        fechaConversion = datetime.strptime(fecha, formato)
        return True
    except ValueError:
        return False

def validar_caducidad(fecha):
    formato = "%d/%m/%Y"
    fecha_actual = datetime.now()
    fecha_dada = datetime.strptime(fecha, formato)
    return fecha_dada < fecha_actual


def validar_cantidad(cantidad):
    if cantidad.isdigit():
        if int(cantidad) > 0:
            return True
        else:
            print("cantidad del producto no puede ser menor o igual a 0")
            return False
    else:
        print("No se admite texto en cantidad del producto")
        return False


def validar_precio(precio):
    if precio.isdigit():
        if int(precio) > 0:
            return True
        else:
            print("precio del producto no puede ser menor o igual a 0")
            return False
    else:
        print("No se admite texto en precio del producto")
        return False

def registrarProducto():
    codigo= ""
    while not codigo:
        codigo = input("Ingrese el codigo del producto: ")
        if not codigo:
            print("Favor de ingresar los datos requeridos")
            codigo = ""
        else:
            if Producto.validar_codigo(codigo):
                print("Codigo de producto ya registrado ")
                codigo = ""

    nombre = ""
    while not nombre:
        #validar que el nombre no este registrado
        nombre = input("Ingrese el nombre del producto: ")
        if not nombre:
            print("Favor de ingresar los datos requeridos")
            nombre =""
        else:
            if Producto.buscar_nombre(nombre):
                nombre=""

    marca = ""
    while not marca:
        marca = input("Ingrese la marca del producto: ")

    proveedor = ""
    while not proveedor:
        proveedor = input("Ingrese el proveedor del producto: ")
        if not proveedor:
            print("Favor de ingresar los datos requeridos")
            proveedor = ""
        else:
            if not Proveedores.validar_provedor(proveedor):
                proveedor = ""


    cantidad = ""
    while not cantidad:
        #validar que sea digito y que sea mayor a 0
        cantidad = input("Ingrese la cantidad del producto: ")
        if not cantidad:
            print("Favor de ingresar los datos requeridos")
            cantidad = ""
        else:
            if not validar_cantidad(cantidad):
                cantidad = ""

    tamanio = ""
    while not tamanio:
        tamanio = input("Ingrese el tamaño del producto (ej. 10kg, 250ml, 30pcs): ")
        if not tamanio:
            print("Favor de ingresar los datos requeridos")
        elif not validar_tamanio(tamanio):
            print(
                "Tamaño inválido. Debe ser un número seguido de una unidad de medida válida (kg, g, L, ml, pcs, m, cm, in).")
            tamanio = ""


    precio = ""
    while not precio:
        #validar que ele precio sea mayor a 0
        precio = input("Ingrese el precio del producto: ")
        if not precio:
            print("Favor de ingresar los datos requeridos")
            precio = ""
        else:
            if not validar_precio(precio):
                precio=""

    fecha_vencimiento = ""
    while not fecha_vencimiento:
        fecha_vencimiento = input("Ingrese la fecha de vencimiento (dd/mm/yyyy): ")
        if not fecha_vencimiento:
            print("Favor de ingresar los datos requeridos")
            fecha_vencimiento = ""
        else:
            if validar_fecha(fecha_vencimiento):
                if validar_caducidad(fecha_vencimiento):
                    print("El producto se encuntra caduco")
                    fecha_vencimiento = ""
            else:
                print("Favor de ingresar una fecha valida (dd/mm/yyyy)")
                fecha_vencimiento = ""


    registro = Producto(codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_vencimiento)
    if registro.registrar():
        print("Producto registrado exitosamente")
    else:
        print("Producto no registrado")

def actualizarproducto():
   codigo = input("Ingrese el codigo del producto: ")

   nombre = ""
   while not nombre:
       nombre = input("Ingrese el nombre del producto: ")
       if nombre:
           if Producto.buscar_nombre(nombre):
               nombre = ""
       else:
           break


   proveedor = ""
   while not proveedor:
       proveedor=input("Ingrese el proveedor del producto: ")
       if not Proveedores.validar_provedor(proveedor):
           print("Proveedor no encontrado")
           proveedor=""
       else:
           break

   tamanio = ""
   while not tamanio:
       tamanio = input("Ingrese la unidad de medida del producto")
       if tamanio:
           if not validar_tamanio(tamanio):
               tamanio =""
       else:
           break

   precio = ""
   while not precio:
       precio = input("Ingrese el precio del producto: ")
       if precio:
           if not validar_precio(precio):
               precio =""
       else:
           break

   Producto.actualizar(codigo, nombre, proveedor, tamanio, precio)

def menuProductos():
    if Proveedores.proveedores:
        while True:
            print("---Menu de productos---")
            print("1. Registrar")
            print("2. Detalles")
            print("3. Actualizar")
            print("4. Crear archivo")
            print("5. Salir")
            opcion = input("Ingrese opcion: ")
            if opcion == "1":
                registrarProducto()
            elif opcion == "2":
                print("1. Busqueda por nombre")
                print("2. Gestion de productos")
                opc1 = input("Ingrese opcion: ")
                if opc1 == "1":
                    nombre = input("Ingrese nombre del producto: ")
                    Producto.detalles_nombre(nombre)
                elif opc1 == "2":
                    Producto.detalles()

            elif opcion == "3":
                actualizarproducto()
            elif opcion == "4":
                while True:
                    print("---Menu de archivos---")
                    print("1. Crear archivo csv")
                    print("2. Crear archivo json")
                    print("3. Crear archivo pdf")
                    print("4. Crear archivo xlsx")
                    print("5. Salir")
                    opc2 = input("Ingrese opcion: ")
                    if opc2 == "1":
                        Producto.crear_archivo_csv()
                    elif opc2 == "2":
                        Producto.crear_archivo_json()
                    elif opc2 == "3":
                        Producto.crear_archivo_pdf()
                    elif opc2 == "4":
                        Producto.crear_archivo_xlsx()
                    elif opc2 == "5":
                        break
            elif opcion == "5":
                break
    else:
        print("No se encuentra ningun proveedore registrado")