# Classe Arv_Bin

class Node:
    def __init__(self, cod, posicao):
        self.cod = cod
        self.posicao = posicao
        self.esquerda = None
        self.direita = None


def inserir(raiz, cod, posicao):

    novo = Node(cod, posicao)

    if raiz is None:
        return novo

    atual = raiz

    while True:

        if cod < atual.cod:

            if atual.esquerda is None:
                atual.esquerda = novo
                break

            atual = atual.esquerda

        else:

            if atual.direita is None:
                atual.direita = novo
                break

            atual = atual.direita

    return raiz


def buscar(raiz, codigo):

    atual = raiz

    while atual is not None:

        if codigo == atual.cod:
            return atual.posicao

        if codigo < atual.cod:
            atual = atual.esquerda
        else:
            atual = atual.direita

    return None


def em_ordem(raiz, posicoes):

    if raiz is not None:

        em_ordem(raiz.esquerda, posicoes)

        posicoes.append(raiz.posicao)

        em_ordem(raiz.direita, posicoes)

    return posicoes


def remover(raiz, cod):

    if raiz is None:
        return None

    if cod < raiz.cod:

        raiz.esquerda = remover(raiz.esquerda, cod)

    elif cod > raiz.cod:

        raiz.direita = remover(raiz.direita, cod)

    else:
        if raiz.esquerda is None and raiz.direita is None:
            return None

        if raiz.esquerda is None:
            return raiz.direita

        if raiz.direita is None:
            return raiz.esquerda

        sucessor = raiz.direita

        while sucessor.esquerda is not None:
            sucessor = sucessor.esquerda

        raiz.cod = sucessor.cod
        raiz.posicao = sucessor.posicao

        raiz.direita = remover(raiz.direita, sucessor.cod)

    return raiz

