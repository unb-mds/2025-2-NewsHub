import os
import requests
import logging
from datetime import datetime
from newspaper import Article
from sqlalchemy.exc import IntegrityError
from newspaper.configuration import Configuration
from app.repositories.news_repository import NewsRepository
from app.repositories.news_source_repository import NewsSourceRepository
from app.models.news import News, NewsValidationError
from app.models.news_source import NewsSource
from app.models.exceptions import NewsSourceValidationError


# TODO: Enviar a header da noticia pra IA para ela criar os topicos da noticia (categorizar) e criar na tabela de topicos.

# TODO: fazer consultas no banco para topicos mais selecionados e a partir desses topicos, pedir para IA criar palavras chaves para noticias e enviar para o endpoint de search.

# TODO: Tratar a quantidade de requests que vou fazer para cada topico, enviar um objeto com os topicos e varias informacoes do tipo

# TODO: adicionar parâmetro para dizer se vou rodar um top headlines ou um search por palavra chave

class NewsService():
    def __init__(self, news_repo: NewsRepository | None = None, news_source_repo: NewsSourceRepository | None = None):
        self.news_repo = news_repo or NewsRepository()
        self.news_sources_repo = news_source_repo or NewsSourceRepository()
        self.gnews_api_key = os.getenv('GNEWS_API_KEY')
        self.api_endpoint = "https://gnews.io/api/v4/top-headlines"
        self.api_endpoint_search = "https://gnews.io/api/v4/search"

    # TODO: Nao devo receber uma lista de topicos, devo criar uma função para calcular quais topicos devem ser pesquisados, além de selecionar quantas consultas serão feitas em cada endpoint (search e top headlines)
    
    def collect_and_enrich_new_articles(self, topics: list[str] | None = None):
        if not self.gnews_api_key:
            logging.error("A variável de ambiente GNEWS_API_KEY não foi configurada.")
            raise ValueError("A variável de ambiente GNEWS_API_KEY não foi configurada.")
        
        all_articles_metadata = []
        
        search_topics = topics or [None]

        for topic in search_topics:
            logging.info(f"Buscando notícias para o tópico: {'Geral' if topic is None else topic}")
            articles_metadata = self.discover_articles_via_gnews(topic)
            all_articles_metadata.extend(articles_metadata)

        logging.info(f"Encontrados {len(all_articles_metadata)} artigos na API.")

        new_articles_count = 0
        new_sources_count = 0

        for i, article_meta in enumerate(all_articles_metadata, 1):
            title = article_meta.get('title')
            logging.info(f"Processando artigo {i}/{len(all_articles_metadata)}: '{title}'")
            article_url = article_meta.get('url')
            if not article_url:
                logging.warning("Artigo sem URL encontrado, pulando.")
                continue

            if self.news_repo.find_by_url(article_url):
                logging.info(f"Artigo já existe no banco de dados, pulando: {article_url}")
                continue

            source_name = article_meta.get('source', {}).get('name')
            source_url = article_meta.get('source', {}).get('url')

            if not source_name or not source_url:
                logging.warning(f"Pulando artigo por falta de dados da fonte: {article_url}")
                continue

            news_source_model = self.news_sources_repo.find_by_url(source_url)
            if not news_source_model:
                try:
                    logging.info(f"Nova fonte encontrada: '{source_name}'. Criando no banco de dados.")
                    new_source = NewsSource(name=source_name, url=source_url)
                    news_source_model = self.news_sources_repo.create(new_source)
                    new_sources_count += 1
                except IntegrityError:
                    logging.warning(f"Race condition ao criar fonte. Buscando novamente por URL: {source_url}")
                    news_source_model = self.news_sources_repo.find_by_url(source_url)
                    if not news_source_model:
                        logging.error(f"Não foi possível encontrar a fonte por URL '{source_url}' após erro de integridade.")
                        continue
                except (NewsSourceValidationError, Exception) as e:
                    logging.error(f"Não foi possível criar a fonte '{source_name}': {e}", exc_info=True)
                    continue
            
            source_id = news_source_model.id

            article_content = self.scrape_article_content(article_url)
            if not article_content:
                logging.warning(f"Falha ao extrair conteúdo do artigo, pulando: {article_url}")
                continue

            try:
                published_at_str = article_meta.get('publishedAt')
                if published_at_str.endswith('Z'):
                    published_at_str = published_at_str[:-1] + '+00:00'
                published_at_dt = datetime.fromisoformat(published_at_str)

                article = News(
                    title=article_meta.get('title'),
                    url=article_url,
                    description=article_meta.get('description'),
                    content=article_content,
                    image_url=article_meta.get('image'),
                    published_at=published_at_dt,
                    source_id=source_id,
                )
                
                self.news_repo.create(article)
                new_articles_count += 1
                logging.info(f"Novo artigo salvo: '{article.title}'")

            except (NewsValidationError, Exception) as e:
                logging.error(f"Não foi possível criar o artigo '{article_meta.get('title')}': {e}", exc_info=True)
                continue
            
        return new_articles_count, new_sources_count

    def discover_articles_via_gnews(self, topic: str | None = None, language='pt', country='br', max_articles=10):
        params = {'lang': language, 'country': country, 'apikey': self.gnews_api_key, 'max': max_articles}
        if topic: params['topic'] = topic

        try:
            response = requests.get(self.api_endpoint, params=params)
            response.raise_for_status()
            return response.json().get('articles', [])
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao chamar a GNews API: {e}", exc_info=True)
            return []

    def scrape_article_content(self, url: str) -> str | None:
        try:
            logging.debug(f"Fazendo scraping de: {url}")
            
            config = Configuration()
            config.browser_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            config.request_timeout = 15
            config.keep_article_html = True

            article = Article(url, config=config)
            article.download()
            article.parse()
            return article.article_html
        except Exception as e:
            logging.error(f"Erro no scraping de {url}: {e}", exc_info=True)
            return None
