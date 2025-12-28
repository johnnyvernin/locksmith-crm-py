import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('chaveiro.db')
    c = conn.cursor()
    
    # Tabela de produtos (estoque)
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER DEFAULT 0,
            preco_custo REAL DEFAULT 0,
            preco_venda REAL DEFAULT 0,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de movimentações (entradas e saídas)
    c.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            descricao TEXT,
            valor REAL NOT NULL,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de movimentações de estoque
    c.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            observacao TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado com sucesso!")