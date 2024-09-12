from pymongo import MongoClient

# Configura a conexão com o MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["agenda_telefonica"]  # Nome do banco de dados
contatos_collection = db["contatos"]  # Nome da coleção


def adicionar_contato(nome, telefone, email=None):
    contato = {"nome": nome, "telefone": telefone, "email": email}
    contatos_collection.insert_one(contato)
    print(f"Contato {nome} adicionado com sucesso!")


def listar_contatos():
    contatos = contatos_collection.find()
    if contatos.count() > 0:
        for contato in contatos:
            print(f"ID: {contato['_id']}")
            print(f"Nome: {contato['nome']}")
            print(f"Telefone: {contato['telefone']}")
            if contato.get("email"):
                print(f"Email: {contato['email']}")
            print("-" * 20)
    else:
        print("Nenhum contato encontrado.")


def atualizar_contato(contato_id, nome=None, telefone=None, email=None):
    dados_atualizados = {}
    if nome:
        dados_atualizados["nome"] = nome
    if telefone:
        dados_atualizados["telefone"] = telefone
    if email:
        dados_atualizados["email"] = email

    result = contatos_collection.update_one(
        {"_id": contato_id}, {"$set": dados_atualizados}
    )
    if result.modified_count > 0:
        print(f"Contato {contato_id} atualizado com sucesso!")
    else:
        print("Nenhum contato foi atualizado.")


def remover_contato(contato_id):
    result = contatos_collection.delete_one({"_id": contato_id})
    if result.deleted_count > 0:
        print(f"Contato {contato_id} removido com sucesso!")
    else:
        print("Nenhum contato foi removido.")


from bson.objectid import ObjectId


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
            contato_id_str = input(
                "ID do contato a ser atualizado (use o ID que é mostrado ao listar contatos): "
            )
            try:
                contato_id = ObjectId(contato_id_str)
                nome = input("Novo nome (deixe em branco para manter o atual): ")
                telefone = input(
                    "Novo telefone (deixe em branco para manter o atual): "
                )
                email = input("Novo email (deixe em branco para manter o atual): ")
                atualizar_contato(contato_id, nome, telefone, email)
            except Exception as e:
                print(f"Erro ao atualizar contato: {e}")

        elif opcao == "4":
            contato_id_str = input(
                "ID do contato a ser removido (use o ID que é mostrado ao listar contatos): "
            )
            try:
                contato_id = ObjectId(contato_id_str)
                remover_contato(contato_id)
            except Exception as e:
                print(f"Erro ao remover contato: {e}")

        elif opcao == "5":
            break

        else:
            print("Opção inválida! Tente novamente.")


# Executa o menu
menu()
