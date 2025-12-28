from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os
import webbrowser
from threading import Timer

app = Flask(__name__, static_folder='static')
CORS(app)

def get_db():
    conn = sqlite3.connect('chaveiro.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal - serve o HTML
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# === PRODUTOS (ESTOQUE) ===
@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    conn = get_db()
    produtos = conn.execute('SELECT * FROM produtos ORDER BY nome').fetchall()
    conn.close()
    return jsonify([dict(p) for p in produtos])

@app.route('/api/produtos', methods=['POST'])
def add_produto():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO produtos (nome, quantidade, preco_custo, preco_venda)
        VALUES (?, ?, ?, ?)
    ''', (data['nome'], data.get('quantidade', 0), 
          data.get('preco_custo', 0), data.get('preco_venda', 0)))
    conn.commit()
    produto_id = c.lastrowid
    conn.close()
    return jsonify({'id': produto_id, 'message': 'Produto adicionado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    data = request.json
    conn = get_db()
    conn.execute('''
        UPDATE produtos 
        SET nome=?, quantidade=?, preco_custo=?, preco_venda=?
        WHERE id=?
    ''', (data['nome'], data['quantidade'], 
          data['preco_custo'], data['preco_venda'], id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Produto atualizado com sucesso!'})

@app.route('/api/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    conn = get_db()
    conn.execute('DELETE FROM produtos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Produto excluído com sucesso!'})

# === MOVIMENTAÇÕES DE ESTOQUE ===
@app.route('/api/movimentacoes-estoque', methods=['POST'])
def add_movimentacao_estoque():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    
    # Registra a movimentação
    c.execute('''
        INSERT INTO movimentacoes_estoque (produto_id, tipo, quantidade, observacao)
        VALUES (?, ?, ?, ?)
    ''', (data['produto_id'], data['tipo'], data['quantidade'], data.get('observacao', '')))
    
    # Atualiza o estoque do produto
    if data['tipo'] == 'entrada':
        c.execute('UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?', 
                  (data['quantidade'], data['produto_id']))
    else:  # saída
        c.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?', 
                  (data['quantidade'], data['produto_id']))
    
    conn.commit()
    conn.close()
    return jsonify({'message': 'Movimentação registrada com sucesso!'})

@app.route('/api/movimentacoes-estoque', methods=['GET'])
def get_movimentacoes_estoque():
    conn = get_db()
    movs = conn.execute('''
        SELECT me.*, p.nome as produto_nome
        FROM movimentacoes_estoque me
        JOIN produtos p ON me.produto_id = p.id
        ORDER BY me.data DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    return jsonify([dict(m) for m in movs])

# === MOVIMENTAÇÕES FINANCEIRAS ===
@app.route('/api/movimentacoes', methods=['GET'])
def get_movimentacoes():
    conn = get_db()
    movs = conn.execute('SELECT * FROM movimentacoes ORDER BY data DESC LIMIT 100').fetchall()
    conn.close()
    return jsonify([dict(m) for m in movs])

@app.route('/api/movimentacoes', methods=['POST'])
def add_movimentacao():
    data = request.json
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO movimentacoes (tipo, descricao, valor)
        VALUES (?, ?, ?)
    ''', (data['tipo'], data['descricao'], data['valor']))
    conn.commit()
    mov_id = c.lastrowid
    conn.close()
    return jsonify({'id': mov_id, 'message': 'Movimentação registrada com sucesso!'})

@app.route('/api/movimentacoes/<int:id>', methods=['DELETE'])
def delete_movimentacao(id):
    conn = get_db()
    conn.execute('DELETE FROM movimentacoes WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Movimentação excluída com sucesso!'})

# === DASHBOARD (RESUMO) ===
@app.route('/api/resumo', methods=['GET'])
def get_resumo():
    conn = get_db()
    
    # Saldo total
    entradas = conn.execute("SELECT COALESCE(SUM(valor), 0) FROM movimentacoes WHERE tipo='entrada'").fetchone()[0]
    saidas = conn.execute("SELECT COALESCE(SUM(valor), 0) FROM movimentacoes WHERE tipo='saida'").fetchone()[0]
    saldo = entradas - saidas
    
    # Movimentações do mês
    hoje = datetime.now()
    inicio_mes = hoje.replace(day=1).strftime('%Y-%m-%d')
    entradas_mes = conn.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM movimentacoes WHERE tipo='entrada' AND date(data) >= ?",
        (inicio_mes,)
    ).fetchone()[0]
    saidas_mes = conn.execute(
        "SELECT COALESCE(SUM(valor), 0) FROM movimentacoes WHERE tipo='saida' AND date(data) >= ?",
        (inicio_mes,)
    ).fetchone()[0]
    
    # Total de produtos
    total_produtos = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    
    # Produtos com estoque baixo
    produtos_baixo = conn.execute("SELECT COUNT(*) FROM produtos WHERE quantidade <= 5").fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'saldo_total': saldo,
        'entradas_mes': entradas_mes,
        'saidas_mes': saidas_mes,
        'saldo_mes': entradas_mes - saidas_mes,
        'total_produtos': total_produtos,
        'produtos_estoque_baixo': produtos_baixo
    })

def manutenção_db():
    """Realiza manutenção preventiva no banco de dados"""
    try:
        conn = sqlite3.connect('chaveiro.db')
        c = conn.cursor()
        
        # VACUUM - Compacta e otimiza o banco
        print("🔧 Otimizando banco de dados...")
        c.execute('VACUUM')
        
        # ANALYZE - Atualiza estatísticas para melhor performance
        c.execute('ANALYZE')
        
        # Verifica integridade
        result = c.execute('PRAGMA integrity_check').fetchone()
        if result[0] == 'ok':
            print("✅ Banco de dados íntegro e otimizado!")
        else:
            print("⚠️ Problemas detectados no banco:", result[0])
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Erro na manutenção do banco: {e}")

def abrir_navegador():
    """Abre o navegador automaticamente após 1.5 segundos"""
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Inicializa o banco se não existir
    if not os.path.exists('chaveiro.db'):
        from database import init_db
        init_db()
    
    # Manutenção do banco
    manutenção_db()
    
    print("=" * 50)
    print("🔑 Sistema de Chaveiro iniciado!")
    print("📱 Acesse: http://localhost:5000")
    print("🌐 Abrindo navegador automaticamente...")
    print("=" * 50)
    
    # Abre o navegador após 1.5 segundos (tempo para o servidor iniciar)
    Timer(1.5, abrir_navegador).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)