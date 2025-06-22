from flask import Flask, jsonify, request
import db

app = Flask(__name__)
db.criar_tabelas()

# --- AUTORES ---

@app.route("/autores", methods=["GET"])
def get_autores():
    con = db.conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM autores")
    autores = [{"id_autor": row[0], "nome": row[1]} for row in cur.fetchall()]
    con.close()
    return jsonify(autores)

@app.route("/autores", methods=["POST"])
def add_autor():
    data = request.json
    nome = data.get("nome")
    if not nome:
        return jsonify({"erro": "Nome é obrigatório"}), 400
    con = db.conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Autor adicionado com sucesso!"}), 201

@app.route("/autores/<int:autor_id>", methods=["DELETE"])
def delete_autor(autor_id):
    con = db.conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM autores WHERE id_autor = ?", (autor_id,))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Autor removido com sucesso!"})

# --- LIVROS ---

@app.route("/livros", methods=["GET"])
def get_livros():
    con = db.conectar()
    cur = con.cursor()
    cur.execute('''
        SELECT livros.id_livro, livros.titulo, livros.ano, autores.nome
        FROM livros JOIN autores ON livros.id_autor = autores.id_autor
    ''')
    livros = [
        {
            "id_livro": row[0],
            "titulo": row[1],
            "ano": row[2],
            "autor": row[3]
        }
        for row in cur.fetchall()
    ]
    con.close()
    return jsonify(livros)

@app.route("/livros", methods=["POST"])
def add_livro():
    data = request.json
    titulo = data.get("titulo")
    ano = data.get("ano")
    id_autor = data.get("id_autor")

    if not titulo or not ano or not id_autor:
        return jsonify({"erro": "Título, ano e id_autor são obrigatórios"}), 400

    con = db.conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO livros (titulo, ano, id_autor) VALUES (?, ?, ?)",
                (titulo, ano, id_autor))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Livro adicionado com sucesso!"}), 201

@app.route("/livros/<int:livro_id>", methods=["DELETE"])
def delete_livro(livro_id):
    con = db.conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM livros WHERE id_livro = ?", (livro_id,))
    con.commit()
    con.close()
    return jsonify({"mensagem": "Livro removido com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)
