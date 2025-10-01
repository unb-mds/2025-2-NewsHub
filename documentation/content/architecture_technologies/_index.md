---
title: "Architecture & Technologies"
---

# 🚀 Tecnologias e Arquitetura do Synapse

> O projeto Synapse está organizado em duas grandes partes: **backend** e **frontend**, apoiado por um banco de dados relacional e containerização via **Docker**. Essa separação garante escalabilidade, manutenção e clareza no desenvolvimento.

---

## ⚙️ Backend (Flask)

A estrutura do backend segue uma arquitetura modular em camadas que divide responsabilidades de forma clara e coesa.

| Caminho/Arquivo | Responsabilidade |
| :--- | :--- |
| **`backend/app/__init__.py`** | Inicializa a aplicação Flask, configurando todos os módulos e extensões. |
| **`backend/app/extensions.py`** | Centraliza a inicialização de extensões como `SQLAlchemy`, `JWT` e `Migrate`. |
| **`backend/app/main.py`** | Ponto de entrada que registra blueprints, rotas e inicializa o app. |
| **`backend/app/controllers/`** | Camada que lida com requisições HTTP, chamando os serviços adequados. |
| **`backend/app/entities/`** | Define as entidades de domínio, representando os objetos centrais do negócio. |
| **`backend/app/models/`** | Modelos ORM que correspondem diretamente às tabelas do banco de dados. |
| **`backend/app/repositories/`** | Abstrai a lógica de acesso e manipulação de dados no banco (CRUD). |
| **`backend/app/routes/`** | Definição dos endpoints da API e mapeamento de URLs para os `controllers`. |
| **`backend/app/services/`** | Implementação da lógica de negócio, orquestrando as operações. |
| **`tests/`** | Testes unitários e de integração para garantir a qualidade e estabilidade do backend. |
| **`requirements.txt`** | Lista de dependências Python do projeto. |
| **`Dockerfile`** | Script para construir a imagem Docker do serviço de backend. |
| **`crontab`** | Configuração dos jobs periódicos (ex: coleta de notícias da API externa). |

---

## 🎨 Frontend (React)

O frontend é uma *Single Page Application* (SPA) construída em React, com uma estrutura moderna e componentizada.

| Caminho | Responsabilidade |
| :--- | :--- |
| **`frontend/src/`** | Diretório raiz com todo o código-fonte da aplicação. |
| **`frontend/components/`** | Armazena componentes de UI reutilizáveis (botões, cards, inputs, etc.). |
| **`frontend/pages/`** | Componentes que representam páginas completas, combinando múltiplos componentes. |
| **`frontend/main.jsx`** | Ponto de entrada da aplicação, onde o React é renderizado no DOM. |

---

## 🗃️ Banco de Dados (PostgreSQL)

Utilizamos o **PostgreSQL** como banco de dados relacional, gerenciado pelo ORM **SQLAlchemy**. A modelagem atual permite uma personalização profunda da experiência do usuário.

![schema banco de dados](../assets/images/db-structure.jpg)


> Essa estrutura garante que os feeds sejam altamente personalizados, baseados em uma combinação de **categorias**, **fontes** e **tópicos** escolhidos pelo usuário.

---

## 🔗 APIs e Serviços Externos

O Synapse atua como um orquestrador inteligente, consumindo e processando dados de diversas fontes externas para entregar um produto final coeso e de alto valor. O fluxo de obtenção e processamento de notícias segue uma pipeline clara, executada pelo nosso job agendado (`cron`).

**Fluxo de Dados:** 🗓️ `Job` → 📰 `GNews` → 📄 `Newspaper3k` → ✨ `IA` → 🗃️ `Banco de Dados`

#### 1\. GNews API - Descoberta de Notícias

  * **O que é?** Uma API que permite pesquisar e obter artigos de notícias de milhares de fontes ao redor do mundo.
  * **Como é usado?** É o ponto de partida do nosso fluxo. O `cron` job executa um script que consulta a `GNews API` em busca de notícias recentes baseadas nos tópicos e palavras-chave de interesse definidos no sistema.
  * **Dados Obtidos:** Título, link para o artigo original, nome da fonte, data de publicação e uma breve descrição.

#### 2\. Newspaper3k - Extração de Conteúdo

  * **O que é?** Uma biblioteca Python avançada para extração de artigos e *web scraping*.
  * **Como é usado?** Após obter a lista de links da GNews, nosso script utiliza a `Newspaper3k` para "visitar" cada link. A biblioteca então analisa o HTML da página e extrai de forma inteligente apenas o conteúdo relevante do artigo, ignorando anúncios, menus e outros ruídos.
  * **Dados Obtidos:** O texto completo e limpo do artigo, a imagem principal, e metadados como autores.

#### 3\. API de IA (LLM) - Sumarização Inteligente

  * **O que é?** Um serviço de um Modelo de Linguagem Grande (LLM), como as APIs da OpenAI (GPT) ou Google (Gemini).
  * **Como é usado?** Com o texto completo do artigo em mãos (obtido pela `Newspaper3k`), nosso serviço envia este conteúdo para a API de IA com um *prompt* específico, instruindo-a a gerar um resumo conciso, neutro e informativo. Este resumo é a base da experiência rápida que o Synapse oferece.
  * **Dados Obtidos:** Um resumo em texto com os pontos-chave do artigo original.

> Ao final deste fluxo, os dados processados (título, fonte, link, texto completo e o resumo da IA) são salvos em nosso banco de dados **PostgreSQL**, prontos para serem exibidos aos usuários no frontend.


---

## 🐳 Docker & Orquestração (Docker Compose)

O ambiente é totalmente containerizado com **Docker** e orquestrado via **Docker Compose** para garantir consistência e facilidade de configuração. A arquitetura é composta por quatro serviços principais:

* **`backend`**
    * **Descrição**: Serviço da API em `Flask`.
    * **Detalhes**: Conecta-se ao banco via `DATABASE_URL`, expõe a porta `5001` e utiliza volumes para *hot reload* em desenvolvimento.

* **`frontend`**
    * **Descrição**: Serviço da interface em `React` (Vite).
    * **Detalhes**: Roda na porta `5173` e compartilha o código-fonte via volume para desenvolvimento ágil.

* **`cron`**
    * **Descrição**: Container dedicado a rodar jobs agendados (`cron`).
    * **Detalhes**: Utiliza a mesma imagem do `backend` para executar tarefas como a coleta periódica de notícias.

* **`db`**
    * **Descrição**: Serviço de banco de dados `PostgreSQL 14`.
    * **Detalhes**: Persiste os dados em um volume Docker (`postgres_data`) e inclui um `healthcheck` para garantir que os outros serviços só iniciem quando o banco estiver pronto.

> Essa abordagem modular permite que cada serviço seja desenvolvido, atualizado e escalado de forma independente, simplificando todo o ciclo de vida da aplicação.