import sqlite3
import re
import os


def Limpar_Tela():
    os.system("cls" if os.name == "nt" else "clear")


def Pausar():
    input("Pressione Enter para voltar ao menu.")


def Validar_Telefone(telefone):
    return re.match(r"^\d{10,11}$", telefone)


def Confirmar_Acao(mensagem):
    while True:
        confirmacao = input(f"{mensagem} (S/N): ").strip().lower()
        if confirmacao in ["s", "n"]:
            return confirmacao == "s"
        print("Resposta inválida. Por favor, digite 'S' para Sim ou 'N' para Não.")


def Conectar_Banco():
    try:
        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        return conexao, cursor
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        exit()


conexao, cursor = Conectar_Banco()


def Menu():
    Limpar_Tela()
    print("1 - Cadastrar Contato")
    print("2 - Listar Contatos")
    print("3 - Buscar Contato")
    print("4 - Apagar Contato")
    print("5 - Editar Contato")
    print("6 - Sair")
    Escolha_Opcao()


def Escolha_Opcao():
    try:
        opcao = int(input("Escolha uma opção:\n "))
        if opcao == 1:
            Cadastrar_Contato()
        elif opcao == 2:
            Listar_Contatos()
        elif opcao == 3:
            Buscar_Contato()
        elif opcao == 4:
            Apagar_Contato()
        elif opcao == 5:
            Editar_Contato()
        elif opcao == 6:
            print("Saindo...")
            conexao.close()
            Pausar()
            Limpar_Tela()
        else:
            print("Opção Inválida. Por favor, escolha uma opção válida.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")


def Cadastrar_Contato():
    Limpar_Tela()
    nome = input("Qual o nome do contato: \n").strip()

    while True:
        numero = input("Qual o telefone do contato (apenas dígitos): \n").strip()
        if Validar_Telefone(numero):
            break
        print("Telefone inválido. Deve conter 10 ou 11 dígitos.")

    while True:
        email = input("Qual o email do contato: \n").strip()
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            break
        print("Email inválido. Tente novamente.")

    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,))
    if cursor.fetchone():
        print("Já existe um contato com esse nome.")
        Pausar()
        return Cadastrar_Contato()

    cursor.execute(
        "INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)",
        (nome, numero, email),
    )
    conexao.commit()
    print(f"Contato salvo: {nome} - {numero}, {email}")

    if Confirmar_Acao("Deseja cadastrar um novo contato?"):
        Cadastrar_Contato()
    else:
        Menu()


def Listar_Contatos():
    Limpar_Tela()
    cursor.execute("SELECT * FROM contatos")
    contatos = cursor.fetchall()

    if contatos:
        print("\nLista de Contatos:")
        for contato in contatos:
            print(
                f"ID: {contato[0]} - Nome: {contato[1]} - Telefone: {contato[2]} - Email: {contato[3]}"
            )
    else:
        print("Nenhum contato cadastrado.")

    Pausar()
    Menu()


def Buscar_Contato():
    Limpar_Tela()
    nome = input("Digite o nome do contato que deseja buscar: \n").strip()
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,))
    contato = cursor.fetchone()

    if contato:
        print(
            f"ID: {contato[0]} - Nome: {contato[1]} - Telefone: {contato[2]} - Email: {contato[3]}"
        )
    else:
        print("Contato não encontrado.")

    Pausar()
    Menu()


def Apagar_Contato():
    Limpar_Tela()
    nome = input("Digite o nome do contato que deseja apagar: \n").strip()
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,))
    contato = cursor.fetchone()

    if contato:
        print(
            f"ID: {contato[0]} - Nome: {contato[1]} - Telefone: {contato[2]} - Email: {contato[3]}"
        )
        if Confirmar_Acao(f"Tem certeza que deseja apagar o contato {nome}?"):
            cursor.execute("DELETE FROM contatos WHERE nome = ?", (nome,))
            conexao.commit()
            Limpar_Tela()
            print(f"Contato {nome} apagado com sucesso.")
    else:
        print("Contato não encontrado.")

    Pausar()
    Menu()


def Editar_Contato():
    Limpar_Tela()
    nome = input("Digite o nome do contato que deseja editar: \n").strip()
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,))
    contato = cursor.fetchone()

    if contato:
        Limpar_Tela()
        print(
            f"Contato encontrado: {contato[1]} - Telefone: {contato[2]} - Email: {contato[3]}"
        )

        novo_nome = input("Novo nome (pressione Enter para manter o atual): ").strip()
        novo_telefone = input(
            "Novo telefone (pressione Enter para manter o atual): "
        ).strip()
        novo_email = input("Novo email (pressione Enter para manter o atual): ").strip()

        if novo_nome:
            nome = novo_nome
        if novo_telefone and Validar_Telefone(novo_telefone):
            telefone = novo_telefone
        else:
            telefone = contato[2]
        if novo_email and re.match(r"[^@]+@[^@]+\.[^@]+", novo_email):
            email = novo_email
        else:
            email = contato[3]

        cursor.execute(
            "UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?",
            (nome, telefone, email, contato[0]),
        )
        conexao.commit()
        print(f"Contato atualizado: {nome} - Telefone: {telefone} - Email: {email}")
    else:
        print("Contato não encontrado.")

    Pausar()
    Menu()


# Inicia o programa
Menu()
