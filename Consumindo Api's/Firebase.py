import firebase_admin
from firebase_admin import credentials, db

# Carregar as credenciais do Firebase
cred = credentials.Certificate("")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://projetofaculdadefiap-default-rtdb.firebaseio.com/"}
)

# Referência para o nó onde armazenaremos os contatos
contatos_ref = db.reference("contatos")


def adicionar_contato(nome, telefone, email=None):
    contato_id = contatos_ref.push().key  # Gera uma nova chave única
    contatos_ref.child(contato_id).set(
        {"nome": nome, "telefone": telefone, "email": email}
    )
    print(f"Contato {nome} adicionado com sucesso!")


def listar_contatos():
    contatos = contatos_ref.get()
    if contatos:
        for contato_id, detalhes in contatos.items():
            print(f"ID: {contato_id}")
            print(f"Nome: {detalhes['nome']}")
            print(f"Telefone: {detalhes['telefone']}")
            if detalhes.get("email"):
                print(f"Email: {detalhes['email']}")
            print("-" * 20)
    else:
        print("Nenhum contato encontrado.")


def atualizar_contato(contato_id, nome=None, telefone=None, email=None):
    contato_ref = contatos_ref.child(contato_id)
    dados_atualizados = {}
    if nome:
        dados_atualizados["nome"] = nome
    if telefone:
        dados_atualizados["telefone"] = telefone
    if email:
        dados_atualizados["email"] = email

    contato_ref.update(dados_atualizados)
    print(f"Contato {contato_id} atualizado com sucesso!")


def remover_contato(contato_id):
    contatos_ref.child(contato_id).delete()
    print(f"Contato {contato_id} removido com sucesso!")


def menu():
    while True:
        print("\n1. Adicionar Contato")
        print("2. Listar Contatos")
        print("3. Atualizar Contato")
        print("4. Remover Contato")
        print("5. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            telefone = input("Telefone: ")
            email = input("Email (opcional): ")
            adicionar_contato(nome, telefone, email)

        elif opcao == "2":
            listar_contatos()

        elif opcao == "3":
            contato_id = input("ID do contato a ser atualizado: ")
            nome = input("Novo nome (deixe em branco para manter o atual): ")
            telefone = input("Novo telefone (deixe em branco para manter o atual): ")
            email = input("Novo email (deixe em branco para manter o atual): ")
            atualizar_contato(contato_id, nome, telefone, email)

        elif opcao == "4":
            contato_id = input("ID do contato a ser removido: ")
            remover_contato(contato_id)

        elif opcao == "5":
            break

        else:
            print("Opção inválida! Tente novamente.")


# Executa o menu
menu()
