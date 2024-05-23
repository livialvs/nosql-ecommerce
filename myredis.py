from bson import ObjectId
from bson.json_util import dumps
import json
import redis
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mymongo import readAllProdutosRedis

client = MongoClient("mongodb+srv://livialvss:fatec@fatec.psqy8bt.mongodb.net/mercadolivre", server_api=ServerApi('1'))
db = client.mercadolivre

conR = redis.Redis(
    host='redis-12881.c8.us-east-1-4.ec2.redns.redis-cloud.com',
    port=12881,
    password='6EVQgRslmdE3Yeh7cBUxzkYhfZNKH3Ql'
)

def migrarUsuarioParaRedis(cpf):
    usuario = db.usuario.find_one({"cpf": cpf})
    if usuario:
        usuario['_id'] = str(usuario['_id'])
        conR.set("user-" + cpf, dumps(usuario))
        print(f"Usuário com CPF {cpf} migrado para o Redis.")
    else:
        print(f"Usuário com CPF {cpf} não encontrado no MongoDB.")


def migrarVendedorParaRedis(cpf):
    vendedor = db.vendedor.find_one({"cpf": cpf})
    if vendedor:
        vendedor['_id'] = str(vendedor['_id'])
        conR.set("vendedor-" + cpf, dumps(vendedor))
        print(f"Vendedor com CPF {cpf} migrado para o Redis.")
    else:
        print(f"Vendedor com CPF {cpf} não encontrado no MongoDB.")

def migrarUsuarioParaMongo(cpf):

    chave = "user-" + cpf
    if conR.exists(chave):
        usuario = json.loads(conR.get(chave))
        if '_id' in usuario:
            usuario['_id'] = ObjectId(usuario['_id'])
        result = db.usuario.update_one({"cpf": cpf}, {"$set": usuario}, upsert=True)
        if result.modified_count > 0 or result.upserted_id:
            print(f"Usuário com CPF {cpf} atualizado no MongoDB.")
        else:
            print(f"Usuário com CPF {cpf} não encontrado no MongoDB para atualização.")
        conR.delete(chave)
    else:
        print(f"Usuário com CPF {cpf} não encontrado no Redis.")

def migrarVendedorParaMongo(cpf):
    chave = "vendedor-" + cpf
    if conR.exists(chave):
        vendedor = json.loads(conR.get(chave))
        if '_id' in vendedor:
            vendedor['_id'] = ObjectId(vendedor['_id'])
        result = db.vendedor.update_one({"cpf": cpf}, {"$set": vendedor}, upsert=True)
        if result.modified_count > 0 or result.upserted_id:
            print(f"Vendedor com CPF {cpf} atualizado no MongoDB.")
        else:
            print(f"Vendedor com CPF {cpf} não encontrado no MongoDB para atualização.")
        conR.delete(chave)
    else:
        print(f"Vendedor com CPF {cpf} não encontrado no Redis.")

def manipularUsuarioRedis(cpf):
    chave = "user-" + cpf
    if conR.exists(chave):
        usuario = json.loads(conR.get(chave))
        print("Dados do Usuário:")
        print(usuario)
        
        while True:
            print("\nO que você deseja alterar?")
            print("1 - Endereços")
            print("2 - Favoritos")
            print("0 - Sair")

            opcao = input("Digite o número da opção desejada: ")

            if opcao == "1":
                manipularEnderecos(usuario, chave)
            elif opcao == "2":
                manipularFavoritos(usuario, chave)
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

        conR.set(chave, json.dumps(usuario))
        print(f"Dados do usuário {cpf} atualizados no Redis.")
    else:
        print(f"Usuário {cpf} não encontrado no Redis.")

def manipularVendedorRedis(cpf):
    chave = "vendedor-" + cpf
    if conR.exists(chave):
        vendedor = json.loads(conR.get(chave))
        print("Dados do Vendedor:")
        print(vendedor)
        
        while True:
            print("\nO que você deseja alterar?")
            print("1 - Atualizar dados")
            print("2 - Deletar")
            print("0 - Sair")

            opcao = input("Digite o número da opção desejada: ")

            if opcao == "1":
                atualizarVendedor(vendedor, chave)
            elif opcao == "2":
                deletarVendedor(vendedor, chave)
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")

        conR.set(chave, json.dumps(vendedor))
        print(f"Dados do vendedor {cpf} atualizados no Redis.")
    else:
        print(f"Vendedor {cpf} não encontrado no Redis.")


def manipularEnderecos(usuario, chave):
    while True:
        print("\nEndereços cadastrados:")
        for i, endereco in enumerate(usuario.get('enderecos', [])):
            print(f"{i+1}: {endereco}")

        print("\nEscolha uma opção:")
        print("1 - Adicionar endereço")
        print("2 - Alterar endereço")
        print("3 - Remover endereço")
        print("0 - Voltar")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            adicionarEndereco(usuario)
        elif opcao == "2":
            alterarEndereco(usuario)
        elif opcao == "3":
            removerEndereco(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        
        conR.set(chave, json.dumps(usuario))
        print(f"Endereços do usuário atualizados no Redis.")

def adicionarEndereco(usuario):
    novo_endereco = {
        "rua": input("Rua: "),
        "numero": input("Número: "),
        "bairro": input("Bairro: "),
        "cidade": input("Cidade: "),
        "estado": input("Estado: ")
    }
    usuario.setdefault('enderecos', []).append(novo_endereco)

def alterarEndereco(usuario):
    try:
        indice = int(input("Digite o número do endereço a ser alterado: ")) - 1
        if 0 <= indice < len(usuario.get('enderecos', [])):
            usuario['enderecos'][indice]['rua'] = input("Nova rua: ")
            usuario['enderecos'][indice]['numero'] = input("Novo número: ")
            usuario['enderecos'][indice]['bairro'] = input("Novo bairro: ")
            usuario['enderecos'][indice]['cidade'] = input("Nova cidade: ")
            usuario['enderecos'][indice]['estado'] = input("Novo estado: ")
        else:
            print("Endereço não encontrado.")
    except ValueError:
        print("Entrada inválida.")

def removerEndereco(usuario):
    try:
        indice = int(input("Digite o número do endereço a ser removido: ")) - 1
        if 0 <= indice < len(usuario.get('enderecos', [])):
            usuario['enderecos'].pop(indice)
        else:
            print("Endereço não encontrado.")
    except ValueError:
        print("Entrada inválida.")

def manipularFavoritos(usuario, chave):
    while True:
        print("\nFavoritos cadastrados:")
        for i, favorito in enumerate(usuario.get('favoritos', [])):
            print(f"{i+1}: {favorito}")

        print("\nEscolha uma opção:")
        print("1: Adicionar favorito")
        print("2: Remover favorito")
        print("0: Voltar")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            adicionarFavorito(usuario)
        elif opcao == "2":
            removerFavorito(usuario)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
        
        conR.set(chave, json.dumps(usuario))
        print("Favoritos do usuário atualizados no Redis.")

def adicionarFavorito(usuario):
    produtos = listarProdutosParaFavoritos()
    produto_num = int(input("Digite o número do produto a ser adicionado aos favoritos: "))
    if 1 <= produto_num <= len(produtos):
        produto = produtos[produto_num - 1]
        favorito = {
            'id': {'$oid': str(produto['ID'])},  
            'nome': produto['Nome'],  
            'preco': produto['Preço'],  
            'vendedor': {
                'id': {'$oid': str(produto['Vendedor']['ID'])},  
                'nome': produto['Vendedor']['Nome'] 
            }
        }
        usuario.setdefault('favoritos', []).append(favorito)
        print("Produto adicionado aos favoritos com sucesso.")
    else:
        print("Número de produto inválido.")

def removerFavorito(usuario):
    try:
        indice = int(input("Digite o número do favorito a ser removido: ")) - 1
        if 0 <= indice < len(usuario.get('favoritos', [])):
            usuario['favoritos'].pop(indice)
        else:
            print("Favorito não encontrado.")
    except ValueError:
        print("Entrada inválida.")

def listarProdutosParaFavoritos():
    produtos = readAllProdutosRedis()
    for i, produto in enumerate(produtos, start=1):
        print(f"{i} - ID: {produto['ID']}, Nome: {produto['Nome']}, Preço: {produto['Preço']}, Quantidade: {produto['Quantidade']}")
    return produtos

def atualizarVendedor(vendedor, chave):
    while True:
        print("\nO que você deseja atualizar?")
        print("1 - Nome")
        print("2 - Email")
        print("3 - CPF")
        print("0 - Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            vendedor['nome'] = input("Novo nome: ")
        elif opcao == "2":
            vendedor['email'] = input("Novo email: ")
        elif opcao == "3":
            novo_cpf = input("Novo CPF: ")
            if novo_cpf != vendedor['cpf']:
                # Deleta o vendedor original do MongoDB
                db.vendedor.delete_one({"cpf": vendedor['cpf']})
                vendedor['cpf'] = novo_cpf
                nova_chave = "vendedor-" + vendedor['cpf']
                conR.delete(chave)
                chave = nova_chave
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

        conR.set(chave, json.dumps(vendedor))
        print(f"Dados do vendedor {vendedor['cpf']} atualizados no Redis.")


def deletarVendedor(vendedor, chave):
    db.vendedor.delete_one({"cpf": vendedor['cpf']}) 
    conR.delete(chave) 
    print(f"Vendedor com CPF {vendedor['cpf']} deletado do Redis e MongoDB.")

def main():
    while True:
        print("\nEscolha uma operação:")
        print("1 - Usuário")
        print("2 - Vendedor")
        print("0 - Sair")

        opcao_principal = input("Digite o número da opção desejada: ")

        if opcao_principal == "1":
            print("1 - Migrar usuário do MongoDB para o Redis")
            print("2 - Manipular usuário no Redis")
            print("3 - Migrar usuário do Redis para o MongoDB")
            print("0 - Sair")

            opcao_usuario = input("Digite o número da opção desejada: ")

            if opcao_usuario == "1":
                cpf = input("Digite o CPF do usuário a ser migrado: ")
                migrarUsuarioParaRedis(cpf)
            elif opcao_usuario == "2":
                cpf = input("Digite o CPF do usuário a ser manipulado: ")
                manipularUsuarioRedis(cpf)
            elif opcao_usuario == "3":
                cpf = input("Digite o CPF do usuário a ser migrado de volta: ")
                migrarUsuarioParaMongo(cpf)
            elif opcao_usuario == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")
        elif opcao_principal == "2":
            print("1 - Migrar vendedor do MongoDB para o Redis")
            print("2 - Manipular vendedor no Redis")
            print("3 - Migrar vendedor do Redis para o MongoDB")
            print("0 - Sair")

            opcao_vendedor = input("Digite o número da opção desejada: ")

            if opcao_vendedor == "1":
                cpf = input("Digite o cpf do vendedor a ser migrado: ") 
                migrarVendedorParaRedis(cpf) 
            elif opcao_vendedor == "2":
                cpf = input("Digite o cpf do vendedor a ser manipulado: ") 
                manipularVendedorRedis(cpf)
            elif opcao_vendedor == "3":
                cpf = (input("Digite o cpf do vendedor a ser migrado de volta: "))
                migrarVendedorParaMongo(cpf)
            elif opcao_vendedor == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")
        elif opcao_principal == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

           
