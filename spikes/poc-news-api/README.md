# [Resultado da Spike] PoC - Consumo de API de Notícias e Extração de Conteúdo

- **Autor:** @gccintra
- **Data:** 10 de setembro de 2025
- **Status:** Concluído

## 1. Objetivo Original da Pesquisa
O objetivo inicial desta spike era criar uma Prova de Conceito (PoC) para validar tecnicamente o consumo de uma API de notícias. A meta era entender a facilidade de integração, a estrutura dos dados retornados e como poderíamos utilizar essas informações no nosso back-end.

## 2. Metodologia e Execução
1.  A API escolhida para o teste inicial foi a **NewsAPI.org**, devido à sua boa documentação e à existência de uma biblioteca cliente para Python.
2.  Foi obtida uma chave de API do plano gratuito.
3.  Desenvolvemos um script Python para se conectar à API e chamar o endpoint `get_everything`, buscando por um tema de interesse.

## 3. Descoberta Crítica: Limitação do Conteúdo da API
Durante a execução da PoC, fizemos uma descoberta fundamental que impacta diretamente a arquitetura do nosso produto:

**A API de notícias não retorna o conteúdo completo do artigo.**

O campo `content` presente na resposta da API é apenas um trecho (snippet) do texto original, frequentemente finalizado com uma indicação como `[+XXXX chars]`.

Essa limitação inviabiliza nossa proposta de valor principal, que depende de ter acesso ao texto completo para:
1.  Realizar os resumos com o nosso módulo de IA.
2.  Exibir a notícia completa dentro da nossa própria plataforma, sem redirecionar o usuário para um site externo.

## 4. Pivô da Pesquisa e Solução: Web Scraping
Para resolver o problema, a pesquisa foi estendida para encontrar uma forma de obter o texto completo a partir da URL do artigo, que é fornecida pela API. A solução encontrada foi a utilização de uma biblioteca de **web scraping especializada em notícias**.

A biblioteca **`newspaper3k`** foi selecionada para esta tarefa, pois ela é projetada para identificar e extrair automaticamente o corpo principal de um artigo, limpando elementos indesejados como menus, anúncios e rodapés.

## 5. Fluxo de Trabalho Híbrido Proposto
Com base na descoberta, o fluxo de trabalho para obter as notícias no NewsHub deve ser um **modelo híbrido**:

1.  **Passo 1 - Descoberta (API):** Utilizar a **NewsAPI.org** para descobrir novas notícias, obter seus metadados (título, fonte, imagem) e, mais importante, a **URL** para o artigo original.
2.  **Passo 2 - Extração (Web Scraping):** Para cada URL descoberta, nosso sistema utilizará a biblioteca **`newspaper3k`** para visitar a página e extrair o conteúdo textual completo do artigo.
3.  **Passo 3 - Armazenamento:** O texto completo extraído será salvo em nosso banco de dados, pronto para ser usado pelo módulo de resumo da IA e para ser exibido aos nossos usuários.
