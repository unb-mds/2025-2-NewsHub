# Releases do Projeto Synapse

---

# Release 1: Validação, Base Técnica e Core Funcional (01/10/2025)

> **Objetivo da Release:** O foco principal da Release 1 foi estratégico: **validar a viabilidade** da ideia do Synapse e **retirar as principais incertezas** técnicas e de produto. O trabalho se concentrou em **construir a base** da aplicação em três frentes essenciais:
> 1.  Uma **arquitetura robusta** e escalável com Docker, Flask e React.
> 2.  O **ciclo de vida completo do usuário**, incluindo autenticação e gerenciamento de perfil.
> 3.  A entrega do protótipo funcional do **motor de coleta de notícias**, o job automatizado que é o coração do produto.
>
> Ao final desta etapa, provamos que o conceito é tecnicamente realizável e temos o alicerce pronto para escalar as funcionalidades de entrega de conteúdo ao usuário.

### Foco Estratégico da Release
* **Validar a Ideia:** Provar que o conceito do agregador inteligente era tecnicamente possível com as ferramentas escolhidas.
* **Retirar Incertezas:** Solidificar as decisões de arquitetura (Flask, React, Docker) e as metodologias de trabalho da equipe.
* **Provar a Viabilidade:** Demonstrar que os componentes críticos — banco de dados, API, frontend e o job agendado — poderiam operar de forma integrada e eficiente.
* **Construir a Base:** Entregar o alicerce de código e infraestrutura sobre o qual todas as futuras funcionalidades serão construídas, garantindo a manutenibilidade e escalabilidade do projeto.

---

## Detalhamento das Sprints

### Sprint 0: Base Técnica e Alinhamento
* **🎯 Meta:** Reduzir as principais incertezas do projeto e alinhar a visão técnica e de produto da equipe, garantindo uma base sólida e escalável para o futuro.
* **🗓️ Prazos:** 24/08/2025 – 06/09/2025

#### ✅ Escopo Entregue
* Proposta de Projeto (`#1`)
* Implementação de Sistema de Recomendação (`#2`)
* Criar Documentos/Artefatos Iniciais na Wiki (`#3`)
* Containerização com Docker (`#4`)
* Arquitetura de Front-end com React (`#5`)
* Estrutura de uma API com Flask (`#6`)
* Integração Flask e SQLAlchemy (`#7`)
* Pesquisa e Definição de Metodologias Ágeis (`#8`)
* Configurar o Ambiente de Desenvolvimento com Docker (`#9`)
* Configuração de Banco de Dados (`#12`)
* Documento de Arquitetura (`#13`)
* Definir Escopo do MVP (`#14`)
* Pesquisar e definir a biblioteca de componentes UI (`#15`)

#### ⚠️ Pendências
* Criar Design System (`#11`)


---

### Sprint 1: Autenticação de Usuário
* **🎯 Meta:** Implementar as funcionalidades essenciais de autenticação, permitindo que um usuário crie uma conta e acesse a plataforma.
* **🗓️ Prazos:** 07/09/2025 – 13/09/2025

#### ✅ Escopo Entregue
* Criar Meu Cadastro (`#17`)
* Autenticação de Usuário com E-mail (`#18`)
* Criar Design System (`#11`)
* Prova de Conceito para Consumo de APIs de Notícias (`#16`)

---

### Sprint 2: Gerenciamento de Conta do Usuário
* **🎯 Meta:** Garantir que o usuário possa manter seus dados cadastrais atualizados e, crucialmente, implementar a infraestrutura de coleta de notícias.
* **🗓️ Prazos:** 14/09/2025 – 20/09/2025

#### ✅ Escopo Entregue
* Editar Informações da Conta (`#57`)
* Alterar Senha (`#58`)
* Script de Coleta de Notícias e Gerenciamento de Fontes (`#21`)
* Configurar contêiner do job agendado (Cron) (`#81`)

#### ⚠️ Pendências
* Visualizar Página de Perfil e Preferências (`#22`)
* Gerenciar Tópicos de Interesse (`#59`)

---

### Sprint 3: Ciclo Completo e Documentação
* **🎯 Meta:** Finalizar o ciclo completo de gerenciamento de conta e personalização de conteúdo, e consolidar a documentação técnica da Release 1.
* **🗓️ Prazos:** 21/09/2025 – 27/09/2025

#### ✅ Escopo Entregue
* Criar gitpage com Hugo (`#90`)
* Implementar Swagger para documentação dos endpoints (`#112`)
* Atualizar `README.md` (`#92`)
* Criar testes unitários da Sprint 2 (`#93`)
* Gerenciar Tópicos de Interesse (`#59`)
* Visualizar Página de Perfil e Preferências (`#22`)
* Gerenciar Fontes de Notícias Preferidas (`#80`)
* Logout de Usuário (`#19`)

#### ⚠️ Pendências
* Criar diagrama C4 (`#91`)