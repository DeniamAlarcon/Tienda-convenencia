import csv
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
        self.entradas = cantidad
        self.salidas = 0
        self.stock = cantidad
        self.existenciasAnteriores = cantidad
        self.ajuste =0


    @classmethod
    def leer_archivo(cls):
        with open('D:\\Tienda-convenencia\\Archivos\\productos.csv',
                  encoding='utf8') as archivo_productos:
            reader = csv.DictReader(archivo_productos)
            filas = list(reader)
            if not filas or all(not any(row.values()) for row in filas):
                print('No hay datos que leer')
                return

            for row in filas:
                producto = Producto(
                    row["codigo"],
                    row["nombre"],
                    row["marca"],
                    row["proveedor"],
                    row["cantidad"],
                    row["unidad_medida"],
                    row["precio"],
                    row["fecha_caducidad"]
                )
                producto.entradas = row["entradas"]
                producto.salidas = row["salidas"]
                producto.stock = row["stock"]
                producto.existenciasAnteriores = row["existencias_anteriores"]
                producto.ajuste = row["ajuste"]
                Producto.lista_productos.append(producto)




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
                    print("Codigo: ",product.codigo, "Nombre: ",product.nombre, "Marca: ",product.marca, "Proveedor: ",product.proveedor, "Cantidad: ",product.cantidad, "Unidad de medida: ",product.tamanio, "Precio: ",product.precio, "Fecha de caducidad:",product.fecha_caducidad)
                else:
                    print("producto no encontrado")
        else:
            print("producto no encontrado")

    @classmethod
    def detalles(self):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                print("Codigo: ",product.codigo, "Nombre: ",product.nombre, "Marca: ",product.marca, "Proveedor: ",product.proveedor, "Cantidad: ",product.cantidad, "Unidad de medida: ",product.tamanio, "Precio: ",product.precio, "Fecha de caducidad:",product.fecha_caducidad)
        else:
            print("No hay registro de productos")

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

    @classmethod
    def validar_marca(cls, marca):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.marca == marca:
                    return True
                else:
                    return False
        else:
            return False
    @classmethod
    def validar_nombre(cls, nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    return True
                else:
                    return False
        else:
            return False

    @classmethod
    def validar_stock(cls,nombre):
        if Producto.lista_productos.__len__() != 0:
            for product in Producto.lista_productos:
                if product.nombre == nombre:
                    return product.stock