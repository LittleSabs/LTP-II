import tkinter as tk
from tkinter import ttk, messagebox
import db

db.criar_tabelas()

janela = tk.Tk()
janela.title("📘 BookNook - Sua Biblioteca Aconchegante")
janela.geometry("840x650")
janela.configure(bg="#fff0f5")  

estilo_fonte = ("Comic Sans MS", 11)
cor_fundo = "#fff0f5"
cor_destaque = "#ffe4e1"
cor_botao = "#d8bfd8"
cor_excluir = "#f08080"

style = ttk.Style()
style.configure("Treeview", font=estilo_fonte, rowheight=25, background=cor_fundo)
style.configure("Treeview.Heading", font=("Comic Sans MS", 12, "bold"))

def inserir_autor():
    nome = entry_nome_autor.get()
    if nome.strip() == "":
        messagebox.showwarning("Oops!", "O nome do autor não pode ficar vazio 🥺")
        return
    try:
        con = db.conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO autores (nome) VALUES (?)", (nome,))
        con.commit()
        con.close()
        entry_nome_autor.delete(0, tk.END)
        listar_autores()
        atualizar_combobox_autores()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_autores():
    for item in tree_autores.get_children():
        tree_autores.delete(item)
    con = db.conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM autores")
    for row in cur.fetchall():
        tree_autores.insert("", tk.END, values=row)
    con.close()

def deletar_autor():
    item = tree_autores.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um autor para remover 💔")
        return
    autor_id = tree_autores.item(item, "values")[0]
    try:
        con = db.conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM autores WHERE id_autor=?", (autor_id,))
        con.commit()
        con.close()
        listar_autores()
        atualizar_combobox_autores()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_combobox_autores():
    con = db.conectar()
    cur = con.cursor()
    cur.execute("SELECT id_autor, nome FROM autores")
    autores = cur.fetchall()
    con.close()
    combo_autores_livros['values'] = [f"{a[0]} - {a[1]}" for a in autores]

def inserir_livro():
    titulo = entry_titulo.get()
    ano = entry_ano.get()
    autor = combo_autores_livros.get()

    if not titulo or not ano or not autor:
        messagebox.showwarning("Oops!", "Preencha todos os campos para adicionar o livro ✨")
        return

    try:
        autor_id = int(autor.split(" - ")[0])
        con = db.conectar()
        cur = con.cursor()
        cur.execute("INSERT INTO livros (titulo, ano, id_autor) VALUES (?, ?, ?)",
                    (titulo, ano, autor_id))
        con.commit()
        con.close()
        entry_titulo.delete(0, tk.END)
        entry_ano.delete(0, tk.END)
        combo_autores_livros.set("")
        listar_livros()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_livros():
    for item in tree_livros.get_children():
        tree_livros.delete(item)
    con = db.conectar()
    cur = con.cursor()
    cur.execute('''SELECT livros.id_livro, livros.titulo, livros.ano, autores.nome
                   FROM livros JOIN autores ON livros.id_autor = autores.id_autor''')
    for row in cur.fetchall():
        tree_livros.insert("", tk.END, values=row)
    con.close()

def deletar_livro():
    item = tree_livros.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione um livro para excluir 🥹")
        return
    livro_id = tree_livros.item(item, "values")[0]
    try:
        con = db.conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM livros WHERE id_livro=?", (livro_id,))
        con.commit()
        con.close()
        listar_livros()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface
titulo = tk.Label(janela, text="📘 BookNook - Biblioteca Aconchegante", font=("Comic Sans MS", 20, "bold"), bg=cor_fundo, fg="#6a5acd")
titulo.pack(pady=10)

# Autores
frame_autores = tk.LabelFrame(janela, text="🌷 Autores", font=("Comic Sans MS", 13, "bold"), bg=cor_destaque, padx=10, pady=10)
frame_autores.pack(fill="x", padx=10, pady=8)

tk.Label(frame_autores, text="Nome:", font=estilo_fonte, bg=cor_destaque).grid(row=0, column=0, padx=5, pady=5)
entry_nome_autor = tk.Entry(frame_autores, font=estilo_fonte)
entry_nome_autor.grid(row=0, column=1, padx=5, pady=5)

tk.Button(frame_autores, text="🌟 Adicionar", bg=cor_botao, font=estilo_fonte, command=inserir_autor).grid(row=0, column=2, padx=5)
tk.Button(frame_autores, text="❌ Remover", bg=cor_excluir, font=estilo_fonte, command=deletar_autor).grid(row=0, column=3, padx=5)

tree_autores = ttk.Treeview(frame_autores, columns=("ID", "Nome"), show="headings")
tree_autores.heading("ID", text="ID")
tree_autores.heading("Nome", text="Nome")
tree_autores.grid(row=1, column=0, columnspan=4, pady=10, padx=5)

# Livros
frame_livros = tk.LabelFrame(janela, text="📖 Livros", font=("Comic Sans MS", 13, "bold"), bg=cor_destaque, padx=10, pady=10)
frame_livros.pack(fill="x", padx=10, pady=8)

tk.Label(frame_livros, text="Título:", font=estilo_fonte, bg=cor_destaque).grid(row=0, column=0, padx=5)
entry_titulo = tk.Entry(frame_livros, font=estilo_fonte)
entry_titulo.grid(row=0, column=1, padx=5)

tk.Label(frame_livros, text="Ano:", font=estilo_fonte, bg=cor_destaque).grid(row=0, column=2, padx=5)
entry_ano = tk.Entry(frame_livros, font=estilo_fonte)
entry_ano.grid(row=0, column=3, padx=5)

tk.Label(frame_livros, text="Autor:", font=estilo_fonte, bg=cor_destaque).grid(row=1, column=0, padx=5, pady=5)
combo_autores_livros = ttk.Combobox(frame_livros, state="readonly", font=estilo_fonte, width=30)
combo_autores_livros.grid(row=1, column=1, columnspan=2, padx=5)

tk.Button(frame_livros, text="📚 Adicionar Livro", bg=cor_botao, font=estilo_fonte, command=inserir_livro).grid(row=1, column=3, padx=5)
tk.Button(frame_livros, text="🗑️ Excluir Livro", bg=cor_excluir, font=estilo_fonte, command=deletar_livro).grid(row=1, column=4, padx=5)

tree_livros = ttk.Treeview(frame_livros, columns=("ID", "Título", "Ano", "Autor"), show="headings")
tree_livros.heading("ID", text="ID")
tree_livros.heading("Título", text="Título")
tree_livros.heading("Ano", text="Ano")
tree_livros.heading("Autor", text="Autor")
tree_livros.grid(row=2, column=0, columnspan=5, pady=10, padx=5)

# Inicialização
listar_autores()
listar_livros()
atualizar_combobox_autores()

janela.mainloop()