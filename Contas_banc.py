# Classe Contas_banc

from Arv_Bin import inserir, buscar, em_ordem
from Bancos import buscar_bancos
from Pessoa import buscar_pessoa

ARQ_CONTAS = "dados/contas_banc.dat"


class Contas_banc:

    def __init__(self, cod_conta, cod_banco, cod_pessoa, descricao, saldo):
        self.cod_conta = cod_conta
        self.cod_banco = cod_banco
        self.cod_pessoa = cod_pessoa
        self.descricao = descricao
        self.saldo = saldo


def linha_conta(conta):

    return (
        f"{conta.cod_conta}|"
        f"{conta.cod_banco}|"
        f"{conta.cod_pessoa}|"
        f"{conta.descricao}|"
        f"{conta.saldo}\n"
    )


def montar_conta(linha):

    dados = linha.strip().split("|")

    return Contas_banc(
        int(dados[0]),
        int(dados[1]),
        int(dados[2]),
        dados[3],
        float(dados[4])
    )


def carregar_contas():
    raiz = None

    try:

        with open(ARQ_CONTAS, "r") as arquivo:

            posicao = arquivo.tell()
            linha = arquivo.readline()

            while linha:

                if linha.strip() and not linha.startswith("*"):

                    conta = montar_conta(linha)

                    raiz = inserir(raiz, conta.cod_conta, posicao)

                posicao = arquivo.tell()
                linha = arquivo.readline()

    except FileNotFoundError:

        pass

    return raiz


def incluir_contas_banc(raiz, raiz_banco, raiz_pessoa):

    cod_conta = int(input("Código da conta: "))

    if buscar(raiz, cod_conta) is not None:

        print("\nConta já existente!!")

        return raiz

    cod_banco = int(input("Código do banco: "))

    banco = buscar_bancos(raiz_banco, cod_banco)

    if banco is None:

        print("\nBanco não cadastrado!")

        return raiz

    print("Banco: ", banco.descricao)

    cod_pessoa = int(input("Código da pessoa: "))

    pessoa = buscar_pessoa(raiz_pessoa, cod_pessoa)

    if pessoa is None:

        print("\nPessoa não cadastrada!")

        return raiz

    print("Pessoa: ", pessoa.nome)

    descricao = input("Descrição da conta: ")

    saldo = float(input("Saldo: "))

    contas_banc = Contas_banc(cod_conta, cod_banco, cod_pessoa, descricao, saldo)

    with open(ARQ_CONTAS, "a") as arquivo:

        arquivo.seek(0, 2)

        posicao = arquivo.tell()

        arquivo.write(linha_conta(contas_banc))

    raiz = inserir(raiz, cod_conta, posicao)

    print("\nConta Bancária cadastrada com sucesso!")

    return raiz


def buscar_contas_banc(raiz, cod):

    posicao = buscar(raiz, cod)

    if posicao is None:
        return None

    try:

        with open(ARQ_CONTAS, "r") as arquivo:

            arquivo.seek(posicao)

            linha = arquivo.readline()

    except FileNotFoundError:

        return None

    return montar_conta(linha)


def atualizar_saldo_conta(raiz_contas, cod_conta, valor, operacao):

    if buscar(raiz_contas, cod_conta) is None:

        print("\nConta não encontrada! O saldo não foi alterado.")

        return raiz_contas

    linhas = []

    try:

        with open(ARQ_CONTAS, "r") as arquivo:

            linha = arquivo.readline()

            while linha:

                if linha.strip():

                    if not linha.startswith("*"):

                        conta = montar_conta(linha)

                        if conta.cod_conta == cod_conta:

                            if operacao == "1":

                                conta.saldo = conta.saldo + valor

                            elif operacao == "2":

                                conta.saldo = conta.saldo - valor

                            else:

                                print("\nOperação inválida!")

                                return raiz_contas

                            linha = linha_conta(conta)

                    linhas.append(linha)

                linha = arquivo.readline()

    except FileNotFoundError:

        print("\nArquivo de contas não encontrado!")

        return raiz_contas

    with open(ARQ_CONTAS, "w") as arquivo:

        for linha in linhas:

            arquivo.write(linha)

    print("\nSaldo da conta atualizado!")

    return carregar_contas()


def saldos_das_contas(raiz_contas, raiz_bancos, raiz_pessoas):

    posicoes = em_ordem(raiz_contas, [])

    print("\n" + "=" * 65)
    print("SALDOS DE TODAS AS CONTAS".center(65))
    print("=" * 65)

    print(
        f"{'Cód':>5} "
        f"{'Banco':<14} "
        f"{'Pessoa':<14} "
        f"{'Descrição':<16} "
        f"{'Saldo':>12}"
    )

    print("-" * 65)

    saldo_geral = 0.0
    contas = 0

    try:

        with open(ARQ_CONTAS, "r") as arquivo:

            for posicao in posicoes:

                arquivo.seek(posicao)

                linha = arquivo.readline()

                if not linha.strip():
                    continue

                conta = montar_conta(linha)

                banco = buscar_bancos(raiz_bancos, conta.cod_banco)

                if banco is not None:
                    nome_banco = banco.descricao
                else:
                    nome_banco = "(não encontrado)"

                pessoa = buscar_pessoa(raiz_pessoas, conta.cod_pessoa)

                if pessoa is not None:
                    nome_pessoa = pessoa.nome
                else:
                    nome_pessoa = "(não encontrada)"

                print(
                    f"{conta.cod_conta:>5} "
                    f"{nome_banco[:14]:<14} "
                    f"{nome_pessoa[:14]:<14} "
                    f"{conta.descricao[:16]:<16} "
                    f"{conta.saldo:>12.2f}"
                )

                saldo_geral = saldo_geral + conta.saldo

                contas = contas + 1

    except FileNotFoundError:

        pass

    print("-" * 65)

    if contas == 0:

        print("Nenhuma conta cadastrada.")

        print("=" * 65)

        return

    print(f"Contas cadastradas: {contas}")
    print(f"{'SALDO GERAL:':>52} {saldo_geral:>12.2f}")
    print("=" * 65)


def mostrar_conta(conta, raiz_bancos, raiz_pessoas):

    banco = buscar_bancos(raiz_bancos, conta.cod_banco)

    pessoa = buscar_pessoa(raiz_pessoas, conta.cod_pessoa)

    print("\n-DADOS DA CONTA BANCÁRIA-")

    print("Código da conta: ", conta.cod_conta)

    if banco is not None:
        print("Banco: ", banco.descricao)
    else:
        print("Banco não encontrado!!")

    if pessoa is not None:
        print("Pessoa: ", pessoa.nome)
    else:
        print("Pessoa não encontrada!!")

    print("Descrição: ", conta.descricao)
    print(f"Saldo:  {conta.saldo:.2f}")
