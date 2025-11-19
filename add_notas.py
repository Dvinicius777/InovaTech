# ============================================================
# populate_db.py — InovaTech v2.2
# Função:
#   Gera e popula o banco academia.db com dados de exemplo
#   para uso no sistema InovaTech (app.py v19.3)
#
# Desenvolvido por: Douglas Vinicius (UNIP – 2025)
# ============================================================

import sqlite3
import os
from datetime import date

DB = "academia.db"

# ======== Reinicializa o banco de dados (com confirmação) ========
if os.path.exists(DB):
  try:
    resp = input("⚠️ Deseja recriar o banco de dados 'academia.db'? (S/N): ").strip().lower()
  except EOFError:
    resp = "s"  # fallback silencioso se não houver input (ex: execução automática)

  if resp != "s":
    print("Operação cancelada. Banco existente preservado.")
    exit(0)

  os.remove(DB)
  print("🗑️ Banco de dados antigo removido.")

conn = sqlite3.connect(DB)
cur = conn.cursor()

print("🧩 Criando estrutura de tabelas...")

# ======== Criação completa das tabelas ========
cur.executescript("""
CREATE TABLE IF NOT EXISTS utilizadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT UNIQUE,
    pass TEXT,
    role TEXT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS turmas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE,
    ano INTEGER,
    semestre INTEGER
);

CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT,
    email TEXT UNIQUE,
    turma_id INTEGER,
    data_nascimento TEXT,
    FOREIGN KEY (turma_id) REFERENCES turmas(id)
);

CREATE TABLE IF NOT EXISTS notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    disciplina TEXT,
    nota REAL,
    data DATE,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);

CREATE TABLE IF NOT EXISTS frequencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    disciplina TEXT,
    data_aula DATE,
    status TEXT,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id)
);

CREATE TABLE IF NOT EXISTS atividades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT,
    disciplina TEXT,
    data_entrega DATE,
    status_envio TEXT DEFAULT 'Pendente'
);

CREATE TABLE IF NOT EXISTS submissoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    atividade_id INTEGER,
    aluno_id INTEGER,
    nome_ficheiro TEXT,
    path_ficheiro TEXT,
    data_envio DATE,
    FOREIGN KEY (atividade_id) REFERENCES atividades(id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    UNIQUE(atividade_id, aluno_id)
);
""")

print("✅ Tabelas criadas/verificadas.")

# ======== Inserção de dados iniciais ========
print("📚 Inserindo dados base (usuários, turmas, alunos, notas, frequência, atividades)...")

cur.executescript("""
INSERT OR IGNORE INTO utilizadores (user, pass, role, name) VALUES
('prof.inova', '123', 'professor', 'Prof. Carlos Mendes'),
('aluno1', '123', 'aluno', 'Maria Silva'),
('aluno2', '123', 'aluno', 'João Pereira'),
('aluno3', '123', 'aluno', 'Ana Costa');

INSERT OR IGNORE INTO turmas (nome, ano, semestre) VALUES ('ADS 2025', 2025, 2);

INSERT OR IGNORE INTO alunos (nome_completo, email, turma_id, data_nascimento) VALUES
('Maria Silva', 'maria@inovatech.edu', 1, '2002-05-12'),
('João Pereira', 'joao@inovatech.edu', 1, '2001-09-23'),
('Ana Costa', 'ana@inovatech.edu', 1, '2003-03-30');

INSERT INTO atividades (titulo, disciplina, data_entrega, status_envio) VALUES
('Trabalho de Redes', 'Infraestrutura de Redes', '2025-11-25', 'Pendente'),
('Atividade de Python', 'Programação Estruturada', '2025-11-20', 'Pendente'),
('Pesquisa sobre LGPD', 'Governança e Ética', '2025-11-30', 'Enviado');

INSERT INTO notas (aluno_id, disciplina, nota, data) VALUES
(1, 'Infraestrutura de Redes', 8.5, '2025-10-05'),
(1, 'Programação Estruturada', 9.0, '2025-10-15'),
(2, 'Governança e Ética', 7.2, '2025-10-12'),
(3, 'Infraestrutura de Redes', 6.8, '2025-10-10');

INSERT INTO frequencia (aluno_id, disciplina, data_aula, status) VALUES
(1, 'Infraestrutura de Redes', '2025-10-01', 'Presente'),
(1, 'Infraestrutura de Redes', '2025-10-02', 'Falta'),
(2, 'Governança e Ética', '2025-10-03', 'Presente'),
(3, 'Programação Estruturada', '2025-10-04', 'Presente');
""")

# ======== Disciplinas e atividades extras ========
cur.executescript("""
INSERT INTO atividades (titulo, disciplina, data_entrega, status_envio) VALUES
('Trabalho de Segurança da Informação', 'Segurança da Informação', '2025-12-05', 'Pendente'),
('Relatório de Banco de Dados Avançado', 'Banco de Dados II', '2025-12-10', 'Pendente'),
('Estudo de Redes IPv6', 'Infraestrutura de Redes', '2025-12-15', 'Pendente'),
('Apresentação sobre IA Generativa', 'Inteligência Artificial', '2025-12-20', 'Pendente');

INSERT INTO notas (aluno_id, disciplina, nota, data) VALUES
(1, 'Segurança da Informação', 8.2, '2025-11-10'),
(2, 'Banco de Dados II', 9.1, '2025-11-11'),
(3, 'Inteligência Artificial', 9.5, '2025-11-11');
""")

conn.commit()

print("\n📊 Tabelas criadas:")
for (name,) in cur.execute("SELECT name FROM sqlite_master WHERE type='table';"):
    print(f" - {name}")

conn.close()

print("\n✅ Banco 'academia.db' criado e populado com sucesso!")
print("👩‍🏫 Professor: prof.inova / 123")
print("👨‍🎓 Alunos: aluno1, aluno2, aluno3 / 123")

# ============================================
# FIM DO ARQUIVO — populate_db.py v2.2
# Desenvolvido por Douglas Vinicius (UNIP – 2025)
# ============================================
