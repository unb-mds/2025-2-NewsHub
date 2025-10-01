import os
import requests
from newspaper import Article # Adicionando a biblioteca de scraping

# --- CONFIGURAÇÃO INICIAL ---

# No terminal, antes de rodar, faça: export GNEWS_API_KEY='sua_chave_gnews_aqui'
API_KEY = os.getenv('GNEWS_API_KEY')
API_ENDPOINT = "https://gnews.io/api/v4/search"

if not API_KEY:
    raise ValueError("A variável de ambiente GNEWS_API_KEY não foi configurada.")

# --- FUNÇÕES ---

def discover_articles_via_gnews(query, language='pt', country='br', max_articles=1):
    """Usa a GNews API para descobrir os artigos e suas URLs."""
    print(f"[*] PASSO 1: Buscando artigos com a GNews API sobre '{query}'...")
    params = {'q': query, 'lang': language, 'country': country, 'apikey': API_KEY, 'max': max_articles}
    
    try:
        response = requests.get(API_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json().get('articles', [])
    except Exception as e:
        print(f"    [!] Erro ao chamar a GNews API: {e}")
        return []

def scrape_article_content(url):
    """Usa a newspaper3k para extrair o conteúdo completo de uma URL."""
    try:
        print(f"    -> PASSO 2: Fazendo scraping da URL com newspaper3k...")
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"    [!] Erro no scraping de {url}: {e}")
        return None

# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    articles_metadata = discover_articles_via_gnews('bolsonaro', max_articles=1)
    
    if not articles_metadata:
        print("\nNenhum artigo encontrado pela API. Encerrando.")
    else:
        print(f"\n[OK] Descoberta concluída. {len(articles_metadata)} artigos encontrados.")
        print("\n--- INICIANDO ANÁLISE E EXTRAÇÃO ---")
        
        for i, article_meta in enumerate(articles_metadata, 1):
            print(f"\n{'='*50}")
            print(f"ANALISANDO ARTIGO {i}")
            print(f"TÍTULO: {article_meta.get('title')}")
            print(f"FONTE: {article_meta.get('source', {}).get('name')}")
            print(f"URL: {article_meta.get('url')}")
            
            
            # 3. EXTRAÇÃO DO CONTEÚDO COMPLETO
            full_text = scrape_article_content(article_meta.get('url'))
            
            print("\n[B] CONTEÚDO COMPLETO (EXTRAÍDO COM NEWSPAPER3K):")
            if full_text:
                print(f"{full_text}") 
                print(f"(Tamanho: {len(full_text)} caracteres)")
            else:
                print("[FALHA] Não foi possível extrair o conteúdo completo.")
        
        print(f"\n{'='*50}")