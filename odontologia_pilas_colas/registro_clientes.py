"""
Módulo compartido por los programas del consultorio odontológico.

Se encarga de:
  - la tabla de precios y las opciones válidas
  - capturar un cliente con validación (cada campo se vuelve a preguntar
    hasta que el dato sea válido, igual que en la v5.0 de la actividad 1)
  - cargar y guardar los clientes en un archivo JSON
"""

import json
import os
import unicodedata
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DATOS = os.path.join(BASE_DIR, "datos_clientes.json")
ARCHIVO_EJEMPLO = os.path.join(BASE_DIR, "datos", "clientes_ejemplo.json")

PRECIOS = {
    "Particular": {"valor_cita": 80000, "Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
    "EPS": {"valor_cita": 5000, "Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
    "Prepagada": {"valor_cita": 30000, "Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0},
}
TIPOS_CLIENTE = list(PRECIOS.keys())
TIPOS_ATENCION = ["Limpieza", "Calzas", "Extracción", "Diagnóstico"]
PRIORIDADES = ["Normal", "Urgente"]


# ---------------------------------------------------------------------------
# Utilidades de formato y fechas
# ---------------------------------------------------------------------------
def formato_pesos(valor):
    """280000 -> '$280.000'"""
    return "$" + f"{valor:,}".replace(",", ".")


def convertir_fecha(texto):
    """Convierte 'YYYY-MM-DD' en un objeto date (para poder comparar fechas)."""
    return datetime.strptime(texto, "%Y-%m-%d").date()


def _sin_tildes(texto):
    """'Extracción' -> 'extraccion' (para aceptar el dato con o sin tilde)."""
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn").lower()


# ---------------------------------------------------------------------------
# Entradas validadas: cada una repite la pregunta hasta que el dato sea válido
# ---------------------------------------------------------------------------
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


def pedir_fecha(mensaje):
    while True:
        texto = input(mensaje).strip()
        try:
            return convertir_fecha(texto).isoformat()  # se guarda siempre como YYYY-MM-DD
        except ValueError:
            print("ERROR: La fecha debe tener el formato YYYY-MM-DD (ejemplo: 2026-10-15)")


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
def crear_cliente(cedula, nombre, telefono, tipo_cliente, tipo_atencion, cantidad, prioridad, fecha_cita):
    """Arma el diccionario de un cliente y calcula el valor a pagar.

    Valor = valor de la cita + (valor de la atención * cantidad)
    """
    valor_total = PRECIOS[tipo_cliente]["valor_cita"] + PRECIOS[tipo_cliente][tipo_atencion] * cantidad
    return {
        "cedula": cedula,
        "nombre": nombre,
        "telefono": telefono,
        "tipo_cliente": tipo_cliente,
        "tipo_atencion": tipo_atencion,
        "cantidad": cantidad,
        "prioridad": prioridad,
        "fecha_cita": fecha_cita,
        "valor_total": valor_total,
        "estado": "Pendiente",  # pasa a "Atendido" cuando el cliente es atendido
    }


def capturar_cliente():
    print("\n--- Registro de nuevo cliente ---")
    cedula = pedir_texto("Cédula: ", "La cédula")
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
    return crear_cliente(cedula, nombre, telefono, tipo_cliente, tipo_atencion, cantidad, prioridad, fecha_cita)


def mostrar_clientes(clientes):
    if len(clientes) == 0:
        print("No hay clientes registrados.")
        return
    print(f"{'Nº':<4}{'Cédula':<12}{'Nombre':<22}{'Atención':<13}{'Cant.':<6}"
          f"{'Prioridad':<10}{'Fecha':<12}{'Estado':<10}{'Valor':>11}")
    print("-" * 100)
    for numero, c in enumerate(clientes, start=1):
        print(f"{numero:<4}{c['cedula']:<12}{c['nombre'][:21]:<22}{c['tipo_atencion']:<13}{c['cantidad']:<6}"
              f"{c['prioridad']:<10}{c['fecha_cita']:<12}{c['estado']:<10}{formato_pesos(c['valor_total']):>11}")


# ---------------------------------------------------------------------------
# Persistencia en JSON
# ---------------------------------------------------------------------------
def cargar_clientes(ruta=ARCHIVO_DATOS):
    with open(ruta, "r", encoding="utf-8") as archivo:
        clientes = json.load(archivo)
    for cliente in clientes:
        cliente.setdefault("estado", "Pendiente")
    return clientes


def guardar_clientes(clientes, ruta=ARCHIVO_DATOS):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=2, ensure_ascii=False)


def preparar_clientes():
    """Carga datos_clientes.json si existe; si no, carga los datos de ejemplo."""
    if os.path.exists(ARCHIVO_DATOS):
        try:
            clientes = cargar_clientes(ARCHIVO_DATOS)
            print(f"Se cargaron {len(clientes)} clientes desde datos_clientes.json")
            return clientes
        except (json.JSONDecodeError, OSError):
            print("ADVERTENCIA: no se pudo leer datos_clientes.json. Se usarán los datos de ejemplo.")
    clientes = cargar_clientes(ARCHIVO_EJEMPLO)
    print(f"Se cargaron {len(clientes)} clientes de ejemplo (datos/clientes_ejemplo.json)")
    return clientes
