# Diccionario de usuarios para autenticación
usuarios = {
    "Montserrat": "montse123",
    "usuario": "TDS1"
}

# Función para solicitar y verificar usuario y contraseña
def solicitar_credenciales():
    while True:
        usuario = input("Ingrese usuario: ").strip()
        contraseña = input("Ingrese contraseña: ").strip()

        if not usuario or not contraseña:
            print("Ingrese los campos solicitados.")
        elif usuario in usuarios and usuarios[usuario] == contraseña:
            return True
        else:
            print("Usuario o contraseña no válidos.")

# Función para mostrar el menú de operaciones
def mostrar_menu():
    while True:
        print("\n--- Menú de Operaciones ---")
        print("1. Ventas")
        print("2. Productos")
        print("3. Proveedores")
        print("4. Usuarios")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("Accediendo a Ventas...")
            # Aquí iría la lógica para el módulo de Ventas
        elif opcion == '2':
            print("Accediendo a Productos...")
            # Aquí iría la lógica para el módulo de Productos
        elif opcion == '3':
            print("Accediendo a Proveedores...")
            # Aquí iría la lógica para el módulo de Proveedores
        elif opcion == '4':
            print("Accediendo a Usuarios...")
            # Aquí iría la lógica para el módulo de Usuarios
        elif opcion == '5':
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# Función principal
def main():
    if solicitar_credenciales():
        mostrar_menu()

if __name__ == "__main__":
    main()