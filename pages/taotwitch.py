import streamlit as st
import pandas as pd
import plotly.express as px
from apis.twitch_api import buscar_dados_completos

# Carrega o CSS externo
with open("pages/styletwitch.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Aqui o ajuste para imagem e título lado a lado ---
col_img, col_title = st.columns([1, 8])
with col_img:
    st.image("imagens/taotwitch.svg", width=100)  # Ajuste a largura que preferir
with col_title:
    st.markdown("<h1 style='margin:0; padding-top:10px;'>TAO Analytics Twitch </h1>", unsafe_allow_html=True)

nome_canal = st.text_input("Digite o nome do canal da Twitch:", value="")

if nome_canal:
    dados = buscar_dados_completos(nome_canal)

    if dados:
        status = dados['live']['is_live']
        status_texto = "🔴 AO VIVO" if status else "⚫ Offline"
        cor_status = "#9b59b6" if status else "#6c757d"

        st.markdown(f"""
        <div class="status-badge" style="background-color:{cor_status};">
            {status_texto}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <img src="{dados['foto_url']}" alt="Foto do canal">
            <h2>{dados['nome']}</h2>
            <p>{dados['descricao']}</p>
            <p><strong>Criado em:</strong> {dados['criado_em']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Garantindo que seguidores seja inteiro e formatado
        seguidores = dados.get('seguidores', 0)
        if not isinstance(seguidores, int):
            try:
                seguidores = int(seguidores)
            except:
                seguidores = 0

        visualizacoes = dados.get('visualizacoes', 0)
        if not isinstance(visualizacoes, int):
            try:
                visualizacoes = int(visualizacoes)
            except:
                visualizacoes = 0

        st.markdown(f"""
        <div class="card">
            <h3>📊 Estatísticas</h3>
            <p><strong>Seguidores:</strong> {seguidores:,}</p>
            <p><strong>Visualizações:</strong> {visualizacoes:,}</p>
        </div>
        """, unsafe_allow_html=True)

        if status:
            st.markdown(f"""
            <div class="card">
                <h3>🔴 Ao Vivo</h3>
                <p><strong>Título:</strong> {dados['live']['title']}</p>
                <p><strong>Jogo:</strong> {dados['live']['game']}</p>
                <p><strong>Viewers:</strong> {dados['live']['viewer_count']:,}</p>
                <p><strong>Iniciada em:</strong> {dados['live']['started_at']}</p>
            </div>
            """, unsafe_allow_html=True)

        # Top 10 vídeos - gráfico horizontal
        df_videos = pd.DataFrame(dados['videos'])
        if not df_videos.empty:
            st.markdown("### 📊 Top 10 Vídeos")
            fig_videos = px.bar(
                df_videos.sort_values('views', ascending=True).head(10),
                x='views',
                y='titulo',
                orientation='h',
                labels={'views': 'Visualizações', 'titulo': 'Título'},
                text='views'
            )
            fig_videos.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(autorange="reversed"),
                margin=dict(l=150, r=30, t=40, b=40),
                height=450
            )
            fig_videos.update_traces(marker_color='#9b59b6', textposition='outside')
            st.plotly_chart(fig_videos, use_container_width=True)

        # Clipes populares
        df_clips = pd.DataFrame(dados['clips'])
        if not df_clips.empty:
            st.markdown("### 📊 Clipes Populares")
            fig_clips = px.bar(
                df_clips.sort_values('views', ascending=False),
                x='views',
                y='titulo',
                orientation='h',
                labels={'views': 'Visualizações', 'titulo': 'Título'},
            )
            fig_clips.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(autorange="reversed"),
                margin=dict(l=150, r=30, t=40, b=40),
                height=450
            )
            fig_clips.update_traces(marker_color='#9b59b6') 
            st.plotly_chart(fig_clips, use_container_width=True)

        # Mostrar vídeos (2 por linha)
        st.markdown("### 🎬 Últimos Vídeos")
        col1, col2 = st.columns(2)
        for i, video in enumerate(dados['videos'][:6]):
            bloco = f"""
            <div class="card mini-card">
                <p class="texto-destaque">{video['titulo']}</p>
                <div class="video-info">
                    <span>Views: {video['views']:,}</span>
                    <span>Data: {video['criado_em']}</span>
                </div>
                <a href="{video['url']}" target="_blank"><button>Assistir</button></a>
            </div>
            """
            if i % 2 == 0:
                col1.markdown(bloco, unsafe_allow_html=True)
            else:
                col2.markdown(bloco, unsafe_allow_html=True)

        # Mostrar clipes (2 por linha)
        st.markdown("### 📽️ Clipes")
        col3, col4 = st.columns(2)
        for i, clip in enumerate(dados['clips'][:6]):
            bloco = f"""
            <div class="card mini-card">
                <p class="texto-destaque">{clip['titulo']}</p>
                <div class="video-info">
                    <span>Views: {clip['views']:,}</span>
                    <span>Data: {clip['created_at']}</span>
                </div>
                <a href="{clip['url']}" target="_blank"><button>Assistir</button></a>
            </div>
            """
            if i % 2 == 0:
                col3.markdown(bloco, unsafe_allow_html=True)
            else:
                col4.markdown(bloco, unsafe_allow_html=True)

    else:
        st.error("❌ Canal não encontrado. Verifique o nome.")
