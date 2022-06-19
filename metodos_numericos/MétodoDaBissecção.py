from math import log


def unbreakable_float(prompt=''):
    """
    Lê um número de ponto flutuante e previne que o programa quebre caso o usuário insira uma entrada inválida.
    :param prompt: mensagem que aparece no prompt.
    """
    while True:
        try:
            n = float(input(prompt))
            return n
        except ValueError:
            print('Entrada inválida!')


def unbreakable_int(prompt=''):
    """
    Lê um número inteiro e previne que o programa quebre caso o usuário insira uma entrada inválida.
    :param prompt: mensagem que aparece no prompt.
    """
    while True:
        try:
            n = int(input(prompt))
            return n
        except ValueError:
            print('Entrada inválida!')


def dados_de_entrada():
    """
    :return: dados de entrada.
    """
    e = unbreakable_float('Digite a tolerância dos critérios de parada: ')
    n = unbreakable_int('Digite o número máximo de iterações: ')
    a = unbreakable_float('Digite o limite inferior do intervalo: ')
    b = unbreakable_float('Digite o limite superior do intervalo: ')
    return e, n, a, b


def f(x):
    """
    Função dada.
    :param x: argumento da função.
    :return: valor da função no ponto x.
    """
    return x * log(x, 10) - 1


def criterio_de_parada1(e, a, b, x):
    """
    Testa se a precisão desejada foi atingida.
    :param e: tolerância.
    :param a: limite inferior do intervalo.
    :param b: limite superior do intervalo.
    :param x: aproximação atual da raiz.
    :return: True se a condição for verificada, False caso contrário.
    """
    if x == 0:
        if b - a <= e and abs(f(x)) <= e:
            return True
        else:
            return False

    else:
        if (b - a) / abs(x) <= e and abs(f(x)) <= e:
            return True
        else:
            return False


def criterio_de_parada2(i, max_i):
    """
    Testa se o número máximo de iterações foi atingido.
    :param i: iteração atual.
    :param max_i: número máximo de iterações.
    :return: True se a condição for verificada, False caso contrário.
    """
    if i > max_i:
        return True
    else:
        return False


def gera_aproximacoes(e, max_i, a, b, arquivo):
    """
    Gera um arquivo contendo os dados de entrada, a aproximação da raiz e sua precisão a cada iteração.
    :param e: tolerância.
    :param max_i: número máximo de iterações.
    :param a: limite inferior do intervalo.
    :param b: limite superior do intervalo.
    :param arquivo: arquivo texto onde será registrado o resultado.
    """
    i = 0
    while True:
        i += 1
        x = (b + a) / 2

        if x == 0:
            precisao = b - a
        else:
            precisao = (b - a) / abs(x)

        arquivo.write(f'i = {i}\n')
        arquivo.write(f'x = {x}\n')
        arquivo.write(f'f(x) = {f(x)}\n')
        arquivo.write(f'Precisão = {precisao}\n')
        arquivo.write('\n')

        if criterio_de_parada1(e, a, b, x) is True:
            arquivo.write(f'Precisão desejada atingida! ')
            break

        if criterio_de_parada2(i, max_i) is True:
            arquivo.write(f'Número máximo de iterações atingido! ')
            break

        # Atualiza os limites do intervalo para a próxima iteração
        if f(a) * f(x) < 0:
            b = x
        else:
            a = x


def metodo_da_bissecao():
    """
    Chamada das funções.
    """
    epsilon, numero_max_de_iteracoes, limite_inferior, limite_superior = dados_de_entrada()
    with open("arquivo_de_resultados.txt", "w+", encoding='utf-8') as arquivo:
        arquivo.write(f'Tolerância: {epsilon}\n')
        arquivo.write(f'Número máximo de iterações: {numero_max_de_iteracoes}\n')
        arquivo.write(f'Intervalo inicial: [{limite_inferior} ; {limite_superior}]\n')
        arquivo.write('\n')
        gera_aproximacoes(epsilon, numero_max_de_iteracoes, limite_inferior, limite_superior, arquivo)


metodo_da_bissecao()
