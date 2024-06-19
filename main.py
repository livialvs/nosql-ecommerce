import json
from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:bjuyKIxnbzxkEDzxymZReYoY:1abf4483408b4dfc664dddbc5c1ad955ec15e4b4c08cd1e20d55557cc8da1425")
db = client.get_database_by_api_endpoint(
    "https://77851314-0af5-4590-8784-01b23081c901-us-east-2.apps.astra.datastax.com"
)

usuarioCol = db.get_collection("usuario")
vendCol = db.get_collection("vendedor")
prodCol = db.get_collection("produto")
compCol = db.get_collection("compra")
favCol = db.get_collection("favoritos")


#CREATE de usuário, vendedor, produto e compra

def createUsuario():
    mycolAstra = usuarioCol

    print("\nCreate - Usuário\n")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    key = 'S'  
    enderecos = []
    while (key.upper() != 'N'):
        print("\nInserindo um novo endereço")
        pais = input("País: ")
        estado = input("Estado: ")
        cidade = input("Cidade: ")
        bairro = input("Bairro: ")
        rua = input("Rua: ")
        numero = input("Número: ")
        endereco = {        
            "pais": pais,
            "estado": estado,
            "cidade": cidade,
            "bairro": bairro,
            "rua": rua,
            "numero": numero
        }
        enderecos.append(endereco) 
        key = input("Deseja cadastrar um novo endereço (S/N)? ")
    mydoc = { "nome": nome, "cpf": cpf, "endereco": enderecos, "email": email }

    x = mycolAstra.insert_one(mydoc)
    print("Documento inserido no Cassandra com ID ",x.inserted_id)


def createVendedor():
    mycolAstra = vendCol

    print("\nCreate - Vendedor\n")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")

    mydoc = { "nome": nome, "cpf": cpf, "email": email }

    x = mycolAstra.insert_one(mydoc)
    print("Documento inserido no Cassandra com ID ",x.inserted_id)

def findVendedor(vendedorCpf):
    vendedor = vendCol.find_one({"cpf": vendedorCpf})
    return vendedor


def createProduto():
    try:
        mycolAstra = prodCol

        print("\nCreate - Produto\n")
        vendedorCpf = input("CPF do Vendedor: ")

        vendedor = findVendedor(vendedorCpf)
        if not vendedor:
            print(f"Vendedor com CPF {vendedorCpf} não encontrado.")
            return

        nome = input("Nome: ")
        preco = float(input("Preço: "))
        quantidade = input("Quantidade: ")
        status = input("Status: ")


        mydoc = {
            "nome": nome,
            "preco": preco,
            "quantidade": quantidade,
            "status": status,
            "vendedor": vendedorCpf
        }

        x = mycolAstra.insert_one(mydoc)
        print("Documento inserido no Cassandra com ID ", x.inserted_id)

    except ValueError as e:
        print(f"Erro ao inserir produto: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")


def findUsuario(usuarioCpf):
    usuario = usuarioCol.find_one({"cpf": usuarioCpf})
    return usuario


def createCompra():
    mycol_compra = compCol
    mycol_produto = prodCol
    mycol_usuario = usuarioCol
    mycol_vendedor = vendCol

    print("\nCreate - Compra\n")

    clienteCpf = input("CPF do Cliente: ")

    cliente = findUsuario(clienteCpf)
    if not cliente:
        print(f"Usuário com CPF {clienteCpf} não encontrado.")
        return
    

    print("\nProdutos disponíveis:")
    for produto in mycol_produto.find():
        print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")

    produtoId = input("ID do Produto: ")

    produto = mycol_produto.find_one({"_id": produtoId})
    if produto is None:
        print("Produto não encontrado.")
        return
    
    quantidade = int(input("Quantidade: "))
    precoTotal = int(produto["preco"]) * quantidade

    usuario = {
        "cpf": cliente["cpf"],
        "nome": cliente["nome"]
    }

    produtos = {
        "id": produto["_id"],
        "nome": produto["nome"],
        "preco": produto["preco"],
        "quantidade": quantidade
    }

    mydoc = {
        "usuario": usuario,
        "produtos": produtos,
        "precoTotal": precoTotal,
        "vendedor": produto["vendedor"]
    }

    x = mycol_compra.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)


def createFavoritos():
    mycol_favoritos = favCol
    mycol_produto = prodCol
    mycol_usuario = usuarioCol

    print("\nCreate - Favoritos\n")

    clienteCpf = input("CPF do Cliente: ")

    cliente = findUsuario(clienteCpf)
    if not cliente:
        print(f"Usuário com CPF {clienteCpf} não encontrado.")
        return
    

    print("\nProdutos disponíveis:")
    for produto in mycol_produto.find():
        print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")

    produtoId = input("ID do Produto: ")

    produto = mycol_produto.find_one({"_id": produtoId})
    if produto is None:
        print("Produto não encontrado.")
        return
    
    mydoc = {
        "usuario": cliente["cpf"],
        "produtoId": produto["_id"],
        "produtoNome": produto["nome"],
        "produtoPreco": produto["preco"]
    }

    x = mycol_favoritos.insert_one(mydoc)
    print("Documento inserido com ID ", x.inserted_id)
    


#READ de usuário, vendedor, produto, compra e favoritos


def readUsuario():
    mycolAstra = usuarioCol

    print("\nRead - Usuário\n")
    for usuario in mycolAstra.find():
        print(usuario)


def readVendedor():
    mycolAstra = vendCol

    print("\nRead - Vendedor\n")
    for vendedor in mycolAstra.find():
        print(vendedor)


def readProduto():
    mycolAstra = prodCol

    print("\nRead - Produto\n")
    for produto in mycolAstra.find():
        print(produto)


def readCompra():
    mycolAstra = compCol

    print("\nRead - Compra\n")
    for compra in mycolAstra.find():
        print(compra)


def readFavoritos():
    mycolAstra = favCol
    mycol_produto = prodCol

    print("\nRead - Favoritos\n")
    usuarioCpf = input("CPF do Usuário: ")
    usuario = findUsuario(usuarioCpf)

    if usuario:
        favoritos = list(mycolAstra.find({"usuario": usuarioCpf}))
        if favoritos:
            print("Favoritos do usuário:")
            for favorito in favoritos:
                produto = mycol_produto.find_one({"id": favorito["produtoId"]})
                if produto:
                    print(f"ID: {produto['id']}, Nome: {produto['nome']}, Preço: {produto['preco']}")
                else:
                    print(f"Produto com ID {favorito['produtoId']} não encontrado.")
        else:
            print("Usuário não tem produtos favoritos.")
    else:
        print("Usuário não encontrado.")
        

#SEARCH de produto


def searchProduto():
    mycolAstra = prodCol

    print("\nSearch - Produto\n")
    produtoId = input("ID do Produto: ").strip()  # Remover espaços em branco

    try:
        produto = mycolAstra.find_one({"_id": produtoId})
        if produto:
            print(produto)
        else:
            print("Produto não encontrado.")
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")

#UPDATE de usuário


def updateUsuario():
    mycolAstra = usuarioCol

    print("\nUpdate - Usuário\n")
    cpf = input("CPF do Usuário: ")

    # Verifique se o usuário existe
    usuario = mycolAstra.find_one({"cpf": cpf})
    if not usuario:
        print("Usuário não encontrado.")
        return

    print("\nO que você deseja alterar?")
    print("1 - Nome")
    print("2 - Email")
    print("3 - Endereço")
    print("4 - Adicionar Endereço")
    print("5 - Adicionar Favoritos")
    choice = input("Escolha uma opção: ")

    if choice == '1':
        nome = input("Novo Nome: ")
        mycolAstra.update_one({"cpf": cpf}, {"$set": {"nome": nome}})
    elif choice == '2':
        email = input("Novo Email: ")
        mycolAstra.update_one({"cpf": cpf}, {"$set": {"email": email}})
    elif choice == '3':
        if 'endereco' in usuario and usuario['endereco']:
            print("\nEndereços:")
            for idx, endereco in enumerate(usuario['endereco']):
                print(f"{idx + 1} - {endereco}")
            endereco_idx = int(input("Qual endereço você deseja alterar? (Digite o número): ")) - 1
            if 0 <= endereco_idx < len(usuario['endereco']):
                print("\nInserindo um novo endereço")
                pais = input("País: ")
                estado = input("Estado: ")
                cidade = input("Cidade: ")
                bairro = input("Bairro: ")
                rua = input("Rua: ")
                numero = input("Número: ")
                endereco = {
                    "pais": pais,
                    "estado": estado,
                    "cidade": cidade,
                    "bairro": bairro,
                    "rua": rua,
                    "numero": numero
                }
                usuario['endereco'][endereco_idx] = endereco
                mycolAstra.update_one({"cpf": cpf}, {"$set": {"endereco": usuario['endereco']}})
            else:
                print("Número de endereço inválido.")
        else:
            print("Usuário não tem endereços cadastrados.")
    elif choice == '4':
        print("\nInserindo um novo endereço")
        pais = input("País: ")
        estado = input("Estado: ")
        cidade = input("Cidade: ")
        bairro = input("Bairro: ")
        rua = input("Rua: ")
        numero = input("Número: ")
        endereco = {
            "pais": pais,
            "estado": estado,
            "cidade": cidade,
            "bairro": bairro,
            "rua": rua,
            "numero": numero
        }
        mycolAstra.update_one({"cpf": cpf}, {"$push": {"endereco": endereco}})
    elif choice == '5':
        print("\nAdicionando favoritos")
        produtoId = input("ID do Produto: ")
        mycolAstra.update_one({"cpf": cpf}, {"$push": {"favoritos": produtoId}})


#DELETE de compra


def deleteCompra():
    mycolAstra = compCol

    print("\nDelete - Compra\n")

    compras = list(mycolAstra.find())
    if not compras:
        print("Nenhuma compra encontrada.")
        return

    print("\nCompras disponíveis:")
    for compra in compras:
        print(f"ID: {compra['_id']}, Detalhes: {compra}")

    compraId = input("\nDigite o ID da Compra que você deseja deletar: ")
    result = mycolAstra.delete_one({"_id": compraId})

    if result.deleted_count > 0:
        print("Compra deletada com sucesso.")
    else:
        print("ID da Compra não encontrado.")