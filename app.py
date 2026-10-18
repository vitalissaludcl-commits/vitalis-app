import streamlit as st
import datetime

# Configuración de la página
st.set_page_config(page_title="Vitalis Salud - Asistente Clínico", page_icon="🩺", layout="wide")

st.title("🩺 Vitalis Salud: Asistente de Ficha Clínica por Voz")
st.markdown("---")

# --- BARRA LATERAL: CONFIGURACIÓN E HISTORIAL ---
with st.sidebar:
    st.header("⚙️ Configuración de Consulta")
    modalidad = st.radio("Modalidad de Atención:", ["Presencial", "Online"])
    
    plataforma = "N/A (Presencial)"
    if modalidad == "Online":
        plataforma = st.selectbox("Plataforma de Telemedicina:", ["Google Meet", "WhatsApp", "Zoom", "Microsoft Teams", "Otra"])
        st.info(f"💡 Asegúrate de permitir la captura de audio del sistema para {plataforma}.")
    
    st.markdown("---")
    st.header("📂 Historial de Consultas")
    # Simulación de historial guardado
    pacientes_guardados = ["Juan Pérez - 18/10/2026", "María González - 17/10/2026"]
    paciente_seleccionado = st.selectbox("Consultas anteriores guardadas:", ["-- Nuevo Registro --"] + pacientes_guardados)

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎙️ Control de Audio y Transcripción")
    
    # Datos básicos del paciente para el registro
    nombre_paciente = st.text_input("Nombre y Apellido del Paciente:", value="Juan Pérez" if paciente_seleccionado != "-- Nuevo Registro --" else "")
    edad_paciente = st.number_input("Edad:", min_value=0, max_value=120, value=35)
    
    st.markdown("### Controles de Grabación")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        btn_iniciar = st.button("🔴 Iniciar", use_container_width=True)
    with c2:
        btn_pausar = st.button("⏸️ Pausar", use_container_width=True)
    with c3:
        btn_terminar = st.button("⏹️ Terminar", use_container_width=True)
        
    estado_grabacion = st.empty()
    if btn_iniciar:
        estado_grabacion.success("Grabación en curso... (Capturando audio de la consulta)")
    elif btn_pausar:
        estado_grabacion.warning("Grabación pausada.")
    elif btn_terminar:
        estado_grabacion.info("Grabación finalizada. Listo para generar nota.")

    st.markdown("#### Transcripción Cruda (Diarización)")
    transcripcion_ejemplo = """[Médico]: Buenos días, cuénteme cuál es el motivo de su consulta el día de hoy.
[Paciente]: Hola doctor, amanecí con mucho dolor de cabeza y tos seca desde hace tres días.
[Médico]: Entiendo. ¿Ha presentado fiebre o algún otro síntoma?
[Paciente]: Sí, ayer en la tarde tuve 38.2 °C y me siento con bastante decaimiento."""
    
    texto_transcrito = st.text_area(
        "Transcripción en tiempo real / editable:", 
        value=transcripcion_ejemplo, 
        height=220
    )
    
    btn_generar_ficha = st.button("✨ Generar Ficha Clínica Estructurada", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 Resumen Estructurado (Evolución Médica)")
    
    if btn_generar_ficha or paciente_seleccionado != "-- Nuevo Registro --":
        # Aquí posteriormente conectaremos el modelo/API para procesar el texto automáticamente
        st.success("Ficha médica procesada correctamente.")
        
        tab1, tab2, tab3 = st.tabs(["Ficha Médica", "Receta / Indicaciones", "Certificado"])
        
        with tab1:
            st.markdown("### Ficha Clínica de Atención")
            
            anamnesis = st.text_area(
                "Anamnesis / Motivo de Consulta:",
                value="Paciente acude por cuadro de 3 días de evolución caracterizado por cefalea holocránea y tos seca. Refiere registro febril cuantificado en 38.2 °C el día de ayer, asociado a compromiso del estado general.",
                height=120
            )
            
            examen_fisico = st.text_area(
                "Examen Físico / Funciones Vitales:",
                value="Normotenso, febril al tacto. Orofaringe congestiva sin exudado. Auscultación pulmonar: Murmullo pulmonar presente, sin ruidos agregados.",
                height=100
            )
            
            diagnostico = st.text_input(
                "Hipótesis Diagnóstica / Diagnóstico:",
                value="Sindrome Febril / Cuadro Respiratorio Alto de probable etiología viral"
            )
            
        with tab2:
            st.markdown("### Plan de Tratamiento e Indicaciones")
            receta = st.text_area(
                "Receta Médica e Indicaciones al Paciente:",
                value="1. Paracetamol 500 mg: Tomar 1 comprimido cada 8 horas por 3 días en caso de dolor o fiebre.\n2. Reposo relativo por 48 horas e hidratación abundante.\n3. Acudir a servicio de urgencia en caso de dificultad respiratoria o fiebre persistente sobre 39 °C.",
                height=150
            )
            
        with tab3:
            st.markdown("### Certificado Médico / Licencia")
            tipo_cert = st.selectbox("Tipo de documento:", ["Certificado de Atención", "Reposo Médico", "Orden de Exámenes"])
            detalle_cert = st.text_area("Detalle del documento:", value="Se certifica la atención médica del paciente el día de hoy con indicación de reposo por 48 hrs.")

        st.markdown("---")
        btn_guardar = st.button("💾 Guardar Registro en Sistema", use_container_width=True)
        if btn_guardar:
            st.toast("✅ Registro guardado exitosamente.")
    else:
        st.info("👈 Haz clic en 'Generar Ficha Clínica Estructurada' para procesar el audio o la transcripción.")
