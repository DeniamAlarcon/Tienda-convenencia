from datetime import datetime
from Productos import *
class Ticket:
    lista_ticket=[]
    def __init__(self, nombre, cantidad):

        self.nombre = nombre
        self.cantidad = cantidad
        self.total = 0


    def guardar_producto(self):
        Ticket.calcular_total(self)
        self.lista_ticket.append(self)
        return True


    def calcular_total(self):
        for product in Producto.lista_productos:
            if product.nombre == self.nombre:
                self.total += int(product.precio) * int(self.cantidad)

    @classmethod
    def mostar_ticket(self):
        total_pagar = 0
        print("Compra generada el: ", datetime.now())
        print(f"{'nombre':<10} {'cantidad':<20} {'monto':<15}")
        print("=" * 60)
        for ticket in Ticket.lista_ticket:
            print(f"{ticket.nombre:<20} {ticket.cantidad:<10} {ticket.total:<10}")
            total_pagar += int(ticket.total)
        print("=" * 60)
        print("Total a pagar: ", total_pagar)
        return int(total_pagar)


    @classmethod
    def limpiar_ticket(cls):
        Ticket.lista_ticket.clear()

