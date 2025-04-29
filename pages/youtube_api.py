from googleapiclient.discovery import build

API_KEY = "AIzaSyDeQIV5c4j10lVj4Cfo0bggrehu4q2Hb8Y"

def buscar_canal_youtube(nome_canal):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    busca = youtube.search().list(
        q=nome_canal,
        part="snippet",
        type="channel",
        maxResults=1
    ).execute()

    if not busca['items']:
        return None

    canal_info = busca['items'][0]['snippet']
    canal_id = canal_info['channelId']
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
        "inscritos": int(stats.get('subscriberCount', 0)),
        "views": int(stats.get('viewCount', 0)),
        "videos": int(stats.get('videoCount', 0)),
        "criado_em": snippet.get('publishedAt', '')[:10],
        "pais": snippet.get('country', 'Não informado')  # ✅ Agora é seguro
    }

    return dados_canal
