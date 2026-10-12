# Classe Bancos

from Arv_Bin import inserir, buscar

ARQ_BANCOS = "dados/bancos.dat"


class Bancos:

    def __init__(self, cod_banco, descricao):
        self.cod_banco = cod_banco
        self.descricao = descricao


def montar_banco(linha):

    dados = linha.strip().split("|")

    return Bancos(
        int(dados[0]),
        dados[1].strip()
    )


def carregar_bancos():

    raiz = None

    try:

        with open(ARQ_BANCOS, "r") as arquivo:

            posicao = arquivo.tell()
            linha = arquivo.readline()

            while linha:

                if linha.strip() and not linha.startswith("*"):

                    banco = montar_banco(linha)

                    raiz = inserir(raiz, banco.cod_banco, posicao)

                posicao = arquivo.tell()
                linha = arquivo.readline()

    except FileNotFoundError:

        pass

    return raiz


def incluir_bancos(raiz):

    cod_banco = int(input("Código do banco: "))

    if buscar(raiz, cod_banco) is not None:

        print("\nBanco já cadastrado!")

        return raiz

    descricao = input("Descrição: ")

    bancos = Bancos(cod_banco, descricao)

    with open(ARQ_BANCOS, "a") as arquivo:

        arquivo.seek(0, 2)

        posicao = arquivo.tell()

        arquivo.write(
            f"{bancos.cod_banco}|{bancos.descricao}\n"
        )

    raiz = inserir(raiz, cod_banco, posicao)

    print("\nBanco cadastrado com sucesso!")

    return raiz


def buscar_bancos(raiz, cod):

    posicao = buscar(raiz, cod)

    if posicao is None:
        return None

    try:

        with open(ARQ_BANCOS, "r") as arquivo:

            arquivo.seek(posicao)

            linha = arquivo.readline()

    except FileNotFoundError:

        return None

    return montar_banco(linha)


def mostrar_bancos(bancos):

    print("\n-DADOS DO BANCO-")
    print("Código do banco:", bancos.cod_banco)
    print("Descrição:", bancos.descricao)
