def casoElastoplastico():
    F2 = (p * (a + b + c) * L1 * (a + b) * A2 * E2) / (a ** 2 * L2 * A1 * E1 + (a + b) ** 2 * L1 * A2 * E2)
    F1 = (p * (a + b + c) - F2 * (a + b)) / a
    S1 = F1 / A1
    S2 = F2 / A2
    d = (a + b + c) * (((F1 * L1) / (A1 * E1)) / a)
    return F1, F2, S1, S2, d

def casoPlastico(limitante):
    if limitante == 'S1':
        F1 = Sy1 * A1
        F2 = (p * (a + b + c) - F1 * a) / (a + b)
        S1 = Sy1
        S2 = F2 / A2
        d = (((F2 * L2) / (A2 * E2)) * (a + b + c)) / (a + b)
    elif limitante == 'S2':
        F2 = Sy2 * A2
        F1 = (p * (a + b + c) - F2 * (a + b)) / a
        S1 = F1 / A1
        S2 = Sy2
        d = (((F1 * L1) / (A1 * E1)) * (a + b + c)) / a
    return F1, F2, S1, S2, d

with open('entrada.txt') as arquivo:
    P, a, b, c, L1, L2, A1, A2, E1, E2, Sy1, Sy2, n \
        = [float(linha) for linha in arquivo]

with open('saida.txt', 'w') as arquivo:
    strFormat = f'>{len(str(int(P))) + 4}'
    floatFormat = f'{strFormat}.3f'
    arquivo.write(f'{"P":{strFormat}}  {"F1":{strFormat}}  {"F2":{strFormat}} \
        {"S1":{strFormat}}  {"S2":{strFormat}}  {"L":{strFormat}}\n')

    regimeElastoplastico = True
    for p in range(0, int(P + 1), int(P / n)):

        if regimeElastoplastico:
            F1, F2, S1, S2, d = casoElastoplastico()

        if S1 >= Sy1:
            regimeElastoplastico = False
            F1, F2, S1, S2, d = casoPlastico(limitante='S1')
            if S2 > Sy2:
                arquivo.write(f'A viga não é capaz de suportar p = {p}\n')
                break

        elif S2 >= Sy2:
            regimeElastoplastico = False
            F1, F2, S1, S2, d = casoPlastico(limitante='S2')
            if S1 > Sy1:
                arquivo.write(f'A viga não é capaz de suportar p = {p}\n')
                break

        arquivo.write(f'{p:{floatFormat}} {F1:{floatFormat}} {F2:{floatFormat}} \
            {S1:{floatFormat}} {S2:{floatFormat}} {d:{floatFormat}}\n')
