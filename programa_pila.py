"""
- Aplicación para un consultorio odontológico: plan de contingencia (Pila)
- Versión: v1.0
- Qué incluye:
    - Estructura dinámica: Pila (LIFO) implementada con nodos enlazados
    - Filtro de clientes: solo extracción dental + prioridad "Urgente" + cita pendiente
    - Ordenamiento por fecha: la fecha más cercana queda en el TOPE de la pila
    - Informe de la Pila (en pantalla y guardado en informe_pila.txt)
    - Atención de la Pila: se llama primero al cliente del tope (desapilar)
- Qué problemas/errores (BUGS) tiene:
    B-1. No se valida que la cédula no esté repetida entre clientes
    B-2. Las citas con fecha ya vencida también entran a la pila (no se
         compara contra la fecha de hoy)
"""

from consultorio import Consultorio


def ejecutar(consultorio):
    """Menú de la Pila. Trabaja sobre el consultorio que recibe."""
    consultorio.generar_pila_de_contingencia()
    print("\nSe generó la Pila de contingencia.")
    print(consultorio.generar_informe_de_la_pila())

    while True:
        print("\n--- Pila de contingencia ---")
        print("1. Consultar el informe de la Pila (y guardarlo en un archivo)")
        print("2. Consultar el cliente del tope (el siguiente a llamar)")
        print("3. Atender al cliente del tope (desapilar)")
        print("4. Ver cuántos clientes quedan en la Pila")
        print("0. Volver")
        opcion = input("Elija una opción: ").strip()

        if opcion == "1":
            informe = consultorio.generar_informe_de_la_pila()
            print(informe)
            consultorio.guardar_informe_de_la_pila(informe)
        elif opcion == "2":
            consultorio.consultar_cliente_del_tope()
        elif opcion == "3":
            consultorio.atender_cliente_del_tope()
        elif opcion == "4":
            print(f"Clientes en la Pila: {len(consultorio.pila_contingencia)}")
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
