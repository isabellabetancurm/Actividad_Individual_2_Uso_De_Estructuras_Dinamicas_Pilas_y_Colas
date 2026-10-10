class Nodo:
    """Nodo de una estructura dinámica enlazada.

    Guarda un dato (en este proyecto, un cliente) y una referencia al
    siguiente nodo. La Pila y la Cola se construyen encadenando nodos,
    por eso crecen y se reducen dinámicamente (no tienen tamaño fijo).
    """

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
