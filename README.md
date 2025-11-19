InovaTech
Sistema Acadêmico – Projeto Acadêmico

O InovaTech é um sistema acadêmico desenvolvido como parte das atividades da graduação em Análise e Desenvolvimento de Sistemas.
O objetivo foi simular, de forma funcional, um ambiente acadêmico que integra diferentes perfis (aluno, professor e administração), oferecendo navegação clara, páginas estruturadas e funcionalidades reais de um sistema web.

Todo o desenvolvimento foi feito praticamente de forma individual, com uso de IA apenas como apoio para dúvidas técnicas específicas.

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

Templates Jinja2 (integrados ao Flask)

Ferramentas

Windows (ambiente de desenvolvimento)

VS Code

Git e GitHub

IA Generativa utilizada apenas para suporte técnico (revisão de ideias e correções pontuais)

Funcionalidades
Área do Aluno

Login autenticado

Visualização de notas

Acesso a materiais enviados pelos professores

Consulta ao calendário acadêmico

Área do Professor

Cadastro e edição de notas

Upload de materiais

Controle de turmas e conteúdos

Administração

Banco de dados estruturado em SQLite

Organização interna por pastas (templates, static, uploads)

Lógica de sessão e rotas protegidas

Estrutura do Projeto
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
├── app.py
├── add_notas.py
├── populate_db.py
└── demais arquivos auxiliares


A estrutura foi pensada para ser simples e de fácil manutenção, mantendo arquivos estáticos, páginas, banco de dados e backend claramente separados.

Como Executar o Projeto

Instale o Flask:

pip install flask


Execute o servidor:

python app.py


Abra no navegador:

http://127.0.0.1:5000


O sistema inicializa automaticamente e já utiliza o banco de dados academia.db.

Objetivo Educacional do Projeto

O InovaTech foi criado para:

Praticar Python aplicado ao desenvolvimento web

Reforçar lógica de programação

Estudar arquitetura básica de aplicações Flask

Trabalhar com banco de dados SQLite

Integrar frontend e backend

Aplicar versionamento de código

Simular um sistema acadêmico próximo de um produto real

Autor

Douglas Vinicius
Estudante de Análise e Desenvolvimento de Sistemas
Contato profissional: vinimoreira565@gmail.com
