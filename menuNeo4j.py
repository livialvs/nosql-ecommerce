from main import *

uri = "neo4j+s://89dff8b3.databases.neo4j.io"
username = "neo4j"
password = "N8Htqbw46ntHASPyib15pCMVX7TS7xjm4DneoM7JudQ"
driver = GraphDatabase.driver(uri, auth=(username, password))

def main():
    while True:
        print("\nMenu Principal")
        print("1 - Create Usuário")
        print("2 - Create Vendedor")
        print("3 - Create Produto")
        print("4 - Create Compra")
        print("5 - Create Favoritos")
        print("6 - Read Usuários")
        print("7 - Read Vendedores")
        print("8 - Read Produtos")
        print("9 - Read Compras")
        print("10 - Read Favoritos")
        print("0 - Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            createUsuario()
        elif choice == '2':
            createVendedor()
        elif choice == '3':
            createProduto()
        elif choice == '4':
            createCompra()
        elif choice == '5':
            createFavoritos()
        elif choice == '6':
            readUsuario()
        elif choice == '7':
            readVendedor()
        elif choice == '8':
            readProduto()
        elif choice == '9':
            readCompra()
        elif choice == '10':
            readFavoritos()
        elif choice == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
