

class Producto:
    lista_productos = []
    def __init__(self,codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad):
        self.codigo = codigo
        self.nombre = nombre
        self.marca = marca
        self.proveedor = proveedor
        self.cantidad = cantidad
        self.tamanio = tamanio
        self.precio = precio
        self.fecha_caducidad = fecha_caducidad

    def registrar(self):
        Producto.lista_productos.append(self)
        return True

    def detalles():
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                print(product.codigo)
        else:
            print("No hay productos registrados")