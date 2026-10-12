# main

import os

from Pessoa import (
    carregar_pessoas,
    incluir_pessoa,
    buscar_pessoa,
    mostrar_pessoa
)

from Cat_gastos import (
    carregar_cat_gastos,
    incluir_cat_gastos,
    buscar_cat_gastos,
    mostrar_cat_gastos
)

from Bancos import (
    carregar_bancos,
    incluir_bancos,
    buscar_bancos,
    mostrar_bancos
)

from Contas_banc import (
    carregar_contas,
    incluir_contas_banc,
    buscar_contas_banc,
    mostrar_conta,
    saldos_das_contas
)

from Transacoes import (
    carregar_trans,
    incluir_trans,
    trans_periodo,
    excluir_trans,
    buscar_transacao
)


def menu():

    print("\n" + "=" * 45)
    print("CONTROLE FINANCEIRO".center(45))
    print("=" * 45)

    print("\n--- CADASTROS ---")
    print(" 1 - Incluir Pessoa")
    print(" 2 - Incluir Categoria de Gastos")
    print(" 3 - Incluir Banco")
    print(" 4 - Incluir Conta Bancária")

    print("\n--- TRANSAÇÕES ---")
    print(" 5 - Lançar Transação")
    print(" 6 - Consultar Transação")
    print(" 7 - Transações por Período")
    print(" 8 - Excluir Transação")

    print("\n--- CONSULTAS E RELATÓRIOS ---")
    print(" 9 - Consultar Pessoa")
    print("10 - Consultar Categoria de Gastos")
    print("11 - Consultar Banco")
    print("12 - Consultar Conta Bancária")
    print("13 - Saldos de Todas as Contas")

    print("\n 0 - Sair")
    print("=" * 45)

def principal():

    if not os.path.exists("dados"):
        os.makedirs("dados")

    raiz_pessoas = carregar_pessoas()
    raiz_cat = carregar_cat_gastos()
    raiz_bancos = carregar_bancos()
    raiz_contas = carregar_contas()
    raiz_trans = carregar_trans()

    while True:

        menu()

        opcao = input("Opção: ").strip()

        try:

            if opcao == "1":

                raiz_pessoas = incluir_pessoa(raiz_pessoas)

            elif opcao == "2":

                raiz_cat = incluir_cat_gastos(raiz_cat)

            elif opcao == "3":

                raiz_bancos = incluir_bancos(raiz_bancos)

            elif opcao == "4":

                raiz_contas = incluir_contas_banc(
                    raiz_contas,
                    raiz_bancos,
                    raiz_pessoas
                )

            elif opcao == "5":

                raiz_trans, raiz_contas = incluir_trans(
                    raiz_trans,
                    raiz_cat,
                    raiz_contas,
                    raiz_bancos
                )

            elif opcao == "6":

                buscar_transacao(
                    raiz_trans,
                    raiz_cat,
                    raiz_contas,
                    raiz_bancos
                )

            elif opcao == "7":

                trans_periodo(
                    raiz_trans,
                    raiz_cat,
                    raiz_contas,
                    raiz_bancos
                )

            elif opcao == "8":

                raiz_trans = excluir_trans(raiz_trans, raiz_contas)

            elif opcao == "9":

                cod = int(input("\nCódigo da pessoa: "))

                pessoa = buscar_pessoa(raiz_pessoas, cod)

                if pessoa is None:
                    print("\nPessoa não encontrada!")
                else:
                    mostrar_pessoa(pessoa)

            elif opcao == "10":

                cod = int(input("\nCódigo da categoria: "))

                categoria = buscar_cat_gastos(raiz_cat, cod)

                if categoria is None:
                    print("\nCategoria não encontrada!")
                else:
                    mostrar_cat_gastos(categoria)

            elif opcao == "11":

                cod = int(input("\nCódigo do banco: "))

                banco = buscar_bancos(raiz_bancos, cod)

                if banco is None:
                    print("\nBanco não encontrado!")
                else:
                    mostrar_bancos(banco)

            elif opcao == "12":

                cod = int(input("\nCódigo da conta: "))

                conta = buscar_contas_banc(raiz_contas, cod)

                if conta is None:
                    print("\nConta não encontrada!")
                else:
                    mostrar_conta(conta, raiz_bancos, raiz_pessoas)

            elif opcao == "13":

                saldos_das_contas(raiz_contas, raiz_bancos, raiz_pessoas)

            elif opcao == "0":

                print("\nEncerrando o programa...")

                break

            else:

                print("\nOpção inválida!")

        except ValueError:

            print("\nValor inválido! Digite apenas números.")

        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    principal()
