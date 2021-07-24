import numpy as np
import random
import argparse
from ferramentas import *
from usina_arquivos import *
from mapas import *

gtexto = ''
listafitness = []
listamedia = []

def main():
    parser = argparse.ArgumentParser(description = 'Algoritmo Genético para encontrar a melhor peça para o jogo Tetris')
    parser.add_argument('-p', '--populacao', required = False, help = 'tamanho da população, padrão 100', default = 100)
    parser.add_argument('-g', '--geracao', required = False, help = 'limite maximo de gerações, padrão 1000', default = 1000)
    parser.add_argument('-e', '--equipes', required = False, help = 'tamanho das equipes, padrão 3', default = 3)
    parser.add_argument('-t', '--torneio', required = False, help = 'quantidade de equipes, padrão 20', default = 20)
    parser.add_argument('-m', '--mutacao', required = False, help = 'taxa de mutacao, padrão 1', default = 1)
    args = vars(parser.parse_args())

    def montar_mapa():
        return mapa2


    def iniciar_populacao(tamanho_populacao = 100, tamanho_cromo = 4):
        populacao = dict()  # talvez dict() seja melhor
        i = 0
        while (len(populacao) < tamanho_populacao):
            # l: L
            # b: barra
            # c: caixa
            # s: S
            # t: T
            formato = random.choice(['l', 'b', 'c', 's', 't'])
            objeto = produzir_objeto(formato)
            # print(objeto)
            individuo = produzir_individuo(objeto)
            populacao[i] = individuo

            i += 1

        return populacao


    def calculo_fitness(populacao, mapa):
        lista_fitness = []
        for i in populacao:
            # print('objeto: ', populacao[i][0])
            # print('largura: ', largura(populacao[i][0]))
            # print('pos: ', populacao[i][1])
            mapa_com_objeto = gravidade(populacao[i], mapa)
            fit = fitness4(mapa_com_objeto)
            # fit = 1/(fit + 1)

            # print('mapa_com_objeto: \n', mapa_com_objeto)
            # print('objeto: \n', populacao[i][0])
            # print('fitness: ', fit)

            lista_fitness.append(fit)

        lista_fitness = np.asarray(lista_fitness)
        return lista_fitness


    # torneio para selecionar quem participara da reprodução
    def selecao_torneio(fitness, tamanho_torneio = 3, tamanho_selecionados = 20):
        # matriz que contem o endereço dos indivíduos que participarão da reprodução
        selecionados = np.zeros(tamanho_selecionados, dtype = np.int32)
        # laço for para preencher a matriz selecionados com os indivíduos selecionados
        for i in range(tamanho_selecionados):
            # seleciona 3 números aleatorios entre 0 e tamanho da população/fitness
            chamados = np.random.randint(len(fitness), size = tamanho_torneio)
            # matriz com a fitness dos 3 indivíduos escolhidos
            fitness_chamados = np.asarray([fitness[chamados[0]], fitness[chamados[1]], fitness[chamados[2]]])
            # acha o endereço do melhor indivíduo
            melhor = np.argmax(fitness_chamados)
            melhor = chamados[melhor]
            # joga o valor do endereço do vencedor do torneio no array 'selecionados'
            selecionados[i] = melhor
        # retorna um array com o endereço dos vencedores
        # print(selecionados)
        return selecionados


    def crossover(populacao, selecionados, fitness):
        '''print('selecionados: ')
        for i in selecionados:
            print(populacao[i])'''

        filhos = dict()
        for i in range(0, len(selecionados), 2):
            ind1 = populacao[selecionados[i]]
            ind2 = populacao[selecionados[i+1]]
            fit1 = fitness[selecionados[i]]
            fit2 = fitness[selecionados[i+1]]

            obj1, pos1 = ind1
            obj2, pos2 = ind2

            if fit1 > fit2:
                posfinal1 = ((pos1)+(pos2*2))/2
                # posfinal2 = ((pos2)+(pos1*2))/2

            else:
                posfinal1 = ((pos2)+(pos1*2))/2
                # posfinal2 = ((pos1)+(pos2*2))/2
                # ch = random.choice([-1, 1])
                # posfinal2 = posfinal1 + ch
            while True:
            	ch = random.choice([-1, 1])
            	posfinal2 = posfinal1 + ch
            	if posfinal2 >= 0:
            		break

            # print('Antes de passar nos ifs')
            # print('posfinal1: ', posfinal1)
            # print('posfinal2: ', posfinal2)

            posfinal1 = arredondar(posfinal1)
            posfinal2 = arredondar(posfinal2)
            posfinal1 = int(posfinal1)
            posfinal2 = int(posfinal2)

            objfinal1 = juntarobjetos(obj1, obj2)
            objfinal2 = juntarobjetos(obj2, obj1)

            if (10 - posfinal1) < largura(objfinal1):
                posfinal1 = (10 - posfinal1)
            if (10 - posfinal2) < largura(objfinal2):
                posfinal2 = (10 - posfinal2)

            if posfinal1 < 0 or posfinal2 < 0:
            	# print('Alguém ainda conseguiu passar...')
            	# print('posfinal1: ', posfinal1)
            	# print('posfinal2: ', posfinal2)
            	if posfinal1 < 0:
            		posfinal1 = -posfinal1 + posfinal1
            	if posfinal2 < 0:
            		posfinal2 = -posfinal2 + posfinal2

            individuofinal1 = (objfinal1, posfinal1)
            individuofinal2 = (objfinal2, posfinal2)
            # filhos.append(individuofinal1)
            # filhos.append(individuofinal2)
            filhos[i] = individuofinal1
            filhos[i+1] = individuofinal2

        # filhos = np.asarray(filhos)
        '''print('filhos: ')
        for i in filhos:
            print(filhos[i])'''
        return filhos


    def mutacao(filhos, probabilidade = 1):
        for i in range(len(filhos)):
            rolagem_dado = random.uniform(0, 100)
            if(rolagem_dado <= probabilidade):
                formato = random.choice(['l', 'b', 'c', 's', 't'])
                objeto = produzir_objeto(formato)
                individuo = produzir_individuo(objeto)
                filhos[i] = individuo
        return filhos


    def nova_populacao(populacao, fitness, filhos, filhos_fitness):
        filhos = list(filhos.values())
        while(len(filhos) > 0):
            # print('len(filhos): ', len(filhos))
            # endereço do pior indivíduo da população
            minimo = np.argmin(fitness)
            # endereço do melhor filho
            maximo = np.argmax(filhos_fitness)
            # se o filho for melhor, fazer a substituição
            if(filhos_fitness[maximo] >= fitness[minimo]):
                # pior indivíduo sendo substituido pelo melhor filho
                populacao[minimo] = filhos[maximo]
                # fitness do pior indivíduo sendo substituido pela fitness do melhor filho
                fitness[minimo] = filhos_fitness[maximo]
                # deletar o melhor filho do array 'filhos' pois ele já foi inserido na matriz 'população'
                filhos = np.delete(filhos, maximo, 0)
                '''print(filhos)
                filhos.pop(maximo)'''
                # deletar a melhar fitness do filho do array 'filhos_fitness' pois ele já foi inserido na matriz 'fitness'
                filhos_fitness = np.delete(filhos_fitness, maximo, 0)
            else:
                # se o melhor filho não é melhor que o pior da população, então não há o por que de continuar verificando
                break
        # retorna a nova população e a nova fitness
        return populacao, fitness


    def geracoes(tamanho_populacao = 100, qunatidade_geracao = 1000,
                tamanho_torneio = 3, tamanho_selecionados = 20, taxa_mutacao = 1):
        global gtexto, listamedia, listafitness

        mapa = montar_mapa()
        # iniciar a primeira população
        popu = iniciar_populacao(tamanho_populacao)
        # calcular a fitness da primeira população
        fit = calculo_fitness(popu, mapa)
        # print('fit: ', fit)
        # valor da geração atual
        geracao = 1

        # imprimir as informações
        media, melhor, texto = calcula_e_imprime_geracao(geracao, fit, popu)
        gtexto = gtexto + texto
        listamedia.append(media)
        listafitness.append(melhor)

        # laço infinito até alguma condição de parada for alcançada
        while(True):
            # mapa = 0  # não adianta
            # mapa = montar_mapa()  # não adianta
            # print(popu)
            '''con = 0
            for i in popu:
            	if popu[i][0].tolist() == [1,1,1,1]:
            		con += 1
            print(con)'''
            # endereço dos vencedores do torneio
            sele = selecao_torneio(fit, tamanho_torneio, tamanho_selecionados)
            # print('sele: ', sele)
            # geração dos filhos
            filh = crossover(popu, sele, fit)
            # print('filh: ', filh)
            # mutação dos filhos (caso ocorra)
            filh = mutacao(filh, probabilidade = taxa_mutacao)
            # print('mut: ', filh)
            # calculo da fitness dos filhos
            filh_fit = calculo_fitness(filh, mapa)
            # print('filh_fit: ', filh_fit)
            # nova geração
            populacao, fitness = nova_populacao(popu, fit, filh, filh_fit)
            # print(populacao)
            geracao = geracao + 1
            # if fit.tolist() == fitness.tolist(): print(True)
            # if popu == populacao: print(True)
            # imprimir as informações
            media, melhor, texto = calcula_e_imprime_geracao(geracao, fit, popu)
            gtexto = gtexto + texto
            listamedia.append(media)
            listafitness.append(melhor)

            # condições de paradas
            # se a geração atual alcançar o limite 
            if(geracao >= qunatidade_geracao):
                print('Máximo de gerações alcançado\n')
                break
            # se a solução foi encontrada
            if(np.max(fit) >= 2.425):
                print('Solução Encontrada')
                break

            '''if geracao == 2 or geracao == 999:
            	for i in popu:
            		print(i, popu[i])
            	# input()'''


        vezAtual = checa_vez_atual()
        cria_pasta(vezAtual)
        salva_relatorio(vezAtual, gtexto)
        salva_fig_melhor_fitness(vezAtual, geracao, tamanho_populacao,listafitness)
        salva_fig_media_fitness(vezAtual, geracao, tamanho_populacao,listafitness, listamedia)
    

    # executar algoritmo genetico
    geracoes(tamanho_populacao = int(args['populacao']), 
        qunatidade_geracao = int(args['geracao']), 
        tamanho_torneio = int(args['equipes']), 
        tamanho_selecionados = int(args['torneio']),
        taxa_mutacao = int(args['mutacao']))

    
######################################################################################################################
# rodar Script
if __name__ == '__main__':
    main()