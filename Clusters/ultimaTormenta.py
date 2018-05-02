import math
from operator import attrgetter

import matplotlib.pyplot as pl
import random
import easygui

class Individuo(object):
    """
    El atributo valor es un conjunto de centroides
    """


    def __init__(self):
        self.valor = 0
        self.fitness = 0
        self.puntos = []

    def setValorRandom(self,cantidad,minx,maxx,miny,maxy):
        individuo = []
        for i in range(cantidad):
            x = random.randrange(minx, maxx)
            y = random.randrange(miny, maxy)
            individuo.append((x, y))
        self.valor = individuo

    def setValor(self,valor):
        self.valor = valor

    def setFitness(self):

        for i in range(len(self.valor)):
            fitness = 0
            alelo = self.valor[i]
            distancia = 0
            puntos = self.puntos[i]

            # puntos[j] es un punto de todos los puntos que pertenecen al individuo i
            for j in range(len(puntos)):
                punto = puntos[j]
                distancia = distancia + math.hypot(alelo[0] - punto[0], alelo[1] - punto[1])

            errorIndividuo = distancia / len(self.puntos)
            fitness = fitness + errorIndividuo
        self.fitness = fitness
        return fitness


    def setPuntos(self,dataset):
        for i in range(len(self.valor)):
            self.puntos.append([])

        for i in range(len(dataset)):
            punto = dataset[i]
            posicionCentroide = calcularCentroide(punto,self)
            self.puntos[posicionCentroide].append(punto)


#formato de la solucion o individuo: [(2,3),(5,1)(3,14)]

#FUNCIONES EN GENERAL

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
            #print(type(tupla[0]))
            tupla = (float(tupla[0]),float(tupla[1]))
            #print(type(tupla[0]))
            salida.append(tupla)
        return salida

def graficarPuntos(x, y):
    '''Recibe como parametro todas las coords x, luego todas los coords y, y las grafica'''
    pl.scatter(x,y)


def generarPoblacionInicial(tamanoPoblacion,tamanoIndividuo,minx,maxx,miny,maxy):
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = Individuo()
        individuo.setValorRandom(tamanoIndividuo,minx,maxx,miny,maxy)
        individuo.setPuntos(dataset)
        poblacion.append(individuo)
    return poblacion

def calcularCentroide(punto,individuo):
    centroideMinimo = 0
    centroide = individuo.valor[0]
    min = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
    for i in range(1,len(individuo.valor)):
        centroide = individuo.valor[i]
        dist = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
        if (dist < min):
            min = dist
            centroideMinimo = i

    return centroideMinimo



def seleccionRanking(poblacion,cantidadSeleccionar):
    fitness = []
    listpob = []
    for i in poblacion:
        listpob.append(i.valor)

    for i in poblacion:
        fitness.append(i.setFitness())
    fitness.sort()
    listaPobOrdenada = list(zip(*sorted(zip(listpob, fitness))))
    print(fitness)
    print(listaPobOrdenada)


 #   puntos = list(range(1,len(poblacion)+1))
 #   puntos.reverse()
 #   ranking = []
 #   print(puntos)




dataset = leerTxt("C:\\PythonProjects\\geneticClustering\\Clusters\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))

TotalSeleccion = 5

poblacion = generarPoblacionInicial(10,3,minx,maxx,miny,maxy)

sel = seleccionRanking(poblacion,4)
#poblacion.sort(key = lambda individuo: individuo.fitness)
#seleccionRanking(poblacion,3)




ind = poblacion[len(poblacion) - 1]
for i in range(len(ind.puntos)):
    if ind.puntos[i]:
        px,py = zip(*ind.puntos[i])
        graficarPuntos(px,py)

for centroide in ind.valor:
    px,py = centroide
    graficarPuntos(px, py)



pl.show()



