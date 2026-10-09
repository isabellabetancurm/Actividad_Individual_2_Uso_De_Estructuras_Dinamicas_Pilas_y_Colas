from .nodo import Nodo


class PilaVaciaError(Exception):
    """Se lanza al intentar sacar o consultar un elemento de una pila vacía."""
    pass


class Pila:
    """Pila (LIFO: el último en entrar es el primero en salir).

    Implementada con nodos enlazados. Solo se trabaja por un extremo, el
    TOPE: ahí se apila (push), se desapila (pop) y se consulta (peek).
    """

    def __init__(self):
        self._tope = None  # referencia al nodo que está arriba de la pila
        self._tamano = 0

    def esta_vacia(self):
        return self._tope is None

    def apilar(self, dato):
        """push: el nuevo nodo pasa a ser el tope."""
        nuevo = Nodo(dato)
        nuevo.siguiente = self._tope
        self._tope = nuevo
        self._tamano += 1

    def desapilar(self):
        """pop: saca y devuelve el dato del tope."""
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        nodo = self._tope
        self._tope = nodo.siguiente
        self._tamano -= 1
        return nodo.dato

    def ver_tope(self):
        """peek: devuelve el dato del tope sin sacarlo."""
        if self.esta_vacia():
            raise PilaVaciaError("La pila está vacía.")
        return self._tope.dato

    def tamano(self):
        return self._tamano

    def __len__(self):
        return self._tamano

    def __iter__(self):
        """Recorre la pila desde el tope hasta la base, sin modificarla."""
        actual = self._tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
