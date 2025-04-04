import sqlite3

def criar_tabela():
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE NOT NULL,
                        quantidade INTEGER NOT NULL,
                        preco REAL NOT NULL)''')
    conexao.commit()
    conexao.close()

def inserir_produto(nome, quantidade, preco):
    try:
        conexao = sqlite3.connect("estoque.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        conexao.commit()
        print("Produto inserido com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: Já existe um produto com esse nome.")
    finally:
        conexao.close()

def listar_produtos():
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    print("Lista de produtos:")
    for produto in produtos:
        print(produto)

def atualizar_produto(id, quantidade, preco):
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE produtos SET quantidade = ?, preco = ? WHERE id = ?", (quantidade, preco, id))
    if cursor.rowcount == 0:
        print("Erro: Produto não encontrado.")
    else:
        conexao.commit()
        print("Produto atualizado com sucesso!")
    conexao.close()

def deletar_produto(id):
    conexao = sqlite3.connect("estoque.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        print("Erro: Produto não encontrado.")
    else:
        conexao.commit()
        print("Produto deletado com sucesso!")
    conexao.close()

def menu():
    criar_tabela()
    while True:
        print("\nMENU:\n1 - Inserir produto\n2 - Listar produtos\n3 - Atualizar produto\n4 - Deletar produto\n5 - Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome = input("Nome do produto: ")
            quantidade = int(input("Quantidade: "))
            preco = float(input("Preço: "))
            inserir_produto(nome, quantidade, preco)
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            id = int(input("ID do produto a atualizar: "))
            quantidade = int(input("Nova quantidade: "))
            preco = float(input("Novo preço: "))
            atualizar_produto(id, quantidade, preco)
        elif opcao == "4":
            id = int(input("ID do produto a deletar: "))
            deletar_produto(id)
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()