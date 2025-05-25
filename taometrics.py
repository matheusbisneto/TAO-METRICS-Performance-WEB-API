import streamlit as st
from datetime import datetime
import psycopg2
import os

def conectar():
    return psycopg2.connect(
        host=st.secrets["general"]["DB_HOST"],
        dbname=st.secrets["general"]["DB_NAME"],
        user=st.secrets["general"]["DB_USER"],
        password=st.secrets["general"]["DB_PASS"],
        port=st.secrets["general"]["DB_PORT"]
    )

# Configuração da página
st.set_page_config(page_title="Tao Metrics", layout="centered", initial_sidebar_state="collapsed")

# CSS para visual moderno
st.markdown("""
    <style>
        /* Oculta barra lateral */
        .css-1d391kg {display: none;}
        .css-18e3p5e {display: none;}

        /* Imagens não interativas */
        img {
            pointer-events: none;
            user-select: none;
        }

        /* Estilo base para todos os botões */
        .stButton > button {
            font-weight: bold;
            padding: 0.5em 1em;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            width: 100%;
        }

        /* Container para topo direito */
        .top-right-container {
            display: flex;
            justify-content: flex-end;
            align-items: center;
            gap: 10px;
            position: absolute;
            top: 10px;
            right: 20px;
            z-index: 9999;
        }
    </style>
""", unsafe_allow_html=True)

# Topo direito sem a opção de "Sair"
st.markdown("""
    <div class="top-right-container">
        <!-- Não há mais a opção de "Sair" -->
    </div>
""", unsafe_allow_html=True)

# Título com logo à direita (usando colunas Streamlit)
col_logo, col_title = st.columns([1, 4])
with col_title:
    st.title("Bem-vindo ao Tao Metrics")
    st.subheader("Seu analista de engajamento")
with col_logo:
    st.image("imagens/tao.svg", width=300)

st.markdown("---")

# Colunas com ícones + botões
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.image("imagens/youtube.svg", width=60)
    if st.button("YouTube"):
        st.switch_page("pages/taoyoutube.py")

with col2:
    st.image("imagens/twitch.svg", width=60)
    if st.button("Twitch"):
        st.switch_page("pages/taotwitch.py")

with col3:
    st.image("https://img.icons8.com/ios-filled/100/000000/combo-chart--v1.png", width=60)
    if st.button("Seu Dashboard"):
        st.switch_page("pages/taodashboard.py")

with col4:
    st.image("imagens/spotify.svg", width=60)
    if st.button("Spotify"):
        st.switch_page("pages/taospotify.py")

st.markdown("---")

# Campo de busca
pesquisa = st.text_input("🔎 Pesquise o nome do influenciador...")
if pesquisa:
    st.success(f"Buscando dados para: **{pesquisa}** (Selecione primeiro a plataforma)")

# Espaço antes do rodapé
st.markdown("---")

# Rodapé profissional
st.markdown("#### ℹ️ Sobre o Projeto")
st.info(
    "TAO Metrics – Projeto acadêmico desenvolvido para o Centro Universitário UNIBTA\n\n"
    "Curso: Ciências da Computação | Projeto Multidisciplinar 2025\n\n"
    "© Copyright Tao Metrics"
)

st.markdown("#### 👥 Colaboradores no GitHub")
st.markdown("- Matheus Bisneto: github.com/matheusbisneto")
st.markdown("- Gustavo P. Reis: github.com/Gustavo-P-Reis")
st.markdown("- Wendell  Matias: github.com/Mendell")
