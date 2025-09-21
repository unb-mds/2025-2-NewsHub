# NewsHub

NewsHub é um projeto de agregador de notícias desenvolvido para a disciplina de Métodos de Desenvolvimento de Software. A arquitetura é composta por um backend em Flask (Python) e um frontend em React (JavaScript), orquestrados com Docker.

## Pré-requisitos

Antes de começar, garanta que você tenha as seguintes ferramentas instaladas em sua máquina:

- **Git**: Para clonar o repositório.
- **Docker e Docker Compose**: Para rodar o ambiente de desenvolvimento de forma conteinerizada.
- **Python 3.12+** e **pip**: Necessário apenas para o desenvolvimento local do backend.
- **Node.js e npm**: Necessário apenas para o desenvolvimento local do frontend.

---

## Como Rodar o Projeto (Docker)

1.  **Clone o repositório:**

    ```sh
    git clone https://github.com/unb-mds/NewsHub.git
    cd NewsHub
    ```

2.  **Suba os contêineres:**
    Este comando irá construir as imagens do backend e frontend e iniciar todos os serviços em segundo plano (`-d`).

    ```sh
    # No Windows (CMD/PowerShell):
    docker-compose up --build -d
    # No Linux (Bash/Zsh):
    docker compose up --build -d
    ```

3.  **Pronto!** A aplicação inicializará o banco de dados automaticamente na primeira vez que for executada.

A aplicação estará disponível nos seguintes endereços:
- **Frontend (React)**: http://localhost:5173
- **Backend (Flask API)**: http://localhost:5001

