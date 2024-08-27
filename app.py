from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar as tabelas no banco de dados
def cria_tabelas():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            genero TEXT NOT NULL,
            paginas INTEGER DEFAULT 0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT,
            FOREIGN KEY (livro_id) REFERENCES livros(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()

# Página inicial - Menu
@app.route('/')
def index():
    return render_template('menu.html')

# Rotas para gerenciar livros
@app.route('/livros')
def livros():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return render_template('livros.html', livros=livros)

@app.route('/add_livro', methods=['GET', 'POST'])
def add_livro():
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano']
        genero = request.form['genero']
        paginas = request.form['paginas']
        novo_livro(titulo, autor, ano, genero, paginas)
        return redirect(url_for('livros'))
    return render_template('add_livro.html')

def novo_livro(titulo, autor, ano, genero, paginas=0):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano, genero, paginas)
        VALUES (?, ?, ?, ?, ?);
    """, (titulo, autor, ano, genero, paginas))
    conn.commit()
    conn.close()

# Rotas para gerenciar usuários
@app.route('/usuarios')
def usuarios():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/add_usuario', methods=['GET', 'POST'])
def add_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        novo_usuario(nome, email, telefone)
        return redirect(url_for('usuarios'))
    return render_template('add_usuario.html')

def novo_usuario(nome, email, telefone):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nome, email, telefone)
        VALUES (?, ?, ?);
    """, (nome, email, telefone))
    conn.commit()
    conn.close()

# Rotas para gerenciar empréstimos
@app.route('/emprestimos')
def emprestimos():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emprestimos")
    emprestimos = cursor.fetchall()
    conn.close()
    return render_template('emprestimos.html', emprestimos=emprestimos)

@app.route('/add_emprestimo', methods=['GET', 'POST'])
def add_emprestimo():
    if request.method == 'POST':
        livro_id = request.form['livro_id']
        usuario_id = request.form['usuario_id']
        data_emprestimo = request.form['data_emprestimo']
        data_devolucao = request.form.get('data_devolucao')
        novo_emprestimo(livro_id, usuario_id, data_emprestimo, data_devolucao)
        return redirect(url_for('emprestimos'))
    return render_template('add_emprestimo.html')

def novo_emprestimo(livro_id, usuario_id, data_emprestimo, data_devolucao=None):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, data_devolucao)
        VALUES (?, ?, ?, ?);
    """, (livro_id, usuario_id, data_emprestimo, data_devolucao))
    conn.commit()
    conn.close()

# Rotas para gerenciar categorias
@app.route('/categorias')
def categorias():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/add_categoria', methods=['GET', 'POST'])
def add_categoria():
    if request.method == 'POST':
        nome = request.form['nome']
        nova_categoria(nome)
        return redirect(url_for('categorias'))
    return render_template('add_categoria.html')

def nova_categoria(nome):
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO categorias (nome)
        VALUES (?);
    """, (nome,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    cria_tabelas()
    app.run(debug=True, use_reloader=False)
