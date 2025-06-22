import sqlite3

def conectar():
    return sqlite3.connect("booknook.db")

def criar_tabelas():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS autores (
        id_autor INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS livros (
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        ano TEXT NOT NULL,
        id_autor INTEGER NOT NULL,
        FOREIGN KEY(id_autor) REFERENCES autores(id_autor)
    )
    """)

    con.commit()
    con.close()