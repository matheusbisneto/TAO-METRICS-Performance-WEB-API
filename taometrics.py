import streamlit as st
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
import os

# Carrega o .env
load_dotenv()

def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# Configuração da página
st.set_page_config(page_title="Tao Metrics", layout="centered", initial_sidebar_state="collapsed")

# Inicializa variáveis de sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None

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

# Topo direito com nome do usuário e botão sair (ou botão login)
st.markdown("""
    <div class="top-right-container">
""", unsafe_allow_html=True)

if st.session_state.logado:
    st.markdown(f"<span>👤 <b>{st.session_state.usuario}</b></span>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="btn_sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.experimental_rerun()
else:
    if st.button("🔐 Login / Cadastro", key="btn_login"):
        st.switch_page("pages/taocadastro.py")

st.markdown("</div>", unsafe_allow_html=True)

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

# Se o usuário estiver logado, permitir envio de feedback
if st.session_state.logado:
    st.markdown("#### 💬 Enviar Feedback")
    feedback_text = st.text_area("Deixe seu feedback sobre o TAO Metrics:")

    if st.button("📨 Enviar Feedback"):
        if feedback_text.strip() == "":
            st.warning("Por favor, digite uma mensagem antes de enviar.")
        else:
            try:
                conn = conectar()
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO feedbacks (usuario_id, mensagem, enviado_em) VALUES (%s, %s, %s)",
                    (st.session_state.usuario_id, feedback_text, datetime.utcnow())
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Feedback enviado com sucesso!")
            except Exception as e:
                st.error(f"Erro na conexão com o banco de dados: {e}")
else:
    st.markdown("⚠️ Faça login para enviar feedbacks.")