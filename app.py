import streamlit as st
from PIL import Image

st.title("💬 Mi Chat con Imágenes")

# Inicializar historial
if "historial" not in st.session_state:
    st.session_state.historial = []

# Dibujar chat previo
for chat in st.session_state.historial:
    with st.chat_message(chat["rol"]):
        if chat["texto"]: st.write(chat["texto"])
        if chat["imagen"]: st.image(chat["imagen"], width=250)

# Formulario de entrada
with st.form("enviar_mensaje", clear_on_submit=True):
    texto = st.text_input("Escribe un mensaje:")
    foto = st.file_uploader("Sube una foto:", type=["png", "jpg", "jpeg"])
    enviar = st.form_submit_button("Enviar")

if enviar and (texto or foto):
    img = Image.open(foto) if foto else None
    st.session_state.historial.append({"rol": "user", "texto": texto, "imagen": img})
    st.rerun()
