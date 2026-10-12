# Classe Pessoa

from Arv_Bin import inserir, buscar

ARQ_PESSOAS = "dados/pessoas.dat"


class Pessoa:

    def __init__(self, cod, nome):
        self.cod = cod
        self.nome = nome


def montar_pessoa(linha):

    dados = linha.strip().split("|")

    return Pessoa(
        int(dados[0]),
        dados[1].strip()
    )


def carregar_pessoas():

    raiz = None

    try:

        with open(ARQ_PESSOAS, "r") as arquivo:

            posicao = arquivo.tell()
            linha = arquivo.readline()

            while linha:

                if linha.strip() and not linha.startswith("*"):

                    pessoa = montar_pessoa(linha)

                    raiz = inserir(raiz, pessoa.cod, posicao)

                posicao = arquivo.tell()
                linha = arquivo.readline()

    except FileNotFoundError:

        pass

    return raiz


def incluir_pessoa(raiz):

    cod = int(input("Código da pessoa: "))

    if buscar(raiz, cod) is not None:

        print("\nPessoa já cadastrada!")

        return raiz

    nome = input("Nome da pessoa: ")

    pessoa = Pessoa(cod, nome)

    with open(ARQ_PESSOAS, "a") as arquivo:

        arquivo.seek(0, 2)

        posicao = arquivo.tell()

        arquivo.write(
            f"{pessoa.cod}|{pessoa.nome}\n"
        )

    raiz = inserir(raiz, cod, posicao)

    print("\nPessoa cadastrada com sucesso!")

    return raiz


def buscar_pessoa(raiz, cod):

    posicao = buscar(raiz, cod)

    if posicao is None:
        return None

    try:

        with open(ARQ_PESSOAS, "r") as arquivo:

            arquivo.seek(posicao)

            linha = arquivo.readline()

    except FileNotFoundError:

        return None

    return montar_pessoa(linha)


def mostrar_pessoa(pessoa):

    print("\n-DADOS DA PESSOA-")
    print("Código da pessoa:", pessoa.cod)
    print("Nome:", pessoa.nome)
