# Definiciones

## Estructura de datos dinámica
Estructura que **crece y se reduce mientras el programa se ejecuta**, porque no tiene un
tamaño fijo. En este proyecto se construyen encadenando **nodos**.

## Nodo
Objeto que guarda un dato (aquí, un `Cliente`) y una referencia al **siguiente** nodo.
Está en `estructuras/nodo.py`.

## Pila (LIFO: *Last In, First Out*)
El **último** en entrar es el **primero** en salir, como una pila de platos. Solo se
trabaja por un extremo, el **tope**. Está en `estructuras/pila.py`.

| Operación | Método | Qué hace |
|---|---|---|
| push | `apilar(dato)` | Pone un dato arriba, en el tope |
| pop | `desapilar()` | Saca y devuelve el dato del tope |
| peek | `ver_tope()` | Pregunta quién está en el tope, sin sacarlo |
| — | `esta_vacia()` | Dice si no hay datos |

**En el consultorio:** la Pila de contingencia guarda las extracciones urgentes. Se apilan
de la fecha más lejana a la más cercana para que la cita más próxima quede en el tope y se
llame primero.

## Cola (FIFO: *First In, First Out*)
El **primero** en entrar es el **primero** en salir. Se agrega por el **final** y se saca
por el **frente**. Está en `estructuras/cola.py`.

Sirve para muchos procesos de la vida real:
- **La fila de un banco:** la primera persona en llegar es la primera en ser atendida.
- **Colas de trabajo:** en computación los recursos son limitados (memoria, disco, ancho de
  banda, procesador), así que no se puede atender a todos a la vez y se atiende de a poco.
- **Colas de impresión.**

| Operación | Método | Qué hace |
|---|---|---|
| enqueue | `encolar(dato)` | Agrega un dato al final de la cola |
| dequeue | `desencolar()` | Saca y devuelve el dato del frente (lo atiende) |
| peek | `ver_frente()` | Pregunta quién sigue, **sin atenderlo** |
| — | `esta_vacia()` | Dice si no hay datos |

En Python una cola suele hacerse con `collections.deque` (`append` para encolar y `popleft`
para desencolar). Aquí se construyó a mano con nodos para mostrar cómo funciona por dentro.

**En el consultorio:** la agenda es una Cola. Los clientes se atienden en estricto orden, y
quien llega nuevo se agrega al final.

## Cola sin prioridad y cola con prioridad
- **Sin prioridad:** se atiende estrictamente por orden de llegada. Es la que usa este proyecto.
- **Con prioridad estricta:** siempre se atiende primero a quien tiene mayor prioridad. Su
  riesgo es la **inanición** (*starvation*): si no dejan de llegar clientes de mayor
  prioridad, los de menor prioridad pueden no ser atendidos nunca. Una forma de evitarlo es
  rotar los turnos entre las colas (*Round Robin*).

**Por qué la agenda de este proyecto es sin prioridad:** el enunciado pide atender los
clientes "en el estricto orden que define la agenda", así que nadie se salta la fila. La
prioridad "Urgente" solo se usa como **filtro** para decidir quién entra a la Pila de
contingencia; no cambia el orden de la Cola.

## Costo de las operaciones
Todas las operaciones de la Pila y de la Cola son de **tiempo constante, O(1)**: solo tocan
los extremos y no recorren la estructura. La Cola guarda una referencia a su último nodo
precisamente para poder encolar sin recorrerla completa.

## Pila vs. Cola

| | Pila | Cola |
|---|---|---|
| Orden | LIFO (último en entrar, primero en salir) | FIFO (primero en entrar, primero en salir) |
| Extremos | Uno: el tope | Dos: frente y final |
| Ejemplo cotidiano | Pila de platos | Fila de un banco |
| En este proyecto | Extracciones urgentes | Agenda de atención |
