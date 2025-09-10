import os
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from newspaper import Article 

# No terminal, antes de rodar o script, faça: export NEWS_API_KEY='sua_chave_aqui'
API_KEY = os.getenv('NEWS_API_KEY')

if not API_KEY:
    raise ValueError("A variável de ambiente NEWS_API_KEY não foi configurada.")

newsapi = NewsApiClient(api_key=API_KEY)


def discover_articles_via_api(query, language='en', page_size=5):
    """
    Usa a NewsAPI para descobrir os artigos mais recentes.
    Retorna uma lista de artigos encontrados.
    """
    print(f"[*] Buscando artigos com a NewsAPI sobre '{query}'...")
    try:
        headlines = newsapi.get_everything(q=query,
                                                  language=language,
                                                  page_size=page_size)
        return headlines.get('articles', [])
    except NewsAPIException as e:
        print(f"Erro ao chamar a NewsAPI: {e}")
        return []

def scrape_article_content(url):
    """
    Usa a biblioteca Newspaper para baixar e extrair o conteúdo de um artigo.
    Retorna o texto completo do artigo.
    """
    try:
        print(f"    -> Fazendo scraping da URL: {url}")
        article = Article(url)
        
        article.download()
        
        article.parse()
        
        return article.text
    except Exception as e:
        print(f"    [!] Erro ao fazer o scraping de {url}: {e}")
        return None


if __name__ == "__main__":
    articles_metadata = discover_articles_via_api('apple', page_size=3)
    
    if not articles_metadata:
        print("\nNenhum artigo encontrado pela API. Encerrando.")
    else:
        print(f"\n[OK] {len(articles_metadata)} artigos encontrados. Iniciando extração de conteúdo...")
        
        full_articles = []
        
        for article_meta in articles_metadata:
            full_text = scrape_article_content(article_meta['url'])
            
            if full_text:
                full_articles.append({
                    'title': article_meta.get('title'),
                    'source': article_meta.get('source', {}).get('name'),
                    'url': article_meta.get('url'),
                    'full_text': full_text
                })
            print("-" * 20)

        print("\n\n--- RESULTADO FINAL DO PROCESSO HÍBRIDO ---")
        for i, article in enumerate(full_articles, 1):
            print(f"\nARTIGO {i}: {article['title']}")
            print(f"FONTE: {article['source']}")
            print(f"URL: {article['url']}")
            print("\nCONTEÚDO EXTRAÍDO:")
            print(f"{article['full_text']}")
            print("=" * 50)