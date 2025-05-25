import streamlit as st
import plotly.express as px
import pandas as pd
from apis.youtube_api import buscar_canal_youtube, buscar_videos_do_canal
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

st.set_page_config(page_title="YouTube Analytics Dashboard", layout="wide")

# Carregando estilos
with open("pages/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def carregar_css(caminho):
    with open(caminho) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css("pages/styleyoutube.css")

dashboard_style = """
    <style>
        .container {
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        }
        .header {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        .header img {
            border-radius: 10px;
            margin-right: 30px;
        }
        .nome-canal {
            font-size: 32px;
            font-weight: bold;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 20px;
        }
        .info-card {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        .info-title {
            font-size: 18px;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 24px;
            color: #111;
            font-weight: bold;
        }
    </style>
"""
st.markdown(dashboard_style, unsafe_allow_html=True)

col_img, col_title = st.columns([1, 8])

with col_img:
    st.image("imagens/taoyoutube.svg", width=100)  # Ajuste a largura para o tamanho desejado

with col_title:
    st.markdown("<h1 style='color: #111; margin: 0;'>TAO Analytics Youtube</h1>", unsafe_allow_html=True)


# Campo de pesquisa SEMPRE VISÍVEL
nome_pesquisa = st.text_input("🔎 Pesquise o nome do influenciador:")

# Verifica se o campo foi preenchido
if nome_pesquisa:
    dados = buscar_canal_youtube(nome_pesquisa)

    if dados:
        st.markdown("<div class='container'>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="header">
                <img src="{dados.get('foto_url', '')}" width="150">
                <div class="nome-canal">{dados.get('nome', 'Sem nome')}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
    <div class="info-grid">
        <div class="info-card">
            <div class="info-title" data-icon="👥">Inscritos</div>
            <div class="info-value">{dados.get('inscritos', 0):,}</div>
        </div>
        <div class="info-card">
            <div class="info-title" data-icon="👁️">Visualizações</div>
            <div class="info-value">{dados.get('views', 0):,}</div>
        </div>
        <div class="info-card">
            <div class="info-title" data-icon="🎞️">Total de Vídeos</div>
            <div class="info-value">{dados.get('videos', 0)}</div>
        </div>
        <div class="info-card">
            <div class="info-title" data-icon="📅">Criado em</div>
            <div class="info-value">{dados.get('criado_em', 'Desconhecido')}</div>
        </div>
        <div class="info-card">
            <div class="info-title" data-icon="🌍">País</div>
            <div class="info-value">{dados.get('pais', 'Não informado')}</div>
        </div>
        <div class="info-card">
            <div class="info-title" data-icon="📝">Descrição</div>
            <div class="info-value" style="font-size: 16px;">{dados.get('descricao', 'Descrição não disponível')[:150]}...</div>
        </div>
    </div>
""", unsafe_allow_html=True)


        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("## 🗓️ Filtro de Data")
        data_inicio = st.date_input('Data de Início', pd.to_datetime('2020-01-01'))
        data_fim = st.date_input('Data de Fim', pd.to_datetime('today'))

        data_inicio = pd.to_datetime(data_inicio)
        data_fim = pd.to_datetime(data_fim)

        st.markdown("## 📈 Desempenho dos Últimos 30 Vídeos")
        videos = buscar_videos_do_canal(dados.get("canal_id"), max_videos=30)

        if videos:
            df = pd.DataFrame(videos)
            df['data'] = pd.to_datetime(df['data']).dt.tz_localize(None)
            df = df[(df['data'] >= data_inicio) & (df['data'] <= data_fim)]
            df = df.sort_values("data")

            fig_views = px.line(df, x="data", y="views", title="📈 Visualizações ao Longo do Tempo", markers=True)
            st.plotly_chart(fig_views, use_container_width=True)

            fig_likes = px.bar(df, x="data", y="likes", title="👍 Curtidas por Vídeo", color_discrete_sequence=['#EF476F'])
            st.plotly_chart(fig_likes, use_container_width=True)

            fig_comments = px.area(df, x="data", y="comentarios", title="💬 Comentários por Vídeo", color_discrete_sequence=['#118AB2'])
            st.plotly_chart(fig_comments, use_container_width=True)

            st.markdown("### 🗂️ Lista de Vídeos Recentes")
            st.dataframe(df[['data', 'titulo', 'views', 'likes', 'comentarios', 'url']].sort_values("data", ascending=False).reset_index(drop=True))

            df['dia_semana'] = df['data'].dt.day_name()
            metric_dia = st.selectbox("📊 Métrica para Melhor Dia da Semana:", ["views", "likes", "comentarios"])
            melhor_dia = df.groupby('dia_semana')[metric_dia].mean().reindex(['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

            fig_dia = px.bar(x=melhor_dia.index, y=melhor_dia.values,
                             labels={'x':'Dia da Semana', 'y': f'Média de {metric_dia.capitalize()}'},
                             title=f"📅 Melhor Dia da Semana para Postar (baseado em {metric_dia})",
                             color_discrete_sequence=['#06d6a0'])
            st.plotly_chart(fig_dia, use_container_width=True)

            titulos = df['titulo'].fillna('')
            vectorizer = TfidfVectorizer(stop_words='english', max_features=20)
            X = vectorizer.fit_transform(titulos)
            palavras = vectorizer.get_feature_names_out()
            importancias = np.array(X.sum(axis=0))[0]

            top_palavras = pd.DataFrame({'palavra': palavras, 'importancia': importancias})
            top_palavras = top_palavras.sort_values(by='importancia', ascending=False)

            fig_titulos = px.line_polar(top_palavras, r='importancia', theta='palavra', line_close=True,
                                        title="🔥 Tópicos Mais Comuns nos Títulos dos Vídeos (Radar)")
            fig_titulos.update_traces(fill='toself', line_color='#ffd166', marker=dict(size=8))
            fig_titulos.update_layout(polar=dict(radialaxis=dict(visible=True, showticklabels=False),
                                                 angularaxis=dict(direction="clockwise")),
                                      showlegend=False, template='plotly_dark', margin=dict(t=60, b=0, l=0, r=0))
            st.plotly_chart(fig_titulos, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum vídeo recente encontrado para análise.")
    else:
        st.error("❌ Canal não encontrado. Por favor, verifique o nome do canal e tente novamente.")
else:
    st.info("🧠 Digite o nome de um canal do YouTube para começar a análise.")
