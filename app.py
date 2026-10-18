import streamlit as st
from streamlit_mic_recorder import mic_recorder
import google.genai as genai
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Vitalis Salud - Asistente Clínico", page_icon="🩺", layout="wide")

st.title("🩺 Vitalis Salud: Asistente de Ficha Clínica por Voz")
st.markdown("---")

# --- OBTENER LA CLAVE API DE FORMA AUTOMÁTICA DESDE LOS SECRETS ---
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]

# --- BARRA LATERAL: CONFIGURACIÓN E HISTORIAL ---
with st.sidebar:
    st.header("⚙️ Configuración de Consulta")
    modalidad = st.radio("Modalidad de Atención:", ["Presencial", "Online"])
    
    plataforma = "N/A (Presencial)"
    if modalidad == "Online":
        plataforma = st.selectbox("Plataforma de Telemedicina:", ["Google Meet", "WhatsApp", "Zoom", "Microsoft Teams", "Otra"])
        st.info(f"💡 Recuerda permitir la captura de audio del sistema para {plataforma}.")
    
    st.markdown("---")
    st.header("🔑 Estado de la Clave API")
    if api_key:
        st.success("✅ Clave API cargada de forma segura y permanente.")
    else:
        st.warning("⚠️ No se encontró la clave en los Secrets de Streamlit.")
        api_key = st.text_input("Ingresa tu Gemini API Key manualmente:", type="password")

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎙️ Grabación de Audio de la Consulta")
    
    nombre_paciente = st.text_input("Nombre y Apellido del Paciente:")
    edad_paciente = st.number_input("Edad:", min_value=0, max_value=120, value=30)
    
    st.write("Presiona el botón para **grabar la voz de la consulta**:")
    
    # Grabador de voz usando el micrófono del navegador
    audio_rec = mic_recorder(
        start_prompt="🔴 Iniciar Grabación",
        stop_prompt="⏹️ Detener Grabación",
        key='recorder'
    )
    
    audio_bytes = None
    if audio_rec:
        audio_bytes = audio_rec['bytes']
        st.audio(audio_bytes, format='audio/wav')
        st.success("✅ Audio grabado correctamente.")

    st.markdown("#### Transcripción / Notas Manuales")
    texto_manual = st.text_area(
        "Si prefieres dictar o escribir apuntes directamente:",
        height=150,
        placeholder="Escribe o pega aquí la conversación si no grabaste audio..."
    )
    
    btn_generar = st.button("✨ Generar Ficha Clínica con IA", type="primary", use_container_width=True)

with col2:
    st.subheader("📋 Ficha Clínica Estructurada por IA")
    
    if btn_generar:
        if not api_key:
            st.error("⚠️ Por favor configura tu **Gemini API Key** en los Secrets de Streamlit.")
        elif not audio_bytes and not texto_manual.strip():
            st.warning("⚠️ Debes **grabar audio** o **escribir notas** antes de generar la ficha.")
        else:
            with st.spinner("🧠 Analizando la consulta médica y estructurando la ficha..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    prompt_sistema = f"""
                    Eres un asistente médico experto de la empresa Vitalis Salud.
                    Tu tarea es analizar el audio/texto de la consulta del paciente {nombre_paciente} ({edad_paciente} años) y redactar una ficha clínica profesional.
                    
                    Estructura la respuesta de manera clara en las siguientes secciones:
                    1. Anamnesis / Motivo de Consulta
                    2. Examen Físico / Datos Clínicos
                    3. Diagnóstico / Hipótesis Diagnóstica
                    4. Plan de Tratamiento e Indicaciones Médicas
                    5. Certificado / Indicaciones de Reposo (si aplica)
                    """
                    
                    if audio_bytes:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=[
                                genai.types.Part.from_bytes(data=audio_bytes, mime_type='audio/wav'),
                                prompt_sistema
                            ]
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-3.8-flash',
                            contents=f"{prompt_sistema}\n\nTexto de la consulta:\n{texto_manual}"
                        )
                        
                    st.session_state['ficha_texto'] = response.text
                    
                except Exception as e:
                    st.error(f"Error al procesar con IA: {e}")

    if 'ficha_texto' in st.session_state and st.session_state['ficha_texto']:
        st.success("✅ Ficha clínica redactada con éxito:")
        st.markdown(st.session_state['ficha_texto'])
        
        # Botón para copiar directamente al portapapeles con JavaScript
        texto_limpio = st.session_state['ficha_texto'].replace('`', '\\`').replace('$', '\\$')
        components.html(f"""
            <button id="btnCopy" style="
                background-color: #0E1117;
                color: white;
                border: 1px solid #31333F;
                padding: 10px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                width: 100%;
                margin-top: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            ">📋 Copiar Ficha al Portapapeles</button>

            <script>
            document.getElementById('btnCopy').addEventListener('click', function() {{
                const textToCopy = `{texto_limpio}`;
                navigator.clipboard.writeText(textToCopy).then(function() {{
                    const btn = document.getElementById('btnCopy');
                    btn.innerText = "✅ ¡Copiado al Portapapeles!";
                    btn.style.backgroundColor = "#28a745";
                    setTimeout(function() {{
                        btn.innerText = "📋 Copiar Ficha al Portapapeles";
                        btn.style.backgroundColor = "#0E1117";
                    }}, 2000);
                }});
            }});
            </script>
        """, height=65)
