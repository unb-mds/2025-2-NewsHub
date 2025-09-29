# Synapse

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Pull Requests](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)

Synapse é um projeto de agregador de notícias inteligente, projetado para combater o excesso de informação e oferecer uma experiência de leitura rápida e personalizada. A plataforma utiliza uma API de notícias para descobrir artigos, IA para gerar resumos, e um sistema de recomendação que aprende com as interações do usuário para customizar o feed de notícias.

Desenvolvido com um back-end em Flask (Python) e um front-end em React, o sistema é totalmente containerizado com Docker para garantir um ambiente de desenvolvimento e implantação consistente.

## ✨ Principais Funcionalidades

* **Coleta Automatizada:** Um job diário busca e enriquece notícias de fontes globais usando a GNews API e web scraping.
* **Feed Personalizado:** Os utilizadores podem gerir tópicos de interesse e fontes de notícias preferidas para customizar o seu feed.
* **Gestão de Conta:** Sistema completo de autenticação, visualização e edição de perfil.
* **(Futuro) Resumos com IA:** Geração de resumos concisos para otimizar o tempo de leitura.
* **(Futuro) Newsletter Diária:** Envio de um e-mail personalizado com as notícias mais relevantes para o utilizador.

## 🚀 Stack de Tecnologias

| Camada | Tecnologia |
| :--- | :--- |
| **Front-end** | React.js, Vite, Tailwind CSS |
| **Back-end** | Python, Flask, SQLAlchemy |
| **Base de Dados** | PostgreSQL |
| **Infraestrutura** | Docker, Docker Compose |
| **Coleta de Dados**| GNews API, Newspaper3k |

## 🏁 Como Rodar o Projeto (Ambiente Docker)

**Pré-requisitos:**
* Git
* Docker e Docker Compose

1.  **Clone o repositório:**
    ```sh
    git clone [https://github.com/unb-mds/2025-2-NewsHub.git](https://github.com/unb-mds/2025-2-NewsHub.git)
    cd 2025-2-NewsHub
    ```

2.  **Configure as Variáveis de Ambiente:**
    Crie um ficheiro `.env` na raiz do projeto para o back-end e as chaves de API. Pode usar o `.env.example` como base.

3.  **Configure o Ambiente do Front-end:**
    O front-end precisa saber onde a API do back-end está a ser executada.
    * Na pasta `frontend/`, crie um ficheiro chamado `.env`.
    * Adicione a seguinte linha a este ficheiro:
        ```env
        VITE_API_BASE_URL=http://localhost:5001
        ```
    Este ficheiro não deve ser versionado (já está no `.gitignore`) para garantir que cada programador possa ter a sua própria configuração local.

4.  **Suba os contentores:**
    Este comando irá construir as imagens e iniciar todos os serviços.
    ```sh
    docker compose up --build -d
    ```

5.  **Pronto!** A aplicação estará disponível em:
    * **Frontend (React):** `http://localhost:5173`
    * **Backend (Flask API):** `http://localhost:5001`
    * **Documentação da API (Swagger):** `http://localhost:5001/api/docs`

## 🤝 Como Contribuir
Este é um projeto de código aberto e adoraríamos receber a sua contribuição! Para saber como, por favor leia o nosso **[Guia de Contribuição](CONTRIBUTING.md)**.

## 📜 Código de Conduta
Para garantir uma comunidade acolhedora e inclusiva, esperamos que todos os participantes sigam o nosso **[Código de Conduta](CODE_OF_CONDUCT.md)**.

## 📄 Licença
Este projeto está licenciado sob a Licença MIT. Veja o ficheiro [LICENSE](LICENSE) para mais detalhes.
