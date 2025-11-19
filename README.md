# InovaTech
InovaTech – Sistema Acadêmico

Este projeto foi desenvolvido como parte das atividades da graduação em Análise e Desenvolvimento de Sistemas. O objetivo é simular um sistema acadêmico funcional, integrando diferentes áreas (aluno, professor e administração), de forma simples, organizada e próxima da realidade de uma aplicação web.

O desenvolvimento foi realizado praticamente de forma individual, com apoio técnico pontual de ferramentas de IA para dúvidas específicas e otimizações.

Tecnologias Utilizadas
Backend

Python (Flask)

SQLite para persistência de dados

Estrutura modular para rotas, templates e banco

Bibliotecas padrão do Python

Frontend

HTML5

CSS3

JavaScript

Templates Jinja2 integrados ao Flask

Ferramentas de Desenvolvimento

Visual Studio Code

Git e GitHub

Ambiente Windows

IA Generativa apenas como suporte técnico (refinamento de ideias e correções)

Principais Funcionalidades
Área do Aluno

Login autenticado

Visualização de notas

Acesso a materiais enviados pelo professor

Consulta ao calendário acadêmico

Área do Professor

Cadastro e edição de notas

Upload de materiais

Controle de turmas e conteúdos

Administração

Banco de dados estruturado em SQLite

Organização interna por pastas (templates, static, uploads)

Rotas protegidas e lógica de sessão

Arquitetura e Estrutura do Projeto
InovaTech/
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── logo-inovatech.png
│
├── templates/
│   ├── index.html
│   ├── aluno.html
│   └── professor.html
│
├── uploads/
│
├── academia.db
└── app.py


A estrutura foi pensada para ser clara e de fácil manutenção, separando arquivos estáticos, páginas, banco de dados e código backend.

Como Executar o Projeto

Instale o Flask:

pip install flask


Execute o servidor:

python app.py


Abra no navegador:

http://127...


O sistema inicializa imediatamente e já se conecta ao banco academia.db.

Objetivo Educacional do Projeto

O InovaTech foi criado para:

praticar Python aplicado ao desenvolvimento web

reforçar lógica de programação

aprender arquitetura de aplicações Flask

trabalhar com banco de dados

integrar frontend e backend

aplicar versionamento de código

simular um sistema acadêmico próximo de um produto real

Autor

Douglas Vinicius
Estudante de Análise e Desenvolvimento de Sistemas
Contato profissional: vinimoreira565@gmail.com
