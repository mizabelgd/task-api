# Prompt 1 - .gitignore

Contexto: Estou iniciando uma API Python com FastAPI.
Objetivo: Gere um arquivo .gitignore para Python, ambiente virtual, cache de testes e configurações locais do editor.
Estilo: Organize por seções com comentários.
Resposta: Forneça apenas o arquivo .gitignore, nada mais.

# Prompt 2 - README.md
Contexxto: MVP de micro-API RESTful para gestão de tarefas.
Objetivo: Escrever e criar um README inicial com objetivo, stack, como rodar localmente e roadmap de releases.
Estilo: Markdown simples, direto e profissional.
Resposta: Forneça o README completo.

# Prompt 3 - Endpoint de healtcheck

Contexto: Projeto em Python com FastAPI.
Objetivo: Criar app/main.py com uma instância FastAPI e endpoint GET /health retornando status ok e timestamp.
Estilo: Tipagem e código limpo.
Resposta: Forneça apenas o código de app/main.py

# Prompt 4 - Geração de Diagrama

Contexto: Estou projetando uma micro-API de gerenciamento de tarefas em Python com FastAPI. Ela terá um backend que se comunica com um banco de dados PostgreSQL.
Objetivo: Crie um diagrama de componentes usando Mermaid.js, que mostre a interação entre o backend e banco de dados. O backend deve ter componentes para controller, service e repository.
Estilo: Use o tipo diagrama C4-PlantUML, se possível, ou um diagrama de componentes simples. Identifique as setas de comunicação.
Resposta: Forneça apenas o código Mermaid na pasta docs.
Descrição: O diagrama de componentes ilustra a comunicação entre o backend (FastAPI) via HTTP/JSON, que por sua vez, interage com o banco de dados (PostgreSQL) por meio de queries SQL. A arquitetura do backend é dividida em controller, service e repository, sendo que o controller recebe as requisições, o service implementa a lógica de negócio e o repository gerencia a interação com o banco de dados.