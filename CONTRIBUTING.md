# Guia de Contribuição do Synapse

Olá! Ficamos muito felizes com seu interesse em contribuir para o Synapse. Este documento contém tudo que você precisa para começar.

## Como Posso Contribuir?
* **Reportando Bugs:** Encontrou um problema? Abra uma [Issue](https://github.com/unb-mds/2025-2-NewsHub/issues) detalhando o problema, como reproduzi-lo e o comportamento esperado.
* **Sugerindo Melhorias:** Tem uma ideia para uma nova funcionalidade? Abra uma [Issue](https://github.com/unb-mds/2025-2-NewsHub/issues) com a tag `enhancement`.
* **Contribuindo com Código:** Se você quer corrigir um bug ou implementar uma nova funcionalidade, siga o fluxo de trabalho abaixo.

## Nosso Fluxo de Trabalho (Git Workflow)

1.  **Crie uma Branch a partir da `develop`:** Todo novo trabalho deve partir da branch `develop` atualizada.
    ```sh
    git switch develop
    git pull origin develop
    git switch -c <tipo>/<nome-descritivo-da-branch>
    ```
    *Exemplos de nomes:* `feat/user-profile`, `fix/login-bug`, `chore/update-readme`

2.  **Faça Commits Atômicos e Semânticos:** Siga o padrão de [Conventional Commits](https://www.conventionalcommits.org/pt-br). Cada commit deve ser uma pequena unidade lógica de trabalho.

3.  **Mantenha sua Branch Atualizada:** Antes de submeter seu trabalho, sincronize sua branch com a `develop` para resolver conflitos localmente.
    ```sh
    # Estando na sua branch de feature
    git pull origin develop
    ```

4.  **Abra um Pull Request (PR):** Envie suas alterações para a branch `develop`. Use o [template de PR](.github/PULL_REQUEST_TEMPLATE.md) para garantir que sua descrição esteja completa.

5.  **Aguarde a Revisão:** Pelo menos um outro membro da equipe precisa revisar e aprovar seu PR antes do merge.

### Padrão de Commits
Usamos o padrão de Commits Convencionais com emojis. A estrutura é: `<emoji> <tipo>(<escopo>): <descrição>`

| Tipo | Emoji | Descrição |
| :--- | :--- | :--- |
| `feat` | ✨ | Uma nova funcionalidade para o usuário. |
| `fix` | 🐛 | Uma correção de bug. |
| `docs`| 📚 | Mudanças apenas na documentação. |
| `chore`| 🔧 | Mudanças de configuração, scripts, tarefas. |
| `refactor`| ♻️ | Refatoração de código que não altera a funcionalidade. |
| `test`| 🧪 | Adição ou modificação de testes. |
| `style`| 💄 | Mudanças de estilo e formatação de código. |

### Configuração do Ambiente
As instruções para rodar o projeto localmente com Docker estão no nosso **[README.md](README.md)**.