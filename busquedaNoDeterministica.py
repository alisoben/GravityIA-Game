import random

class BusquedaNoDeterministica:
    def noDeterminista(self, estado):
        return random.choice(estado.acciones())
