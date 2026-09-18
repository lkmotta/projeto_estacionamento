import sqlite3
import json
import os

DB_FILE = 'estacionamento_local.db'
SESSION_FILE = 'session.json'

def init_db():
    """Inicializa o banco de dados com algumas vagas padrão se não existirem."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY,
            estado TEXT NOT NULL
        )
    ''')
    
    # Popula o banco na primeira execução
    cursor.execute('SELECT COUNT(*) FROM vagas')
    if cursor.fetchone()[0] == 0:
        vagas_iniciais = [(i, 'livre') for i in range(1, 11)] # 10 vagas
        cursor.executemany('INSERT INTO vagas (id, estado) VALUES (?, ?)', vagas_iniciais)
        conn.commit()
    conn.close()

def get_vagas():
    """Retorna todas as vagas e seus estados."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, estado FROM vagas')
    vagas = cursor.fetchall()
    conn.close()
    return vagas

def atualizar_vaga(id_vaga, novo_estado):
    """Atualiza o estado de uma vaga (livre/ocupada)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE vagas SET estado = ? WHERE id = ?', (novo_estado, id_vaga))
    sucesso = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return sucesso

# Gerenciamento de Sessão (Login Único)

def check_login():
    """Verifica se há uma sessão salva ativa."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get('logged_in', False), data.get('username', '')
    return False, ""

def do_login(username):
    """Cria o arquivo de sessão local."""
    with open(SESSION_FILE, 'w') as f:
        json.dump({'logged_in': True, 'username': username}, f)

def do_logout():
    """Remove a sessão local."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)