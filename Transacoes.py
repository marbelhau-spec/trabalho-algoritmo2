# Classe Transacoes

from Arv_Bin import inserir, buscar, em_ordem, remover
from Cat_gastos import buscar_cat_gastos
from Contas_banc import buscar_contas_banc, atualizar_saldo_conta
from Bancos import buscar_bancos

ARQ_TRANS = "dados/transacoes.dat"


def nome_operacao(operacao):

    if operacao == "1":
        return "Crédito"

    if operacao == "2":
        return "Débito"

    return "(inválida)"


class Transacoes:

    def __init__(self, cod_trans, cod_cat, cod_conta, data, valor, debito_credito):
        self.cod_trans = cod_trans
        self.cod_cat = cod_cat
        self.cod_conta = cod_conta
        self.data = data
        self.valor = valor
        self.debito_credito = debito_credito


def data_para_numero(data):

    partes = data.strip().split("/")

    if len(partes) != 3:
        return None

    dia = partes[0].strip()
    mes = partes[1].strip()
    ano = partes[2].strip()

    if not (dia.isdigit() and mes.isdigit() and ano.isdigit()):
        return None

    if len(dia) != 2 or len(mes) != 2 or len(ano) != 4:
        return None

    if int(dia) < 1 or int(dia) > 31:
        return None

    if int(mes) < 1 or int(mes) > 12:
        return None

    return ano + mes + dia

def montar_transacao(linha):

    dados = linha.strip().split("|")

    return Transacoes(
        int(dados[0]),
        int(dados[1]),
        int(dados[2]),
        dados[3],
        float(dados[4]),
        dados[5]
    )


def carregar_trans():

    raiz = None

    try:

        with open(ARQ_TRANS, "r") as arquivo:

            posicao = arquivo.tell()
            linha = arquivo.readline()

            while linha:

                if linha.strip() and not linha.startswith("*"):

                    transacao = montar_transacao(linha)

                    raiz = inserir(raiz, transacao.cod_trans, posicao)

                posicao = arquivo.tell()
                linha = arquivo.readline()

    except FileNotFoundError:

        pass

    return raiz


def incluir_trans(raiz, raiz_cat, raiz_conta, raiz_banco):
    cod_trans = int(input("Código da transação: "))

    if buscar(raiz, cod_trans) is not None:

        print("\nTransação já existente!")

        return raiz, raiz_conta

    cod_cat = int(input("Código da categoria de gastos: "))

    cat_gastos = buscar_cat_gastos(raiz_cat, cod_cat)

    if cat_gastos is None:

        print("\nCategoria de gastos não cadastrada!")

        return raiz, raiz_conta

    print("Categoria: ", cat_gastos.descricao)

    cod_conta = int(input("Código da conta bancária: "))

    conta = buscar_contas_banc(raiz_conta, cod_conta)

    if conta is None:

        print("\nConta não cadastrada!")

        return raiz, raiz_conta

    banco = buscar_bancos(raiz_banco, conta.cod_banco)

    if banco is not None:
        print("Banco: ", banco.descricao)
    else:
        print("Banco não encontrado!")

    data = input("Data (dd/mm/aaaa): ")

    if data_para_numero(data) is None:

        print("\nData inválida! Use o formato dd/mm/aaaa.")

        return raiz, raiz_conta

    valor = float(input("Valor: "))

    if valor <= 0:

        print("\nO valor deve ser maior que zero!")

        return raiz, raiz_conta

    debito_credito = input("Digite 1 para Crédito ou 2 para Débito: ")

    if debito_credito != "1" and debito_credito != "2":

        print("\nOpção inválida!!")

        return raiz, raiz_conta

    transacoes = Transacoes(cod_trans, cod_cat, cod_conta, data, valor, debito_credito)

    with open(ARQ_TRANS, "a") as arquivo:

        arquivo.seek(0, 2)

        posicao = arquivo.tell()

        arquivo.write(
            f"{transacoes.cod_trans}|"
            f"{transacoes.cod_cat}|"
            f"{transacoes.cod_conta}|"
            f"{transacoes.data}|"
            f"{transacoes.valor}|"
            f"{transacoes.debito_credito}\n"
        )

    raiz = inserir(raiz, cod_trans, posicao)

    print("\nTransação cadastrada com sucesso!")

    raiz_conta = atualizar_saldo_conta(
        raiz_conta,
        cod_conta,
        valor,
        debito_credito
    )

    return raiz, raiz_conta

def buscar_transacao(raiz_trans, raiz_cat, raiz_contas, raiz_bancos):

    cod_trans = int(input("\nCódigo da transação: "))

    posicao = buscar(raiz_trans, cod_trans)

    if posicao is None:

        print("\nTransação não encontrada!")

        return

    with open(ARQ_TRANS, "r") as arquivo:

        arquivo.seek(posicao)

        linha = arquivo.readline()

    transacao = montar_transacao(linha)

    mostrar_transacoes(transacao, raiz_cat, raiz_contas, raiz_bancos)

def trans_periodo(raiz_trans, raiz_cat, raiz_contas, raiz_bancos):

    data_inicial = input("Data inicial (dd/mm/aaaa): ")
    data_final = input("Data final (dd/mm/aaaa): ")

    inicio = data_para_numero(data_inicial)
    fim = data_para_numero(data_final)

    if inicio is None or fim is None:

        print("\nData inválida! Use o formato dd/mm/aaaa.")

        return

    if inicio > fim:

        inicio, fim = fim, inicio

        data_inicial, data_final = data_final, data_inicial

    posicoes = em_ordem(raiz_trans, [])

    print("\n" + "=" * 66)
    print(f"TRANSAÇÕES DE {data_inicial} ATÉ {data_final}".center(66))
    print("=" * 66)

    print(
        f"{'Cód':>5} "
        f"{'Data':<11} "
        f"{'Categoria':<14} "
        f"{'Banco':<12} "
        f"{'Operação':<9} "
        f"{'Valor':>10}"
    )

    print("-" * 66)

    total_credito = 0.0
    total_debito = 0.0
    encontradas = 0

    try:

        with open(ARQ_TRANS, "r") as arquivo:

            for posicao in posicoes:

                arquivo.seek(posicao)

                linha = arquivo.readline()

                if not linha.strip():
                    continue

                transacao = montar_transacao(linha)

                data = data_para_numero(transacao.data)

                if data is None:
                    continue

                if data < inicio or data > fim:
                    continue

                categoria = buscar_cat_gastos(raiz_cat, transacao.cod_cat)

                if categoria is not None:
                    descricao = categoria.descricao
                else:
                    descricao = "(não encontrada)"

                conta = buscar_contas_banc(raiz_contas, transacao.cod_conta)

                nome_banco = "(não encontrado)"

                if conta is not None:

                    banco = buscar_bancos(raiz_bancos, conta.cod_banco)

                    if banco is not None:
                        nome_banco = banco.descricao

                print(
                    f"{transacao.cod_trans:>5} "
                    f"{transacao.data:<11} "
                    f"{descricao[:14]:<14} "
                    f"{nome_banco[:12]:<12} "
                    f"{nome_operacao(transacao.debito_credito):<9} "
                    f"{transacao.valor:>10.2f}"
                )

                if transacao.debito_credito == "1":
                    total_credito = total_credito + transacao.valor
                else:
                    total_debito = total_debito + transacao.valor

                encontradas = encontradas + 1

    except FileNotFoundError:

        pass

    print("-" * 66)

    if encontradas == 0:

        print("Nenhuma transação encontrada nesse período.")

        print("=" * 66)

        return

    print(f"Transações no período: {encontradas}")
    print(f"Total de créditos:  {total_credito:>12.2f}")
    print(f"Total de débitos:   {total_debito:>12.2f}")
    print(f"SALDO DO PERÍODO:   {total_credito - total_debito:>12.2f}")
    print("=" * 66)


def excluir_trans(raiz_trans, raiz_contas):

    print("\n- EXCLUSÃO DE TRANSAÇÃO -")

    cod_trans = int(input("Código da transação: "))

    posicao = buscar(raiz_trans, cod_trans)

    if posicao is None:

        print("\nTransação não encontrada!")

        return raiz_trans

    confirma = input("Confirma a exclusão? (S/N): ")

    if confirma.strip().upper() != "S":

        print("\nExclusão cancelada.")

        return raiz_trans

    with open(ARQ_TRANS, "r+") as arquivo:

        arquivo.seek(posicao)

        linha = arquivo.readline()

        arquivo.seek(posicao)

        transacao = montar_transacao(linha)

        if transacao.debito_credito == "1":
            raiz_contas = atualizar_saldo_conta(raiz_contas, transacao.cod_conta, transacao.valor, "2")
        elif transacao.debito_credito == "2":
            raiz_contas = atualizar_saldo_conta(raiz_contas, transacao.cod_conta, transacao.valor, "1")

        arquivo.write("*" + linha)

    raiz_trans = remover(raiz_trans, cod_trans)

    print("\nTransação excluída com sucesso!")

    return raiz_trans


def mostrar_transacoes(transacao, raiz_cat, raiz_contas, raiz_bancos):

    cat_gastos = buscar_cat_gastos(raiz_cat, transacao.cod_cat)

    conta = buscar_contas_banc(raiz_contas, transacao.cod_conta)

    bancos = None

    if conta is not None:

        bancos = buscar_bancos(raiz_bancos, conta.cod_banco)

    print("\n-DADOS DA TRANSAÇÃO-")

    print("Código da transação:", transacao.cod_trans)

    print("Código da categoria:", transacao.cod_cat)

    if cat_gastos is not None:
        print("Categoria de gastos:", cat_gastos.descricao)
    else:
        print("Categoria de gastos não encontrada!!")

    print("Código da conta:", transacao.cod_conta)

    if bancos is not None:
        print("Banco:", bancos.descricao)
    else:
        print("Banco não encontrado!!")

    print("Data:", transacao.data)

    print(f"Valor: {transacao.valor:.2f}")

    print("Operação:", nome_operacao(transacao.debito_credito))