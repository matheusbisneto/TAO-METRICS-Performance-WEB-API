import os
from dotenv import load_dotenv
import streamlit as st
import requests
import base64

load_dotenv()  # Carrega variáveis do .env

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def gerar_token(client_id, client_secret):
    auth = f"{client_id}:{client_secret}"
    b64_auth = base64.b64encode(auth.encode()).decode()
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def buscar_artista(nome, token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": nome, "type": "artist", "limit": 1}
    r = requests.get(url, headers=headers, params=params).json()
    artistas = r.get("artists", {}).get("items", [])
    return artistas[0] if artistas else None

def buscar_top_musicas(artista_id, token):
    url = f"https://api.spotify.com/v1/artists/{artista_id}/top-tracks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"market": "BR"}
    r = requests.get(url, headers=headers, params=params).json()
    return r.get("tracks", [])

def buscar_analise_musica(track_id, token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(url, headers=headers).json()

def buscar_artistas_relacionados(artista_id, token):
    url = f"https://api.spotify.com/v1/artists/{artista_id}/related-artists"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers).json()
    return r.get("artists", [])

def buscar_discografia_completa(artista_id, token, tipo="album,single"):
    url = f"https://api.spotify.com/v1/artists/{artista_id}/albums"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 50, "include_groups": tipo, "market": "BR"}
    r = requests.get(url, headers=headers, params=params).json()
    return r.get("items", [])

# --- Aqui o ajuste para imagem e título lado a lado ---
col_img, col_title = st.columns([1, 8])
with col_img:
    st.image("imagens/taospotify.svg", width=100)  # Ajuste a largura que preferir
with col_title:
    st.markdown("<h1 style='margin:0; padding-top:10px;'>TAO Analytics Spotify </h1>", unsafe_allow_html=True)

artista_nome = st.text_input("Digite o nome do artista")

if st.button("Buscar") and artista_nome:
    token = gerar_token(CLIENT_ID, CLIENT_SECRET)
    if not token:
        st.error("Erro ao gerar token.")
    else:
        artista = buscar_artista(artista_nome, token)
        if not artista:
            st.warning("Artista não encontrado.")
        else:
            st.image(artista["images"][0]["url"], width=200)
            st.subheader(artista["name"])
            st.write(f"🎧 Seguidores: {artista['followers']['total']:,}")
            st.write(f"🔥 Popularidade: {artista['popularity']}/100")
            st.write("🎼 Gêneros:", ", ".join(artista.get("genres", [])))

            # Top músicas
            with st.expander("🎵 Top Músicas"):
                top_musicas = buscar_top_musicas(artista["id"], token)
                for m in top_musicas:
                    st.markdown(f"**{m['name']}** — Popularidade: {m['popularity']}")
                    if m["preview_url"]:
                        st.audio(m["preview_url"], format="audio/mp3")

                    analise = buscar_analise_musica(m["id"], token)
                    if analise and "danceability" in analise:
                        st.markdown("**🎚️ Análise de Áudio**")
                        st.write({
                            "🎶 Dançabilidade": analise.get("danceability"),
                            "💥 Energia": analise.get("energy"),
                            "🎭 Valência (felicidade)": analise.get("valence"),
                            "🎧 Acústica": analise.get("acousticness"),
                            "⚡ BPM": analise.get("tempo")
                        })
                    else:
                        st.warning("❌ Não foi possível obter a análise de áudio desta música.")

            # Discografia completa
            with st.expander("📀 Discografia Completa"):
                albuns = buscar_discografia_completa(artista["id"], token)
                st.write(f"{len(albuns)} lançamentos encontrados.")
                for album in albuns:
                    st.markdown(f"**{album['name']}** ({album['release_date']})")
                    st.image(album["images"][0]["url"], width=100)

            # Artistas relacionados
            with st.expander("👥 Artistas Relacionados"):
                relacionados = buscar_artistas_relacionados(artista["id"], token)
                for rel in relacionados[:5]:
                    st.markdown(f"**{rel['name']}** — Popularidade: {rel['popularity']}")
                    if rel.get("images"):
                        st.image(rel["images"][0]["url"], width=100)

st.caption("🔗 Feito com a API do Spotify e Streamlit.")
