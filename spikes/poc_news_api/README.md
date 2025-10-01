# [Resultado da Spike] PoC - GNews API e Extração de Conteúdo Híbrida

- **Autor:** @gccintra
- **Data:** 10 de setembro de 2025
- **Issue Original:** #16

## 1. Objetivo da Pesquisa
Esta Prova de Conceito (PoC) foi realizada para encontrar e validar uma API de notícias que atendesse aos requisitos do projeto NewsHub, principalmente:
1.  Permitir o uso em um ambiente de produção para um projeto acadêmico/não-comercial.
2.  Fornecer um método viável para obter o conteúdo completo dos artigos de notícias.

A API selecionada para este teste foi a **[GNews API](https://gnews.io/)**.

## 2. Metodologia
Foi desenvolvido um script Python que implementa um fluxo de trabalho híbrido:
1.  **Descoberta:** O script primeiro chama a GNews API para buscar os metadados dos artigos mais recentes sobre um determinado tópico.
2.  **Extração:** Em seguida, para cada artigo descoberto, o script utiliza a biblioteca `newspaper3k` para visitar a URL original e fazer o web scraping do conteúdo textual completo.

## 3. Descobertas e Análise

### Sobre a GNews API
* **Termos de Uso:** O plano gratuito da GNews se mostrou adequado para os nossos requisitos, permitindo o uso em produção para projetos de baixo volume e não-comerciais.
* **Qualidade dos Dados:** As buscas por notícias em português (`lang=pt`, `country=br`) retornaram resultados relevantes e de boa qualidade.
* **Conteúdo:** A análise da resposta da API confirmou que, assim como outras, a GNews retorna apenas um trecho ou resumo no campo `content`. Isso validou a necessidade de uma solução complementar.

### Sobre o Web Scraping com `newspaper3k`
* A biblioteca `newspaper3k` foi **extremamente eficaz**. Ela conseguiu extrair com sucesso o conteúdo completo e limpo da maioria das URLs fornecidas pela GNews, removendo elementos de navegação e anúncios.

## 4. Fluxo Híbrido Validado
A spike confirmou que a arquitetura híbrida é a solução correta para o nosso projeto. O processo de usar a API para descobrir notícias e o web scraping para extrair o conteúdo é funcional e robusto.
