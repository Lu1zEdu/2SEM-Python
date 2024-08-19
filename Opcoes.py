def opcoes():
    print('Cadastrar = = 1')
    print('Mostrar = = 2')
    print('Remover = = 3')
    print('Atualizar = = 4')
    print('Sair = = 5')
    escolher_Opcaoo()



def escolher_Opcaoo():
    escolha= int(input('Escolha uma opções anteriores :  \n'))
    match escolha:
        case 1:
            nome = input("Qual o seu nome :");
            data = int(input(f"{nome} , quando que vc faz aniversario : \n"));
            email = input(f"{nome} , qual o seu email :\n");

        case 2:
            print()

if __name__ == "__main__":
    opcoes()