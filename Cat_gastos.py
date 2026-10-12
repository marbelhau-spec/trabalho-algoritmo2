# Classe Cat_gastos

from Arv_Bin import inserir, buscar

ARQ_CAT = "dados/cat_gastos.dat"


class Cat_gastos:

    def __init__(self, cod_cat, descricao):
        self.cod_cat = cod_cat
        self.descricao = descricao


def montar_cat_gastos(linha):

    dados = linha.strip().split("|")

    return Cat_gastos(
        int(dados[0]),
        dados[1].strip()
    )


def carregar_cat_gastos():

    raiz = None

    try:

        with open(ARQ_CAT, "r") as arquivo:

            posicao = arquivo.tell()
            linha = arquivo.readline()

            while linha:

                if linha.strip() and not linha.startswith("*"):

                    cat_gastos = montar_cat_gastos(linha)

                    raiz = inserir(raiz, cat_gastos.cod_cat, posicao)

                posicao = arquivo.tell()
                linha = arquivo.readline()

    except FileNotFoundError:

        pass

    return raiz


def incluir_cat_gastos(raiz):

    cod_cat = int(input("Código da categoria de gastos: "))

    if buscar(raiz, cod_cat) is not None:

        print("\nCategoria de gastos já cadastrada!")

        return raiz

    descricao = input("Descrição: ")

    cat_gastos = Cat_gastos(cod_cat, descricao)

    with open(ARQ_CAT, "a") as arquivo:

        arquivo.seek(0, 2)

        posicao = arquivo.tell()

        arquivo.write(
            f"{cat_gastos.cod_cat}|{cat_gastos.descricao}\n"
        )

    raiz = inserir(raiz, cod_cat, posicao)

    print("\nCategoria de gastos cadastrada com sucesso!")

    return raiz


def buscar_cat_gastos(raiz, cod):

    posicao = buscar(raiz, cod)

    if posicao is None:
        return None

    try:

        with open(ARQ_CAT, "r") as arquivo:

            arquivo.seek(posicao)

            linha = arquivo.readline()

    except FileNotFoundError:

        return None

    return montar_cat_gastos(linha)


def mostrar_cat_gastos(cat_gastos):

    print("\n-DADOS DA CATEGORIA DE GASTOS-")
    print("Código da categoria:", cat_gastos.cod_cat)
    print("Descrição:", cat_gastos.descricao)
