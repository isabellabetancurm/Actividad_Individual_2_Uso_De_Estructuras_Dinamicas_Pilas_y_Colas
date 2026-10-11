"""
Captura de datos por teclado con validación.

Cada dato se vuelve a preguntar hasta que sea válido (igual que en la v5.0
de la actividad 1) y se usa try/except para las conversiones numéricas y de fecha.
"""

import unicodedata
from datetime import date, datetime

from cliente import Cliente, PRIORIDADES, TIPOS_ATENCION, TIPOS_CLIENTE


def _sin_tildes(texto):
    """'Extracción' -> 'extraccion' (para aceptar el dato con o sin tilde)."""
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn").lower()


def pedir_texto(mensaje, nombre_campo):
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print(f"ERROR: {nombre_campo} no puede estar vacío")


def pedir_opcion(mensaje, opciones, nombre_campo):
    while True:
        valor = _sin_tildes(input(mensaje).strip())
        for opcion in opciones:
            if _sin_tildes(opcion) == valor:
                return opcion  # se devuelve la forma oficial (con tilde y mayúscula)
        print(f"ERROR: {nombre_campo} debe ser uno de: {', '.join(opciones)}")


def pedir_cantidad(mensaje):
    while True:
        try:  # Manejo de errores: si no es un número entero, int() lanza ValueError
            cantidad = int(input(mensaje).strip())
        except ValueError:
            print("ERROR: La cantidad debe ser un número entero")
            continue
        if cantidad <= 0:
            print("ERROR: La cantidad debe ser mayor que 0")
        else:
            return cantidad


def pedir_cedula(mensaje, cedulas_con_cita_pendiente):
    """La cédula identifica al cliente: no puede haber dos citas pendientes con la misma."""
    while True:
        valor = input(mensaje).strip()
        if valor == "":
            print("ERROR: La cédula no puede estar vacía")
        elif valor in cedulas_con_cita_pendiente:
            print("ERROR: Ya hay un cliente con una cita pendiente con esa cédula")
        else:
            return valor


def pedir_fecha(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            print("ERROR: La fecha debe tener el formato YYYY-MM-DD (ejemplo: 2026-10-15)")
            continue
        if fecha < date.today():
            print("ERROR: La fecha de la cita no puede ser anterior a hoy")
        else:
            return fecha.isoformat()  # se guarda siempre como YYYY-MM-DD


def pedir_hora(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            return datetime.strptime(texto, "%H:%M").strftime("%H:%M")  # se guarda siempre como HH:MM
        except ValueError:
            print("ERROR: La hora debe tener el formato HH:MM en 24 horas (ejemplo: 14:30)")


def capturar_cliente(cedulas_con_cita_pendiente=()):
    """Pide todos los datos de un cliente y devuelve un objeto Cliente."""
    print("\n--- Registro de nuevo cliente ---")
    cedula = pedir_cedula("Cédula: ", cedulas_con_cita_pendiente)
    nombre = pedir_texto("Nombre: ", "El nombre")
    telefono = pedir_texto("Teléfono: ", "El teléfono")
    tipo_cliente = pedir_opcion("Tipo de cliente (Particular, EPS, Prepagada): ", TIPOS_CLIENTE, "El tipo de cliente")
    tipo_atencion = pedir_opcion(
        "Tipo de atención (Limpieza, Calzas, Extracción, Diagnóstico): ", TIPOS_ATENCION, "El tipo de atención"
    )
    if tipo_atencion in ("Limpieza", "Diagnóstico"):
        cantidad = 1  # regla del enunciado de la actividad 1
        print("La cantidad se fija automáticamente en 1")
    else:
        cantidad = pedir_cantidad("Cantidad (piezas dentales): ")
    prioridad = pedir_opcion("Prioridad (Normal, Urgente): ", PRIORIDADES, "La prioridad")
    fecha_cita = pedir_fecha("Fecha de la cita (YYYY-MM-DD): ")
    hora_cita = pedir_hora("Hora de la cita (HH:MM, 24 horas): ")
    return Cliente(cedula, nombre, telefono, tipo_cliente, tipo_atencion,
                   cantidad, prioridad, fecha_cita, hora_cita)
