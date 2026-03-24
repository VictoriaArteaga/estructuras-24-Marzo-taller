import streamlit as st
import pandas as pd
from structures.TriageManager import TriageManager
from structures.Patient import Patient

st.set_page_config(
    page_title="Dashboard de Triage",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stMetric { background-color: #f0f2f6; padding: 15px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

manager = TriageManager()

st.title("Sistema de Triage - Hospital Central")
st.markdown("---")

with st.sidebar:
    st.header("Panel Medico")
    st.markdown("Acciones de atencion y control.")
    
    if st.button("Llamar Siguiente Paciente", type="primary", use_container_width=True):
        patient = manager.dispatchPatient()
        if patient:
            st.success(f"Llamando a consultorio: {patient.fullName}")
        else:
            st.warning("No hay pacientes en la sala de espera.")
            
    if st.button("Deshacer Ultima Atencion", use_container_width=True):
        restored_patient = manager.UndoLastDispatch()
        if restored_patient:
            st.info(f"Registro revertido para: {restored_patient.fullName}")
        else:
            st.warning("El historial de atencion esta vacio.")

    counts = manager.getCounts()
    st.divider()
    st.metric(label="Pacientes Nivel Alto", value=counts["high"])
    st.metric(label="Pacientes Nivel Medio", value=counts["medium"])
    st.metric(label="Pacientes Nivel Bajo", value=counts["low"])
    st.metric(label="Total Atendidos Hoy", value=counts["history"])

tab_registration, tab_monitor = st.tabs(["Admision y Registro", "Monitor de Sala de Espera"])

with tab_registration:
    st.subheader("Registrar Nuevo Ingreso")
    
    with st.form("patient_registration", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Nombre Completo del Paciente")
            patient_age = st.number_input("Edad", min_value=0, max_value=120)
            
        with col2:
            priority_map = {
                "Prioridad Alta (Rojo / Naranja)": "High",
                "Prioridad Media (Amarillo)": "Medium",
                "Prioridad Baja (Verde / Azul)": "Low"
            }
            triage_selection = st.selectbox(
                "Clasificacion de Triage", 
                options=list(priority_map.keys())
            )
            
        submit_button = st.form_submit_button("Guardar Registro", type="primary")
        
        if submit_button:
            if patient_name:
                priority_level = priority_map[triage_selection]
                new_patient = Patient(patient_name, patient_age, priority_level)
                manager.registerPatient(new_patient)
                st.success(f"Ingreso confirmado para {patient_name}.")
            else:
                st.error("El nombre del paciente es obligatorio para el registro.")

with tab_monitor:
    st.subheader("Pacientes Aguardando Atencion")
    
    system_state = manager.getSystemState()
    all_waiting = system_state["high"] + system_state["medium"] + system_state["low"]
    
    if all_waiting:
        waiting_data = []
        for p in all_waiting:
            waiting_data.append({
                "Nombre del Paciente": p.fullName,
                "Edad": p.age,
                "Nivel Asignado": p.priorityLevel
            })
        
        df_waiting = pd.DataFrame(waiting_data)
        st.dataframe(
            df_waiting, 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.info("No se registran pacientes en espera en este momento.")
        
    st.markdown("---")
    st.subheader("Historial de Pacientes Atendidos")
    
    if system_state["history"]:
        history_data = []
        for p in reversed(system_state["history"]):
            history_data.append({
                "Nombre del Paciente": p.fullName,
                "Edad": p.age,
                "Nivel Asignado": p.priorityLevel
            })
            
        df_history = pd.DataFrame(history_data)
        st.dataframe(
            df_history,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aun no se han procesado atenciones en el sistema.")