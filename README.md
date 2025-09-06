# NewsHub

NewsHub é um projeto de agregador de notícias desenvolvido para a disciplina de Métodos de Desenvolvimento de Software. A arquitetura é composta por um backend em Flask (Python) e um frontend em React (JavaScript), orquestrados com Docker.

## Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em sua máquina:

- **Git**: Para clonar o repositório.
- **Docker e Docker Compose**: Para rodar o ambiente de desenvolvimento de forma conteinerizada.
- **Python 3.12+** e **pip**: Necessário apenas para o desenvolvimento local do backend.
- **Node.js e npm**: Necessário apenas para o desenvolvimento local do frontend.

---

## Como Rodar o Projeto (Docker - Método Recomendado)

Este é o método mais simples e rápido para ter todo o ambiente (backend, frontend e banco de dados) funcionando, sem a necessidade de instalar Python ou Node.js diretamente na sua máquina.

1.  **Clone o repositório:**

    ```sh
    git clone https://github.com/unb-mds/NewsHub.git
    cd NewsHub
    ```

2.  **Crie o arquivo de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`. O Docker Compose usará este arquivo para obter as credenciais do banco de dados.

    ```sh
    # No Windows (CMD):
    copy .env.example .env
    # No Linux / macOS / WSL:
    cp .env.example .env
    ```

3.  **Suba os contêineres:**
    Este comando irá construir as imagens do backend e frontend e iniciar todos os serviços em segundo plano (`-d`).

    ```sh
    # No Windows (CMD/PowerShell):
    docker-compose up --build -d
    # No Linux (Bash/Zsh):
    docker compose up --build -d
    ```

4.  **Inicialize o Banco de Dados:**
    Com os contêineres em execução, execute o comando abaixo uma única vez para criar as tabelas no banco de dados.

    ```sh
    docker-compose exec backend flask init-db
    ```

5.  **Pronto!**
    A aplicação estará disponível nos seguintes endereços:
    - **Frontend (React)**: http://localhost:5173
    - **Backend (Flask API)**: http://localhost:5001

---

## Desenvolvimento Local (Alternativo - Ambiente Virtual)

Use este método se preferir rodar os serviços diretamente na sua máquina, sem Docker. Você precisará de uma instância do PostgreSQL rodando localmente.

### 1. Backend (Python/Flask)

**a. Crie e ative o ambiente virtual (`.venv`)**

Abra o terminal na raiz do projeto (`NewsHub/`).

- **Windows (CMD / PowerShell):**

  ```shell
  # Criar o ambiente
  python -m venv .venv

  # Ativar no CMD
  .\.venv\Scripts\activate

  # Ativar no PowerShell (pode exigir permissão de execução de scripts)
  .\.venv\Scripts\Activate.ps1
  ```

- **Linux / macOS / WSL (Windows Subsystem for Linux):**

  ```shell
  # Criar o ambiente
  python3 -m venv .venv

  # Ativar
  source .venv/bin/activate
  ```

**b. Instale as dependências**

Com o ambiente virtual ativado, instale os pacotes Python:

```shell
pip install -r backend/requirements.txt
```

**c. Configure e inicie o backend**

1.  Crie um arquivo `.env` na raiz do projeto e adicione a URL de conexão do seu banco de dados PostgreSQL local.
    Para que os comandos `flask` funcionem da raiz do projeto, **é essencial adicionar a variável `FLASK_APP`**.
    ```
    # Exemplo de conteúdo para o arquivo .env
    FLASK_APP=backend.app.main
    DATABASE_URL=postgresql+psycopg://SEU_USUARIO:SUA_SENHA@localhost:5432/SEU_BANCO
    ```
2.  Com o ambiente virtual ativado, execute os comandos a partir da **raiz do projeto**:

    Inicialize o banco de dados:

    ```shell
    flask init-db
    ```

    Inicie o servidor Flask:

    ```shell
    flask run --port 5001
    ```

### 2. Frontend (React/Vite)

1.  Em um **novo terminal**, navegue até a pasta do frontend: `cd frontend`
2.  Instale as dependências do Node.js: `npm install`
3.  Inicie o servidor de desenvolvimento: `npm run dev`
4.  O frontend estará disponível em http://localhost:5173.
