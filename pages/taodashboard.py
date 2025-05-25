import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
from apis.youtube_api import buscar_canal_youtube, buscar_videos_do_canal
from apis.twitch_api import buscar_dados_completos
import datetime
from dotenv import load_dotenv
import os

# Carrega o .env
load_dotenv()

# Função para conectar ao banco
def conectar():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )

# Inicializa session_state para evitar erros de atributo
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None
if "canais" not in st.session_state:
    st.session_state.canais = []

# Se não estiver logado, pedir para entrar
if not st.session_state.logado:
    st.warning("❌ Você precisa estar logado para acessar o TAO Dashboard.")
    st.write("Por favor, faça login na página de acesso.")
    st.stop()

# Carregar URLs salvas do banco para o usuário e atualizar session_state.canais
def carregar_urls(usuario_id):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, titulo, url, criado_em FROM dashboards WHERE usuario_id = %s ORDER BY criado_em DESC", (usuario_id,))
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados
    except Exception as e:
        st.error(f"Erro ao carregar URLs: {e}")
        return []

# Atualiza session_state.canais com as URLs salvas, sem duplicatas
urls_salvas = carregar_urls(st.session_state.usuario_id)
if urls_salvas:
    canais_salvos = [url for _, _, url, _ in urls_salvas]
    for canal in canais_salvos:
        if canal not in st.session_state.canais:
            st.session_state.canais.append(canal)

# Layout e título
st.set_page_config(page_title=f"TAO Dashboard - {st.session_state.usuario}", layout="wide")
st.title(f"📊 TAO Dashboard - {st.session_state.usuario}")

# Função para salvar URL no banco para o usuário logado
def salvar_url(titulo, url, usuario_id):
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO dashboards (usuario_id, titulo, url, criado_em) VALUES (%s, %s, %s, %s)",
            (usuario_id, titulo, url, datetime.datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar URL: {e}")
        return False

# Campo para adicionar novo canal
url_canal = st.text_input("🔗 Cole a URL do canal (Twitch ou YouTube):")
titulo_canal = st.text_input("📝 Título para este canal (opcional):")

if st.button("Adicionar Canal e Salvar"):
    if not url_canal.strip():
        st.error("Por favor, insira uma URL válida.")
    else:
        titulo = titulo_canal.strip() or "Sem título"
        if salvar_url(titulo, url_canal.strip(), st.session_state.usuario_id):
            st.success("Canal salvo com sucesso!")
            if url_canal.strip() not in st.session_state.canais:
                st.session_state.canais.append(url_canal.strip())

# Mostrar canais salvos
st.markdown("### 📂 Canais Salvos")
if urls_salvas:
    for id_, titulo, url, criado_em in urls_salvas:
        st.write(f"**{titulo}** — {url} (salvo em {criado_em.strftime('%d/%m/%Y %H:%M')})")
else:
    st.info("Nenhum canal salvo ainda.")

# Exibir dados e gráficos para os canais na session_state
dados_canais = []

for canal in st.session_state.canais:
    if "twitch.tv" in canal:
        nome_canal = canal.rstrip('/').split('/')[-1]
        dados = buscar_dados_completos(nome_canal.lower())

        if dados and 'nome' in dados:
            dados_canais.append({"tipo": "Twitch", "dados": dados})

    elif "youtube.com" in canal:
        nome_canal = canal.rstrip('/').split('/')[-1]
        dados = buscar_canal_youtube(nome_canal)

        if dados and 'nome' in dados:
            dados_canais.append({"tipo": "YouTube", "dados": dados})

for canal_info in dados_canais:
    tipo = canal_info["tipo"]
    dados = canal_info["dados"]

    if tipo == "Twitch":
        st.markdown(f"#### Análise do Canal Twitch: {dados.get('nome', 'Nome não disponível')} 🔴")
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(dados['foto_url'], width=150)
        with col2:
            st.write(f"🧾 Login: `{dados.get('login', 'Não disponível')}`")
            st.write(f"📅 Criado em: `{dados.get('criado_em', 'Desconhecido')}`")
            st.write(f"🆔 ID: `{dados.get('id', 'Não disponível')}`")
            st.write(f"📣 Descrição: {dados.get('descricao', 'Descrição não disponível')}")
            st.write(f"👥 Seguidores: `{dados.get('seguidores', 0)}`")
            st.write(f"📊 Visualizações (últimos 20 vídeos): `{dados.get('visualizacoes', 0)}`")

            if dados.get('live', {}).get('is_live', False):
                st.success(f"🟢 **Ao Vivo:** {dados['live']['title']}")
                st.write(f"👀 {dados['live']['viewer_count']} espectadores")
                st.write(f"🎮 Jogo: {dados['live']['game']}")
                st.write(f"📅 Iniciado em: {dados['live']['started_at']}")
            else:
                st.info("🔴 Canal está OFFLINE no momento.")

        st.markdown("---")

        st.subheader("📈 Desempenho das Últimos Lives")
        if dados.get("videos"):
            df_videos = pd.DataFrame(dados["videos"])
            colunas_videos = ['titulo', 'views']
            if 'data_publicacao' in df_videos.columns:
                colunas_videos.append('data_publicacao')

            fig_videos = px.bar(df_videos, x="titulo", y="views", title="Visualizações por Vídeo")
            st.plotly_chart(fig_videos, use_container_width=True)
            st.dataframe(df_videos[colunas_videos], use_container_width=True)
        else:
            st.info("Este canal ainda não possui vídeos públicos.")

    elif tipo == "YouTube":
        st.markdown(f"#### Análise do Canal YouTube: {dados.get('nome', 'Nome não disponível')} 🔵")
        st.markdown(f"👥 Inscritos: {dados.get('inscritos', 0):,}")
        st.markdown(f"👁️ Visualizações: {dados.get('views', 0):,}")
        st.markdown(f"🎞️ Total de Vídeos: {dados.get('videos', 0)}")
        st.markdown(f"📅 Criado em: {dados.get('criado_em', 'Desconhecido')}")
        st.markdown(f"🌍 País: {dados.get('pais', 'Não informado')}")
        st.markdown(f"📝 Descrição: {dados.get('descricao', 'Descrição não disponível')[:150]}...")

        st.markdown("### 📈 Desempenho dos Últimos Vídeos")
        videos = buscar_videos_do_canal(dados.get("canal_id"), max_videos=30)

        if videos:
            df_videos = pd.DataFrame(videos)
            df_videos['data'] = pd.to_datetime(df_videos['data']).dt.tz_localize(None)

            fig_views = px.line(df_videos, x='data', y='views', title='📈 Visualizações ao Longo do Tempo', markers=True)
            st.plotly_chart(fig_views, use_container_width=True)

            fig_likes = px.bar(df_videos, x='data', y='likes', title='👍 Curtidas por Vídeo', color_discrete_sequence=['#EF476F'])
            st.plotly_chart(fig_likes, use_container_width=True)

            fig_comments = px.area(df_videos, x='data', y='comentarios', title='💬 Comentários por Vídeo', color_discrete_sequence=['#118AB2'])
            st.plotly_chart(fig_comments, use_container_width=True)

            st.markdown("### 🗂️ Lista de Vídeos Recentes")
            st.dataframe(df_videos[['data', 'titulo', 'views', 'likes', 'comentarios', 'url']].sort_values("data", ascending=False).reset_index(drop=True))
        else:
            st.warning("⚠️ Nenhum vídeo recente encontrado para análise.")
