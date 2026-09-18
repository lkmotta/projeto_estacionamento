import sqlite3
import json
import os
import re

DB_FILE = 'estacionamento_local.db'
SESSION_FILE = 'session.json'

def init_db():
    """Inicializa o banco de dados com suporte a vagas reservadas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vagas (
            id INTEGER PRIMARY KEY,
            estado TEXT NOT NULL,
            reservada INTEGER NOT NULL DEFAULT 0
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM vagas')
    if cursor.fetchone()[0] == 0:
        vagas_iniciais = []
        for i in range(1, 11):
            # As últimas 3 vagas (8, 9, 10) são reservadas para servidores
            reservada = 1 if i >= 8 else 0
            vagas_iniciais.append((i, 'livre', reservada))
        cursor.executemany('INSERT INTO vagas (id, estado, reservada) VALUES (?, ?, ?)', vagas_iniciais)
        conn.commit()
    conn.close()

def get_vagas():
    """Retorna todas as vagas com id, estado e indicativo de reservada."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, estado, reservada FROM vagas')
    vagas = cursor.fetchall()
    conn.close()
    return vagas

def validar_credencial(login_input):
    """
    Valida o tipo de login:
    - Aluno: RA numérico com exatamente 7 dígitos.
    - Servidor: Email estritamente @utfpr.edu.br ou @professores.utfpr.edu.br.
    """
    login_input = login_input.strip()
    if re.match(r'^\d{7}$', login_input):
        return True, 'aluno'
    
    if login_input.endswith('@utfpr.edu.br') or login_input.endswith('@professores.utfpr.edu.br'):
        return True, 'servidor'
        
    return False, None

def atualizar_vaga(id_vaga, novo_estado, user_type):
    """Atualiza a vaga aplicando regras de reserva para servidores."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT estado, reservada FROM vagas WHERE id = ?', (id_vaga,))
    vaga = cursor.fetchone()
    
    if not vaga:
        conn.close()
        return False, "Vaga não encontrada."
        
    _, reservada = vaga
    
    # Validação do Requisito 3: Proteção de vagas de servidores
    if novo_estado == 'ocupada' and reservada == 1 and user_type != 'servidor':
        conn.close()
        return False, "Acesso negado: As vagas 8, 9 e 10 são reservadas exclusivamente para servidores."
        
    cursor.execute('UPDATE vagas SET estado = ? WHERE id = ?', (novo_estado, id_vaga))
    conn.commit()
    conn.close()
    return True, f"Vaga {id_vaga} alterada para {novo_estado.upper()} com sucesso!"

# Gerenciamento de Sessão 

def check_login():
    """Verifica se há sessão ativa e retorna (is_logged, username, user_type)."""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            data = json.load(f)
            return data.get('logged_in', False), data.get('username', ''), data.get('user_type', 'aluno')
    return False, "", ""

def do_login(username, user_type):
    """Grava a sessão do usuário com seu tipo."""
    with open(SESSION_FILE, 'w') as f:
        json.dump({'logged_in': True, 'username': username, 'user_type': user_type}, f)

def do_logout():
    """Remove o arquivo de sessão local."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
