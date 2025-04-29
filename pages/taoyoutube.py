import streamlit as st
from pages.youtube_api import buscar_canal_youtube

# Configuração da página
st.set_page_config(page_title="YouTube Analytics", layout="wide")

# Estilo customizado
st.markdown("""
    <style>
        body {
            background-color: #ffe5e5;
        }
        .container {
            background-color: #fff0f0;
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 0 15px rgba(150, 0, 0, 0.1);
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
            color: #8b0000;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin-top: 20px;
        }
        .info-card {
            background-color: #ffebeb;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(200, 0, 0, 0.15);
        }
        .info-title {
            color: #aa0000;
            font-size: 18px;
            margin-bottom: 5px;
        }
        .info-value {
            font-size: 22px;
            color: #660000;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #880000;'>🎥 Analisador de Canal do YouTube</h1>", unsafe_allow_html=True)

nome_pesquisa = st.text_input("🔎 Pesquise o nome do influenciador:")

if nome_pesquisa:
    dados = buscar_canal_youtube(nome_pesquisa)

    if dados:
        st.markdown("<div class='container'>", unsafe_allow_html=True)

        # Cabeçalho com foto e nome
        st.markdown(f"""
            <div class="header">
                <img src="{dados.get('foto_url', '')}" width="150">
                <div class="nome-canal">{dados.get('nome', 'Sem nome')}</div>
            </div>
        """, unsafe_allow_html=True)

        # Blocos de informações
        st.markdown(f"""
            <div class="info-grid">
                <div class="info-card">
                    <div class="info-title">👥 Inscritos</div>
                    <div class="info-value">{dados.get('inscritos', 0):,}</div>
                </div>
                <div class="info-card">
                    <div class="info-title">👁️ Visualizações</div>
                    <div class="info-value">{dados.get('views', 0):,}</div>
                </div>
                <div class="info-card">
                    <div class="info-title">🎞️ Total de Vídeos</div>
                    <div class="info-value">{dados.get('videos', 0)}</div>
                </div>
                <div class="info-card">
                    <div class="info-title">📅 Criado em</div>
                    <div class="info-value">{dados.get('criado_em', 'Desconhecido')}</div>
                </div>
                <div class="info-card">
                    <div class="info-title">🌍 País</div>
                    <div class="info-value">{dados.get('pais', 'Não informado')}</div>
                </div>
                <div class="info-card">
                    <div class="info-title">📝 Descrição</div>
                    <div class="info-value" style="font-size: 16px;">{dados.get('descricao', 'Descrição não disponível')[:150]}...</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("❌ Canal não encontrado.")
