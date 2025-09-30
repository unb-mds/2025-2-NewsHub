# Arquitetura do Projeto Synapse

O projeto Synapse está organizado em duas grandes partes: backend e frontend, apoiado por um banco de dados relacional e containerização via Docker. Essa separação garante escalabilidade, manutenção e clareza no desenvolvimento.

---

## Backend

A estrutura do backend segue uma arquitetura modular em camadas que divide responsabilidades:

- **backend/app/__init__.py**  
  Inicializa a aplicação Flask e configura todos os módulos e extensões necessárias.

- **backend/app/extensions.py**  
  Inicialização e configuração das extensões do Flask (banco de dados, JWT, migrações).

- **backend/app/main.py**  
  Ponto central para registrar blueprints, rotas e inicializar o app.

- **backend/app/controllers/**  
  Camada responsável por lidar com requisições HTTP chamando serviços e regras de negócio.

- **backend/app/entities/**  
  Define as entidades de domínio, representando os objetos centrais do negócio.

- **backend/app/models/**  
  Modelos ORM correspondentes às tabelas do banco de dados.

- **backend/app/repositories/**  
  Abstrações para persistência e manipulação de dados no banco.

- **backend/app/routes/**  
  Definição de endpoints e mapeamento de URLs para os controllers.

- **backend/app/services/**  
  Implementação da lógica de negócio e regras específicas.

- **tests/**  
  Testes unitários e de integração do backend.

- **requirements.txt**  
  Lista de dependências Python necessárias para rodar a aplicação.

- **Dockerfile**  
  Definição da imagem Docker para o backend.

- **crontab**  
  Configuração de jobs periódicos (coleta de notícias da API externa).

---

## Frontend

O frontend é uma SPA construída em React, organizada da seguinte forma:

- **frontend/src/**  
  Código-fonte do frontend.

- **frontend/components/**  
  Componentes reutilizáveis de interface.

- **frontend/pages/**  
  Páginas completas, combinando múltiplos componentes.

- **frontend/main.jsx**  
  Ponto de entrada da aplicação, inicializando rotas e renderização no DOM.

---

## Banco de Dados

O banco de dados utilizado é **PostgreSQL**, acessado via SQLAlchemy/ORM e estruturado para refletir entidades de usuários, notícias e preferências personalizadas. Atualmente, a modelagem conta com:

- **users**  
  Armazena dados de autenticação e perfis de usuários.

- **news**  
  Contém informações das notícias obtidas via API GNews.

- **sources**  
  Lista de fontes disponíveis para consulta de notícias.

- **categories**  
  Categorias de classificação das notícias.

- **user_news_sources** *(tabela auxiliar)*  
  Responsável por armazenar as fontes escolhidas por cada usuário, criando uma relação personalizada entre usuários e suas preferências de fontes.

- **topics**  
  Define tópicos de interesse que organizam e classificam notícias além de categorias e fontes, permitindo personalização mais detalhada.

- **users_topics** *(tabela auxiliar)*  
  Relação entre usuários e os tópicos de seu interesse, possibilitando que cada usuário configure quais assuntos deseja acompanhar.

Essa estrutura relacional garante que os usuários possam ter feeds de notícias altamente personalizados, baseados em **categorias**, **fontes** e **tópicos** específicos.

---

## Docker e Orquestração

O Synapse é totalmente containerizado com **Docker** e orquestrado via **Docker Compose**, permitindo execução consistente em diferentes ambientes. A configuração define quatro serviços principais:

- **backend**  
  Serviço Flask responsável pela API. Conecta-se ao banco via variável `DATABASE_URL`, expõe a porta **5001** e monta volumes para hot reload em desenvolvimento.

- **frontend**  
  Serviço de interface em React. Roda na porta **5173** e compartilha código-fonte via volume local para facilitar desenvolvimento.

- **cron**  
  Container dedicado a rodar jobs periódicos, como a coleta de notícias da API GNews, com acesso ao banco de dados e às mesmas dependências do backend.

- **db**  
  Serviço PostgreSQL 14 (imagem `alpine`), persistindo dados em um volume Docker (`postgres_data`) para evitar perda de dados entre reinícios. Inclui `healthcheck` para garantir que o banco esteja acessível antes de iniciar os demais containers.

Essa abordagem modular permite que cada serviço seja atualizado, escalado e monitorado de forma independente, simplificando tanto o desenvolvimento quanto a implantação em produção.
