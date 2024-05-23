import pymongo
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://livialvss:fatec@fatec.psqy8bt.mongodb.net/mercadolivre", server_api=ServerApi('1'))
db = client.test


global mydb
mydb = client.mercadolivre


# find


def findSort():
    global mydb
    mycol = mydb.usuario
    print("\n####SORT####") 
    mydoc = mycol.find().sort("nome")
    for x in mydoc:
        print(x)


def findUser(cpf):
    global mydb
    mycol = mydb.usuario
    print("\n####FIND####")
    myuser = { "cpf": cpf}
    global user
    user = mycol.find_one(myuser)  
    return user  


def findVendedor(cpf):
    global mydb
    mycol = mydb.vendedor
    print("\n####FIND####")
    myvendedor = { "cpf": cpf}
    global vendedor
    vendedor = mycol.find_one(myvendedor)
    return vendedor


def findProduto(produtoId):
    global mydb
    mycol = mydb.produto
    print("\n####FIND####")
    try:
        myproduto = {"_id": ObjectId(produtoId)}
    except Exception as e:
        print("ID do produto inválido:", e)
        return None
    produto = mycol.find_one(myproduto)
    return produto



def findCompra(compraId):
    global mydb
    mycol = mydb.compra
    print("\n####FIND####")
    mycompra = { "_id": ObjectId(compraId)}
    global compra
    compra = mycol.find_one(mycompra)
    return compra


# create


def createUsuario(nome, cpf, email, enderecos):
    global mydb
    mycol = mydb.usuario
    print("\n####CREATE####")
    mydict = {"nome": nome, "cpf": cpf, "email": email, "enderecos": enderecos}
    x = mycol.insert_one(mydict)
    print(x.inserted_id)


def createVendedor(vendedorNome, vendedorCpf, vendedorEmail):
    global mydb
    mycol = mydb.vendedor
    print("\n####CREATE####")
    mydict = { "nome": vendedorNome, "cpf": vendedorCpf, "email": vendedorEmail}
    x = mycol.insert_one(mydict)
    print(x.inserted_id)


def createProduto(produtoNome, produtoPreco, produtoQuantidade, vendedor_id, vendedor_nome):
    global mydb
    mycol = mydb.produto
    print("\n####CREATE####")
    mydict = { "nome": produtoNome, "preco": produtoPreco, "quantidade": produtoQuantidade, "vendedor": {"id": vendedor_id, "nome": vendedor_nome}}
    x = mycol.insert_one(mydict)
    print(x.inserted_id)


def createCompra(compraStatus, compraPreco, compraData, compraFormaPagamento, produtos, usuario_id, usuario_nome):
    global mydb
    mycol = mydb.compra
    print("\n####CREATE####")
    
    lista_produtos = []
    for produto in produtos:
        produto_dict = {
            "id": ObjectId(produto.get("_id")),
            "nome": produto.get("nome"),
            "preco": produto.get("preco"),
            "quantidade": produto.get("quantidade"),
            "vendedor": {
                "id": ObjectId(produto.get("vendedor").get("id")),
                "nome": produto.get("vendedor").get("nome")
            }
        }
        lista_produtos.append(produto_dict)
    
    mydict = {
        "compraStatus": compraStatus,
        "compraPreco": compraPreco,
        "compraData": compraData,
        "compraFormaPagamento": compraFormaPagamento,
        "produtos": lista_produtos,  
        "usuario": {
            "id": usuario_id,
            "nome": usuario_nome
        }
    }
    x = mycol.insert_one(mydict)
    print(x.inserted_id)

#read

def readUsuario(cpf):
    global mydb
    mycol = mydb.compra
    usuario = findUser(cpf)
    if usuario:
        print("Detalhes do Usuário:")
        print("\nNome:", usuario.get("nome"))
        print("CPF:", usuario.get("cpf"))
        print("Email:", usuario.get("email"))
        
        enderecos = usuario.get("enderecos", [])
        if enderecos:
            print("\nEndereços:")
            for endereco in enderecos:
                print("\nEstado:", endereco.get("estado"))
                print("Cidade:", endereco.get("cidade"))
                print("Bairro:", endereco.get("bairro"))
                print("Rua:", endereco.get("rua"))
                print("Número:", endereco.get("numero"), "\n")
        else:
            print("Este usuário não possui endereços cadastrados.")
        
        favoritos = usuario.get("favoritos", [])
        if favoritos:
            print("\nFavoritos:")
            for favorito in favoritos:
                print("\nID:", favorito.get("id"))
                print("Nome:", favorito.get("nome"))
                print("Preço:", favorito.get("preco"))
                vendedor = favorito.get("vendedor", {})
                if vendedor:
                    print("Vendedor:")
                    print(" - ID:", ObjectId(vendedor.get("id")))
                    print(" - Nome:", vendedor.get("nome"))
                else:
                    print("Vendedor não especificado")
        else:
            print("Este usuário não possui favoritos cadastrados.")
        
        compras = mycol.find({"usuario.id": usuario.get("_id")})
        if compras:
            for compra in compras:
                print("------------------------------------------")
                print("Detalhes da Compra:")
                print("ID:", compra.get("_id"))
                print("Status:", compra.get("compraStatus"))
                print("Preço:", compra.get("compraPreco"))
                print("Data:", compra.get("compraData"))
                print("Forma de Pagamento:", compra.get("compraFormaPagamento"))
                for produto in compra.get("produtos", []):
                    print("\nProduto:")
                    print(" - ID:", ObjectId(produto.get("_id")))
                    print(" - Nome:", produto.get("nome"))
                    print(" - Preço:", produto.get("preco"))
                    print(" - Vendedor:")
                    print("  - ID:", ObjectId(produto.get("vendedor").get("_id")))
                    print("  - Nome:", produto.get("vendedor").get("nome"))
        else:
            print("Este usuário não possui compras cadastradas.")
    else:
        print("Usuário não encontrado.")
    return usuario


def readVendedor(cpf):
    vendedor = findVendedor(cpf)
    if vendedor:
        print("Detalhes do Vendedor:")
        print("Nome:", vendedor["nome"])
        print("CPF:", vendedor["cpf"])
        print("Email:", vendedor["email"])
    else:
        print("Vendedor não encontrado.")
    return vendedor


def readProduto(produtoId):
    produto = findProduto(produtoId)
    if produto:
        print("Detalhes do Produto:")
        print("Nome:", produto["nome"])
        print("Preço:", produto["preco"])
        print("Quantidade:", produto["quantidade"])
        print("Vendedor:")
        print(" - ID:", produto["vendedor"]["id"])
        print(" - Nome:", produto["vendedor"]["nome"])
    else:
        print("Produto não encontrado.")
    return produto


def readCompra(compraId):
    compra = findCompra(compraId)
    if compra:
        print("Detalhes da Compra:")
        print("Status:", compra.get("compraStatus"))
        print("Preço:", compra.get("compraPreco"))
        print("Data:", compra.get("compraData"))
        print("Forma de Pagamento:", compra.get("compraFormaPagamento"))
        
        print("\nProdutos:")
        for produto in compra.get("produtos", []):
            print("\nID:", ObjectId(produto.get("id")))
            print("Nome:", produto.get("nome"))
            print("Preço:", produto.get("preco"))
            vendedor = produto.get("vendedor")
            if vendedor:
                print("Vendedor:")
                print(" - ID:", ObjectId(vendedor.get("id")))
                print(" - Nome:", vendedor.get("nome"))
            else:
                print("Vendedor não especificado")
        
        print("\nUsuário:")
        print("ID:", compra["usuario"].get("id"))
        print("Nome:", compra["usuario"].get("nome"))
    else:
        print("Compra não encontrada.")
    return compra


# read all

def readAllUsuarios():
    global mydb
    mycol = mydb.usuario
    print("\n####READ ALL USUARIOS####")
    usuarios = mycol.find({})
    for usuario in usuarios:
        print("------------------------------------------")
        print("\nDetalhes do Usuário:")
        print("\nId:", usuario.get("_id"))
        print("Nome:", usuario.get("nome"))
        print("CPF:", usuario.get("cpf"))
        print("E-mail:", usuario.get("email"))
        
        enderecos = usuario.get("enderecos", [])
        if enderecos:
            print("\nEndereços:")
            for endereco in enderecos:
                print("\n - Estado:", endereco.get("estado"))
                print(" - Cidade:", endereco.get("cidade"))
                print(" - Bairro:", endereco.get("bairro"))
                print(" - Rua:", endereco.get("rua"))
                print(" - Número:", endereco.get("numero"))
        else:
            print("\nEste usuário não possui endereços cadastrados.")

        favoritos = usuario.get("favoritos", [])
        if favoritos:
            print("\nFavoritos:")
            for favorito in favoritos:
                print("ID:", ObjectId(favorito.get("_id")))
                print("Nome:", favorito.get("nome"))
                print("Preço:", favorito.get("preco"))
                vendedor = favorito.get("vendedor", {})
                print("Vendedor:")
                print(" - ID:", ObjectId(vendedor.get("_id")))
                print(" - Nome:", vendedor.get("nome"))
        else:
            print("\nEste usuário não possui favoritos cadastrados.")


def readAllVendedores():
    global mydb
    mycol = mydb.vendedor
    print("\n####READ ALL VENDEDORES####")
    vendedores = mycol.find({})
    for vendedor in vendedores:
        print("------------------------------------------")
        print("\nDetalhes do Vendedor:")
        print("ID:", vendedor.get("_id"))
        print("Nome:", vendedor.get("nome"))
        print("CPF:", vendedor.get("cpf"))
        print("E-mail:", vendedor.get("email"))


def readAllProdutosRedis():
    global mydb
    mycol = mydb.produto
    produtos = mycol.find({})
    resultado = []
    for produto in produtos:
        resultado.append({
            "ID": produto["_id"],
            "Nome": produto["nome"],
            "Preço": produto["preco"],
            "Quantidade": produto["quantidade"],
            "Vendedor": {
                "ID": produto["vendedor"]["id"],
                "Nome": produto["vendedor"]["nome"]
            }
        })
    return resultado
    

def readAllProdutos():
    global mydb
    mycol = mydb.produto
    print("\n####READ ALL PRODUTOS####")
    produtos = mycol.find({})
    for produto in produtos:
        print("------------------------------------------")
        print("\nDetalhes do Produto:")
        print("ID:", produto["_id"])
        print("Nome:", produto["nome"])
        print("Preço:", produto["preco"])
        print("Quantidade:", produto["quantidade"])
        print("Vendedor:")
        print(" - ID:", produto["vendedor"]["id"])
        print(" - Nome:", produto["vendedor"]["nome"])


def readAllCompras():
    global mydb
    mycol = mydb.compra
    print("\n####READ ALL COMPRAS####")
    compras = mycol.find({})
    for compra in compras:
        print("------------------------------------------")
        print("Detalhes da Compra:")
        print("ID:", compra["_id"])
        print("Status:", compra.get("compraStatus"))
        print("Preço:", compra.get("compraPreco"))
        print("Data:", compra.get("compraData"))
        print("Forma de Pagamento:", compra.get("compraFormaPagamento"))
        print("\nProdutos:")
        for produto in compra.get("produtos", []):
            print("\nProduto:")
            print(" - ID:", ObjectId(produto.get("id")))
            print(" - Nome:", produto.get("nome"))
            print(" - Preço:", produto.get("preco"))
            vendedor = produto.get("vendedor", {})
            print(" - Vendedor:")
            print("    - ID:", ObjectId(vendedor.get("_id")))
            print("    - Nome:", vendedor.get("nome"))
        usuario = compra.get("usuario", {})
        print("\nUsuário:")
        print("ID:", ObjectId(usuario.get("_id")))
        print("Nome:", usuario.get("nome"))


def readComprasUsuario(cpf):
    global mydb
    mycol = mydb.compra
    print("\n####READ COMPRAS USUARIO####")
    usuario = findUser(cpf)
    if usuario:
        compras = mycol.find({"usuario.id": usuario.get("_id")})
        for compra in compras:
            print("------------------------------------------")
            print("Detalhes da Compra:")
            print("ID:", compra.get("_id"))
            print("Status:", compra.get("compraStatus"))
            print("Preço:", compra.get("compraPreco"))
            print("Data:", compra.get("compraData"))
            print("Forma de Pagamento:", compra.get("compraFormaPagamento"))
            for produto in compra.get("produtos", []):
                print("\nProduto:")
                print(" - ID:", ObjectId(produto.get("_id")))
                print(" - Nome:", produto.get("nome"))
                print(" - Preço:", produto.get("preco"))
                print(" - Vendedor:")
                print("  - ID:", ObjectId(produto.get("vendedor").get("_id")))
                print("  - Nome:", produto.get("vendedor").get("nome"))
            print("\nUsuário:")
            print("ID:", ObjectId(compra.get("usuario").get("_id")))
            print("Nome:", compra.get("usuario").get("nome"))
    else:
        print("Usuário não encontrado.")
        

# update


def updateUsuario(usuarioId, updates):
    global mydb
    mycol = mydb.usuario
    print("\n####UPDATE####")
    mycol.update_one({"_id": usuarioId}, {"$set": updates})


def updateVendedor(vendedorId, updates):
    global mydb
    mycol = mydb.vendedor
    print("\n####UPDATE####")
    mycol.update_one({"_id": vendedorId}, {"$set": updates})


def updateProduto(produtoId, updates):
    global mydb
    mycol = mydb.produto
    print("\n####UPDATE####")
    mycol.update_one({"_id": produtoId}, {"$set": updates})


def adicionarEndereco(usuarioId, novoEndereco):
    global mydb
    mycol = mydb.usuario
    print("\n####ADICIONAR ENDEREÇO####")
    mycol.update_one({"_id": usuarioId}, {"$push": {"enderecos": novoEndereco}})
    print("Endereço adicionado com sucesso!")

def removerEndereco(usuarioId, enderecoRemover):
    global mydb
    mycol = mydb.usuario
    print("\n####REMOVER ENDEREÇO####")
    mycol.update_one({"_id": usuarioId}, {"$pull": {"enderecos": enderecoRemover}})
    print("Endereço removido com sucesso!")


# delete


def deleteUsuario(cpf):
    global mydb
    mycol = mydb.usuario
    print("\n####DELETE####")
    mycol.delete_one({"cpf": cpf})

def deleteVendedor(cpf):
    global mydb
    mycol = mydb.vendedor
    print("\n####DELETE####")
    mycol.delete_one({"cpf": cpf})

def deleteProduto(produtoId):
    global mydb
    mycol = mydb.produto
    print("\n####DELETE####")
    mycol.delete_one({"_id": ObjectId(produtoId)})

def deleteCompra(compraId):
    global mydb
    mycol = mydb.compra
    print("\n####DELETE####")
    mycol.delete_one({"_id": ObjectId(compraId)})


# favoritos

def addFavorito(cpf, produtoId):
    global mydb
    mycol = mydb.usuario
    print("\n####ADICIONAR FAVORITO####")
    usuario = findUser(cpf)
    if usuario:
        produto = findProduto(produtoId)
        if produto:
            favorito = {
                "id": produto.get("_id"),
                "nome": produto.get("nome"),
                "preco": produto.get("preco"),
                "vendedor": {
                    "id": produto["vendedor"].get("id"),
                    "nome": produto["vendedor"].get("nome")
                }
            }
            result = mycol.update_one(
                {"cpf": cpf},
                {"$push": {"favoritos": favorito}}
            )
            if result.modified_count > 0:
                print("Produto adicionado aos favoritos com sucesso!")
            else:
                print("Erro ao adicionar favorito.")
        else:
            print("Produto não encontrado.")
    else:
        print("Usuário não encontrado.")



def removeFavorito(cpf, produtoId):
    global mydb
    mycol = mydb.usuario
    print("\n####REMOVER FAVORITO####")
    usuario = findUser(cpf)
    if usuario:
        try:
            produto_oid = ObjectId(produtoId)
        except Exception as e:
            print("ID do produto inválido:", e)
            return

        result = mycol.update_one(
            {"cpf": cpf},
            {"$pull": {"favoritos": {"id": produto_oid}}}
        )

        if result.modified_count > 0:
            print("Favorito removido com sucesso!")
        else:
            print("Erro ao remover favorito. Usuário ou favorito não encontrado.")
    else:
        print("Usuário não encontrado.")


def readFavoritos(cpf):
    global mydb
    mycol = mydb.usuario
    print("\n####LISTAR FAVORITOS####")
    usuario = findUser(cpf)
    if usuario:
        favoritos = usuario["favoritos"]
        if favoritos:
            print("Favoritos do usuário:\n")
            for favorito in favoritos:
                print("Nome:", favorito["nome"])
                print("Preço:", favorito["preco"])
                if "vendedor" in favorito: 
                    vendedor = favorito["vendedor"]
                    print("Vendedor:")
                    if "id" in vendedor:  
                        vendedor_id = ObjectId(vendedor["id"])
                        print("  - ID:", vendedor_id)
                    if "nome" in vendedor: 
                        print("  - Nome:", vendedor["nome"], "\n")
                else:
                    print("Vendedor não especificado\n")
        else:
            print("O usuário não possui favoritos.")
    else:
        print("Usuário não encontrado.")


