import os
import matplotlib.pyplot as plt

def checa_vez_atual():
    vez = 0
    # Caso o arquivo não exista (1ª vez)
    if not os.path.isfile('vezAtual.txt'):
        with open('vezAtual.txt', 'w') as f:
            f.write('1')
            vez = 1
    else:
        with open('vezAtual.txt', 'r') as f:
            tempvez = f.readline()
            tempvez = int(tempvez)
            vez = tempvez
            vez += 1
        with open('vezAtual.txt', 'w') as f:
            f.write(str(vez))
    return vez


def cria_pasta(vezAtual):
    dirName = '{}_teste'.format(vezAtual)
    try:
        os.mkdir(dirName)
        print("Pasta " , dirName ,  " criada ") 
    except FileExistsError:
        print("Pasta " , dirName ,  " já existe")


def salva_relatorio(vezAtual, texto):
    pasta = '{}_teste'.format(vezAtual)
    nomearq = '{}\\{}_relatorio.txt'.format(pasta, vezAtual)

    with open(nomearq, 'w') as f:
        f.write(texto)


def salva_fig_melhor_fitness(vezAtual, geracoes, tamanho, listafitness):
    pasta = '{}_teste'.format(vezAtual)
    geracoes = list(range(1, geracoes+1))
    plt.plot(geracoes, listafitness)
    plt.grid()
    plt.title('Execuções com poupulação = {} (melhor fitness)'.format(tamanho))
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.savefig('{}\\{}_melhor_fitness.png'.format(pasta, vezAtual))


def salva_fig_media_fitness(vezAtual, geracoes, tamanho, listafitness, listamedia):
    pasta = '{}_teste'.format(vezAtual)
    geracoes = list(range(1, geracoes+1))
    plt.plot(geracoes, listafitness, 'b-', label='fitness')
    plt.plot(geracoes, listamedia, 'r-', label='média')
    plt.legend(loc=0)
    plt.title('Média das execuções com poupulação = {}'.format(tamanho))
    plt.xlabel('Gerações')
    plt.ylabel('Fitness')
    plt.grid()
    plt.savefig('{}\\{}_media_fitness.png'.format(pasta, vezAtual))