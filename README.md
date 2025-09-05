# NewsHub Project (Squad 14)

Este é o repositório para o projeto NewsHub, contendo os serviços de backend, frontend e banco de dados, todos orquestrados com Docker e prontos para desenvolvimento com VS Code.

## 🚀 Começando

Este projeto é configurado para usar **VS Code Dev Containers**, que automatiza completamente a configuração do ambiente de desenvolvimento.

### Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados e rodando:

1.  **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: Essencial para rodar os contêineres.
2.  **[Visual Studio Code](https://code.visualstudio.com/)**: Nosso editor de código padrão.
3.  **Extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)**: A extensão do VS Code que faz a mágica acontecer.

### Passos para Rodar

1.  **Clone o repositório** para a sua máquina local.
    ```bash
    git clone git@github.com:unb-mds/2025-2-squad-14.git
    cd 2025-2-squad-14
    ```

2.  **Abra o projeto no VS Code.**
    ```bash
    code .
    ```

3.  **Reabra no Contêiner.** O VS Code irá detectar a configuração e mostrará uma notificação no canto inferior direito. Clique no botão **"Reopen in Container"**.

    Aguarde o processo. O VS Code irá construir as imagens, iniciar os três contêineres (`backend`, `frontend`, `db`) e conectar você ao ambiente de desenvolvimento.

4.  **Inicialize o Banco de Dados (Apenas na primeira vez).**
    Quando o ambiente estiver pronto (você verá `Dev Container: NewsHub Backend Dev` no canto inferior esquerdo), abra um terminal no VS Code (`Ctrl+` ou `Cmd+`) e execute o único comando manual necessário:
    ```bash
    flask init-db
    ```
    Isso criará as tabelas no banco de dados.

### Acesso aos Serviços

-   **Backend (API)**: `http://localhost:5001`
-   **Frontend**: `http://localhost:5173`
-   **Banco de Dados (PostgreSQL)**: Acessível na porta `5432` para clientes de DB.

### 💡 Solução de Problemas (Troubleshooting)

-   **Erro "Container name is already in use"**:
    Isso acontece se você já tiver contêineres antigos rodando. Para resolver, pare e remova os contêineres atuais executando o seguinte comando no seu terminal (fora do VS Code):
    ```bash
    docker-compose down
    ```
    Depois, tente reabrir no contêiner pelo VS Code novamente.

-   **A notificação "Reopen in Container" não aparece**:
    Verifique se a extensão Dev Containers está instalada e ativada. Você também pode abrir a Paleta de Comandos (`Cmd+Shift+P` ou `Ctrl+Shift+P`) e procurar por `Dev Containers: Reopen in Container`.