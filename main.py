from mymongo import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from myredis import main as redis_main

uri = "mongodb+srv://livialvss:fatec@fatec.psqy8bt.mongodb.net/mercadolivre"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
global db
db = client.mercadolivre


# MENUS 

def menu_principal():
    print("\nMenu Principal:")
    print("1 - Usuário")
    print("2 - Vendedor")
    print("3 - Produto")
    print("4 - Compra")
    print("0 - Sair")


def menu_usuario():
    print("\nMenu Usuário:")
    print("1 - Create Usuário")
    print("2 - Read Usuário")
    print("3 - Update Usuário")
    print("4 - Delete Usuário")
    print("5 - Adicionar favorito")
    print("6 - Remover favorito")
    print("7 - Listar favoritos")
    print("8 - Listar todos os usuários")
    print("0 - Voltar")


def menu_vendedor():
    print("\nMenu Vendedor:")
    print("1 - Create Vendedor")
    print("2 - Read Vendedor")
    print("3 - Update Vendedor")
    print("4 - Delete Vendedor")
    print("5 - Listar todos os vendedores")
    print("0 - Voltar")


def menu_produto():
    print("\nMenu Produto:")
    print("1 - Create Produto")
    print("2 - Read Produto")
    print("3 - Update Produto")
    print("4 - Delete Produto")
    print("5 - Listar todos os produtos")
    print("0 - Voltar")


def menu_compra():
    print("\nMenu Compra:")
    print("1 - Create Compra")
    print("2 - Read Compra")
    print("3 - Delete Compra")
    print("4 - Listar todas as compras")
    print("5 - Listar compras de um usuário")
    print("0 - Voltar")

"""
fazer o adicionar e remover endereço
"""

# CREATE    

def criar_usuario():
    nome = input("Digite o nome do usuário: ")
    cpf = input("Digite o CPF do usuário: ")
    email = input("Digite o e-mail do usuário: ")

    enderecos = []
    key = input("Deseja cadastrar um endereço (S/N)? ")
    while key.upper() == 'S':
        print("Digite o endereço:")
        estado = input("Estado: ")
        cidade = input("Cidade: ")
        bairro = input("Bairro: ")
        rua = input("Rua: ")
        numero = input("Número: ")
        endereco = {"estado": estado, "cidade": cidade, "bairro": bairro, "rua": rua, "numero": numero}
        enderecos.append(endereco)
        key = input("Deseja cadastrar outro endereço (S/N)? ")

    createUsuario(nome, cpf, email, enderecos)
    print("Usuário criado com sucesso!")


def criar_vendedor():
    nome = input("Digite o nome do vendedor: ")
    cpf = input("Digite o CPF do vendedor: ")
    email = input("Digite o e-mail do vendedor: ")
    createVendedor(nome, cpf, email)
    print("Vendedor criado com sucesso!")


def criar_produto():
    vendedorCpf = input("Digite o CPF do vendedor: ")
    vendedor = findVendedor(vendedorCpf)
    if vendedor:
        produtoNome = input("Digite o nome do produto: ")
        produtoPreco = float(input("Digite o preço do produto: "))
        produtoQuantidade = int(input("Digite a quantidade do produto: "))
        createProduto(produtoNome, produtoPreco, produtoQuantidade, vendedor.get("_id"), vendedor.get("nome"))
        print("Produto criado com sucesso!")
    else:
        print("Vendedor não encontrado. Verifique o CPF e tente novamente.")

    
def criar_compra():
    usuario_cpf = input("Digite o CPF do usuário: ")
    usuario = findUser(usuario_cpf)
    if usuario:
        usuario_id = usuario.get("_id")
        usuario_nome = usuario.get("nome") 

        produtos = []
        continuar = 'S'

        while continuar.upper() == 'S':
            produtoId = input("Digite o ID do produto: ")
            quantidade = int(input("Digite a quantidade: "))
            produto = findProduto(produtoId)
            if produto:
                quantidade_disponivel = produto.get("quantidade", 0)
                if quantidade <= 0 or quantidade > quantidade_disponivel:
                    print(f"A quantidade solicitada não está disponível. Quantidade disponível: {quantidade_disponivel}")
                    continuar = input("Deseja escolher outro produto (S/N)? ")
                    continue
                
                vendedor_id = produto.get("vendedor", {}).get("_id")
                vendedor_nome = produto.get("vendedor", {}).get("nome")
                produtos.append({
                    "id": produto.get("_id"),
                    "nome": produto.get("nome"),
                    "preco": produto.get("preco"),
                    "quantidade": quantidade,
                    "vendedor": {
                        "id": vendedor_id,
                        "nome": vendedor_nome
                    }
                })
            else:
                print("Produto não encontrado. Tente novamente.")

            continuar = input("Deseja cadastrar mais um produto (S/N)? ")

        compraPreco = sum(produto["preco"] * produto["quantidade"] for produto in produtos)
        compraData = datetime.datetime.now()
        compraFormaPagamento = input("Digite a forma de pagamento da compra: ")

        createCompra("Em andamento", compraPreco, compraData, compraFormaPagamento, produtos, usuario_id, usuario_nome)
    else:
        print("Usuário não encontrado. Verifique o CPF e tente novamente.")


# UPDATE


def update_usuario(cpf):
    user = findUser(cpf)
    if user:
        print("Nome: ", user["nome"])
        print("CPF: ", user["cpf"])
        print("Email: ", user["email"])
        print("Endereços: ")
        for endereco in user["enderecos"]:  
            print("Estado: ", endereco["estado"])
            print("Cidade: ", endereco["cidade"])
            print("Bairro: ", endereco["bairro"])
            print("Rua: ", endereco["rua"])
            print("Número: ", endereco["numero"], "\n")    

        while True:
            print("\nMenu de Atualização:")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Email")
            print("4 - Endereços")
            print("5 - Adicionar Endereço")
            print("6 - Remover Endereço")
            print("0 - voltar")

            opcao = input("Escolha o número da opção que deseja alterar (ou '0' para voltar): ")

            if opcao == '0':
                break
            elif opcao == '1':
                novo_nome = input("Digite o novo nome: ")
                updateUsuario(user["_id"], {"nome": novo_nome})
            elif opcao == '2':
                novo_cpf = input("Digite o novo CPF: ")
                updateUsuario(user["_id"], {"cpf": novo_cpf})
            elif opcao == '3':
                novo_email = input("Digite o novo email: ")
                updateUsuario(user["_id"], {"email": novo_email})
            elif opcao == '4':
                if not user["enderecos"]:
                    print("Usuário não possui endereços cadastrados.")
                else:
                    print("Endereços cadastrados:")
                    for index, endereco in enumerate(user["enderecos"], start=1):
                        print(f"Endereço {index}:")
                        print("Estado: ", endereco["estado"])
                        print("Cidade: ", endereco["cidade"])
                        print("Bairro: ", endereco["bairro"])
                        print("Rua: ", endereco["rua"])
                        print("Número: ", endereco["numero"], "\n")

                    endereco_index = input("Digite o número do endereço que deseja editar (ou '0' para voltar): ")

                    if endereco_index == '0':
                        break
                    elif endereco_index.isdigit() and 1 <= int(endereco_index) <= len(user["enderecos"]):
                        endereco_selecionado = user["enderecos"][int(endereco_index) - 1]
                        print("Endereço selecionado:")
                        print("Estado: ", endereco_selecionado["estado"])
                        print("Cidade: ", endereco_selecionado["cidade"])
                        print("Bairro: ", endereco_selecionado["bairro"])
                        print("Rua: ", endereco_selecionado["rua"])
                        print("Número: ", endereco_selecionado["numero"])

                        while True:
                            print("\nO que deseja alterar no endereço?")
                            print("1 - Estado")
                            print("2 - Cidade")
                            print("3 - Bairro")
                            print("4 - Rua")
                            print("5 - Número")
                            print("6 - Tudo")
                            print("0 - Voltar")

                            opcao_endereco = input("Escolha o número da informação que deseja alterar: ")

                            if opcao_endereco == '0':
                                break
                            elif opcao_endereco == '1':
                                novo_estado = input("Digite o novo estado: ")
                                updateUsuario(user["_id"], {"enderecos." + str(int(endereco_index) - 1) + ".estado": novo_estado})
                            elif opcao_endereco == '2':
                                nova_cidade = input("Digite a nova cidade: ")
                                updateUsuario(user["_id"], {"enderecos." + str(int(endereco_index) - 1) + ".cidade": nova_cidade})
                            elif opcao_endereco == '3':
                                novo_bairro = input("Digite o novo bairro: ")
                                updateUsuario(user["_id"], {"enderecos." + str(int(endereco_index) - 1) + ".bairro": novo_bairro})
                            elif opcao_endereco == '4':
                                nova_rua = input("Digite a nova rua: ")
                                updateUsuario(user["_id"], {"enderecos." + str(int(endereco_index) - 1) + ".rua": nova_rua})
                            elif opcao_endereco == '5':
                                novo_numero = input("Digite o novo número: ")
                                updateUsuario(user["_id"], {"enderecos." + str(int(endereco_index) - 1) + ".numero": novo_numero})
                            elif opcao_endereco == '6':
                                novo_estado = input("Digite o novo estado: ")
                                nova_cidade = input("Digite a nova cidade: ")
                                novo_bairro = input("Digite o novo bairro: ")
                                nova_rua = input("Digite a nova rua: ")
                                novo_numero = input("Digite o novo número: ")
                                updateUsuario(user["_id"], {
                                    "enderecos." + str(int(endereco_index) - 1) + ".estado": novo_estado,
                                    "enderecos." + str(int(endereco_index) - 1) + ".cidade": nova_cidade,
                                    "enderecos." + str(int(endereco_index) - 1) + ".bairro": novo_bairro,
                                    "enderecos." + str(int(endereco_index) - 1) + ".rua": nova_rua,
                                    "enderecos." + str(int(endereco_index) - 1) + ".numero": novo_numero
                                })
                            else:
                                print("Opção inválida.")
                    else:
                        print("Número de endereço inválido.")
            elif opcao == '5':
                novo_estado = input("Digite o estado: ")
                nova_cidade = input("Digite a cidade: ")
                novo_bairro = input("Digite o bairro: ")
                nova_rua = input("Digite a rua: ")
                novo_numero = input("Digite o número: ")
                
                novo_endereco = {
                    "estado": novo_estado,
                    "cidade": nova_cidade,
                    "bairro": novo_bairro,
                    "rua": nova_rua,
                    "numero": novo_numero
                }
                
                adicionarEndereco(user["_id"], novo_endereco)
            elif opcao == '6':
                if not user["enderecos"]:
                    print("Usuário não possui endereços cadastrados.")
                else:
                    print("Endereços cadastrados:")
                    for index, endereco in enumerate(user["enderecos"], start=1):
                        print(f"Endereço {index}:")
                        print("Estado: ", endereco["estado"])
                        print("Cidade: ", endereco["cidade"])
                        print("Bairro: ", endereco["bairro"])
                        print("Rua: ", endereco["rua"])
                        print("Número: ", endereco["numero"], "\n")

                    endereco_index = input("Digite o número do endereço que deseja remover (ou '0' para voltar): ")

                    if endereco_index == '0':
                        break
                    elif endereco_index.isdigit() and 1 <= int(endereco_index) <= len(user["enderecos"]):
                        endereco_selecionado = user["enderecos"][int(endereco_index) - 1]
                        print("Endereço selecionado:")
                        print("Estado: ", endereco_selecionado["estado"])
                        print("Cidade: ", endereco_selecionado["cidade"])
                        print("Bairro: ", endereco_selecionado["bairro"])
                        print("Rua: ", endereco_selecionado["rua"])
                        print("Número: ", endereco_selecionado["numero"])

                        confirmacao = input("Tem certeza de que deseja remover este endereço? (s/n): ")

                        if confirmacao.lower() == 's':
                            removerEndereco(user["_id"], endereco_selecionado)
                    else:
                        print("Número de endereço inválido.")
            else:
                print("Opção inválida.")
    else:
        print("Usuário não encontrado.")


def update_vendedor(cpf):
    vendedor = findVendedor(cpf)
    if vendedor:
        print("Nome: ", vendedor["nome"])
        print("CPF: ", vendedor["cpf"])
        print("Email: ", vendedor["email"])

        while True:
            print("\nMenu de Atualização:")
            print("1 - Nome")
            print("2 - CPF")
            print("3 - Email")
            print("0 - voltar")

            opcao = input("Escolha o número da opção que deseja alterar (ou '0' para voltar): ")

            if opcao == '0':
                break
            elif opcao == '1':
                novo_nome = input("Digite o novo nome: ")
                updateVendedor(vendedor["_id"], {"nome": novo_nome})
            elif opcao == '2':
                novo_cpf = input("Digite o novo CPF: ")
                updateVendedor(vendedor["_id"], {"cpf": novo_cpf})
            elif opcao == '3':
                novo_email = input("Digite o novo email: ")
                updateVendedor(vendedor["_id"], {"email": novo_email})
            else:
                print("Opção inválida.")
    else:
        print("Vendedor não encontrado.")

def update_produto(produtoId):
    produto = findProduto(produtoId)
    if produto:
        print("Nome: ", produto["nome"])
        print("Preço: ", produto["preco"])
        print("Quantidade: ", produto["quantidade"])

        while True:
            print("\nMenu de Atualização:")
            print("1 - Nome")
            print("2 - Preço")
            print("3 - Quantidade")
            print("0 - voltar")

            opcao = input("Escolha o número da opção que deseja alterar (ou '0' para voltar): ")

            if opcao == '0':
                break
            elif opcao == '1':
                novo_nome = input("Digite o novo nome: ")
                updateProduto(produto["_id"], {"nome": novo_nome})
            elif opcao == '2':
                novo_preco = float(input("Digite o novo preço: "))
                updateProduto(produto["_id"], {"preco": novo_preco})
            elif opcao == '3':
                nova_quantidade = int(input("Digite a nova quantidade: "))
                updateProduto(produto["_id"], {"quantidade": nova_quantidade})
            else:
                print("Opção inválida.")
    else:
        print("Produto não encontrado.")


def main():
    while True:
        menu_principal()
        escolha_principal = input("Escolha uma opção: ")
        if escolha_principal == '1':
            menu_usuario()
            escolha_usuario = input("Escolha uma opção de usuário: ")
            if escolha_usuario == '1':
                criar_usuario()
            elif escolha_usuario == '2':
                cpf = input("Digite o CPF do usuário: ")
                readUsuario(cpf)
            elif escolha_usuario == '3':
                cpf = input("Digite o CPF do usuário: ")
                update_usuario(cpf)
            elif escolha_usuario == '4':
                cpf = input("Digite o CPF do usuário: ")
                deleteUsuario(cpf)
            elif escolha_usuario == '5':
                cpf = input("Digite o CPF do usuário: ")
                produtoId = input("Digite o ID do produto: ")
                addFavorito(cpf, produtoId)
            elif escolha_usuario == '6':
                cpf = input("Digite o CPF do usuário: ")
                produtoId = input("Digite o ID do produto: ")
                removeFavorito(cpf, produtoId)
            elif escolha_usuario == '7':
                cpf = input("Digite o CPF do usuário: ")
                readFavoritos(cpf)
            elif escolha_usuario == '8':
                readAllUsuarios()    
        elif escolha_principal == '2':
            menu_vendedor()
            escolha_vendedor = input("Escolha uma opção de vendedor: ")
            if escolha_vendedor == '1':
                criar_vendedor()
            elif escolha_vendedor == '2':
                cpf = input("Digite o CPF do vendedor: ")
                readVendedor(cpf)
            elif escolha_vendedor == '3':
                cpf = input("Digite o CPF do vendedor: ")
                update_vendedor(cpf)
            elif escolha_vendedor == '4':
                cpf = input("Digite o CPF do vendedor: ")
                deleteVendedor(cpf)
            elif escolha_vendedor == '5':
                readAllVendedores()
        elif escolha_principal == '3':
            menu_produto()
            escolha_produto = input("Escolha uma opção de produto: ")
            if escolha_produto == '1':
                criar_produto()
            elif escolha_produto == '2':
                produtoId = input("Digite o ID do produto: ")
                readProduto(produtoId)
            elif escolha_produto == '3':
                produtoId = input("Digite o ID do produto: ")
                update_produto(produtoId)
            elif escolha_produto == '4':
                produtoId = input("Digite o ID do produto: ")
                deleteProduto(produtoId)
            elif escolha_produto == '5':
                readAllProdutos()
        elif escolha_principal == '4':
            menu_compra()
            escolha_compra = input("Escolha uma opção de compra: ")
            if escolha_compra == '1':
                criar_compra()
            elif escolha_compra == '2':
                compraId = input("Digite o ID da compra: ")
                readCompra(compraId)
            elif escolha_compra == '3':
                compraId = input("Digite o ID da compra: ")
                deleteCompra(compraId)
            elif escolha_compra == '4':
                readAllCompras()
            elif escolha_compra == '5':
                cpf = input("Digite o CPF do usuário: ")
                readComprasUsuario(cpf)
        elif escolha_principal == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()