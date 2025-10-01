# Changelog

Todo o histórico de mudanças deste projeto será documentado neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

---

## [0.1.0-alpha] - 2025-09-30

### ✨ Adicionado (Added)

- **Autenticação de Usuário:** Implementado registro, login e logout de usuários com sessões seguras baseadas em cookies JWT.
- **Gerenciamento de Perfil:** Usuários podem visualizar, editar suas informações (nome, e-mail, data de nascimento) e alterar a senha.
- **Gerenciamento de Tópicos:** Funcionalidade para usuários adicionarem e removerem tópicos de interesse do seu perfil.
- **Gerenciamento de Fontes de Notícias:** Usuários podem selecionar e desmarcar fontes de notícias preferidas para personalizar seu feed.
- **Coleta Automatizada de Notícias:** Criado um job agendado (cron) que roda a cada 6 horas para buscar e salvar novas notícias utilizando a GNews API e web scraping.
- **Interface do Usuário (Frontend):** Desenvolvidas as telas de Login, Registro, Gerenciamento de Conta e Adição de Fontes com React e Tailwind CSS.
- **Documentação da API:** Adicionada documentação interativa da API utilizando Swagger/OpenAPI.
- **Estrutura de Testes:** Configurado ambiente de testes com Pytest para o back-end, incluindo testes para rotas e serviços.
