import tkinter as tk
from tkinter import messagebox
from ProductosOp import *
from ProveedoresOp import *
from ComprasProveedores import *

usuarios = {
    "Montserrat": "montse123",
    "usuario": "TDS1"
}

def solicitar_credenciales():
    def verificar_credenciales():
        usuario = entry_usuario.get().strip()
        contraseña = entry_contraseña.get().strip()

        if not usuario or not contraseña:
            messagebox.showwarning("Advertencia", "Ingrese los campos solicitados.")
        elif usuario in usuarios and usuarios[usuario] == contraseña:
            messagebox.showinfo("Éxito", "Credenciales válidas.")
            credenciales_win.destroy()
            menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña no válidos.")

    credenciales_win = tk.Toplevel()
    credenciales_win.title("Solicitar Credenciales")

    tk.Label(credenciales_win, text="Usuario:").grid(row=0, column=0, padx=10, pady=10)
    entry_usuario = tk.Entry(credenciales_win)
    entry_usuario.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(credenciales_win, text="Contraseña:").grid(row=1, column=0, padx=10, pady=10)
    entry_contraseña = tk.Entry(credenciales_win, show="*")
    entry_contraseña.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(credenciales_win, text="Ingresar", command=verificar_credenciales).grid(row=2, column=0, columnspan=2, pady=10)

def menu():
    def abrir_proveedores():
        menuProveedor()

    def abrir_productos():
        menuProductos()

    def abrir_compras():
        menuComprasProveedor()

    def abrir_usuarios():
        solicitar_credenciales()

    def salir():
        root.destroy()

    root = tk.Tk()
    root.title("Registro de Ventas")

    tk.Label(root, text="--- Registro de Ventas ---", font=("Helvetica", 16)).pack(pady=10)
    tk.Button(root, text="Proveedores", command=abrir_proveedores).pack(pady=5)
    tk.Button(root, text="Productos", command=abrir_productos).pack(pady=5)
    tk.Button(root, text="Compras", command=abrir_compras).pack(pady=5)
    tk.Button(root, text="Usuarios", command=abrir_usuarios).pack(pady=5)
    tk.Button(root, text="Salir", command=salir).pack(pady=20)

    root.mainloop()

def main():
    solicitar_credenciales()

if __name__ == "__main__":
    main()
