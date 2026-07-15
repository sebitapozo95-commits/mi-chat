import streamlit as st
import requests
import json
import datetime

# --- TUS CLAVES REALES DE FIREBASE ---
PROJECT_ID = "mi-chat-web-96461"
API_KEY = "AIzaSyBXJkeRy1yKwVyyipA80BmBGLmO9QTjTjY"

# Dirección URL exacta corregida con tu base de datos de la imagen
FIREBASE_URL = "https://firebaseio.com"

st.set_page_config(page_title="Chat Global", page_icon="💬", layout="centered")
st.title("💬 Nuestro Chat en Tiempo Real")

# Casilla obligatoria para el Nombre de Usuario
nombre_usuario = st.text_input("Tu Nombre de Usuario:", value="Sebastian")

# 1. FUNCIÓN PARA LEER MENSAJES DESDE LA NUBE
def obtener_mensajes():
    try:
        respuesta = requests.get(FIREBASE_URL, timeout=5)
        if respuesta.status_code == 200 and respuesta.json():
            return respuesta.json()
        return {}
    except:
        return {}

# 2. FUNCIÓN PARA ENVIAR UN NUEVO MENSAJE A LA NUBE
def enviar_mensaje(usuario, texto):
    hora = datetime.datetime.now().strftime("%H:%M")
    datos = {
        "usuario": usuario,
        "texto": texto,
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
        with st.chat_message("user" if msg["usuario"] == nombre_usuario else "assistant"):
            st.write(f"**{msg['usuario']}** [{msg['hora']}]: {msg['texto']}")

# Formulario de entrada
with st.form("enviar_bloque", clear_on_submit=True):
    nuevo_texto = st.text_input("Escribe tu mensaje:")
    boton_enviar = st.form_submit_button("Enviar Mensaje")

if boton_enviar and nuevo_texto:
    enviar_mensaje(nombre_usuario, nuevo_texto)
    st.rerun()

# Botón manual para actualizar la pantalla y ver lo que escribió el otro
if st.button("🔄 Actualizar Chat"):
    st.rerun()
