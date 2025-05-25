from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env na inicialização do módulo
load_dotenv()

def get_api_key():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("A chave da API do YouTube não está configurada no .env")
    return api_key

def buscar_canal_youtube(nome_canal):
    api_key = get_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    busca = youtube.search().list(
        q=nome_canal,
        part="snippet",
        type="channel",
        maxResults=1
    ).execute()

    if not busca['items']:
        return None

    canal_info = busca['items'][0]['snippet']
    canal_id = busca['items'][0]['snippet']['channelId']
    nome = canal_info.get('title', 'Sem nome')
    foto_url = canal_info['thumbnails']['high']['url']
    descricao = canal_info.get('description', 'Descrição não disponível')

    estatisticas = youtube.channels().list(
        id=canal_id,
        part="statistics,snippet",
    ).execute()

    stats = estatisticas['items'][0]['statistics']
    snippet = estatisticas['items'][0]['snippet']

    dados_canal = {
        "nome": nome,
        "foto_url": foto_url,
        "descricao": descricao,
        "canal_id": canal_id,
        "inscritos": int(stats.get('subscriberCount', 0)),
        "views": int(stats.get('viewCount', 0)),
        "videos": int(stats.get('videoCount', 0)),
        "criado_em": snippet.get('publishedAt', '')[:10],
        "pais": snippet.get('country', 'Não informado')
    }

    return dados_canal

def buscar_videos_do_canal(canal_id, max_videos=30):
    api_key = get_api_key()
    youtube = build('youtube', 'v3', developerKey=api_key)

    videos = []
    next_page_token = None

    while len(videos) < max_videos:
        request = youtube.search().list(
            channelId=canal_id,
            part="snippet",
            maxResults=50,
            order="date",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            if item['id'].get('kind') != 'youtube#video':
                continue

            video_id = item['id'].get('videoId')
            if not video_id:
                continue

            video_info = youtube.videos().list(
                part="statistics",
                id=video_id
            ).execute()

            if not video_info['items']:
                continue

            video_stats = video_info['items'][0]['statistics']
            video_data = {
                'titulo': item['snippet']['title'],
                'data': item['snippet']['publishedAt'],
                'views': int(video_stats.get('viewCount', 0)),
                'likes': int(video_stats.get('likeCount', 0)),
                'comentarios': int(video_stats.get('commentCount', 0)),
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
            videos.append(video_data)

            if len(videos) >= max_videos:
                break

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return videos[:max_videos]
