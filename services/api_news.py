from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta

newsapi = NewsApiClient(os.getenv('NEWS_KEY'))

def news():

    hoje = datetime.now()
    hoje_formatada = hoje.strftime("%Y-%m-%d")

    mes_passado = hoje - timedelta(days=30)
    mes_passado_formatada = mes_passado.strftime("%Y-%m-%d")


    # /v2/everything (Busca tudo sobre pesca em português do Brasil)
    all_articles = newsapi.get_everything(
        q='pesca',                              # Consulta por "pesca"
        language='pt',                         # Restringe a língua para português
        from_param=f'{mes_passado_formatada}',               # Período de busca (opcional)
        to=f'{hoje_formatada}',                       # Período de busca (opcional)
        sort_by='relevancy',                   # Ordena por relevância (padrão)
        page=1                                # Página 1 dos resultados (opcional)
    )

    news_data = []

    if all_articles['status'] == 'ok':
        for article in all_articles['articles']:
            title = article.get('title')  # Obtém o título, ou None se não existir

            if title and title != '[Removed]':  # Verifica se o título existe e não é "[Removed]"
                news_data.append({
                    'title': title,
                    'description': article['description'],
                    'url': article['url'],
                })

    return news_data[:10]