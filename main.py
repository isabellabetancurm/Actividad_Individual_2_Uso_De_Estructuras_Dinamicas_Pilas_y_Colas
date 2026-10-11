"""
- Aplicación para un consultorio odontológico (Actividad Individual N° 2)
- Versión: v1.0
- Qué incluye:
    - Clases: Cliente (el dato) y Consultorio (administra la Pila y la Cola)
    - Registro de clientes con validación y manejo de errores (de la actividad 1)
    - Pila de contingencia: extracciones urgentes, por fecha (programa_pila.py)
    - Cola de atención: agenda del consultorio (programa_cola.py)
    - Persistencia de los clientes en datos_clientes.json
    - Validaciones al registrar: cédula sin cita pendiente repetida, fecha no
      anterior a hoy y hora en formato HH:MM
- Qué problemas/errores (BUGS) tiene:
    Ninguno conocido.
"""

import programa_cola
import programa_pila
from consultorio import Consultorio
from entradas import capturar_cliente


def main():
    consultorio = Consultorio("Consultorio Odontológico")
    consultorio.cargar_datos_iniciales()

    while True:
        print("\n=== CONSULTORIO ODONTOLÓGICO - PILAS Y COLAS ===")
        print("1. Registrar un cliente")
        print("2. Consultar todos los clientes registrados")
        print("3. Cargar datos de ejemplo (reemplaza los clientes actuales)")
        print("4. Plan de contingencia: Pila de extracciones urgentes")
        print("5. Agenda del consultorio: Cola de atención")
        print("0. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            consultorio.registrar_cliente(capturar_cliente(consultorio.cedulas_con_cita_pendiente()))
            print("Cliente registrado y guardado.")
        elif opcion == "2":
            print()
            consultorio.consultar_todos_los_clientes()
        elif opcion == "3":
            confirmar = input("Esto reemplaza los clientes actuales. ¿Continuar? (s/n): ").strip().lower()
            if confirmar == "s":
                consultorio.cargar_datos_de_ejemplo()
                consultorio.guardar_clientes()
        elif opcion == "4":
            programa_pila.ejecutar(consultorio)
        elif opcion == "5":
            programa_cola.ejecutar(consultorio)
        elif opcion == "0":
            print("Hasta pronto.")
            break
        else:
            print("ERROR: Opción no válida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # Ctrl+C: salir sin mostrar un error feo
        print("\nPrograma finalizado.")
