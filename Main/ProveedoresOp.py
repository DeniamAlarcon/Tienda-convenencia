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
          nombre = input("Ingrese el nombre del proveedor: ")
          while not nombre:
              print("Favor de llenar todos los campos requeridos")
              nombre = input("Ingrese el nombre del proveedor: ")
          correo = input("Ingrese correo electronico del proveedor: ")
          pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
          while not correo:
              print("Favor de llenar todos los campos requeridos")
              correo = input("Ingrese correo electronico del proveedor: ")
          while not re.match(pattern, correo):
              print("Correo no valido")
              correo = input("Ingrese correo del proveedor: ")
          telefono = input("Ingresa el número de telefono: ")
          while not validar_telefono(telefono):
              print("Numero de telefono no valido")
              telefono = input("El numero debe ser mayor a 10 y menoar a 15: ")
          while not telefono.isdigit():
              print("Dato incorrecto")
              telefono = input("El numero debe ser numerico: ")
          registro = Proveedores(nombre, correo, telefono)

          if registro.comprobarExistencia(nombre,correo,telefono):
              print("El proveedor ya existe")
          else:
              if registro.guardar():
                  print("Proveedor registrado")
                  break
              else:
                  print("Ocurrio un error al registrar proveedor")

      except ValueError as e:
          print("Ingrese un numero telefonico valido: ")
      except Exception as e:
          print(f"Favor de llenar los campos requeridos {e}")




def actualizarProveedores():
    while True:
        try:
            id = int(input("Ingrese id del proveedore: "))
            nNombre = input("Ingresa el nombre del proveedor: ")
            nCorreo = input("Ingrese el correo electronico del proveedor: ")
            if nCorreo != "":
                pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
                while not re.match(pattern, nCorreo):
                    nCorreo = input("Ingrese correo del proveedor: ")
            nTelefono = input("Ingrese el telefono del proveedor: ")
            if nTelefono != "":
                while not validar_telefono(nTelefono):
                    print("Se debe ingresar un telefono mayor o igual a 10")
                    nTelefono = input("Ingrese el telefono del proveedor: ")
                while not nTelefono.isdigit():
                    print("Solo se aceptan numeros en el campo telefono")
                    nTelefono = input("El telefono debe ser numerico: ")
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
            Proveedores.eliminarProveedor(id)
       elif opcion == "5":
           print("Saliendo...")
           break
       else:
           print("Opcion invalida")
menuProveedor()