import streamlit as st
import requests

CLIENT_ID = st.secrets["twitch"]["TWITCH_CLIENT_ID"]
OAUTH_TOKEN = st.secrets["twitch"]["TWITCH_OAUTH_TOKEN"]

HEADERS = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {OAUTH_TOKEN}'
}

def buscar_dados_completos(nome_canal):
    url_user = f"https://api.twitch.tv/helix/users?login={nome_canal}"
    resp_user = requests.get(url_user, headers=HEADERS)
    if resp_user.status_code != 200 or not resp_user.json().get("data"):
        print("Erro ao buscar dados do usuário:", resp_user.json())
        return None
    user = resp_user.json()["data"][0]
    user_id = user['id']

    url_followers = f"https://api.twitch.tv/helix/users/follows?to_id={user_id}&first=1"
    resp_followers = requests.get(url_followers, headers=HEADERS)
    data_followers = resp_followers.json()

    seguidores = data_followers.get('total', 0)

    url_videos = f"https://api.twitch.tv/helix/videos?user_id={user_id}&first=20"
    resp_videos = requests.get(url_videos, headers=HEADERS)
    videos = resp_videos.json().get('data', [])
    total_views = sum(video.get('view_count', 0) for video in videos)

    ultimos_videos = [{
        "titulo": video.get("title", ""),
        "views": video.get("view_count", 0),
        "criado_em": video.get("created_at", "")[:10],
        "url": video.get("url", ""),
        "game_id": video.get("game_id"),
        "language": video.get("language"),
        "type": video.get("type")
    } for video in videos]

    url_clips = f"https://api.twitch.tv/helix/clips?broadcaster_id={user_id}&first=5"
    resp_clips = requests.get(url_clips, headers=HEADERS)
    clips = resp_clips.json().get('data', [])

    top_clips = [{
        "titulo": clip.get("title", ""),
        "views": clip.get("view_count", 0),
        "url": clip.get("url", ""),
        "created_at": clip.get("created_at", "")[:10]
    } for clip in clips]

    url_stream = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
    resp_stream = requests.get(url_stream, headers=HEADERS)
    stream_data = resp_stream.json().get('data', [])
    live_info = stream_data[0] if stream_data else None

    game_name = None
    if live_info and live_info.get('game_id'):
        game_id = live_info['game_id']
        url_game = f"https://api.twitch.tv/helix/games?id={game_id}"
        resp_game = requests.get(url_game, headers=HEADERS)
        games = resp_game.json().get('data', [])
        if games:
            game_name = games[0].get('name')

    return {
        "nome": user.get("display_name"),
        "foto_url": user.get("profile_image_url"),
        "descricao": user.get("description"),
        "criado_em": user.get("created_at", "")[:10],
        "id": user_id,
        "login": user.get("login"),
        "seguidores": seguidores,
        "visualizacoes": total_views,
        "videos": ultimos_videos,
        "clips": top_clips,
        "live": {
            "is_live": bool(live_info),
            "title": live_info.get("title") if live_info else None,
            "viewer_count": live_info.get("viewer_count") if live_info else None,
            "game": game_name,
            "started_at": live_info.get("started_at", "")[:10] if live_info else None
        }
    }
