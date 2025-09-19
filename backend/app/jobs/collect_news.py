import logging
import sys
import os
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

load_dotenv()

from app import create_app
from app.services.news_service import NewsService 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

test_topics = ["brasília"]

def run_job():
    app = create_app()

    with app.app_context():
        logging.info("Iniciando o job de coleta de notícias...")

        # TODO: Rodar um For até 100 requisições, essas serão as 100 requisições diárias que nós temos (podento ter até 1000 noticias por dia)
        # TODO: Pra isso vou ter que implementar uma boa lógica para selecionar os topicos e palavras chaves das pesquisas, para nao pegar conteudo repetido ou irrelevante.

        try:
            news_service = NewsService()
            
            new_articles_count, new_sources_count = news_service.collect_and_enrich_new_articles(topics=test_topics)
            
            logging.info(f"Job finalizado com sucesso. {new_articles_count} novas notícias e {new_sources_count} novas fontes foram salvas.")

        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado durante a execução do job: {e}", exc_info=True)

if __name__ == "__main__":
    run_job()