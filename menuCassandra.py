import json
import sys
from astrapy import DataAPIClient
from main import *

# Initialize the client
client = DataAPIClient("AstraCS:bjuyKIxnbzxkEDzxymZReYoY:1abf4483408b4dfc664dddbc5c1ad955ec15e4b4c08cd1e20d55557cc8da1425")
db = client.get_database_by_api_endpoint(
    "https://77851314-0af5-4590-8784-01b23081c901-us-east-2.apps.astra.datastax.com"
)


usuarioCol = db.get_collection("usuario")
vendCol = db.get_collection("vendedor")
prodCol = db.get_collection("produto")
compCol = db.get_collection("compra")
def mainMenu():
    while True:
        print("\n--- Menu Principal ---")
        print("1 - Cadastrar")
        print("2 - Read")
        print("3 - Search de Produto")
        print("4 - Update de Usuário")
        print("5 - Delete de Compra")
        print("6 - Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            cadastrarMenu()
        elif choice == '2':
            readMenu()
        elif choice == '3':
            searchProduto()
        elif choice == '4':
            updateUsuario()
        elif choice == '5':
            deleteCompra()
        elif choice == '6':
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

def cadastrarMenu():
    print("\n--- Menu Cadastrar ---")
    print("1 - Usuário")
    print("2 - Vendedor")
    print("3 - Produto")
    print("4 - Compra")
    print("5 - Favoritos")
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
    else:
        print("Opção inválida. Tente novamente.")

def readMenu():
    print("\n--- Menu Read ---")
    print("1 - Usuários")
    print("2 - Vendedores")
    print("3 - Produtos")
    print("4 - Compras")
    print("5 - Favoritos")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        readUsuario()
    elif choice == '2':
        readVendedor()
    elif choice == '3':
        readProduto()
    elif choice == '4':
        readCompra()
    elif choice == '5':
        readFavoritos()
    else:
        print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    mainMenu()