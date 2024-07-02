from neo4j import GraphDatabase
import uuid

# Initialize the Neo4j driver
uri = "neo4j+s://89dff8b3.databases.neo4j.io"
username = "neo4j"
password = "N8Htqbw46ntHASPyib15pCMVX7TS7xjm4DneoM7JudQ"
driver = GraphDatabase.driver(uri, auth=(username, password))

# CREATE

def createUsuario():
    print("\nCreate - Usuário\n")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    enderecos = []

    while True:
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
        key = input("Deseja cadastrar um novo endereço (S/N)? ").upper()
        if key != 'S':
            break

    with driver.session() as session:
        session.run(
            """
            CREATE (u:Usuario {nome: $nome, cpf: $cpf, email: $email})
            """,
            nome=nome, cpf=cpf, email=email
        )
        
        for endereco in enderecos:
            session.run(
                """
                MATCH (u:Usuario {cpf: $cpf})
                CREATE (e:Endereco {pais: $pais, estado: $estado, cidade: $cidade, bairro: $bairro, rua: $rua, numero: $numero})
                CREATE (u)-[:RESIDE_EM]->(e)
                """,
                cpf=cpf, pais=endereco["pais"], estado=endereco["estado"], cidade=endereco["cidade"], 
                bairro=endereco["bairro"], rua=endereco["rua"], numero=endereco["numero"]
            )
        print("Usuário criado com sucesso.")


def createVendedor():
    print("\nCreate - Vendedor\n")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")

    with driver.session() as session:
        session.run(
            """
            CREATE (v:Vendedor {nome: $nome, cpf: $cpf, email: $email})
            """,
            nome=nome, cpf=cpf, email=email
        )
        print("Vendedor criado com sucesso.")


def createProduto():
    print("\nCreate - Produto\n")
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    vendedorCpf = input("CPF do Vendedor: ")

    with driver.session() as session:
        vendedor = session.run(
            """
            MATCH (v:Vendedor {cpf: $cpf}) RETURN v
            """,
            cpf=vendedorCpf
        ).single()

        if not vendedor:
            print(f"Vendedor com CPF {vendedorCpf} não encontrado.")
            return

        session.run(
            """
            MATCH (v:Vendedor {cpf: $vendedorCpf})
            CREATE (p:Produto {id: randomUUID(), nome: $nome, preco: $preco})-[:VENDIDO_POR]->(v)
            """,
            nome=nome, preco=preco, vendedorCpf=vendedorCpf
        )
        print("Produto criado com sucesso.")


def createCompra():
    print("\nCreate - Compra\n")
    clienteCpf = input("CPF do Cliente: ")

    with driver.session() as session:
        cliente = session.run(
            """
            MATCH (u:Usuario {cpf: $cpf}) RETURN u
            """,
            cpf=clienteCpf
        ).single()

        if not cliente:
            print(f"Usuário com CPF {clienteCpf} não encontrado.")
            return

        print("\nProdutos disponíveis:")
        result = session.run("MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor) RETURN p.id AS id, p.nome AS nome, p.preco AS preco, v.nome AS vendedorNome, v.cpf AS vendedorCpf")
        produtos = result.data()

        if not produtos:
            print("Nenhum produto disponível.")
            return

        for p in produtos:
            print(f"ID: {p['id']}, Nome: {p['nome']}, Preço: {p['preco']}, Vendedor: {p['vendedorNome']} (CPF Vendedor: {p['vendedorCpf']})")

        produtoId = input("ID do Produto: ")
        produto = next((p for p in produtos if p['id'] == produtoId), None)

        if not produto:
            print("Produto não encontrado.")
            return

        quantidade = int(input("Quantidade do Produto: "))
        precoTotal = produto['preco'] * quantidade

        session.run(
            """
            MATCH (u:Usuario {cpf: $clienteCpf})
            MATCH (p:Produto {id: $produtoId})
            CREATE (u)-[:COMPRA {quantidade: $quantidade, precoTotal: $precoTotal}]->(p)
            """,
            clienteCpf=clienteCpf, produtoId=produtoId, quantidade=quantidade, precoTotal=precoTotal
        )

        print(f"Compra realizada com sucesso!\nCliente: {cliente['u']['nome']}\nProduto: {produto['nome']}\nQuantidade: {quantidade}\nPreço Total: {precoTotal}\nVendedor: {produto['vendedorNome']} (CPF Vendedor: {produto['vendedorCpf']})")


def createFavoritos():
    print("\nCreate - Favoritos\n")
    clienteCpf = input("CPF do Cliente: ")

    with driver.session() as session:
        cliente = session.run(
            """
            MATCH (u:Usuario {cpf: $cpf}) RETURN u
            """,
            cpf=clienteCpf
        ).single()

        if not cliente:
            print(f"Usuário com CPF {clienteCpf} não encontrado.")
            return

        print("\nProdutos disponíveis:")
        result = session.run("MATCH (p:Produto) RETURN p.id AS id, p.nome AS nome, p.preco AS preco")
        produtos = result.data()

        if not produtos:
            print("Nenhum produto disponível.")
            return

        for p in produtos:
            print(f"ID: {p['id']}, Nome: {p['nome']}, Preço: {p['preco']}")

        produtoId = input("ID do Produto: ")
        produto = next((p for p in produtos if p['id'] == produtoId), None)

        if not produto:
            print("Produto não encontrado.")
            return

        session.run(
            """
            MATCH (u:Usuario {cpf: $clienteCpf})
            MATCH (p:Produto {id: $produtoId})
            CREATE (u)-[:FAVORITA]->(p)
            """,
            clienteCpf=clienteCpf, produtoId=produtoId
        )
        print("Produto adicionado aos favoritos com sucesso.")


# READ


def readUsuario():
    print("\nRead - Usuário\n")
    with driver.session() as session:
        usuarios = session.run("MATCH (u:Usuario) RETURN u").data()
        for usuario in usuarios:
            print(usuario['u'])


def readVendedor():
    print("\nRead - Vendedor\n")
    with driver.session() as session:
        vendedores = session.run("MATCH (v:Vendedor) RETURN v").data()
        for vendedor in vendedores:
            print(vendedor['v'])


def readProduto():
    print("\nRead - Produtos\n")

    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor)
            RETURN p.id AS id, p.nome AS nome, p.preco AS preco, v.nome AS vendedorNome, v.cpf AS vendedorCpf
            """
        )

        produtos = result.data()
        if produtos:
            for produto in produtos:
                print(f"ID: {produto['id']}")
                print(f"Nome: {produto['nome']}")
                print(f"Preço: {produto['preco']}")
                print(f"Vendedor: {produto['vendedorNome']} (CPF: {produto['vendedorCpf']})\n")
        else:
            print("Nenhum produto encontrado.")


def readCompra():
    print("\nRead - Compras\n")

    with driver.session() as session:
        result = session.run(
            """
            MATCH (u:Usuario)-[c:COMPRA]->(p:Produto)-[:VENDIDO_POR]->(v:Vendedor)
            RETURN u.nome AS clienteNome, u.cpf AS clienteCpf, p.nome AS produtoNome, c.quantidade AS quantidade, c.precoTotal AS precoTotal, v.nome AS vendedorNome, v.cpf AS vendedorCpf
            """
        )

        compras = result.data()
        if compras:
            for compra in compras:
                print(f"Cliente: {compra['clienteNome']} (CPF: {compra['clienteCpf']})")
                print(f"Produto: {compra['produtoNome']}")
                print(f"Quantidade: {compra['quantidade']}")
                print(f"Preço Total: {compra['precoTotal']}")
                print(f"Vendedor: {compra['vendedorNome']} (CPF: {compra['vendedorCpf']})\n")
        else:
            print("Nenhuma compra encontrada.")


def readFavoritos():
    print("\nRead - Favoritos\n")
    usuarioCpf = input("CPF do Usuário: ")

    with driver.session() as session:
        usuario = session.run(
            """
            MATCH (u:Usuario {cpf: $cpf}) RETURN u
            """,
            cpf=usuarioCpf
        ).single()

        if usuario:
            favoritos = session.run(
                """
                MATCH (u:Usuario {cpf: $cpf})-[:FAVORITA]->(p:Produto) RETURN p
                """,
                cpf=usuarioCpf
            ).data()
            if favoritos:
                print("Favoritos do usuário:")
                for favorito in favoritos:
                    print(favorito['p'])
            else:
                print("Usuário não tem produtos favoritos.")
        else:
            print("Usuário não encontrado.")
