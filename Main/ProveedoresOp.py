from Proveedores import *
import re



def validar_telefono(telefono):
    return len(telefono) > 9 and len(telefono) < 16
def validar_correo(pattern,correo):
    if not re.match(pattern, correo):
        return False
def registrarProveedor():
  while True:
      try:
          nombre = input("Ingrese nombre del proveedor: ")
          while not nombre:
              nombre = input("Ingrese nombre del proveedor: ")
          correo = input("Ingrese correo del proveedor: ")
          pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
          while not correo:
              correo = input("Ingrese correo del proveedor: ")
          while not re.match(pattern, correo):
              correo = input("Ingrese correo del proveedor: ")
          telefono = input("Ingrese telefono del proveedor: ")
          while not validar_telefono(telefono):
              telefono = input("El numero debe ser mayor a 10 y menoar a 15: ")
          while not telefono.isdigit():
              telefono = input("El numero debe ser numerico: ")
          registro = Proveedores(nombre, correo, telefono)
          if registro.guardar():
              print("Proveedor registrado correctamente")
              break
          else:
              print("Ocurrio un error al registrar proveedor")

      except ValueError as e:
          print("Ingrese un numero telefonico valido: ")
      except Exception as e:
          print(f"Ocurrió un error: {e}")



def actualizarProveedores():
    while True:
        try:
            id = int(input("Ingrese id del proveedore: "))
            nNombre = input("Ingresa el nombre del proveedor: ")
            nCorreo = input("Ingrese el correo electronico del proveedor: ")
            if nCorreo != "":
                pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
                while not re.match(pattern, correo):
                    correo = input("Ingrese correo del proveedor: ")
            nTelefono = input("Ingrese el telefono del proveedor: ")
            if nTelefono != "":
                while not validar_telefono(nTelefono):
                    nTelefono = input("Ingrese el telefono del proveedor: ")
                while not nTelefono.isdigit():
                    nTelefono = input("El numero debe ser numerico: ")
            Proveedores.actualizar(id, nNombre, nCorreo, nTelefono)
            break
        except ValueError as e:
            print("Ingrese un numero telefonico valido: ")
        except Exception as e:
            print("Error al actualizar proveedore ", e)




def menuProveedor():
   while True:
       print("----MENU DE PROVEEDOR----")
       print("1. Registrar Proveedor")
       print("2. Actualizar Proveedor")
       print("3. Mostrar Proveedor")
       print("4. Eliminar Proveedor")
       print("5. Salir")
       opcion = input("Ingrese opcion: ")
       if opcion == "1":
           registrarProveedor()
       elif opcion == "2":
           actualizarProveedores()
       elif opcion == "3":
           print("1. Busqueda por nombre")
           print("2. Gestion de proveedores")
           opc1= input("Ingrese opcion: ")
           if opc1 == "1":
               nombre = input("Ingrese nombre del proveedor: ")
               Proveedores.mostrar_nombre(nombre)
           elif opc1 == "2":
               Proveedores.mostrar()
       elif opcion == "4":
            id=int(input("Ingrese id del proveedor: "))
            Proveedores.eliminar_proveedor(id)
       elif opcion == "5":
           print("Saliendo...")
           break
       else:
           print("Opcion invalida")
menuProveedor()