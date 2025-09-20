import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout # Garante que os logs vão para o stdout do container
)

# TODO: Rodar um For até 100 requisições, essas serão as 100 requisições diárias que nós temos (podento ter até 1000 noticias por dia)

# TODO: Pra isso vou ter que implementar uma boa lógica para selecionar os topicos e palavras chaves das pesquisas, para nao pegar conteudo repetido ou irrelevante.

def run_collection_job():
    from app import create_app
    from app.services.news_service import NewsService

    app = create_app()
    with app.app_context():
        logging.info("Iniciando o job de coleta de notícias...")


        try:
            news_service = NewsService()

            # TODO: Implementar lógica de seleção de tópicos em vez de uma lista fixa.

            test_topics = ["brasília"]
            new_articles_count, new_sources_count = news_service.collect_and_enrich_new_articles(topics=test_topics)
            logging.info(f"Job finalizado com sucesso. {new_articles_count} novas notícias e {new_sources_count} novas fontes foram salvas.")
        except Exception as e:
            logging.error(f"Ocorreu um erro inesperado durante a execução do job: {e}", exc_info=True)

if __name__ == "__main__":
    run_collection_job()