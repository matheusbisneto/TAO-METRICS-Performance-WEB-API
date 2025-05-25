import streamlit as st
import psycopg2
import bcrypt
import datetime
from dotenv import load_dotenv
import os

# Carrega o .env
load_dotenv()

# 📌 Sessão inicial
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None

# 🔐 Conectar ao banco de dados PostgreSQL
def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# 🔒 Verifica senha com bcrypt
def verificar_senha(senha_digitada, senha_hash):
    return bcrypt.checkpw(senha_digitada.encode('utf-8'), senha_hash.encode('utf-8'))

# 🔒 Cria hash da senha
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 💾 Registrar novo usuário
def registrar_usuario(nome, email, senha):
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        if cur.fetchone():
            return "⚠️ Email já cadastrado."

        senha_hash = hash_senha(senha)
        cur.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, criado_em)
            VALUES (%s, %s, %s, %s)
        """, (nome, email, senha_hash, datetime.datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
        return "✅ Usuário registrado com sucesso!"
    except Exception as e:
        return f"❌ Erro: {e}"

# 🧠 Verificar login
def autenticar_usuario(email, senha):
    try:
        conn = conectar()
        cur = conn.cursor()

        cur.execute("SELECT id, nome, senha_hash FROM usuarios WHERE email = %s", (email,))
        resultado = cur.fetchone()

        if resultado:
            usuario_id, nome, senha_hash = resultado
            if verificar_senha(senha, senha_hash):
                return True, nome, usuario_id
        return False, None, None
    except Exception as e:
        return False, None, None

# 🎨 Interface
st.set_page_config(page_title="Login / Cadastro", page_icon="🔐", layout="centered")
st.title("🔐 Área de Acesso")

abas = st.tabs(["🔓 Login", "📝 Cadastro"])

# 1️⃣ LOGIN
with abas[0]:
    st.subheader("Entrar com sua conta")
    email_login = st.text_input("Email", key="login_email")
    senha_login = st.text_input("Senha", type="password", key="login_senha")

    if st.button("Entrar"):
        sucesso, nome, usuario_id = autenticar_usuario(email_login, senha_login)
        if sucesso:
            st.session_state.logado = True
            st.session_state.usuario = nome
            st.session_state.usuario_id = usuario_id
            st.success(f"✅ Bem-vindo, {nome}!")
            st.switch_page("taometrics.py")
        else:
            st.error("❌ Email ou senha incorretos.")

# 2️⃣ CADASTRO
with abas[1]:
    st.subheader("Criar uma nova conta")

    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        confirmar = st.text_input("Confirmar senha", type="password")
        enviar = st.form_submit_button("Cadastrar")

    if enviar:
        if senha != confirmar:
            st.warning("⚠️ As senhas não coincidem.")
        elif not nome or not email or not senha:
            st.warning("⚠️ Por favor, preencha todos os campos.")
        else:
            resultado = registrar_usuario(nome, email, senha)
            st.info(resultado)
