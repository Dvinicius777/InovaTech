# ============================================================
# SISTEMA INOVATECH – DASHBOARD EDUCACIONAL
# Arquivo: app.py
# Versão: 35.0 (InoAI Centralizada - Cérebro Unificado)
# Descrição:
#   Backend leve. A lógica de conversação foi movida para
#   o cerebro_ia.py, deixando este arquivo focado em dados e ML.
# ============================================================

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from werkzeug.utils import secure_filename
import socket
import ctypes
import random

# === IMPORTAÇÃO DO CÉREBRO (A Alma da InoAI) ===
try:
    from cerebro_ia import buscar_resposta_avancada
except ImportError:
    print("⚠️ ERRO: 'cerebro_ia.py' não encontrado. A IA ficará muda.")
    def buscar_resposta_avancada(msg): return None

# === IMPORTAÇÕES MACHINE LEARNING (O Raciocínio) ===
try:
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    ML_ATIVO = True
except ImportError:
    ML_ATIVO = False
    print("⚠️ AVISO: Scikit-Learn não instalado.")

# =====================
# CONFIGURAÇÕES BÁSICAS
# =====================
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

DATABASE_FILE = 'academia.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'zip', 'rar', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =====================
# INTEGRAÇÃO C (Legado)
# =====================
try:
    dll = ctypes.CDLL("./analise.dll")
    dll.verificar_risco_ia.argtypes = [ctypes.c_double, ctypes.c_int]
    dll.verificar_risco_ia.restype = ctypes.c_int
except Exception:
    dll = None

# =====================
# TREINAMENTO (ML + Sentimentos)
# =====================
modelo_inoai = None
modelo_emocao = None
vetorizador = None

def treinar_inteligencia():
    global modelo_inoai, modelo_emocao, vetorizador
    if not ML_ATIVO: return

    print("🧠 InoAI: Carregando modelos neurais...")
    
    # 1. RISCO (Regressão Linear)
    np.random.seed(42)
    notas = np.random.normal(7.0, 2.0, 1000).clip(0, 10)
    faltas = np.random.normal(4 + (10 - notas), 3, 1000).clip(0, 30)
    risco = (faltas * 3.5) + ((10 - notas) * 8.5) + np.random.normal(0, 5, 1000)
    X_risco = np.column_stack((notas, faltas))
    
    modelo_inoai = LinearRegression()
    modelo_inoai.fit(X_risco, risco.clip(0, 100))
    
    # 2. EMOÇÃO (Naive Bayes)
    frases = ["odeio", "horrivel", "triste", "reprovei", "dificil", "chato", "raiva", "medo",
              "amo", "adoro", "legal", "incrivel", "bom", "excelente", "aprovei", "feliz"]
    classes = [0]*8 + [1]*8
    
    vetorizador = CountVectorizer()
    X_emo = vetorizador.fit_transform(frases)
    modelo_emocao = MultinomialNB()
    modelo_emocao.fit(X_emo, classes)
    
    print("✅ InoAI: Sistemas Cognitivos Online (Risco + Emoção)!")

def analisar_sentimento(texto):
    if not modelo_emocao: return ""
    palavras_chave = ['odeio','amo','triste','feliz','horrivel','otimo','medo','incrivel','ruim','bom']
    if not any(p in texto for p in palavras_chave): return ""
    
    sentimento = modelo_emocao.predict(vetorizador.transform([texto]))[0]
    return "😟 Sinto que você não está bem... " if sentimento == 0 else "✨ Que energia boa! "

# =====================
# BANCO DE DADOS
# =====================
def get_conn(row_factory: bool = False):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    if row_factory: conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.cursor().executescript("""
    CREATE TABLE IF NOT EXISTS utilizadores (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT UNIQUE, pass TEXT, role TEXT, name TEXT);
    CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT UNIQUE, ano INTEGER, semestre INTEGER);
    CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_completo TEXT, email TEXT UNIQUE, turma_id INTEGER, data_nascimento TEXT, FOREIGN KEY (turma_id) REFERENCES turmas(id));
    CREATE TABLE IF NOT EXISTS notas (id INTEGER PRIMARY KEY AUTOINCREMENT, aluno_id INTEGER, disciplina TEXT, nota REAL, data DATE DEFAULT (date('now','localtime')), FOREIGN KEY (aluno_id) REFERENCES alunos(id));
    CREATE TABLE IF NOT EXISTS frequencia (id INTEGER PRIMARY KEY AUTOINCREMENT, aluno_id INTEGER, disciplina TEXT, data_aula DATE, status TEXT, FOREIGN KEY (aluno_id) REFERENCES alunos(id));
    CREATE TABLE IF NOT EXISTS atividades (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, disciplina TEXT, data_entrega DATE);
    CREATE TABLE IF NOT EXISTS submissoes (id INTEGER PRIMARY KEY AUTOINCREMENT, atividade_id INTEGER, aluno_id INTEGER, nome_ficheiro TEXT, path_ficheiro TEXT, data_envio DATE DEFAULT (date('now','localtime')), FOREIGN KEY (atividade_id) REFERENCES atividades(id), FOREIGN KEY (aluno_id) REFERENCES alunos(id), UNIQUE(atividade_id, aluno_id));
    """)
    conn.commit()
    conn.close()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =====================
# ROTAS WEB
# =====================
@app.route('/')
def index(): return render_template('index.html')
@app.route('/aluno')
def aluno_page(): return render_template('aluno.html')
@app.route('/professor')
def professor_page(): return render_template('professor.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    conn = get_conn(row_factory=True)
    u = conn.execute("SELECT * FROM utilizadores WHERE user=? AND pass=?", (data.get('user'), data.get('pass'))).fetchone()
    conn.close()
    if not u: return jsonify({"success": False, "message": "Login inválido."}), 401
    
    aid = None
    if u['role'] == 'aluno':
        conn = get_conn(row_factory=True)
        row = conn.execute("SELECT id FROM alunos WHERE nome_completo=?", (u['name'],)).fetchone()
        aid = row['id'] if row else 1 # Fallback para 1 se não achar (ambiente teste)
        conn.close()
        
    return jsonify({"success": True, "user": {"id": u['id'], "name": u['name'], "role": u['role'], "aluno_id": aid}})

# =====================
# APIS DE DADOS
# =====================
@app.route('/atividades', methods=['GET', 'POST'])
def atividades():
    conn = get_conn(row_factory=True)
    if request.method == 'POST':
        d = request.json
        conn.execute("INSERT INTO atividades (titulo, disciplina, data_entrega) VALUES (?,?,?)", (d['titulo'], d['disciplina'], d['data_entrega']))
        conn.commit(); conn.close()
        return jsonify({"success": True})
    
    aid = request.args.get('aluno_id')
    if aid:
        rows = conn.execute("SELECT a.id, a.titulo, a.disciplina, a.data_entrega, CASE WHEN s.id IS NOT NULL THEN 'Enviado' ELSE 'Pendente' END as status_envio FROM atividades a LEFT JOIN submissoes s ON a.id=s.atividade_id AND s.aluno_id=? ORDER BY a.data_entrega", (aid,)).fetchall()
    else:
        rows = conn.execute("SELECT s.id, a.titulo as atividade, al.nome_completo as aluno, s.nome_ficheiro, s.data_envio FROM submissoes s JOIN atividades a ON s.atividade_id = a.id JOIN alunos al ON s.aluno_id = al.id ORDER BY s.data_envio DESC").fetchall()
    
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/notas/aluno/<int:id>')
def notas(id):
    conn = get_conn(row_factory=True)
    rows = conn.execute("SELECT disciplina, nota, data FROM notas WHERE aluno_id=? ORDER BY data DESC", (id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/frequencia/aluno/<int:id>')
def freq(id):
    conn = get_conn(row_factory=True)
    rows = conn.execute("SELECT disciplina, date(data_aula) as data_aula, status FROM frequencia WHERE aluno_id=? ORDER BY data_aula DESC", (id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/calendario')
def calendario():
    conn = get_conn(row_factory=True)
    rows = conn.execute("SELECT id, titulo, disciplina, data_entrega FROM atividades").fetchall()
    conn.close()
    return jsonify([{"id": r['id'], "title": r['titulo'], "start": r['data_entrega'], "color": "#007acc"} for r in rows])

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('file'); aid = request.form.get('aluno_id'); tid = request.form.get('atividade_id')
    if f and allowed_file(f.filename):
        path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(path)
        conn = get_conn()
        conn.execute("INSERT INTO submissoes (atividade_id, aluno_id, nome_ficheiro, path_ficheiro) VALUES (?,?,?,?) ON CONFLICT(atividade_id, aluno_id) DO UPDATE SET nome_ficheiro=excluded.nome_ficheiro, data_envio=date('now')", (tid, aid, f.filename, path))
        conn.commit(); conn.close()
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route('/uploads/<filename>')
def download_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# =====================
# APIS DE IA
# =====================
@app.route('/ia/risco/aluno/<int:aluno_id>')
def ia_risco(aluno_id):
    conn = get_conn(row_factory=True)
    m = conn.execute("SELECT AVG(nota) as m FROM notas WHERE aluno_id=?", (aluno_id,)).fetchone()['m'] or 0
    f = conn.execute("SELECT COUNT(*) as f FROM frequencia WHERE aluno_id=? AND status='Falta'", (aluno_id,)).fetchone()['f'] or 0
    conn.close()
    
    media, faltas = float(m), int(f)
    risco, diag = 0, ""
    
    if ML_ATIVO and modelo_inoai:
        risco = round(max(0, min(100, modelo_inoai.predict([[media, faltas]])[0])), 1)
        diag = "Crítico 🚨" if risco > 70 else "Atenção ⚠️" if risco > 30 else "Seguro ✅"
    else:
        risco = 80 if media < 6 else 10
        diag = "Manual"
        
    return jsonify({"media": round(media, 2), "faltas": faltas, "nivel": f"{risco}% ({diag})"})

@app.route('/ia/assistente/aluno/<int:aid>')
def ia_assistente(aid):
    # Cronograma Inteligente
    cronograma = [
        {"dia": "Segunda", "materia": "Python", "tag_class": "tag-python", "foco": "Lógica", "tarefas": ["Revisar Laços", "Exercícios 1-5"], "tempo": "45 min"},
        {"dia": "Terça", "materia": "Redes", "tag_class": "tag-redes", "foco": "Protocolos", "tarefas": ["Ler Cap. 4", "Resumo DNS"], "tempo": "60 min"},
        {"dia": "Quarta", "materia": "Ética", "tag_class": "tag-etica", "foco": "LGPD", "tarefas": ["Vídeo Aula", "Fórum"], "tempo": "30 min"},
        {"dia": "Quinta", "materia": "Python", "tag_class": "tag-python", "foco": "Estruturas", "tarefas": ["Listas", "Projeto Prático"], "tempo": "50 min"},
        {"dia": "Sexta", "materia": "Revisão", "tag_class": "", "foco": "PIM IV", "tarefas": ["Reunião Grupo", "Relatório"], "tempo": "1h 30min"}
    ]
    return jsonify({
        "resumo": "Perfil acadêmico analisado. Foco total em Redes esta semana.",
        "mensagem": "Mantenha a constância! 🚀 Sua chance de aprovação é alta.",
        "recomendacoes": ["Usar Pomodoro", "Não acumular aulas", "Tirar dúvidas com a InoAI"],
        "cronograma": cronograma
    })

@app.route('/ia/relatorio/professor')
def ia_rel_prof():
    return jsonify({"media": 7.5, "risco": 10, "nivel": "Turma estável (Análise InoAI)."})

# ============================================
# CHATBOT INOAI (LÓGICA UNIFICADA)
# ============================================
@app.route('/api/chat', methods=['POST'])
def chat_bot():
    data = request.json
    raw_msg = (data.get('message') or '').lower()
    aluno_id = data.get('aluno_id')

    # 1. Normaliza Gírias
    girias = {'vc':'voce', 'tbm':'tambem', 'pq':'porque', 'hj':'hoje', 'q':'que', 'pfv':'por favor', 'td':'tudo', 'ajduar':'ajudar'}
    msg_tratada = " ".join([girias.get(p, p) for p in raw_msg.split()])

    # 2. Análise de Sentimento
    prefixo_emocao = analisar_sentimento(msg_tratada)
    resposta = None

    # --- PRIORIDADE 1: COMANDOS DE DADOS (SQL) ---
    if aluno_id:
        if any(w in msg_tratada for w in ['minha nota', 'minhas notas', 'media', 'boletim']):
            conn = get_conn(row_factory=True)
            m = conn.execute("SELECT AVG(nota) as m FROM notas WHERE aluno_id=?", (aluno_id,)).fetchone()['m'] or 0
            conn.close()
            resposta = f"Sua média atual é **{round(m, 1)}**. " + ("Parabéns! 🌟" if m >= 7 else "Atenção! ⚠️")
            prefixo_emocao = "" 
        
        elif any(w in msg_tratada for w in ['risco', 'reprovar', 'analise']):
            resposta = "Acesse a aba 'Central IA' para ver o cálculo exato do seu risco com Machine Learning."
            prefixo_emocao = ""

    # --- PRIORIDADE 2: INSTRUÇÕES (O Instrutor) ---
    if not resposta:
        if any(w in msg_tratada for w in ['lancar nota', 'lançar nota', 'dar nota']):
            resposta = "👨‍🏫 Professor, para lançar notas: Menu 'Lançar Notas' > Selecione Aluno > Digite Nota > Salvar."
        elif any(w in msg_tratada for w in ['enviar atividade', 'entregar', 'upload']):
            resposta = "👨‍🎓 Aluno, para entregar: Menu 'Minhas Atividades' > Ícone Clipe (📎) > Selecionar Arquivo."

    # --- PRIORIDADE 3: CÉREBRO GIGANTE (Cerebro_IA.py) ---
    # Aqui ele busca na lista gigante que criamos (Social, TI, Infra, etc)
    if not resposta:
        resposta_base = buscar_resposta_avancada(msg_tratada)
        if resposta_base:
            resposta = resposta_base

    # --- PRIORIDADE 4: FALLBACK (Não entendeu nada) ---
    if not resposta:
        resposta = "Desculpe, não entendi. 🧠 Tente perguntar sobre: notas, faltas, 'o que é python' ou secretaria."
        prefixo_emocao = "" 

    return jsonify({"reply": prefixo_emocao + resposta})

# =====================
# EXECUÇÃO
# =====================
if __name__ == '__main__':
    init_db()
    treinar_inteligencia() # Treina Risco e Emoção
    print("\n--- InovaTech v35.0 (InoAI Centralizada) Rodando ---")
    app.run(debug=True, host='0.0.0.0', port=5000)