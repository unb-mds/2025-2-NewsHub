---
title: "About Project"
---

# Proposta de Projeto: Synapse

## 1. Título do Projeto
Synapse: Plataforma de Notícias Inteligente com Agregação via API, Personalização e Sistema de Recomendação.

## 2. Resumo
O projeto Synapse propõe o desenvolvimento de uma plataforma web inovadora para descoberta e consumo de notícias. Utilizando uma API dedicada (GNews), o sistema agregará artigos de fontes globais. Os usuários poderão navegar por notícias categorizadas, aplicar filtros avançados e receber recomendações personalizadas com base em seu comportamento. Um diferencial importante é a newsletter diária opcional, que entrega resumos gerados por IA, agrupando diferentes perspectivas sobre o mesmo evento e alinhando o conteúdo aos interesses de cada usuário.

## 3. Objetivos

### 3.1. Objetivo Geral
Desenvolver uma plataforma web completa e personalizada para consumo de notícias, integrando uma API de conteúdo, processamento com Inteligência Artificial e um sistema de recomendação baseado no comportamento do usuário.

### 3.2. Objetivos Específicos
- **Integração com API de Notícias:** Coletar artigos de forma estruturada e eficiente, substituindo o web scraping tradicional.
- **Desenvolvimento do Portal Web:** Exibir notícias categorizadas, com funcionalidades de busca e filtros.
- **Personalização por Tags:** Permitir que o usuário defina seus interesses por meio de tags.
- **Monitoramento de Comportamento:** Rastrear interações do usuário (artigos lidos, salvos, compartilhados).
- **Sistema de Recomendação:** Implementar algoritmos para sugerir notícias relevantes conforme o perfil do usuário.
- **Funcionalidades de Engajamento:** Recursos como "Salvar para Ler Depois" e "Favoritos".
- **Módulo de IA Avançado:** Utilizar IA para gerar resumos e agrupar artigos sobre o mesmo evento.
- **Newsletter Inteligente:** Enviar diariamente uma newsletter personalizada, baseada no sistema de recomendação e processada por IA.

## 4. Tecnologias Utilizadas

| Categoria          | Tecnologia                                    |
| ------------------ | --------------------------------------------- |
| **Linguagem Principal** | Python                                        |
| **Fonte de Dados** | API de Notícias (NewsAPI.org ou NewsAPI.ai) |
| **Agente de IA** | API de LLM (ex: OpenAI GPT, Google Gemini)    |
| **Banco de Dados** | PostgreSQL ou MySQL                           |
| **Machine Learning** | Pandas, Scikit-learn                          |
| **Containerização** | Docker                                        |
| **Back-End** | Flask                                         |
| **Front-End** | React.js                                      |

## 5. Arquitetura do Sistema

O fluxo de dados será centrado na interação do usuário com a plataforma:

1. Um **Cron Job** ou agendador de tarefas busca periodicamente novos artigos na **API de Notícias** e os armazena no **Banco de Dados**.
2. O **Usuário** acessa o **Portal Web** e interage com o conteúdo (lê, clica, favorita). Essas interações são registradas no banco de dados.
3. O **Sistema de Recomendação** processa os dados de interação para construir um perfil de interesse do usuário.
4. Ao navegar pelo portal, o sistema de recomendação atua em tempo real, filtrando e ordenando as notícias exibidas conforme o perfil do usuário.
5. Para a **Newsletter**, o sistema seleciona os artigos mais relevantes, que são processados pelo **Módulo de IA** (resumo e agrupamento) antes do envio.