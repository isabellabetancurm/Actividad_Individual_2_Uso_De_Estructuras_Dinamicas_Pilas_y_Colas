"""
Modelo de datos del consultorio: la tabla de precios y la clase Cliente
(equivale a la clase Usuario del ejemplo de la tienda).
"""

from datetime import datetime

PRECIOS = {
    "Particular": {"valor_cita": 80000, "Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
    "EPS": {"valor_cita": 5000, "Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
    "Prepagada": {"valor_cita": 30000, "Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0},
}
TIPOS_CLIENTE = list(PRECIOS.keys())
TIPOS_ATENCION = ["Limpieza", "Calzas", "Extracción", "Diagnóstico"]
PRIORIDADES = ["Normal", "Urgente"]


def formato_pesos(valor):
    """280000 -> '$280.000'"""
    return "$" + f"{valor:,}".replace(",", ".")


class Cliente:

    def __init__(self, cedula, nombre, telefono, tipo_cliente, tipo_atencion,
                 cantidad, prioridad, fecha_cita, estado="Pendiente"):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_cliente = tipo_cliente
        self.tipo_atencion = tipo_atencion
        self.cantidad = cantidad
        self.prioridad = prioridad
        self.fecha_cita = fecha_cita  # texto con formato YYYY-MM-DD
        self.estado = estado          # "Pendiente" o "Atendido"
        self.valor_total = self.calcular_valor_total()

    def calcular_valor_total(self):
        """Valor a pagar = valor de la cita + (valor de la atención * cantidad)."""
        valor_cita = PRECIOS[self.tipo_cliente]["valor_cita"]
        valor_atencion = PRECIOS[self.tipo_cliente][self.tipo_atencion]
        return valor_cita + (valor_atencion * self.cantidad)

    def obtener_fecha(self):
        """Devuelve la fecha de la cita como objeto date (para poder compararla)."""
        return datetime.strptime(self.fecha_cita, "%Y-%m-%d").date()

    def esta_pendiente(self):
        return self.estado == "Pendiente"

    def marcar_como_atendido(self):
        self.estado = "Atendido"

    def valor_formateado(self):
        return formato_pesos(self.valor_total)

    def a_diccionario(self):
        """Convierte el cliente en un diccionario para guardarlo en JSON."""
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "tipo_cliente": self.tipo_cliente,
            "tipo_atencion": self.tipo_atencion,
            "cantidad": self.cantidad,
            "prioridad": self.prioridad,
            "fecha_cita": self.fecha_cita,
            "valor_total": self.valor_total,
            "estado": self.estado,
        }

    @staticmethod
    def desde_diccionario(datos):
        """Crea un Cliente a partir de un diccionario leído del JSON."""
        return Cliente(
            datos["cedula"], datos["nombre"], datos["telefono"],
            datos["tipo_cliente"], datos["tipo_atencion"], datos["cantidad"],
            datos["prioridad"], datos["fecha_cita"], datos.get("estado", "Pendiente"),
        )
