# 🔑 Locksmith CRM PY - Sistema Chaveiro (ou carinhosamente K-CRM)

> **Sistema de gestão financeira e estoque desenvolvido para pequenos empreendedores do setor de chaveiro**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📖 História do Projeto

Este projeto nasceu de uma necessidade real compartilhada por um chaveiro profissional no X (antigo Twitter):

> *"Eu sou chaveiro e gostaria de pagar R$20,00/mês num sistema que tenha: Entrada e saída, Estoque básico. Sim, literalmente só isso."*

A demanda evidenciou um problema comum entre microempreendedores: **sistemas complexos e caros para necessidades simples**. A maioria das soluções no mercado oferece dezenas de funcionalidades desnecessárias, cobram valores proibitivos e dependem de internet.

**A solução?** Um sistema desktop **simples, eficiente e acessível** que roda 100% offline no computador do cliente.

---

## ✨ Diferenciais

### 🎯 Focado no Essencial
- Sem firulas, sem complicação
- Interface intuitiva que qualquer pessoa usa
- Apenas as funcionalidades que realmente importam

### 💰 Economicamente Viável
- Sem mensalidades abusivas
- Roda localmente (sem custos de servidor)
- Código aberto e gratuito

### 🔒 Privacidade Total
- Dados ficam 100% no computador do usuário
- Sem cloud, sem terceiros
- Você é dono das suas informações

### 🚀 Performance
- Inicialização em segundos
- Interface responsiva
- Manutenção automática do banco de dados

---

## 🎨 Features

### 📊 Dashboard Inteligente
- **Visão geral financeira**: Saldo total, entradas e saídas do mês
- **Indicadores de estoque**: Total de produtos e alertas automáticos
- **Cards visuais**: Informações importantes de forma clara e objetiva

### 💰 Controle Financeiro
- ✅ Registro de **entradas** (vendas, recebimentos)
- ✅ Registro de **saídas** (compras, despesas, contas)
- ✅ Histórico completo com filtros
- ✅ Cálculo automático de saldo
- ✅ Relatório mensal consolidado

### 📦 Gestão de Estoque
- ✅ Cadastro de produtos com preços (custo/venda)
- ✅ Controle de entradas e saídas de estoque
- ✅ **Alertas automáticos** de estoque baixo (≤5 unidades)
- ✅ Histórico de movimentações
- ✅ Observações em cada movimentação

### 🛠️ Manutenção Inteligente
- ✅ **Otimização automática** do banco ao iniciar
- ✅ Script de manutenção manual com menu interativo
- ✅ **Backup automático** antes de operações críticas
- ✅ Limpeza de backups antigos
- ✅ Verificação de integridade (PRAGMA integrity_check)

---

## 🏗️ Arquitetura Técnica

### Stack Tecnológico

```
Backend
├── Python 3.8+
├── Flask 3.0.0 (API REST)
├── SQLite3 (Banco de dados)
└── Flask-CORS (Segurança)

Frontend
├── HTML5 + CSS3
├── JavaScript Vanilla (ES6+)
├── Design Responsivo
└── Animações CSS

Database
├── SQLite com VACUUM automático
├── Índices otimizados
└── Backup incremental
```

### Estrutura do Projeto

```
sistema-chaveiro/
│
├── app.py                 # Backend Flask + API REST
├── database.py            # Schema e inicialização do DB
├── manutencao.py          # Sistema de manutenção e backup
├── requirements.txt       # Dependências Python
├── README.md              # Este arquivo
│
├── static/
│   └── index.html         # Frontend Single Page Application
│
├── chaveiro.db            # Banco de dados SQLite (gerado automaticamente)
└── chaveiro_backup_*.db   # Backups automáticos
```

### Banco de Dados

```sql
-- Tabela de Produtos
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER DEFAULT 0,
    preco_custo REAL DEFAULT 0,
    preco_venda REAL DEFAULT 0,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Movimentações Financeiras
CREATE TABLE movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,              -- 'entrada' ou 'saida'
    descricao TEXT,
    valor REAL NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Movimentações de Estoque
CREATE TABLE movimentacoes_estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    tipo TEXT NOT NULL,              -- 'entrada' ou 'saida'
    quantidade INTEGER NOT NULL,
    observacao TEXT,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);
```

---

## 🚀 Instalação e Uso

### Pré-requisitos

- **Python 3.8+** instalado ([Download aqui](https://www.python.org/downloads/))
- **Navegador web moderno** (Chrome, Firefox, Edge)

### Passo a Passo

#### 1️⃣ Clone o repositório

```bash
git clone https://github.com/johnnyvernin/locksmith-crm-py.git
cd sistema-chaveiro
```

#### 2️⃣ Crie a estrutura de pastas

```bash
mkdir static
# Coloque os arquivos nas respectivas pastas conforme estrutura acima
```

#### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

#### 4️⃣ Inicialize o banco de dados

```bash
python database.py
```

#### 5️⃣ Inicie o sistema

```bash
python app.py
```

🎉 **Pronto!** O navegador abrirá automaticamente em `http://localhost:5000`

---

## 🛠️ Manutenção do Banco de Dados

### Manutenção Automática ✨

O sistema realiza otimização **automática** toda vez que inicia:
- Compactação (VACUUM)
- Atualização de estatísticas (ANALYZE)
- Verificação de integridade

### Manutenção Manual 🔧

Para manutenção completa com menu interativo:

```bash
python manutencao.py
```

**Menu de opções:**
1. 🔧 Executar manutenção completa (recomendado)
2. 📊 Verificar estado do banco
3. 💾 Criar backup manual
4. 🗑️ Limpar backups antigos

### Manutenção Silenciosa 🤖

Para agendar no sistema operacional:

```bash
python manutencao.py --auto
```

### Por que fazer manutenção?

O SQLite é um banco de dados excelente, mas pode sofrer **fragmentação** com o tempo:
- 📉 Arquivo ocupa mais espaço que necessário
- 🐌 Consultas ficam mais lentas
- 🔍 Índices desatualizados

**A manutenção resolve isso!**
- ✅ Reduz tamanho do arquivo em até 50%
- ✅ Melhora velocidade das consultas
- ✅ Previne corrupção de dados

---

## 📊 API REST Endpoints

### Produtos (Estoque)

```http
GET    /api/produtos           # Lista todos os produtos
POST   /api/produtos           # Cadastra novo produto
PUT    /api/produtos/:id       # Atualiza produto
DELETE /api/produtos/:id       # Remove produto
```

### Movimentações Financeiras

```http
GET    /api/movimentacoes      # Lista movimentações
POST   /api/movimentacoes      # Registra nova movimentação
DELETE /api/movimentacoes/:id  # Remove movimentação
```

### Movimentações de Estoque

```http
GET    /api/movimentacoes-estoque     # Lista movimentações de estoque
POST   /api/movimentacoes-estoque     # Registra movimentação
```

### Dashboard

```http
GET    /api/resumo             # Retorna dados do dashboard
```

**Exemplo de resposta:**

```json
{
  "saldo_total": 15420.50,
  "entradas_mes": 8300.00,
  "saidas_mes": 4120.30,
  "saldo_mes": 4179.70,
  "total_produtos": 42,
  "produtos_estoque_baixo": 3
}
```

---

## 💡 Casos de Uso

### Para Chaveiros
- Controle de vendas de cópias de chaves
- Estoque de virgens (chaves em branco)
- Registro de serviços prestados
- Controle de despesas

### Para Outros Negócios
- Pequenos comércios
- Prestadores de serviço
- Profissionais autônomos
- Microempreendedores individuais (MEI)

---

## 🎯 Roadmap

### ✅ Versão 1.0 (Atual)
- [x] Controle financeiro básico
- [x] Gestão de estoque
- [x] Dashboard com indicadores
- [x] Manutenção automática do banco
- [x] Interface responsiva

### 🚧 Versão 2.0 (Planejado)
- [ ] Relatórios em PDF
- [ ] Gráficos de desempenho (Chart.js)
- [ ] Sistema de categorias
- [ ] Múltiplos usuários com permissões
- [ ] Exportação para Excel
- [ ] Impressão de recibos

### 🔮 Versão 3.0 (Futuro)
- [ ] Aplicativo mobile (React Native)
- [ ] Sincronização em nuvem (opcional)
- [ ] Integração com WhatsApp
- [ ] Emissão de notas fiscais (NFe/NFCe)

---

## 🤝 Como Contribuir

Contribuições são **muito bem-vindas**! Este projeto foi feito para a comunidade.

### Passos para contribuir:

1. Faça um **Fork** do projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Faça **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Áreas que precisam de ajuda:
- 📱 Interface mobile
- 📊 Novos relatórios e gráficos
- 🌍 Tradução para outros idiomas
- 🐛 Correção de bugs
- 📖 Melhoria da documentação

---

## 🐛 Problemas Conhecidos

### Porta 5000 já em uso
**Erro:** `Address already in use`  
**Solução:** Mude a porta no `app.py` (linha final):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para 5001
```

### Navegador não abre automaticamente
**Solução:** Abra manualmente `http://localhost:5000` no navegador

### Erro ao executar manutenção
**Causa:** Sistema ainda está rodando  
**Solução:** Feche o `app.py` antes de executar `manutencao.py`

---

## 📝 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

Isso significa que você pode:
- ✅ Usar comercialmente
- ✅ Modificar o código
- ✅ Distribuir
- ✅ Usar privativamente

---

## 👨‍💻 Autor

Desenvolvido com ❤️ por **[Seu Nome]**

- 🐙 GitHub: [@seu-usuario](https://github.com/johnnyvernin)
- 💼 LinkedIn: [Seu Nome](https://linkedin.com/in/johnnyvernin)
- 🐦 Twitter/X: [@seu-usuario](https://x.com/johnnyvernin)

---

## 🙏 Agradecimentos

- Ao chaveiro que inspirou este projeto com sua demanda real e sincera
- À comunidade Python e Flask pela excelente documentação
- A todos os microempreendedores que lutam diariamente

---

## ⭐ Apoie o Projeto

Se este projeto te ajudou, considere:
- ⭐ Dar uma **estrela** no GitHub
- 🐛 Reportar **bugs** e sugerir melhorias
- 🤝 Contribuir com **código**
- 📢 Compartilhar com outros empreendedores

---

<div align="center">

**Feito com ❤️ para pequenos empreendedores que merecem ferramentas dignas**

[⬆ Voltar ao topo](#-sistema-chaveiro)

</div>
