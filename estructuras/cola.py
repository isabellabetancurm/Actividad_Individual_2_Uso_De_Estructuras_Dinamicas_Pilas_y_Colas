from .nodo import Nodo


class ColaVaciaError(Exception):
    """Se lanza al intentar sacar o consultar un elemento de una cola vacía."""
    pass


class Cola:
    """Cola (FIFO: el primero en entrar es el primero en salir).

    Implementada con nodos enlazados. Se trabaja por dos extremos:
    se encola por el FINAL y se desencola por el FRENTE.
    """

    def __init__(self):
        self._frente = None  # primer nodo: el próximo en salir
        self._final = None   # último nodo: por aquí entran los nuevos
        self._tamano = 0

    def esta_vacia(self):
        return self._frente is None

    def encolar(self, dato):
        """enqueue: agrega el dato al final de la cola."""
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self._frente = nuevo
        else:
            self._final.siguiente = nuevo
        self._final = nuevo
        self._tamano += 1

    def desencolar(self):
        """dequeue: saca y devuelve el dato del frente."""
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía.")
        nodo = self._frente
        self._frente = nodo.siguiente
        if self._frente is None:  # la cola quedó vacía
            self._final = None
        self._tamano -= 1
        return nodo.dato

    def ver_frente(self):
        """peek: devuelve el dato del frente sin sacarlo."""
        if self.esta_vacia():
            raise ColaVaciaError("La cola está vacía.")
        return self._frente.dato

    def tamano(self):
        return self._tamano

    def __len__(self):
        return self._tamano

    def __iter__(self):
        """Recorre la cola desde el frente hasta el final, sin modificarla."""
        actual = self._frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
