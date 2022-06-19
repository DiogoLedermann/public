from math import log


def unbreakable_float(prompt=''):
    """
    Previne que o programa quebre caso o usuário insira uma entrada inválida.
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
    Previne que o programa quebre caso o usuário insira uma entrada inválida.
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
    Recebe os dados de entrada.
    """
    e = unbreakable_float('Digite a tolerância dos critérios de parada: ')
    n = unbreakable_int('Digite o número máximo de iterações: ')
    x = unbreakable_float('Digite a aproximação inicial: ')
    return e, n, x


def f(x):
    """
    Função dada.
    :param x: argumento da função.
    :return: valor da função no ponto x.
    """
    return x * log(x, 10) - 1


def g(x):
    """
    Derivada da funcão dada f.
    :param x: argumento da função.
    :return: valor da derivada no ponto x.
    """
    return log(x, 10) + 1


def criterio_de_parada1(e, x1, x0):
    """
    Testa se a precisão desejada foi atingida.
    :param e: tolerância.
    :param x1: aproximação na iteração i+1.
    :param x0: aproximação na iteração i.
    :return: True se a condição for verificada, False caso contrário.
    """
    if x1 == 0:
        if abs(x1 - x0) <= e and abs(f(x1)) <= e:
            return True
        else:
            return False

    else:
        if abs(x1 - x0) / abs(x1) <= e and abs(f(x1)) <= e:
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


def gera_aproximacoes(e, max_i, x0, arquivo):
    """
    Gera um arquivo contendo os dados de entrada, a aproximação da raiz e sua precisão a cada iteração.
    :param e: tolerância.
    :param max_i: número máximo de iterações.
    :param x0: aproximação inicial.
    :param arquivo: arquivo texto onde será registrado o resultado.
    """
    i = 0
    while True:
        i += 1
        x1 = x0 - f(x0) / g(x0)

        if x1 == 0:
            precisao = abs(x1 - x0)
        else:
            precisao = abs(x1 - x0) / abs(x1)

        arquivo.write(f'i = {i}\n')
        arquivo.write(f'x = {x1}\n')
        arquivo.write(f'f(x) = {f(x1)}\n')
        arquivo.write(f'Precisão = {precisao}\n')
        arquivo.write('\n')

        if criterio_de_parada1(e, x1, x0) is True:
            arquivo.write(f'Precisão desejada atingida! ')
            break

        if criterio_de_parada2(i, max_i) is True:
            arquivo.write(f'Número máximo de iterações atingido! ')
            break

        x0 = x1  # Atualiza a aproximação de x para a próxima iteração


def metodo_de_newton_raphson():
    """
    Chamada das funções.
    """
    epsilon, numero_max_de_iteracoes, aproximacao_inicial = dados_de_entrada()
    with open("arquivo_de_resultados.txt", "w+") as arquivo:
        arquivo.write(f'Tolerância: {epsilon}\n')
        arquivo.write(f'Número máximo de iterações: {numero_max_de_iteracoes}\n')
        arquivo.write(f'Aproximação inicial: {aproximacao_inicial}\n')
        arquivo.write('\n')
        gera_aproximacoes(epsilon, numero_max_de_iteracoes, aproximacao_inicial, arquivo)


metodo_de_newton_raphson()
