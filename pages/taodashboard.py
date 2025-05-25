import streamlit as st
import pandas as pd
import plotly.express as px
from apis.youtube_api import buscar_canal_youtube, buscar_videos_do_canal
from apis.twitch_api import buscar_dados_completos

# Função para salvar URL no banco de dados (você pode ajustar conforme necessário)
def salvar_url(url):
    # Lógica para salvar a URL no banco ou em uma lista
    # Aqui é apenas um exemplo simples, mas você pode adaptar para o seu banco de dados
    if url not in st.session_state.urls_salvas:
        st.session_state.urls_salvas.append(url)
        return True
    return False

# Layout e título
st.set_page_config(page_title="TAO Dashboard", layout="wide")
st.title(f"📊 TAO Dashboard")

# Inicializa a lista de URLs salvas
if "urls_salvas" not in st.session_state:
    st.session_state.urls_salvas = []

# Campo para adicionar novo canal
url_canal = st.text_input("🔗 Cole a URL do canal (Twitch ou YouTube):")

# Botão para salvar URL
if st.button("Salvar URL do Canal"):
    if url_canal and salvar_url(url_canal):
        st.success(f"Canal {url_canal} salvo com sucesso!")
    elif not url_canal:
        st.error("Por favor, insira uma URL válida.")

# Exibir dados e gráficos para os canais inseridos
dados_canais = []

for url_canal in st.session_state.urls_salvas:
    if "twitch.tv" in url_canal:
        nome_canal = url_canal.rstrip('/').split('/')[-1]
        dados = buscar_dados_completos(nome_canal.lower())
        
        if dados and 'nome' in dados:
            dados_canais.append({"tipo": "Twitch", "dados": dados})

    elif "youtube.com" in url_canal:
        nome_canal = url_canal.rstrip('/').split('/')[-1]
        dados = buscar_canal_youtube(nome_canal)

        if dados and 'nome' in dados:
            dados_canais.append({"tipo": "YouTube", "dados": dados})

# Exibir as análises
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
