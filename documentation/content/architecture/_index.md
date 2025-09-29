---
title: "Arquitetura do Projeto"
---

# Arquitetura do Projeto Synapse

O projeto Synapse está organizado em duas grandes partes: backend e frontend, cada uma com sua estrutura modular para facilitar manutenção, escalabilidade e clareza no desenvolvimento.

---

## Backend

A estrutura do backend segue uma arquitetura modular e em camadas para separar responsabilidades:

- **backend/app/__init__.py**  
  Inicializa a aplicação Flask e configura todos os módulos e extensões necessárias.

- **backend/app/extensions.py**  
  Inicialização e configuração das extensões do Flask (como banco de dados, JWT, migrates).

- **backend/app/main.py**  
  Ponto central para registrar blueprints, rotas e inicializar o app.

- **backend/app/controllers/**  
  Contém os controllers responsáveis por lidar com as requisições HTTP e orquestrar chamadas às camadas inferiores.

- **backend/app/entities/**  
  Define as entidades de domínio do sistema, ou seja, as classes que representam os objetos principais do negócio.

- **backend/app/models/**  
  Contém os modelos que representam as tabelas no banco de dados, geralmente usados pelo ORM.

- **backend/app/repositories/**  
  Responsável pelo acesso e manuseio direto dos dados, abstraindo operações CRUD do banco.

- **backend/app/routes/**  
  Definem os endpoints da API e mapeiam as URLs para os controllers correspondentes.

- **backend/app/services/**  
  Camada intermediária contendo a lógica de negócio e regras específicas do projeto.

- **tests/**  
  Testes unitários e de integração para validar o funcionamento das diversas partes do backend.

- **requirements.txt**  
  Declara as dependências Python necessárias para executar o backend.

- **Dockerfile**  
  Definição da imagem Docker para empacotar o backend do projeto.

- **crontab**  
  Arquivo para definição de tarefas agendadas, como o cron job que coleta notícias da API.

---

## Frontend

O frontend é baseado em React com a seguinte organização:

- **frontend/src/**  
  Pasta principal com todo o código fonte JavaScript/TypeScript do frontend.

- **frontend/components/**  
  Componentes React reutilizáveis da interface, organizados por funcionalidade.

- **frontend/pages/**  
  Páginas inteiras que compõem as rotas da aplicação, compostas pelos componentes.

- **frontend/main.jsx**  
  Ponto de entrada da aplicação frontend, responsável por renderizar o React no DOM e configurar rotas principais.

---

## Visão Geral da Arquitetura

- O **backend** é uma API REST construída com Flask, responsável por fornecer dados, autenticação e lógica de negócio. Comunica-se com o banco de dados PostgreSQL (ou similar) e integra-se com APIs externas para coleta de notícias.

- O **frontend** é uma SPA (Single Page Application) feita em React, consumindo a API e apresentando uma experiência interativa ao usuário final.

- O sistema inclui um **cron job** agendado, que roda periodicamente para coletar notícias via API GNews, que são armazenadas no banco e posteriormente expostas no frontend.

- A aplicação é containerizada usando **Docker** e orquestrada via **Docker Compose** para facilitar o desenvolvimento local e a implantação.

Essa estrutura modular, clara e separada por responsabilidades, promove fácil manutenção e escalabilidade do projeto Synapse.
