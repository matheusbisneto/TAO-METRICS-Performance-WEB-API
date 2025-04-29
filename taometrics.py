import streamlit as st
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Tao Metrics", layout="centered", initial_sidebar_state="collapsed")

# Remover a barra lateral usando CSS para esconder completamente
st.markdown("""
    <style>
        .css-1d391kg {display: none;} /* Esconde a barra lateral */
        .css-18e3p5e {display: none;} /* Esconde o botão de abrir a barra lateral */
    </style>
""", unsafe_allow_html=True)

# Título e descrição
st.title("Bem-vindo ao Tao Metrics 🎯")
st.subheader("Seu analista de engajamento")

st.markdown("---")

# Ícones das plataformas
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔴 YouTube"):
        st.switch_page("pages/taoyoutube.py")
with col2:
    if st.button("📸 Instagram"):
        st.info("Em breve...")
with col3:
    if st.button("🎵 TikTok"):
        st.info("Em breve...")

st.markdown("---")

# Barra de pesquisa (apenas ilustrativa agora)
pesquisa = st.text_input("🔎 Pesquise o nome do influenciador...")
if pesquisa:
    st.success(f"Buscando dados para: **{pesquisa}** (Selecione primeiro a plataforma)")
