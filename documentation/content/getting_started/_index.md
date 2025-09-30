---
title: "Getting Started"
---

# Como rodar o Synapse

Este guia explica como executar o projeto Synapse, incluindo backend, frontend, banco de dados e o cron job que faz a requisição das notícias pela API Gnews.

---

## Pré-requisitos

- **Git** (para clonar o repositório)
- **Docker Desktop** (para orquestração dos serviços)
- **Python 3.12+** (para desenvolvimento do backend)
- **Node.js e npm** (para desenvolvimento do frontend)
- **Software de gerenciamento de banco de dados** (opcional, ex: DBeaver, TablePlus, pgAdmin)

---

## Execução Recomendada: Docker

1. **Clonar o repositório**  
    ```
    git clone https://github.com/unb-mds/NewsHub.git
    cd NewsHub
    ```

2. **Criar arquivo de ambiente**  
    ```
    cp .env.example .env
    # Edite o arquivo .env conforme necessário (ex: credenciais do banco, chaves de API)
    ```

3. **Subir os contêineres**  
    ```
    docker compose up --build -d
    ```

4. **Inicializar o banco de dados**  
    ```
    docker compose exec backend flask init-db
    ```

5. **Executar o Cron Job para coleta de notícias**  
    ```
    docker compose exec backend python3 app/jobs/collect_news.py
    ```

6. **Acessar os serviços**  
    - Frontend: [http://localhost:5173](http://localhost:5173)  
    - Backend: [http://localhost:5001](http://localhost:5001)  
    - Banco de Dados: porta definida no `docker-compose.yml` (ex: 5432 para PostgreSQL).  
      Pode usar software gráfico para gerenciá-lo.

---

## Execução Local (Desenvolvimento)

### Backend (Python/Flask)

1. **Criar e ativar ambiente virtual**  
    ```
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

2. **Instalar dependências**  
    ```
    pip install -r backend/requirements.txt
    ```

3. **Configurar variáveis de ambiente**  
    - Crie um arquivo `.env` na raiz do projeto baseado no `.env.example`.  
    - Configure a string de conexão com o banco local. Exemplo:  
    ```
    FLASK_APP=backend.app.main
    DATABASE_URL=postgresql+psycopg://<USUARIO>:<SENHA>@localhost:5432/<SEU_BANCO>
    ```

4. **Inicializar e rodar o backend**  
    ```
    flask init-db
    flask run --port 5001
    ```

### Frontend (React/Vite)

1. **Instalar dependências**  
    ```
    cd frontend
    npm install
    ```

2. **Rodar o servidor de desenvolvimento**  
    ```
    npm run dev
    ```

---

## Gerenciamento do Banco de Dados

- Pode utilizar softwares gráficos como **DBeaver**, **pgAdmin**, **TablePlus** ou similares para acessar e gerenciar o banco.
- Configure a conexão usando credenciais do `.env` ou `docker-compose.yml`.
- Facilita a visualização, edição e administração das tabelas e dados.

---