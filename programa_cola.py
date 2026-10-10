"""
- Aplicación para un consultorio odontológico: agenda de atención (Cola)
- Versión: v1.0
- Qué incluye:
    - Estructura dinámica: Cola (FIFO) implementada con nodos enlazados
    - Agenda: los clientes pendientes quedan en la cola por fecha de cita
      (la más cercana primero) y, a igual fecha, por orden de registro
    - Atención en estricto orden de la agenda (desencolar)
    - Llegada de clientes nuevos: se agregan al final de la cola (encolar)
- Qué problemas/errores (BUGS) tiene:
    B-1. No se valida que la cédula no esté repetida entre clientes
    B-2. La agenda no maneja horas, solo fechas: dentro de un mismo día el
         orden es el de registro
"""

from consultorio import Consultorio
from entradas import capturar_cliente


def ejecutar(consultorio):
    """Menú de la Cola. Trabaja sobre el consultorio que recibe."""
    consultorio.generar_agenda()
    print("\nSe generó la agenda del consultorio.")
    consultorio.consultar_toda_la_cola_de_clientes()

    while True:
        print("\n--- Agenda: cola de atención ---")
        print("1. Registrar la llegada de un cliente nuevo (va al final de la cola)")
        print("2. Atender al siguiente cliente de la cola")
        print("3. Consultar el siguiente cliente en la cola")
        print("4. Consultar toda la cola de clientes (la agenda)")
        print("0. Volver")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            print("Vamos a registrar un cliente en la cola")
            cliente = capturar_cliente()
            consultorio.registrar_cliente(cliente)          # queda guardado en la lista de clientes
            consultorio.agregar_cliente_a_cola(cliente)     # y entra por el final de la cola
            print(f"Cliente registrado. Quedó en el turno nº {len(consultorio.cola_agenda)} de la agenda.")
        elif opcion == "2":
            consultorio.atender_siguiente_cliente()
        elif opcion == "3":
            consultorio.consultar_siguiente_cliente_en_la_cola()
        elif opcion == "4":
            consultorio.consultar_toda_la_cola_de_clientes()
        elif opcion == "0":
            break
        else:
            print("ERROR: Opción no válida")


def main():
    consultorio = Consultorio("Consultorio Odontológico")
    consultorio.cargar_datos_iniciales()
    ejecutar(consultorio)


if __name__ == "__main__":
    main()
