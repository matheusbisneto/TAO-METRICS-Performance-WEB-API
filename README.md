# 📊 TAO-Metrics – Monitoramento Inteligente de Performance de Influenciadores (YouTube | Twitch | Spotify)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

**TAO-Metrics** é um dashboard web interativo que analisa a performance de influenciadores em plataformas como **YouTube**, **Twitch** e **Spotify**, integrando dados em tempo real via APIs públicas.

Este projeto foi desenvolvido como trabalho multidisciplinar do Centro Universitário **UNIBTA**, com foco em:

- 🔄 Integração com múltiplas APIs REST
- 📊 Visualizações dinâmicas com **Plotly**
- 🌐 Interface moderna e responsiva com **Streamlit**
- 🔐 Autenticação de usuários e persistência com **PostgreSQL**

---

## 🚀 Funcionalidades

✅ Login e cadastro com autenticação segura  
✅ Salvamento de canais por usuário autenticado  
✅ Gráficos interativos (visualizações, curtidas, comentários, etc.)  
✅ Dashboard unificado para YouTube, Twitch e Spotify  
✅ Organização modular do código (componentes reutilizáveis)  

---

## 🧪 Tecnologias Utilizadas

- Python 3.10+
- Streamlit
- Plotly
- PostgreSQL
- Psycopg2
- python-dotenv
- APIs públicas: YouTube Data API v3, Twitch API, Spotify API

---

## 📂 Estrutura do Projeto

```text
TAO-Metrics/
├── apis/               # Integrações com APIs externas (YouTube, Twitch)
│   ├── youtube_api.py
│   └── twitch_api.py
├── imagens/            # Imagens usadas na interface
├── pages/              # Páginas adicionais para navegação Streamlit
│ ├──style.py            # Estilo global do dashboard
│ ├──styletwitch.py      # Estilo específico para análises Twitch
│ ├──taocadastro.py      # Página de login/cadastro
│ ├──taodashboard.py     # Dashboard principal (autenticado)
│ ├──taometrics.py       # Página inicial do projeto
│ ├──taospotify.py       # Página de análise de performance no Spotify
│ ├──taotwitch.py        # Página de análise Twitch
│ ├── taoyoutube.py       # Página de análise YouTube
├── taometcis.py        # Página principal
└── .gitignore          # Arquivos e pastas ignoradas no Git
