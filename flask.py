from flask import Flask, request, make_response, jsonify
import sqlite3
import json

app = Flask(__name__)
app.config['APP_NAME'] = "Biblioteca API" 

def cria_tabela():
    conn = sqlite3.connect('livros.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER NOT NULL,
            genero TEXT NOT NULL,
            paginas INTEGER DEFAULT 0  -- Define o padrão para 0 páginas
        );
    """)
    conn.commit()
    conn.close()

def novo_livro(titulo, autor, ano, genero, paginas=0):
    conn = sqlite3.connect('livros.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano, genero, paginas)
        VALUES (?, ?, ?, ?, ?);
    """, (titulo, autor, ano, genero, paginas))
    conn.commit()
    conn.close()

def listar_livros():
    conn = sqlite3.connect('livros.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def detalha_livro(id):
    conn = sqlite3.connect('livros.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros WHERE id=?", (id,))
    item = cursor.fetchone()
    conn.close()
    return item

@app.route('/livros', methods=['GET'])
def get_livros():
    livros = listar_livros()
    livros_lista = [
        {
            'id': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano': livro[3],
            'genero': livro[4],
            'paginas': livro[5]
        } for livro in livros
    ]
    return jsonify(livros_lista), 200 

@app.route('/livro', methods=['POST'])
def add_livro():
    data = request.get_json()
    if not data or 'titulo' not in data or 'autor' not in data or 'ano' not in data or 'genero' not in data:
        return jsonify({'message': 'Dados incompletos!'}), 400

    novo_livro(data['titulo'], data['autor'], int(data['ano']), data['genero'], int(data.get('paginas', 0)))
    return jsonify({'message': 'Livro adicionado com sucesso!'}), 201

@app.route('/livro/<int:id>', methods=['GET'])
def get_livro(id):
    livro = detalha_livro(id)
    if livro:
        livro_dict = {
            'id': livro[0],
            'titulo': livro[1],
            'autor': livro[2],
            'ano': livro[3],
            'genero': livro[4],
            'paginas': livro[5]
        }
        return jsonify(livro_dict), 200
    return jsonify({'message': 'Livro não encontrado!'}), 404

if __name__ == '__main__':
    cria_tabela()
    app.run(debug=True, use_reloader=False)
