---
title: "Getting Started"
---

# 🏁 Getting Started with Synapse

> Olá e seja bem-vindo(a) ao time do Synapse\! Ficamos muito felizes com seu interesse em contribuir. Este guia contém tudo que você precisa para configurar o ambiente, rodar o projeto localmente e fazer sua primeira contribuição.

O **Synapse** é um projeto de agregador de notícias inteligente, projetado para combater o excesso de informação e oferecer uma experiência de leitura rápida e personalizada. Desenvolvido com um back-end em Flask (Python) e um front-end em React, o sistema é totalmente containerizado com Docker para garantir um ambiente consistente para todos.

-----

## 🚀 Rodando o Projeto

Para começar, você só precisa do Git e do Docker instalados na sua máquina. Todo o resto é gerenciado pelos nossos contêineres.

### Pré-requisitos

  * [Git](https://git-scm.com/)
  * [Docker](https://www.docker.com/products/docker-desktop/) e Docker Compose

### Passo a Passo

**1. Clone o Repositório**
Abra seu terminal, clone o projeto e entre na pasta.

```sh
git clone https://github.com/unb-mds/2025-2-Synapse.git
cd 2025-2-Synapse
```

**2. Configure as Variáveis de Ambiente (Backend)**
O backend precisa de um arquivo `.env` para as chaves de API e configurações do banco de dados. Você pode copiar o exemplo:

```sh
# Na raiz do projeto
cp .env.example .env
```

> **Importante:** Abra o arquivo `.env` e preencha as chaves de API necessárias (como a da `GNews API`).

**3. Configure as Variáveis de Ambiente (Frontend)**
O frontend precisa saber o endereço da API. Crie o arquivo `.env` dentro da pasta `frontend/`:

```sh
# Comando executado a partir da raiz do projeto
echo "VITE_API_BASE_URL=http://localhost:5001" > frontend/.env
```

**4. Suba os Contêineres com Docker Compose**
Este é o comando mágico que irá construir as imagens e iniciar todos os serviços (backend, frontend, banco de dados e o job agendado).

```sh
docker compose up --build -d
```

  * A flag `--build` garante que as imagens serão reconstruídas se houver mudanças.
  * A flag `-d` (detached) roda os contêineres em segundo plano.

**5. Tudo Pronto\! ✅**
Se tudo correu bem, a aplicação estará disponível nos seguintes endereços:

  * **🖥️ Frontend (React):** `http://localhost:5173`
  * **⚙️ Backend (Flask API):** `http://localhost:5001`
  * **📚 Documentação da API (Swagger):** `http://localhost:5001/api/docs`

-----

## 🤝 Como Contribuir

Com o ambiente rodando, você está pronto para contribuir\! Existem várias formas de ajudar:

  * **Reportando Bugs:** Encontrou um problema? Abra uma [Issue](https://github.com/unb-mds/2025-2-Synapse/issues) detalhando o erro.
  * **Sugerindo Melhorias:** Tem uma ideia para uma nova funcionalidade? Abra uma [Issue](https://github.com/unb-mds/2025-2-Synapse/issues) com a tag `enhancement`.
  * **Escrevendo Código:** Para corrigir bugs ou implementar features, siga nosso fluxo de trabalho.

### Nosso Fluxo de Trabalho (Git Workflow)

1.  **Crie uma Branch a partir da `dev`**
    Todo novo trabalho deve ser feito em uma branch separada, criada a partir da `dev`.

    ```sh
    # Garanta que sua branch dev local está atualizada
    git switch dev
    git pull origin dev

    # Crie sua nova branch
    git switch -c <tipo>/<nome-descritivo>
    ```

    *Exemplos:* `feat/pagina-de-perfil`, `fix/erro-login-social`, `docs/atualizar-getting-started`

2.  **Faça Commits Atômicos e Semânticos**
    Siga o [Padrão de Commit](https://github.com/iuricode/padroes-de-commits). Cada commit deve representar uma pequena unidade lógica de trabalho. Veja a tabela abaixo.

3.  **Mantenha sua Branch Atualizada**
    Antes de submeter seu trabalho, sincronize sua branch com a `dev` para resolver possíveis conflitos.

    ```sh
    # Estando na sua branch de feature
    git pull origin dev
    ```

4.  **Abra um Pull Request (PR)**
    Quando seu trabalho estiver pronto, envie um Pull Request para a branch `dev`. Preencha o template do PR para que todos entendam o que foi feito.

5.  **Aguarde a Revisão de Código**
    Pelo menos um outro membro da equipe precisa revisar e aprovar seu PR antes que ele seja integrado.

### Padrão de Commits Semânticos

A estrutura é: `<emoji> <tipo>(<escopo>): <descrição>`

| Tipo | Emoji | Descrição |
| :--- | :--- | :--- |
| `feat` | ✨ | Uma nova funcionalidade para o usuário. |
| `fix` | 🐛 | Uma correção de bug. |
| `docs`| 📚 | Mudanças apenas na documentação. |
| `chore`| 🔧 | Mudanças de configuração, scripts, tarefas. |
| `refactor`| ♻️ | Refatoração de código que não altera a funcionalidade. |
| `test`| 🧪 | Adição ou modificação de testes. |
| `style`| 💄 | Mudanças de estilo e formatação de código. |

-----

## 📈 Nosso Processo de Desenvolvimento

Para garantir a qualidade e o alinhamento, seguimos dois conceitos importantes:

### Definition of Ready (DoR)

Uma tarefa está **pronta para ser iniciada** se:

  * ✅ A história está bem escrita e clara.
  * ✅ Os Critérios de Aceitação são objetivos e testáveis.
  * ✅ Foi discutida e entendida por todo o time de desenvolvimento.
  * ✅ Foi estimada em Story Points.

### Definition of Done (DoD)

Uma tarefa é considerada **concluída** quando:

  * ✅ O código foi implementado conforme os Critérios de Aceitação.
  * ✅ O código foi revisado e aprovado por, no mínimo, um colega.
  * ✅ Testes automatizados (quando aplicáveis) foram criados e estão passando.
  * ✅ A funcionalidade foi integrada à branch `dev`.
  * ✅ Foi demonstrada e validada na Sprint Review.

Qualquer dúvida, não hesite em perguntar no nosso canal de comunicação\! Boas contribuições\!
Este guia explica como executar o projeto Synapse, incluindo backend, frontend, banco de dados e o cron job que faz a requisição das notícias pela API Gnews.

---