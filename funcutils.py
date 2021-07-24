import numpy as np

def altura(arr):
    return arr.shape[0]

def largura(arr):
    try:
        return arr.shape[1]
    except:
        return arr.shape[0]

arredondar = lambda num: float('%.0f' % num)

def igualar_tabelas(a, b):
    ha = altura(a)
    hb = altura(b)
    la = largura(a)
    lb = largura(b)
    #print(ha, hb)
    #print(la, lb)

    if ha != hb:
        if ha < hb:
            a = np.vstack((np.zeros((hb-ha, la), dtype='int'), a))
        else:
            b = np.vstack((np.zeros((ha-hb, lb), dtype='int'), b))

        ha = altura(a)
        hb = altura(b)
        la = largura(a)
        lb = largura(b)
        #print(ha, hb)
        #print(la, lb)
        return (a, b)
    else:
        return (a, b)


def substituir(a, b, posicao):
    la = largura(a)

    if posicao == 0:  # só haverá um pedaço
        segunda_parte = b[:, (posicao+la):]
        return np.hstack((a, segunda_parte))
    elif ((10-la) == posicao):
        primeira_parte = b[:,0:posicao]
        return np.hstack((primeira_parte, a))
    else:
        primeira_parte = b[:,0:posicao]
        segunda_parte = b[:, (posicao+la):]

        if len(primeira_parte.shape) == 1:  #coluna única
            primeira_parte = np.vstack(primeira_parte)
        if len(segunda_parte.shape) == 1:  #coluna única
            segunda_parte = np.vstack(segunda_parte)

        return np.hstack((primeira_parte, a, segunda_parte))
