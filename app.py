import streamlit as st
from PIL import Image
import requests
import json
import datetime
import io
import base64

# --- TUS CLAVES REALES DE FIREBASE ---
PROJECT_ID = "mi-chat-web-96461"
API_KEY = "AIzaSyBXJkeRy1yKwVyyipA80BmBGLmO9QTjTjY"

# Dirección URL exacta corregida con tu base de datos de Firebase
FIREBASE_URL = f"https://{PROJECT_ID}://firebaseio.com"

st.set_page_config(page_title="Chat Global Completo", page_icon="💬", layout="centered")
st.title("💬 Nuestro Chat con Texto y Fotos")

# Casilla obligatoria para el Nombre de Usuario
nombre_usuario = st.text_input("Tu Nombre de Usuario:", value="Sebastian")

# 1. FUNCIÓN PARA LEER MENSAJES Y FOTOS DESDE LA NUBE
def obtener_mensajes():
    try:
        respuesta = requests.get(FIREBASE_URL, timeout=5)
        if respuesta.status_code == 200 and respuesta.json():
            return respuesta.json()
        return {}
    except:
        return {}

# 2. FUNCIÓN PARA ENVIAR TEXTO E IMAGEN A LA NUBE
def enviar_mensaje(usuario, texto, foto_archivo):
    hora = datetime.datetime.now().strftime("%H:%M")
    imagen_base64 = ""
    
    # Si el usuario subió una foto, la convertimos a texto para guardarla en Firebase
    if foto_archivo is not None:
        try:
            img = Image.open(foto_archivo)
            # Redimensionar un poco la imagen para que suba rápido a internet
            img.thumbnail((400, 400))
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            imagen_base64 = base64.b64encode(buffer.getvalue()).decode()
        except:
            pass

    datos = {
        "usuario": usuario,
        "texto": texto,
        "imagen": imagen_base64,
        "hora": hora
    }
    try:
        requests.post(FIREBASE_URL, data=json.dumps(datos), timeout=5)
    except:
        pass

# Mostrar los mensajes actuales en la pantalla
mensajes_nube = obtener_mensajes()
if mensajes_nube:
    for key, msg in mensajes_nube.items():
        rol = "user" if msg["usuario"] == nombre_usuario else "assistant"
        with st.chat_message(rol):
            st.write(f"**{msg['usuario']}** [{msg['hora']}]:")
            if msg.get("texto"):
                st.write(msg["texto"])
            if msg.get("imagen"):
                try:
                    img_data = base64.b64decode(msg["imagen"])
                    st.image(io.BytesIO(img_data), width=250)
                except:
                    pass

# Formulario de entrada (¡Aquí vuelve a aparecer la opción de fotos!)
with st.form("enviar_bloque", clear_on_submit=True):
    nuevo_texto = st.text_input("Escribe tu mensaje:")
    foto = st.file_uploader("Sube una foto:", type=["png", "jpg", "jpeg"])
    boton_enviar = st.form_submit_button("Enviar Mensaje")

if boton_enviar and (nuevo_texto or foto):
    enviar_mensaje(nombre_usuario, nuevo_texto, foto)
    st.rerun()

# Botón manual para actualizar la pantalla y ver lo que escribió el otro desde su casa
if st.button("🔄 Actualizar Chat"):
    st.rerun()
