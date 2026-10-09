"""
Clase Consultorio: reúne a los clientes y administra la Pila de contingencia
y la Cola de atención (equivale a la clase Tienda del ejemplo de la tienda).
"""

import json
import os
from datetime import datetime

from cliente import Cliente, formato_pesos
from estructuras import Cola, Pila

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE_DIR, "datos_clientes.json")
ARCHIVO_EJEMPLO = os.path.join(BASE_DIR, "datos", "clientes_ejemplo.json")
ARCHIVO_INFORME = os.path.join(BASE_DIR, "informe_pila.txt")


class Consultorio:

    def __init__(self, nombre):
        self.nombre = nombre
        self.clientes = []                  # todos los clientes registrados
        self.pila_contingencia = Pila()     # extracciones urgentes
        self.cola_agenda = Cola()           # agenda de atención

    # ------------------------------------------------------------------
    # Registro y consulta de clientes
    # ------------------------------------------------------------------
    def registrar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.guardar_clientes()

    def consultar_todos_los_clientes(self):
        if len(self.clientes) == 0:
            print("No hay clientes registrados.")
            return
        print(f"{'Nº':<4}{'Cédula':<12}{'Nombre':<22}{'Atención':<13}{'Cant.':<6}"
              f"{'Prioridad':<10}{'Fecha':<12}{'Estado':<10}{'Valor':>11}")
        print("-" * 100)
        for numero, c in enumerate(self.clientes, start=1):
            print(f"{numero:<4}{c.cedula:<12}{c.nombre[:21]:<22}{c.tipo_atencion:<13}{c.cantidad:<6}"
                  f"{c.prioridad:<10}{c.fecha_cita:<12}{c.estado:<10}{c.valor_formateado():>11}")

    # ------------------------------------------------------------------
    # PILA de contingencia: extracciones urgentes
    # ------------------------------------------------------------------
    @staticmethod
    def es_candidato_a_la_pila(cliente):
        """Criterios del enunciado: extracción dental, prioridad Urgente y cita pendiente."""
        return (
            cliente.esta_pendiente()
            and cliente.tipo_atencion == "Extracción"
            and cliente.prioridad == "Urgente"
        )

    def generar_pila_de_contingencia(self):
        """Genera la Pila con los clientes que cumplen los criterios.

        En una pila sale primero lo último que se apiló. Para que el cliente
        con la fecha MÁS CERCANA quede en el tope (y sea el primero en ser
        llamado), se apila de la fecha más lejana a la más cercana. Si dos
        clientes tienen la misma fecha, se llama primero al que se registró antes.
        """
        candidatos = []
        for posicion, cliente in enumerate(self.clientes):
            if self.es_candidato_a_la_pila(cliente):
                candidatos.append((cliente.obtener_fecha(), posicion, cliente))

        # Orden descendente por (fecha, posición): el último en apilarse es el primero en salir
        candidatos.sort(key=lambda dato: (dato[0], dato[1]), reverse=True)

        self.pila_contingencia = Pila()
        for _, _, cliente in candidatos:
            self.pila_contingencia.apilar(cliente)

    def generar_informe_de_la_pila(self):
        """Arma el informe de la Pila para que en la clínica llamen a los clientes."""
        linea = "=" * 78
        lineas = [
            linea,
            f" INFORME DE LA PILA DE CONTINGENCIA - {self.nombre.upper()}",
            linea,
            f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Criterios: extracción dental + prioridad Urgente + cita pendiente",
            "Orden: fecha de la cita de la más cercana a la más lejana",
            "(el cliente nº 1 está en el TOPE de la pila: es el primero en ser llamado)",
            f"Total de clientes en la pila: {len(self.pila_contingencia)}",
            "",
        ]
        if self.pila_contingencia.esta_vacia():
            lineas.append("No hay clientes que cumplan los criterios.")
        else:
            lineas.append(f"{'Nº':<4}{'Cédula':<13}{'Nombre':<24}{'Teléfono':<13}{'Fecha cita':<12}{'Piezas':>6}")
            lineas.append("-" * 78)
            for numero, c in enumerate(self.pila_contingencia, start=1):  # del tope a la base, sin desapilar
                lineas.append(
                    f"{numero:<4}{c.cedula:<13}{c.nombre[:23]:<24}{c.telefono:<13}"
                    f"{c.fecha_cita:<12}{c.cantidad:>6}"
                )
        lineas.append(linea)
        return "\n".join(lineas)

    def guardar_informe_de_la_pila(self, texto):
        with open(ARCHIVO_INFORME, "w", encoding="utf-8") as archivo:
            archivo.write(texto + "\n")
        print("Informe guardado en informe_pila.txt")

    @staticmethod
    def _describir_extraccion(cliente):
        return (f"{cliente.nombre} (cédula {cliente.cedula}, tel. {cliente.telefono}) - "
                f"extracción de {cliente.cantidad} pieza(s), cita {cliente.fecha_cita}")

    def consultar_cliente_del_tope(self):
        if self.pila_contingencia.esta_vacia():
            print("No hay clientes en la pila.")
        else:
            print("Siguiente a llamar: " + self._describir_extraccion(self.pila_contingencia.ver_tope()))

    def atender_cliente_del_tope(self):
        if self.pila_contingencia.esta_vacia():
            print("No hay clientes en la pila para atender.")
            return
        cliente = self.pila_contingencia.desapilar()  # sale el que está en el tope
        cliente.marcar_como_atendido()
        self.guardar_clientes()
        print("Atendiendo al cliente: " + self._describir_extraccion(cliente))
        if self.pila_contingencia.esta_vacia():
            print("La pila quedó vacía: plan de contingencia completado.")
        else:
            print("Siguiente en la pila: " + self._describir_extraccion(self.pila_contingencia.ver_tope()))

    # ------------------------------------------------------------------
    # COLA de atención: agenda del consultorio
    # ------------------------------------------------------------------
    def generar_agenda(self):
        """Genera la Cola con los clientes pendientes.

        El orden de la agenda es: fecha de la cita (la más cercana primero) y,
        si hay empate, el orden en que se registraron los clientes.
        """
        pendientes = []
        for posicion, cliente in enumerate(self.clientes):
            if cliente.esta_pendiente():
                pendientes.append((cliente.obtener_fecha(), posicion, cliente))

        pendientes.sort(key=lambda dato: (dato[0], dato[1]))

        self.cola_agenda = Cola()
        for _, _, cliente in pendientes:
            self.cola_agenda.encolar(cliente)  # el primero en encolarse es el primero en ser atendido

    def agregar_cliente_a_cola(self, cliente):
        """Un cliente que llega entra por el final de la cola."""
        self.cola_agenda.encolar(cliente)

    @staticmethod
    def _describir_cita(cliente):
        return (f"{cliente.nombre} (cédula {cliente.cedula}) - {cliente.tipo_atencion} "
                f"x{cliente.cantidad}, cita {cliente.fecha_cita}, valor a pagar {cliente.valor_formateado()}")

    def atender_siguiente_cliente(self):
        if self.cola_agenda.esta_vacia():
            print("No hay clientes en la cola para atender.")
            return
        cliente = self.cola_agenda.desencolar()  # sale el que está en el frente
        cliente.marcar_como_atendido()
        self.guardar_clientes()
        print("Atendiendo al cliente: " + self._describir_cita(cliente))
        if self.cola_agenda.esta_vacia():
            print("La agenda quedó vacía: no hay más clientes en espera.")
        else:
            print("Siguiente en la agenda: " + self._describir_cita(self.cola_agenda.ver_frente()))

    def consultar_siguiente_cliente_en_la_cola(self):
        if self.cola_agenda.esta_vacia():
            print("No hay clientes en la cola.")
        else:
            print("El siguiente cliente en la cola es: " + self._describir_cita(self.cola_agenda.ver_frente()))

    def consultar_toda_la_cola_de_clientes(self):
        if self.cola_agenda.esta_vacia():
            print("La agenda está vacía: no hay clientes en espera.")
            return
        print(f"{'Turno':<7}{'Cédula':<12}{'Nombre':<22}{'Atención':<13}{'Cant.':<6}{'Prioridad':<10}{'Fecha':<12}")
        print("-" * 82)
        total_clientes_pendientes = 0
        total_valor_pendiente = 0
        for c in self.cola_agenda:  # del frente al final, sin desencolar
            total_clientes_pendientes += 1
            total_valor_pendiente = total_valor_pendiente + c.valor_total
            print(f"{total_clientes_pendientes:<7}{c.cedula:<12}{c.nombre[:21]:<22}{c.tipo_atencion:<13}"
                  f"{c.cantidad:<6}{c.prioridad:<10}{c.fecha_cita:<12}")
        print(f"Total de clientes en espera: {total_clientes_pendientes}")
        print(f"Total a recaudar: {formato_pesos(total_valor_pendiente)}")

    # ------------------------------------------------------------------
    # Persistencia en JSON
    # ------------------------------------------------------------------
    def guardar_clientes(self, ruta=ARCHIVO_DATOS):
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump([c.a_diccionario() for c in self.clientes], archivo, indent=2, ensure_ascii=False)

    def cargar_clientes(self, ruta=ARCHIVO_DATOS):
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.clientes = [Cliente.desde_diccionario(d) for d in datos]

    def cargar_datos_de_ejemplo(self):
        self.cargar_clientes(ARCHIVO_EJEMPLO)
        print(f"Se cargaron {len(self.clientes)} clientes de ejemplo (datos/clientes_ejemplo.json)")

    def cargar_datos_iniciales(self):
        """Carga datos_clientes.json si existe; si no, carga los datos de ejemplo."""
        if os.path.exists(ARCHIVO_DATOS):
            try:
                self.cargar_clientes(ARCHIVO_DATOS)
                print(f"Se cargaron {len(self.clientes)} clientes desde datos_clientes.json")
                return
            except (json.JSONDecodeError, OSError, KeyError, ValueError):
                print("ADVERTENCIA: no se pudo leer datos_clientes.json. Se usarán los datos de ejemplo.")
        self.cargar_datos_de_ejemplo()
