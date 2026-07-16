import streamlit as st
from PIL import Image
import requests
import json
import datetime
import io
import base64

PROJECT_ID = "mi-chat-web-96461"
API_KEY = "AIzaSyBXJkeRy1yKwVyyipA80BmBGLmO9QTjTjY"
FIREBASE_URL = "https://firebaseio.com"

st.set_page_config(page_title="Chat Privado", page_icon="🔒", layout="centered")

# --- CONTROL DE INICIO DE SESIÓN ---
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔒 Iniciar Sesión en el Chat")
    st.write("Por favor, ingresa tus credenciales para acceder.")
    
    # Formulario de login
    usuario_input = st.text_input("Usuario:")
    contrasena_input = st.text_input("Contraseña:", type="password")
    boton_login = st.button("Ingresar al Chat")
    
    if boton_login:
        # AQUÍ PUEDES CAMBIAR EL USUARIO Y CONTRASEÑA QUE TÚ QUIERAS
        if (usuario_input == "sebastian" and contrasena_input == "12345") or (usuario_input == "amigo" and contrasena_input == "54321"):
            st.session_state["autenticado"] = True
            st.session_state["nombre_usuario"] = usuario_input
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")
            
    st.stop() # Detiene el código aquí si no está autenticado

# --- CÓDIGO DEL CHAT DE FIREBASE (SOLO CORRE SI YA INICIÓ SESIÓN) ---
nombre_usuario = st.session_state["nombre_usuario"]
st.title(f"💬 Chat Privado - Bienvenido, {nombre_usuario}")

# Botón para cerrar sesión si lo deseas
if st.sidebar.button("🚪 Cerrar Sesión"):
    st.session_state["autenticado"] = False
    st.rerun()

def obtener_mensajes():
    try:
        respuesta = requests.get(FIREBASE_URL, timeout=5)
        if respuesta.status_code == 200 and respuesta.json():
            return respuesta.json()
        return {}
    except:
        return {}

def enviar_mensaje(usuario, texto, foto_archivo):
    hora = datetime.datetime.now().strftime("%H:%M")
    imagen_base64 = ""
    
    if foto_archivo is not None:
        try:
            img = Image.open(foto_archivo)
            img.thumbnail((300, 300))
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

mensajes_nube = obtener_mensajes()
if mensajes_nube:
    for key, msg in mensajes_nube.items():
        if isinstance(msg, dict) and "usuario" in msg:
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

with st.form("enviar_bloque", clear_on_submit=True):
    nuevo_texto = st.text_input("Escribe tu mensaje:")
    foto = st.file_uploader("Sube una foto:", type=["png", "jpg", "jpeg"])
    boton_enviar = st.form_submit_button("Enviar Mensaje")

if boton_enviar and (nuevo_texto or foto):
    enviar_mensaje(nombre_usuario, nuevo_texto, foto)
    st.rerun()

if st.button("🔄 Actualizar Chat"):
    st.rerun()
