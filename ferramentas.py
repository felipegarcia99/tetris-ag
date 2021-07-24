import numpy as np
import random
from funcutils import *

def produzir_objeto(tipo):
    if tipo == 'l':
        l = np.array([[1,0,0], [1,1,1]])
        denovo = 's'
        while(denovo == 's'):
            rolagem_dado = random.choice(['s', 'n'])
            if rolagem_dado == 's': # transpor
                l = l.transpose()

            rolagem_dado = random.choice(['s', 'n'])
            if rolagem_dado == 's': # inverter
                l = l[::-1]

            denovo = random.choice(['s', 'n'])
        return l

    elif tipo == 'b':
        rolagem_dado = random.choice(['h', 'v'])
        if rolagem_dado == 'v':
            b = np.array([[1], [1], [1], [1]])
        elif rolagem_dado == 'h':
            b = np.array([1,1,1,1])

        return b

    elif tipo == 'c':
        c = np.array([[1, 1], [1, 1]])
        return c

    elif tipo == 's':
        s = np.array([[1,1,0], [0,1,1]])
        rolagem_dado = random.choice(['s', 'n'])
        if rolagem_dado == 's': # transpor
            s = s.transpose()

        rolagem_dado = random.choice(['s', 'n'])
        if rolagem_dado == 's': # inverter
            s = s[::-1]
            
        return s

    elif tipo == 't':
        t = np.array([[0,1,0], [1,1,1]])
        denovo = 's'
        while(denovo == 's'):
            rolagem_dado = random.choice(['s', 'n'])
            if rolagem_dado == 's': # transpor
                t = t.transpose()

            rolagem_dado = random.choice(['s', 'n'])
            if rolagem_dado == 's': # inverter
                t = t[::-1]

            denovo = random.choice(['s', 'n'])

        return t


def produzir_individuo(objeto):
    try:
        largura = objeto.shape[1]
    except:
        largura = objeto.shape[0]

    posicao = np.random.randint(1, np.abs(10 - largura)+1)

    return (objeto, posicao)


def gravidade(individuo, mapa):
    objeto, posicao = individuo
    try:
        isbarra = False
        largura = objeto.shape[1]
    except:
        isbarra = True
        largura = objeto.shape[0]

    limitacao = mapa[:,posicao:posicao+largura]
    limitacao = np.where(limitacao==1, 0, limitacao) 
    # print('limitacao antes: \n', limitacao)

    podedescer = False
    for linha_atual in limitacao:
        if not np.any(linha_atual):  # checa se todos os elementos são 0
            limitacao = np.delete(limitacao, 0, 0)
            # print('linha atual: ', linha_atual)
            # continue
        else:
            # print('ok')
            if not isbarra:
                count = 0
                num = 2
                for i in range(len(limitacao[0])):
                    if not ((limitacao[0][i] == num) and (objeto[-1][i] == 1)):
                        count += 1
                if count == len(limitacao[0]):
                    # print('espaço para descer')
                    podedescer = True
                    # deve-se fazer um codigo pra checar se o objeto atual é um l, se for, checar se 
                    # dá pra descer dois degraus
                    # print('objeto: \n', objeto)
                    # print('limitacao: \n', limitacao)
                    # print()
                    
                    # agora vem o código para descer
                    primeira_linha = limitacao[0]
                    ultima_linha = objeto[-1]
                    arr1s = np.where(primeira_linha == num)
                    arr1s = arr1s[0]

                    temp = []
                    for i in range(len(primeira_linha)):
                        if i in arr1s:
                            temp.append(primeira_linha[i])
                            continue
                        else:
                            temp.append(ultima_linha[i])

                    # print(temp)
                    # print(primeira_linha)
                    limitacao[0] = temp
                    # print('limitação modificada: \n', limitacao)
                    # print()

                    objeto = np.delete(objeto, -1, 0)
                    # print('objeto modificado: \n', objeto)
                    # print()

                    '''try:
                        unique, counts = np.unique(objeto, return_counts=True)
                        contagem = dict(zip(unique, counts))
                        print('contagem: ',  contagem)
                        if contagem[1] > 4:
                            raise Exception('Contagem maior que 4')
                    except Exception as e:
                        print(e)'''

                else:
                    pass # substituir '1' por '0'
                    # colocado depois de obter a limitação


            # print('posicao: ', posicao)
            # print('objeto: \n', objeto)
            # print('limitacao: \n', limitacao)
            # print()
            nova_limitacao = np.vstack((objeto, limitacao))
            break

    nova_limitacao, mapa = igualar_tabelas(nova_limitacao, mapa)
    # print(nova_limitacao)
    # if podedescer:
    #     print('nova_limitacao: \n', nova_limitacao)

    mapa_com_objeto = substituir(nova_limitacao, mapa, posicao)
    # print(mapa_com_objeto)

    return mapa_com_objeto


def fitness(mapa_com_objeto): # e que tal, quanto menos espaços vazios, mais pontos?
    h = altura(mapa_com_objeto)
    fita = np.linspace(0.1, 1, num=h)
    # print('fita: ', fita)
    soma = np.sum(mapa_com_objeto, axis = 1)
    # print('soma: ', soma)
    listafitness = fita * soma
    # print('listafitness: ', listafitness)
    fitness = np.sum(listafitness)

    return fitness

def fitness2(mapa_com_objeto): # aumenta a fitness, mas o comportamento continua o mesmo
    # resuldato médio: barra na pos 1
    h = altura(mapa_com_objeto)
    # fita = np.linspace(0.1, 1, num=h)
    fita = list(range(1, h+1))
    # print('fita: ', fita)
    soma = np.sum(mapa_com_objeto, axis = 1)
    # print('soma: ', soma)
    listafitness = fita * soma
    # print('listafitness: ', listafitness)
    fitness = np.sum(listafitness)

    return fitness


def fitness3(mapa_com_objeto): # aumenta a fitness, mas o comportamento continua o mesmo
    # resuldato médio: barra na pos 1
    h = altura(mapa_com_objeto)
    # fita = np.linspace(0.1, 1, num=h)
    fita = list(range(1, h+1))
    fita = [i**2 for i in fita]
    # print('fita: ', fita)
    soma = np.sum(mapa_com_objeto, axis = 1)
    # print('soma: ', soma)
    listafitness = fita * soma
    # print('listafitness: ', listafitness)
    fitness = np.sum(listafitness)

    return fitness


def fitness4(mapa_com_objeto):
    h = altura(mapa_com_objeto)
    fita = np.linspace(0.1, 1, num=h)
    # print('fita: ', fita)
    conts1 = []
    for linha in mapa_com_objeto:
        if np.any(linha == 1):
            unique, counts = np.unique(linha, return_counts=True)
            contagem = dict(zip(unique, counts))
            conts1.append(contagem[1])
        else:
            conts1.append(0)
    # print(conts1)
    listafitness = fita * conts1
    # print('listafitness: ', listafitness)
    fitness = np.sum(listafitness)

    return fitness


def juntarobjetos(obj1, obj2):
    '''corte = random.randint(1, 4)

    if corte == 4:
        return obj1

    if not (len(obj1.shape) == 1): # barra
        pedaco1 = obj1[:, 0:corte]

    pedaco1 = []
    pedaco2 = []
    if not (len(obj1.shape) == 1): # barra
        for i in obj1:
            for j in range(len(i)):
                pedaco1.append(i[j])
        contagem = {i:pedaco1.count(i) for i in pedaco1}
        maxi = 4 - contagem[1]
        for i in obj2:
            for j in range(len(i)):
                pedaco2.append[i[j]]
                if i[j] == 1:
                    maxi -= 1
                if maxi == 0:
                    break'''
    return random.choice([obj1, obj2])


def calcula_e_imprime_geracao(geracao, fit, popu):
    media = np.mean(fit, dtype = np.float32)
    melhor = fit[np.argmax(fit)]
    texto = '''geração {geracao}\nMédia fitness: {media}\nMelhor individuo: {ind}\nFitness: {melhor}\n
    '''.format(geracao=geracao,
                media=media,
                ind=popu[np.argmax(fit)],
                melhor=melhor)

    print(texto)
    '''print('geração ', geracao)
    print('Média fitness: ', media)
    print('Melhor individuo: ', popu[np.argmax(fit)])
    print('Fitness: ', melhor)
    print('\n\n')'''

    return (media, melhor, texto)


