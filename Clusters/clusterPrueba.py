import matplotlib.pyplot as plt
from math import log
dir = "C:\\Franco\\Facultad\\IA\\data.txt"


def leerTxt(path):
    '''Lee un txt donde cada linea esta conformada por 2 numeros y convierte cada linea en una tupla de 2 elementos'''
    with open(path, 'r') as file:
        data = file.read()
        lines = data.splitlines()
        #para cada linea del txt
        salida = []
        for line in lines:
            line = line.split()
            #print(tuple(line))
            tupla = tuple(line)
            tupla = (round(int(tupla[0])/1000),round(int(tupla[1])/1000))
            salida.append(tupla)
        return(salida)

'''lista = leerTxt(dir)

#print(lista)
x,y = zip(*lista)
plt.scatter(x,y)
plt.show()'''
