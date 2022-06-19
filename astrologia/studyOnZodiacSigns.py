import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
np.set_printoptions(precision=2, threshold=np.inf, linewidth=np.inf)


def getSigno(dataDeNascimento):

    dia, mes = dataDeNascimento

    if mes == 1:
        return 'Capricórnio' if dia <= 20 else 'Aquário'

    if mes == 2:
        return 'Aquário' if dia <= 18 else 'Peixes'

    if mes == 3:
        return 'Peixes' if dia <= 20 else 'Áries'

    if mes == 4:
        return 'Áries' if dia <= 20 else 'Touro'

    if mes == 5:
        return 'Touro' if dia <= 20 else 'Gêmeos'

    if mes == 6:
        return 'Gêmeos' if dia <= 22 else 'Câncer'

    if mes == 7:
        return 'Câncer' if dia <= 22 else 'Leão'

    if mes == 8:
        return 'Leão' if dia <= 22 else 'Virgem'

    if mes == 9:
        return 'Virgem' if dia <= 22 else 'Libra'

    if mes == 10:
        return 'Libra' if dia <= 22 else 'Escorpião'

    if mes == 11:
        return 'Escorpião' if dia <= 21 else 'Sagitário'

    if mes == 12:
        return 'Sagitário' if dia <= 21 else 'Capricórnio'


def getTestesDePersonalidade(filename, sheet_name):

    planilha = pd.read_excel(filename, sheet_name=sheet_name)
    planilha = planilha.dropna(how='all')
    planilha = planilha.dropna(axis=1, how='all')

    dados = planilha.to_numpy()
    dados = np.delete(dados, 0, axis=1)

    numeroDePessoas = len(dados)

    nomes = dados[:, 0]
    nomes = [nome.split()[0] for nome in nomes]
    nomes = [nome.capitalize() for nome in nomes]

    nascimentos = dados[:, 1]
    nascimentos = [nascimento.date() for nascimento in nascimentos]
    nascimentos = [(nascimento.day, nascimento.month) for nascimento in nascimentos]
    signosPessoais = [getSigno(data) for data in nascimentos]

    respostas = dados[:, 3:]
    for i, respostasPessoais in enumerate(respostas):
        indicesV = [i for i, resposta in enumerate(respostasPessoais) if resposta == 'V']
        indicesF = [i for i, resposta in enumerate(respostasPessoais) if resposta != 'V']
        respostasPessoais[indicesV] = 1
        respostasPessoais[indicesF] = 0

    personalidades = np.reshape(respostas, (numeroDePessoas, 12, 15))

    return nomes, signosPessoais, personalidades


def getPessoasPorSigno(signosPessoais):
    return [signosPessoais.count(signo) for signo in signosExistentes]


def getTaxasDeIdentificacao(pessoas, signosPessoais, personalidades):

    taxasPessoasDoSigno = np.zeros(12)
    taxasControle = np.zeros(12)
    for i, signo in enumerate(signosExistentes):

        repostasPessoasDoSigno = \
            np.array([personalidades[j][i] for j in range(len(pessoas)) if signosPessoais[j] == signo])
        nPessoasDoSigno = len(repostasPessoasDoSigno)
        taxasPessoasDoSigno[i] = repostasPessoasDoSigno.sum() / (nPessoasDoSigno * 15)

        respostasControle = np.array([personalidades[j][i] for j in range(len(pessoas)) if signosPessoais[j] != signo])
        nPessoasControle = len(respostasControle)
        taxasControle[i] = respostasControle.sum() / (nPessoasControle * 15)

    return taxasPessoasDoSigno, taxasControle


def simulacao(nPessoas, taxasControle, influenciaSigno=None):
    
    nomes = ['Adriana', 'Alexandre', 'Ana', 'André', 'Antonio', 'Antônia ', 'Benedito', 'Carlos', 'Cláudio', 'Daniel',
             'Edson', 'Eduardo', 'Fabio', 'Fernando', 'Francisca', 'Francisco', 'Geraldo', 'Joaquim', 'Jorge', 'Josefa',
             'José', 'João', 'Leandro', 'Luciana', 'Luis', 'Luiz', 'Manoel', 'Marcelo', 'Marcos', 'Maria', 'Márcia',
             'Márcio', 'Mário', 'Patrícia', 'Paulo', 'Pedro', 'Rafael', 'Raimunda', 'Raimundo', 'Ricardo', 'Rita',
             'Roberto', 'Rodigo', 'Rosa', 'Sandra', 'Sebastiao', 'Sérgio', 'Sónia', 'Terezinha', 'Vera']
    
    sobrenomes = ['Almeida', 'Alves', 'Andrade', 'Barbosa', 'Barros', 'Batista', 'Borges', 'Campos',
                  'Cardoso', 'Carvalho', 'Castro', 'Costa', 'Dias', 'Duarte', 'Freitas', 'Fernandes', 'Ferreira',
                  'Garcia', 'Gomes', 'Gonçalves', 'Lima', 'Lopes', 'Machado', 'Marques', 'Martins', 'Medeiros',
                  'Melo', 'Mendes', 'Miranda', 'Monteiro', 'Moraes', 'Moereira', 'Moura', 'Nascimento', 'Nunes',
                  'Oliveira', 'Pereira', 'Ramos', 'Reis', 'Ribeiro', 'Rocha', 'Santana', 'Santos', 'Silva', 'Soares',
                  'Souza', 'Teixeira', 'Vieira']

    # noinspection PyUnusedLocal
    pessoas = [f'{np.random.choice(nomes)} {np.random.choice(sobrenomes)} '
               f'{np.random.choice(sobrenomes)} {np.random.choice(sobrenomes)}' for i in range(nPessoas)]

    # noinspection PyUnusedLocal
    signosPessoais = [np.random.choice(signosExistentes) for j in range(nPessoas)]

    pessoasPorSigno = getPessoasPorSigno(signosPessoais)

    personalidades = np.zeros((len(pessoas), 12, 15))
    for i, pessoa in enumerate(pessoas):
        for j, signo in enumerate(signosExistentes):
            
            if influenciaSigno is None:
                taxaDeIdentificacaoSigno = taxasControle[j]
            else:
                taxaDeIdentificacaoControle = taxasControle[j]
                taxaDeIdentificacaoMaxima = 1
                potencial = taxaDeIdentificacaoMaxima - taxaDeIdentificacaoControle
                taxaDeIdentificacaoSigno = taxaDeIdentificacaoControle + ((influenciaSigno / 100) * potencial)

            if signo == signosPessoais[i]:
                personalidades[i][j] = [1 if np.random.random() < taxaDeIdentificacaoSigno else 0 for i in range(15)]
            else:
                personalidades[i][j] = [1 if np.random.random() < taxasControle[j] else 0 for i in range(15)]

    # noinspection PyUnusedLocal
    dados = pessoas, signosPessoais, pessoasPorSigno, personalidades
    
    compatibilidades = getCompatibilidades(pessoas, personalidades)
    taxasSimuladas = getTaxasDeIdentificacao(pessoas, signosPessoais, personalidades)
    palpites = getPalpites(pessoas, compatibilidades)
    acertosPorSigno = getAcertosPorSignos(signosPessoais, palpites)

    resultadosIndividuais = compatibilidades, palpites
    resultadosGerais = taxasPessoasDoSigno, taxasControle, acertosPorSigno

    print(f'\nSimulação: {influencia}% de influencia do signo. Espaço amostral com {nPessoas} pessoas.')
    imprimeResultados(dados, resultadosIndividuais, resultadosGerais, full=False)

    title = f'Taxas de identificação\n' \
            f'(Simulação: {influenciaSigno}% de influência e espaço amostral com {nPessoas} pessoas)'
    graficoTaxasDeIdentificacao(taxasSimuladas, title=title, fullscreen=True)


def getCompatibilidades(pessoas, personalidades):

    compatibilidades = np.zeros((len(pessoas), len(signosExistentes)))

    for i, pessoa in enumerate(pessoas):
        compatibilidades[i] = [sum(personalidades[i][j]) / 15 for j in range(12)]

    return compatibilidades


def getPalpites(pessoas, compatibilidades):

    # noinspection PyUnusedLocal
    palpites = [[] for i in range(len(pessoas))]
    for i in range(len(pessoas)):
        melhorCompatibilidade = max(compatibilidades[i])
        indicesPalpites = [j for j in range(12) if compatibilidades[i][j] == melhorCompatibilidade]
        palpites[i] = [signosExistentes[j] for j in indicesPalpites]

    return palpites


def getAcertosPorSignos(signosPessoais, palpites):

    acertos = np.zeros(12)
    for i, signoPessoal in enumerate(signosPessoais):
        if signoPessoal in palpites[i]:
            indiceSigno = signosExistentes.index(signoPessoal)
            acertos[indiceSigno] += 1

    return acertos


def imprimeResultados(dados, resultadosIndividuais, resultadosGerais, full=False):

    branco, vermelho, verde, azul = '\033[38m', '\033[31m', '\033[32m', '\033[34m'

    pessoas, signosPessoais, pessoasPorSigno, personalidades = dados

    print('RESULTADOS\n')

    if full:

        compatibilidades, palpites = resultadosIndividuais

        for i, pessoa in enumerate(pessoas):
            print(f'Nome: {pessoa}')
            print(f'Signo: {signosPessoais[i]}')
            print(f'Personalidade: ')
            for linha in personalidades[i]:
                print(f'    {linha}')
            print(f'Compatibilidades: ')
            for j, compatibilidade in enumerate(compatibilidades[i]):
                print(f'    {signosExistentes[j]}: {compatibilidade*100:.2f}%')
            print(f'Palpite: {palpites[i]}')
            print()
        print()
        print()

    taxasPessoasDoSigno, taxasControle, acertos = resultadosGerais

    print(f'Taxas de identificação com características dos signos: ')
    for i, signo in enumerate(signosExistentes):
        print(f'    {signo}: ')
        print(f'        As pessoas de {signo} se identificaram com '
              f'{azul}{taxasPessoasDoSigno[i]*100:.2f}%{branco} das características de {signo}')
        print(f'        As pessoas de outros signos se identificaram com '
              f'{azul}{taxasControle[i]*100:.2f}%{branco} das características de {signo}')

    print(f'\nNúmero de pessoas e palpites corretos por signo: ')
    for signo, nPessoas, nAcertos in zip(signosExistentes, pessoasPorSigno, acertos):
        print(f'    {signo:12}: {nPessoas:3} pessoas. {int(nAcertos)} acertos.')

    print(f'\nTotal: {len(pessoas)} pessoas. {sum(acertos):.0f} acertos.')

    taxaDeAcerto = sum(acertos) / len(pessoas)
    if taxaDeAcerto >= 0.5:
        cor = verde
    else:
        cor = vermelho

    print(f'\nA taxa de acerto dos palpites foi de {cor}{taxaDeAcerto*100:.2f}%{branco}')


def graficoTaxasDeIdentificacao(taxasDeIdentificacao, title, fullscreen=False):

    labels = signosExistentes

    taxasPessoasDoSigno, taxasControle = taxasDeIdentificacao
    taxasPessoasDoSigno = [round(taxa*100, 2) for taxa in taxasPessoasDoSigno]
    taxasControle = [round(taxa*100, 2) for taxa in taxasControle]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(constrained_layout=True)
    if fullscreen:
        fig.canvas.manager.full_screen_toggle()

    rects1 = ax.bar(x - width / 2, taxasPessoasDoSigno, width, label='Pessoas do Signo')
    rects2 = ax.bar(x + width / 2, taxasControle, width, label='Grupo Controle')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_title(title, fontsize=36)
    ax.grid(axis='y')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=22)
    ax.tick_params(axis="x", labelrotation=30)

    ax.set_ylabel('Taxa de Identificação (%)', fontsize=30)
    ax.set_ylim([0, 120])
    ax.set_yticks([i for i in range(0, 120, 20)])
    ax.tick_params(axis="y", labelsize=20)

    ax.legend(loc='best', fontsize=18)

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        offset = 0.07
        color = 'orange'
        if rects == rects1:
            offset = -offset
            color = 'cornflowerblue'

        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=((rect.get_x() + rect.get_width() / 2) + offset, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=16, color=color)

    autolabel(rects1)
    autolabel(rects2)

    plt.show()


signosExistentes = ['Capricórnio', 'Aquário', 'Peixes', 'Áries', 'Touro', 'Gêmeos', 'Câncer', 'Leão', 'Virgem', 'Libra',
                    'Escorpião', 'Sagitário']

tracosExistentes = [
    ['Responsável', 'Tradicional', 'Dominador', 'Rancoroso', 'Honesto',
     'Ambicioso', 'Maduro', 'Prático', 'Crítico', 'Trabalhador',
     'Pessimista', 'Persistente', 'Cauteloso', 'Sério', 'Paciente'],

    ['Individualista', 'Excêntrico', 'Comunicativo', 'Sonhador', 'Líder',
     'Rebelde', 'Bondoso', 'Amigo', 'Leal', 'Direto',
     'Imprevisível', 'Sociável', 'Teimoso', 'Convicto', 'Inovador'],

    ['Simpático', 'Intuitivo', 'Defensivo', 'Indeciso', 'Adaptável',
     'Reservado', 'Distraído', 'Sensível', 'Tímido', 'Otimista',
     'Desorganizado', 'Generoso', 'Manipulador', 'Tranquilo', 'Flexível'],

    ['Precipitado', 'Ativo', 'Egoísta', 'Impulsivo', 'Agressivo',
     'Objetivo', 'Mandão', 'Ousado', 'Sincero', 'Corajoso',
     'Espontâneo', 'Independente', 'Realista', 'Pavio-Curto', 'Impaciente'],

    ['Forte', 'Sensual', 'Emotivo', 'Pacífico', 'Esforçado',
     'Metódico', 'Confiável', 'Possessivo', 'Guloso', 'Rígido',
     'Gracioso', 'Polêmico', 'Ciumento', 'Invejoso', 'Preguiçoso'],

    ['Charmoso', 'Persuasivo', 'Inteligente', 'Alegre', 'Curioso',
     'Fofoqueiro', 'Esquecido', 'Irresponsável', 'Lógico', 'Brincalhão',
     'Inconsequente', 'Infantil', 'Bipolar', 'Inquieto', 'Ansioso'],

    ['Ouvinte', 'Romântico', 'Carente', 'Imaginativo', 'Fechado',
     'Atento', 'Caseiro', 'Criativo', 'Confiante', 'Protetor',
     'Vingativo', 'Paranoico', 'Encorajador', 'Ranzinza', 'Guerreiro'],

    ['Vaidoso', 'Brilhante', 'Aventureiro', 'Carismático', 'Impositivo',
     'Exagerado', 'Arrogante', 'Determinado', 'Expressivo', 'Esperto',
     'Empreendedor', 'Amigável', 'Orgulhoso', 'Metido', 'Folgado'],

    ['Observador', 'Analítico', 'Apegado', 'Espirituoso', 'Prestativo',
     'Eficiente', 'Gentil', 'Dedicado', 'Pensativo', 'Brigão',
     'Frio', 'Sistemático', 'Reclamão', 'Detalhista', 'Desconfiado'],

    ['Diplomático', 'Culto', 'Alto astral', 'Educado', 'Conquistador',
     'Equilibrado', 'Ponderado', 'Artístico', 'Estiloso', 'Delicado',
     'Carinhoso', 'Justo', 'Grosso', 'Influenciável', 'Inocente'],

    ['Obstinado', 'Compreensível', 'Companheiro', 'Profundo', 'Calmo',
     'Intenso', 'Competitivo', 'Impiedoso', 'Perverso', 'Astuto',
     'Cabeça-dura', 'Misterioso', 'Mal-humorado', 'Passional', 'Compulsivo'],

    ['Estimulante', 'Desapegado', 'Livre', 'Empolgado', 'Despreocupado',
     'Festeiro', 'Genial', 'Aberto', 'Descuidado', 'Fútil',
     'Desbocado', 'Agitafo', 'Exigente', 'Insensível', 'Inflexível']
]

pessoas, signosPessoais, personalidades = \
    getTestesDePersonalidade('Teste de Personalidade (respostas).xlsx', sheet_name='Respostas ao formulário 1')

pessoasPorSigno = getPessoasPorSigno(signosPessoais)
dados = pessoas, signosPessoais, pessoasPorSigno, personalidades

taxasPessoasDoSigno, taxasControle = getTaxasDeIdentificacao(pessoas, signosPessoais, personalidades)

espacoAmostral = 200
for influencia in []:
    simulacao(espacoAmostral, taxasControle, influenciaSigno=influencia)
    print()

compatibilidades = getCompatibilidades(pessoas, personalidades)
palpites = getPalpites(pessoas, compatibilidades)
acertosPorSigno = getAcertosPorSignos(signosPessoais, palpites)

resultadosIndividuais = compatibilidades, palpites
resultadosGerais = taxasPessoasDoSigno, taxasControle, acertosPorSigno

print(f'DADOS EXPERIMENTAIS. Espaço amostral com {len(pessoas)} pessoas.')
imprimeResultados(dados, resultadosIndividuais, resultadosGerais, full=True)

title = f'Taxas de identificação\n(Dados experimentais: espaço amostral com {len(pessoas)} pessoas)'
graficoTaxasDeIdentificacao((taxasPessoasDoSigno, taxasControle), title=title, fullscreen=True)
