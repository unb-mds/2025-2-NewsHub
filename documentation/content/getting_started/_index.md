---
title: "Getting Started"
---

# Como rodar o Projeto

Este guia explica como executar o projeto Synapse, incluindo backend, frontend e banco de dados, tanto via Docker (recomendado) quanto em ambiente local para desenvolvimento.

---

## Pré-requisitos

- **Git** (para clonar o repositório)
- **Docker Desktop** (para orquestração dos serviços)
- **Python 3.12+** (para desenvolvimento local do backend)
- **Node.js e npm** (para desenvolvimento local do frontend)
- **Software de gerenciamento de banco de dados** (opcional, ex: DBeaver, TablePlus, pgAdmin)

---

## Execução Recomendada: Docker

1. **Clonar o repositório**
    ```bash
    git clone https://github.com/unb-mds/NewsHub.git
    cd NewsHub
    ```

2. **Criar arquivo de ambiente**
    ```bash
    cp .env.example .env
    # Edite o arquivo .env conforme necessário (ex: credenciais do banco, chaves de API)
    ```

3. **Subir os contêineres**
    ```bash
    docker compose up --build -d
    ```

4. **Inicializar o banco de dados**
    ```bash
    docker compose exec backend flask init-db
    ```

5. **Acessar os serviços**
    - **Frontend:** [http://localhost:5173](http://localhost:5173)
    - **Backend:** [http://localhost:5001](http://localhost:5001)
    - **Banco de Dados:** O serviço de banco de dados estará disponível na porta definida no `docker-compose.yml` (ex: 5432 para PostgreSQL).  
      Você pode conectar-se usando um software gráfico para visualizar e gerenciar as tabelas.

---

## Execução Local (Desenvolvimento)

### 1) Backend (Python/Flask)

1. **Criar e ativar ambiente virtual**
    ```bash
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate
    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

2. **Instalar dependências**
    ```bash
    pip install -r backend/requirements.txt
    ```

3. **Configurar variáveis de ambiente**
    - Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias (exemplo em `.env.example`).
    - Configure o banco de dados localmente (ex: PostgreSQL/MySQL) e ajuste a string de conexão:
      ```env
      FLASK_APP=backend.app.main
      DATABASE_URL=postgresql+psycopg://<USUARIO>:<SENHA>@localhost:5432/<SEU_BANCO>
      ```

4. **Inicializar e rodar o backend**
    ```bash
    flask init-db
    flask run --port 5001
    ```

### 2) Frontend (React/Vite)

1. **Instalar dependências**
    ```bash
    cd frontend
    npm install
    ```

2. **Rodar o servidor de desenvolvimento**
    ```bash
    npm run dev
    ```

---

## Gerenciamento do Banco de Dados

- O banco de dados pode ser acessado e gerenciado usando softwares como **DBeaver**, **pgAdmin**, **TablePlus** ou similares.
- Configure a conexão usando as credenciais definidas no `.env` ou no `docker-compose.yml`.
- Isso permite visualizar, editar e administrar as tabelas e dados do projeto de forma gráfica.

---

> **Dica:** Para desenvolvimento, utilize Docker para garantir que todos os serviços estejam integrados e configurados corretamente. O acesso ao banco de dados via software gráfico facilita testes e depuração.