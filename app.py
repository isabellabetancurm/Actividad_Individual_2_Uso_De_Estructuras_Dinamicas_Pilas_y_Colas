"""
Consultorio Odontológico - Pilas y Colas (aplicación web con Streamlit)

Reutiliza exactamente las mismas clases que la versión de consola
(Cliente, Consultorio, Pila y Cola): lo único nuevo es cómo se muestran los datos.

Ejecutar con:  python -m streamlit run app.py
"""

from datetime import date

import streamlit as st

from cliente import Cliente, PRIORIDADES, TIPOS_ATENCION, TIPOS_CLIENTE, formato_pesos
from consultorio import Consultorio

st.set_page_config(page_title="Consultorio Odontológico - Pilas y Colas", page_icon="🦷", layout="wide")


# ---------------------------------------------------------------------------
# Estado de la sesión: el consultorio vive en memoria mientras la app está abierta
# ---------------------------------------------------------------------------
def iniciar():
    if "consultorio" not in st.session_state:
        consultorio = Consultorio("Consultorio Odontológico")
        consultorio.cargar_datos_iniciales()      # datos_clientes.json o, si no existe, los de ejemplo
        consultorio.generar_pila_de_contingencia()
        consultorio.generar_agenda()
        st.session_state.consultorio = consultorio
        st.session_state.mensaje = None
    return st.session_state.consultorio


def avisar(tipo, texto):
    """Guarda un mensaje para mostrarlo arriba en la siguiente carga de la página."""
    st.session_state.mensaje = (tipo, texto)


# ---------------------------------------------------------------------------
# Acciones de los botones (se ejecutan ANTES de volver a dibujar la página)
# ---------------------------------------------------------------------------
def accion_atender_tope():
    cliente = st.session_state.consultorio.atender_cliente_del_tope()  # desapilar
    if cliente is None:
        avisar("warning", "No hay clientes en la pila para atender.")
    else:
        avisar("success", f"Atendido desde la Pila: {cliente.nombre} (cédula {cliente.cedula}). "
                          "Salió del tope y también de la agenda.")


def accion_atender_siguiente():
    cliente = st.session_state.consultorio.atender_siguiente_cliente()  # desencolar
    if cliente is None:
        avisar("warning", "No hay clientes en la cola para atender.")
    else:
        avisar("success", f"Atendido desde la Cola: {cliente.nombre} (cédula {cliente.cedula}). "
                          "Salió del frente de la agenda.")


def accion_reiniciar():
    consultorio = st.session_state.consultorio
    consultorio.cargar_datos_de_ejemplo()
    consultorio.guardar_clientes()
    consultorio.generar_pila_de_contingencia()
    consultorio.generar_agenda()
    avisar("success", f"Se cargaron los {len(consultorio.clientes)} clientes de ejemplo.")


def accion_registrar_cliente():
    s = st.session_state
    cedula = s.f_cedula.strip()
    nombre = s.f_nombre.strip()
    telefono = s.f_telefono.strip()
    if cedula == "" or nombre == "" or telefono == "":
        avisar("error", "La cédula, el nombre y el teléfono no pueden estar vacíos.")
        return

    tipo_atencion = s.f_tipo_atencion
    if tipo_atencion in ("Limpieza", "Diagnóstico"):
        cantidad = 1  # regla del enunciado de la actividad 1
    else:
        cantidad = int(s.f_cantidad)

    cliente = Cliente(cedula, nombre, telefono, s.f_tipo_cliente, tipo_atencion,
                      cantidad, s.f_prioridad, s.f_fecha.isoformat())
    consultorio = s.consultorio
    consultorio.registrar_cliente(cliente)
    consultorio.agregar_cliente_a_cola(cliente)       # el cliente nuevo entra por el FINAL de la cola
    consultorio.generar_pila_de_contingencia()        # y entra a la pila si cumple los criterios

    texto = f"Cliente {nombre} registrado: turno nº {len(consultorio.cola_agenda)} de la cola"
    if consultorio.es_candidato_a_la_pila(cliente):
        texto += " y también entró a la Pila de contingencia."
    else:
        texto += "."
    avisar("success", texto)

    # Se limpian los campos del formulario
    s.f_cedula = ""
    s.f_nombre = ""
    s.f_telefono = ""
    s.f_cantidad = 1


# ---------------------------------------------------------------------------
# Tablas para mostrar las estructuras (se recorren SIN sacar a nadie)
# ---------------------------------------------------------------------------
def filas_pila(consultorio):
    clientes = list(consultorio.pila_contingencia)  # del tope a la base
    filas = []
    for i, c in enumerate(clientes):
        if i == 0:
            posicion = "⬆ TOPE"
        elif i == len(clientes) - 1:
            posicion = "BASE"
        else:
            posicion = "│"
        filas.append({"Posición": posicion, "Cédula": c.cedula, "Nombre": c.nombre,
                      "Teléfono": c.telefono, "Fecha cita": c.fecha_cita, "Piezas": c.cantidad})
    return filas


def filas_cola(consultorio):
    clientes = list(consultorio.cola_agenda)  # del frente al final
    filas = []
    for i, c in enumerate(clientes):
        if i == 0:
            turno = "1 · FRENTE"
        elif i == len(clientes) - 1:
            turno = f"{i + 1} · FINAL"
        else:
            turno = str(i + 1)
        filas.append({"Turno": turno, "Cédula": c.cedula, "Nombre": c.nombre, "Atención": c.tipo_atencion,
                      "Cant.": c.cantidad, "Prioridad": c.prioridad, "Fecha cita": c.fecha_cita,
                      "Valor": c.valor_formateado()})
    return filas


def filas_clientes(consultorio):
    return [{"Cédula": c.cedula, "Nombre": c.nombre, "Tipo de cliente": c.tipo_cliente,
             "Atención": c.tipo_atencion, "Cant.": c.cantidad, "Prioridad": c.prioridad,
             "Fecha cita": c.fecha_cita, "Estado": c.estado, "Valor": c.valor_formateado()}
            for c in consultorio.clientes]


# ---------------------------------------------------------------------------
# Página
# ---------------------------------------------------------------------------
consultorio = iniciar()

st.title("🦷 Consultorio Odontológico — Pilas y Colas")
st.caption("Actividad Individual N° 2 · Programación II")

if st.session_state.mensaje is not None:
    tipo, texto = st.session_state.mensaje
    getattr(st, tipo)(texto)  # st.success / st.warning / st.error
    st.session_state.mensaje = None

# --- Barra lateral: registrar clientes y reiniciar ---------------------------
with st.sidebar:
    st.header("➕ Registrar cliente")
    st.caption("El cliente nuevo entra por el final de la cola y, si es una extracción urgente, también a la pila.")
    with st.form("form_cliente"):
        st.text_input("Cédula", key="f_cedula")
        st.text_input("Nombre", key="f_nombre")
        st.text_input("Teléfono", key="f_telefono")
        st.selectbox("Tipo de cliente", TIPOS_CLIENTE, key="f_tipo_cliente")
        st.selectbox("Tipo de atención", TIPOS_ATENCION, key="f_tipo_atencion")
        st.number_input("Cantidad de piezas (solo Calzas y Extracción)", min_value=1, step=1,
                        key="f_cantidad")  # sin 'value': por defecto arranca en el mínimo (1)
        st.selectbox("Prioridad", PRIORIDADES, key="f_prioridad")
        st.date_input("Fecha de la cita", value=date.today(), key="f_fecha")
        st.form_submit_button("Registrar cliente", type="primary", key="f_enviar",
                              on_click=accion_registrar_cliente)
    st.caption("Para Limpieza y Diagnóstico la cantidad se fija en 1.")

    st.divider()
    st.button("🔄 Reiniciar con los datos de ejemplo", key="btn_reiniciar", on_click=accion_reiniciar)
    st.caption("Reemplaza los clientes actuales por los 9 de ejemplo.")

# --- Pestañas ----------------------------------------------------------------
tab_clientes, tab_pila, tab_cola = st.tabs(
    ["📋 Clientes", "📚 Pila de contingencia", "🗓️ Cola de atención (agenda)"]
)

# Pestaña 1: todos los clientes
with tab_clientes:
    st.subheader("Clientes registrados")
    pendientes = sum(1 for c in consultorio.clientes if c.esta_pendiente())
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de clientes", len(consultorio.clientes))
    m2.metric("Pendientes", pendientes)
    m3.metric("Atendidos", len(consultorio.clientes) - pendientes)
    if consultorio.clientes:
        st.dataframe(filas_clientes(consultorio), hide_index=True)
    else:
        st.info("Aún no hay clientes registrados.")

# Pestaña 2: la Pila
with tab_pila:
    pila = consultorio.pila_contingencia
    st.subheader("Plan de contingencia: extracciones urgentes")
    st.caption("Entran solo los clientes con **extracción dental**, prioridad **Urgente** y cita **pendiente**. "
               "Se apilan de la fecha más lejana a la más cercana, así la cita más próxima queda en el "
               "**tope** y es la primera en ser llamada (LIFO: el último en entrar es el primero en salir).")

    p1, p2 = st.columns(2)
    p1.metric("Clientes en la pila", len(pila))
    if pila.esta_vacia():
        p2.metric("Siguiente a llamar (tope)", "—")
        st.info("No hay clientes en la pila. Registra una extracción urgente en la barra lateral "
                "o reinicia con los datos de ejemplo.")
    else:
        p2.metric("Siguiente a llamar (tope)", pila.ver_tope().nombre)
        st.dataframe(filas_pila(consultorio), hide_index=True)

    st.button("✅ Atender al cliente del tope (desapilar)", key="btn_atender_pila", type="primary",
              on_click=accion_atender_tope, disabled=pila.esta_vacia())

    informe = consultorio.generar_informe_de_la_pila()
    with st.expander("📄 Ver informe de la Pila"):
        st.code(informe, language=None)
    st.download_button("⬇️ Descargar informe (.txt)", data=informe, file_name="informe_pila.txt",
                       mime="text/plain", key="btn_descargar_informe")

# Pestaña 3: la Cola
with tab_cola:
    cola = consultorio.cola_agenda
    st.subheader("Agenda del consultorio")
    st.caption("Los clientes pendientes se atienden en estricto orden de la agenda: por fecha de cita y, a igual "
               "fecha, por orden de registro. Quien llega nuevo entra al final "
               "(FIFO: el primero en entrar es el primero en salir).")

    total_a_recaudar = sum(c.valor_total for c in cola)
    c1, c2, c3 = st.columns(3)
    c1.metric("Clientes en espera", len(cola))
    c2.metric("Total a recaudar", formato_pesos(total_a_recaudar))
    if cola.esta_vacia():
        c3.metric("Siguiente (frente)", "—")
        st.info("La agenda está vacía: no hay clientes en espera.")
    else:
        c3.metric("Siguiente (frente)", cola.ver_frente().nombre)
        st.dataframe(filas_cola(consultorio), hide_index=True)

    st.button("✅ Atender al siguiente cliente (desencolar)", key="btn_atender_cola", type="primary",
              on_click=accion_atender_siguiente, disabled=cola.esta_vacia())
