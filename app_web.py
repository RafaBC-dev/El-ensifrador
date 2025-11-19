import streamlit as st
from encriptador import CifradoCompleto

st.set_page_config(page_title="Encriptador Pro", page_icon="🔐")
st.title("🔐 Encriptador Universal")

# Entrada de Clave
clave = st.text_input("🔑 Clave Secreta (Semilla):", type="password")
# Entrada de Mensaje
mensaje = st.text_area("📝 Mensaje:", height=150)

col1, col2 = st.columns(2)

with col1:
    if st.button("🔒 Cifrar", type="primary", use_container_width=True):
        if clave and mensaje:
            app = CifradoCompleto(clave)
            res = app.codificar(mensaje)
            st.success("Texto Cifrado:")
            st.code(res, language="text")
        else:
            st.warning("Falta clave o mensaje")

with col2:
    if st.button("🔓 Descifrar", use_container_width=True):
        if clave and mensaje:
            app = CifradoCompleto(clave)
            res = app.decodificar(mensaje)
            st.info("Texto Original:")
            st.code(res, language="text")
        else:
            st.warning("Falta clave o mensaje")