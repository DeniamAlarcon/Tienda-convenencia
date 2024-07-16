class Producto:
    lista_productos = []
    def __init__(self ,codigo, nombre, marca, proveedor, cantidad, tamanio, precio, fecha_caducidad):
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

    @classmethod
    def buscar_nombre(self,nombre):
        if self.lista_productos.__len__() != 0:
            for product in self.lista_productos:
                if product.nombre == nombre:
                    print("Nombre de producto ya registrado")
                    return True
                else:
                    return False

    @classmethod
    def detalles_nombre(self, nombre):
        if self.lista_productos.__len__() != 0:
            for product in self.lista_productos:
                if product.nombre == nombre:
                    print(product.codigo, product.nombre, product.marca, product.proveedor, product.cantidad,product.tamanio, product.precio, product.fecha_caducidad)
                else:
                    print("producto no encontrado")
        else:
            print("producto no encontrado")

    @classmethod
    def detalles(self):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                print(product.codigo, product.nombre, product.marca, product.proveedor, product.cantidad, product.tamanio, product.precio, product.fecha_caducidad)
        else:
            print("producto no encontrado")

    @classmethod
    def buscarProducto(self,id):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.codigo == id:
                    return product
        else:
            print("producto no encontrado")
    @classmethod
    def buscarProductoNombre(self, nombre):
        for product in Producto.lista_productos:
            if product.nombre == nombre:
                return product

    @classmethod
    def buscarProductoMarca(self, marca):
        for product in Producto.lista_productos:
            if product.marca == marca:
                return product


    @classmethod
    def actualizar(self,id,nombre,proveedor,tamanio,precio):
        producto = self.buscarProducto(id)
        if producto:
            if not nombre and not proveedor and not tamanio and not precio:
                producto.nombre = producto.nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = producto.tamanio
                producto.precio = producto.precio
            elif not nombre:
                producto.nombre = producto.nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio
            elif not proveedor:
                producto.nombre = nombre
                producto.proveedor = producto.proveedor
                producto.tamanio = tamanio
                producto.precio = precio
            elif not tamanio:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = producto.tamanio
                producto.precio = precio
            elif not precio:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = producto.precio
            else:
                producto.nombre = nombre
                producto.proveedor = proveedor
                producto.tamanio = tamanio
                producto.precio = precio

            print("Prodcuto actualizado")
        else:
            print("Producto no encontrado")

    @classmethod
    def validar_codigo(cls, codigo):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.codigo == codigo:
                    return True
                else:
                    return False
        else:
           return False
