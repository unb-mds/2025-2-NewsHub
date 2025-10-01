# Documento de Requisitos - Synapse

## 1. Introdução
Este documento consolida os **Requisitos Funcionais (RFs)** e os **Requisitos Não Funcionais (RNFs)** do sistema Synapse.  
Ele serve como referência para a equipe de desenvolvimento, garantindo clareza sobre *o que o sistema deve fazer* e *como deve se comportar*.  

---

## 2. Requisitos Funcionais

### Épico 001: Autenticação e Cadastro
*Permitir que os usuários criem e acessem suas contas de forma segura.*

| ID | Requisito Funcional |
| :--- | :--- |
| HU001.1 | Cadastro de Usuário com E-mail e Senha |
| HU001.2 | Autenticação de Usuário com E-mail e Senha |
| HU001.4 | Autenticação com Google (Login Social) |
| HU001.5 | Login sem senha (Magic Login) |

---

### Épico 002: Consumo de Notícias
*Garantir a melhor experiência para o usuário ao visualizar e interagir com conteúdos noticiosos.*

| ID | Requisito Funcional |
| :--- | :--- |
| TT002.1 | (Técnico) Coleta Automatizada de Notícias via Job |
| HU002.1 | Visualização do Feed Principal de Notícias |
| HU002.10 | Ler o conteúdo completo de uma notícia dentro da plataforma |
| HU002.8 | Favoritar / Salvar uma Notícia para ler depois |
| HU002.3 | Filtros Avançados no Feed (por data, etc.) |
| HU002.2 | Aba "Recomendados" com base no comportamento do usuário |
| TT002.2 | (Técnico) Salvar comportamento do usuário para o sistema de recomendação |
| HU002.9 | Interação "Não Tenho Interesse" em uma Notícia |
| HU002.5 | Resumo do Dia com IA (por tópico) |
| HU002.6 | Visualizar Notícias Agrupadas por Fonte |
| HU002.4 | Seção de Notícias "Quentes" (Hot News) |
| HU002.7 | Notícias por Localização |

---

### Épico 003: Perfil e Preferências
*Permitir que o usuário visualize e personalize suas informações e preferências.*

| ID | Requisito Funcional |
| :--- | :--- |
| HU003.1 | Visualizar a Página de Perfil ("Minha Conta") |
| HU003.5 | Seleção Inicial de Interesses (Tópicos) no Onboarding |
| HU003.6 | Editar Informações da Conta (Nome, Data de Nascimento) |
| HU003.7 | Alterar Senha |
| HU003.8 | Gerenciar Tópicos Preferidos (Adicionar/Remover) |
| HU003.9 | Gerenciar Fontes de Notícias Preferidas (Adicionar/Remover) |
| HU003.4 | Logout de Usuário |
| HU003.2 | Visualizar Página de Notícias Favoritas |
| HU003.3 | Histórico de Notícias Lidas |

---

### Épico 004: Newsletter
*Automatizar o envio de newsletters personalizadas com base nos interesses do usuário.*

| ID | Requisito Funcional |
| :--- | :--- |
| HU004.1 | Envio da Newsletter Diária com base nos interesses |
| HU004.5 | Habilitar/Desabilitar Recebimento da Newsletter |
| HU004.2 | Seleção de Interesses específica para a Newsletter |
| HU004.3 | Sistema de Feedback sobre Notícias da Newsletter |
| HU004.4 | Personalização do Prompt de Resumo da IA para a Newsletter |

---

## 3. Requisitos Não Funcionais

### Desempenho
| ID | Requisito | Métrica |
| :--- | :--- | :--- |
| RNF-01 | Tempo de Resposta da API | 95% das requisições GET < 500ms |
| RNF-02 | Carregamento da Página Principal | < 3s em conexão banda larga |
| RNF-03 | Execução do Job de Coleta | Concluir em < 1 hora |
| RNF-04 | Chamadas à IA | Resumo em até 10s |

### Segurança
| ID | Requisito | Métrica |
| :--- | :--- | :--- |
| RNF-05 | Armazenamento de Senhas | Hash + sal (bcrypt) |
| RNF-06 | Autenticação de API | JWT obrigatório |
| RNF-07 | Comunicação Segura | Exclusivamente HTTPS |
| RNF-08 | Proteção de Chaves | Somente via variáveis de ambiente |

### Usabilidade
| ID | Requisito | Métrica |
| :--- | :--- | :--- |
| RNF-09 | Responsividade | Suporte a Desktop, Tablet e Smartphone |
| RNF-10 | Compatibilidade com Navegadores | Últimas 2 versões de Chrome, Firefox, Safari |
| RNF-11 | Feedback Visual | Indicador de carregamento em ações demoradas |

### Manutenibilidade e Escalabilidade
| ID | Requisito | Métrica |
| :--- | :--- | :--- |
| RNF-12 | Containerização | Docker + Docker Compose |
| RNF-13 | Padrões de Código | Python PEP8, JS/React com Prettier |
| RNF-14 | Separação de Camadas | Controller, Service, Repository |
| RNF-15 | Logging | Log de coletas e erros críticos da API |
