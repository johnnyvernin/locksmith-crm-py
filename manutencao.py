import sqlite3
import os
from datetime import datetime

def verificar_tamanho_banco():
    """Mostra o tamanho atual do banco"""
    if os.path.exists('chaveiro.db'):
        tamanho = os.path.getsize('chaveiro.db')
        tamanho_mb = tamanho / (1024 * 1024)
        print(f"📊 Tamanho do banco: {tamanho_mb:.2f} MB ({tamanho:,} bytes)")
        return tamanho
    return 0

def contar_registros():
    """Mostra quantos registros existem"""
    conn = sqlite3.connect('chaveiro.db')
    c = conn.cursor()
    
    produtos = c.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]
    movs = c.execute('SELECT COUNT(*) FROM movimentacoes').fetchone()[0]
    movs_estoque = c.execute('SELECT COUNT(*) FROM movimentacoes_estoque').fetchone()[0]
    
    print(f"📦 Produtos cadastrados: {produtos}")
    print(f"💰 Movimentações financeiras: {movs}")
    print(f"📋 Movimentações de estoque: {movs_estoque}")
    
    conn.close()

def fazer_backup():
    """Cria um backup do banco antes da manutenção"""
    if os.path.exists('chaveiro.db'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'chaveiro_backup_{timestamp}.db'
        
        # Copia o banco
        import shutil
        shutil.copy2('chaveiro.db', backup_name)
        print(f"💾 Backup criado: {backup_name}")
        return backup_name
    return None

def limpar_backups_antigos(manter=5):
    """Remove backups antigos, mantendo apenas os X mais recentes"""
    backups = [f for f in os.listdir('.') if f.startswith('chaveiro_backup_') and f.endswith('.db')]
    backups.sort(reverse=True)
    
    if len(backups) > manter:
        for backup in backups[manter:]:
            os.remove(backup)
            print(f"🗑️  Backup antigo removido: {backup}")

def otimizar_banco():
    """Realiza otimização completa do banco"""
    print("\n" + "=" * 60)
    print("🔧 INICIANDO MANUTENÇÃO DO BANCO DE DADOS")
    print("=" * 60 + "\n")
    
    # 1. Informações iniciais
    print("📊 Estado atual:")
    tamanho_inicial = verificar_tamanho_banco()
    contar_registros()
    print()
    
    # 2. Backup
    print("💾 Criando backup de segurança...")
    fazer_backup()
    print()
    
    # 3. Otimização
    try:
        conn = sqlite3.connect('chaveiro.db')
        c = conn.cursor()
        
        print("🔧 Executando operações de manutenção...")
        
        # Reindex - Reconstrói todos os índices
        print("  → Reconstruindo índices...")
        c.execute('REINDEX')
        
        # Analyze - Atualiza estatísticas
        print("  → Atualizando estatísticas...")
        c.execute('ANALYZE')
        
        # Vacuum - Compacta o banco
        print("  → Compactando banco de dados...")
        c.execute('VACUUM')
        
        # Verifica integridade
        print("  → Verificando integridade...")
        result = c.execute('PRAGMA integrity_check').fetchone()
        
        conn.commit()
        conn.close()
        
        if result[0] == 'ok':
            print("✅ Integridade verificada: OK")
        else:
            print(f"⚠️  ATENÇÃO: {result[0]}")
        
        print()
        
        # 4. Resultado final
        print("📊 Estado após manutenção:")
        tamanho_final = verificar_tamanho_banco()
        
        if tamanho_inicial > tamanho_final:
            economia = tamanho_inicial - tamanho_final
            economia_mb = economia / (1024 * 1024)
            percentual = (economia / tamanho_inicial) * 100
            print(f"💾 Espaço recuperado: {economia_mb:.2f} MB ({percentual:.1f}%)")
        
        print()
        
        # 5. Limpar backups antigos
        print("🗑️  Limpando backups antigos (mantendo os 5 mais recentes)...")
        limpar_backups_antigos(5)
        
        print("\n" + "=" * 60)
        print("✅ MANUTENÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO durante a manutenção: {e}")
        print("💡 Dica: Feche o sistema antes de executar a manutenção")
        return False
    
    return True

def menu_interativo():
    """Menu interativo para o usuário"""
    print("\n" + "=" * 60)
    print("🔧 SISTEMA DE MANUTENÇÃO - CHAVEIRO DB")
    print("=" * 60)
    print("\n1 - Executar manutenção completa (recomendado)")
    print("2 - Apenas verificar estado do banco")
    print("3 - Criar backup manual")
    print("4 - Limpar backups antigos")
    print("0 - Sair")
    print()
    
    opcao = input("Escolha uma opção: ").strip()
    
    if opcao == '1':
        otimizar_banco()
    elif opcao == '2':
        print("\n📊 Informações do banco:")
        verificar_tamanho_banco()
        contar_registros()
    elif opcao == '3':
        fazer_backup()
        print("✅ Backup criado com sucesso!")
    elif opcao == '4':
        limpar_backups_antigos(5)
        print("✅ Limpeza concluída!")
    elif opcao == '0':
        print("👋 Até logo!")
        return False
    else:
        print("❌ Opção inválida!")
    
    return True

if __name__ == '__main__':
    import sys
    
    # Se passar --auto como parâmetro, executa direto
    if '--auto' in sys.argv:
        otimizar_banco()
    else:
        # Senão, mostra menu interativo
        continuar = True
        while continuar:
            continuar = menu_interativo()
            if continuar:
                input("\nPressione ENTER para continuar...")