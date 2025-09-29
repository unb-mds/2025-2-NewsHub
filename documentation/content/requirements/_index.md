---
title: "Requisitos e Fluxos - Detalhado"
---

# Requisitos do Projeto Synapse

## Requisitos Funcionais

- Usuário pode acessar notícias públicas sem login.  
- Sistema de cadastro com os campos obrigatórios:  
  - Nome completo  
  - Email
  - Data de nascimento  
  - Senha (mínimo 8 caracteres e pelo menos uma letra maiúscula)  
  - Confirmação de senha  
- Login autenticado via email e senha.  
- Usuário autenticado acessa conteúdo personalizado com sistema de recomendação.  
- Permitir que usuários definam tópicos favoritos e fontes favoritas.  
- Ao criar um tópico ou adicionar fonte, vincular automaticamente ao usuário na tabela auxiliar correspondente.  
- Sistema de recomendação adaptado ao comportamento e preferências do usuário.  
- Newsletter diária personalizada com conteúdo recomendável e resumos gerados por IA.

## Requisitos Não Funcionais

- Segurança no armazenamento da senha, com validação baseada em regras (senha forte) e uso de JWT para autenticação sem necessidade de armazenar senhas em texto.  
- Performance para resposta rápida da API e frontend.  
- Escalabilidade para suportar o crescimento do número de usuários e volume de notícias.  
- Interface responsiva e acessível em diversos dispositivos.   

## Fluxos do Sistema

1. O visitante acessa a plataforma e visualiza notícias públicas sem necessidade de autenticação.  
2. Para acessar o sistema de recomendação, o usuário deve se cadastrar, fornecendo nome completo, email, data de nascimento, senha e confirmação ou pode apenas logar no sitema se ja tiver cadastro.
3. A senha deve atender os critérios mínimos de segurança (mínimo 8 caracteres, pelo menos uma letra maiúscula).  
4. Finalizado o cadastro, o usuário realiza login com email e senha.  
5. No perfil, o usuário pode configurar tópicos favoritos e fontes preferenciais.  
6. Ao criar um novo tópico ou adicionar novas fontes, o sistema vincula automaticamente esses registros ao usuário, usando tabelas auxiliares para relacionamento.  
7. O usuário autenticado recebe um feed de notícias personalizado pela recomendação inteligente.  
8. O sistema registra o comportamento de leitura e interação do usuário para melhorar recomendações futuras.  
9. Periodicamente, um cron job atualiza as notícias da API, mantendo o conteúdo atualizado.  
10. Usuários recebem newsletters personalizadas conforme seus interesses e preferências definidos.

Este fluxo garante uma experiência aberta para visitantes, e uma experiência rica e personalizada para usuários cadastrados.

---
