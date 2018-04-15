import random
import Clusters.clusterPrueba as cl
import math
import matplotlib.pyplot as pl


class Individuo(object):
    def __init__(self):
        self.x = random.randrange(0,1000)
        self.y = random.randrange(0,1000)

    def __repr__(self):
        return "(%s,%s)"%(self.x,self.y)


    def evaluarFitness(self):
        pass

    def mutar(self):
        pass

    def distancia(self,punto):
        distX = (self.x - punto[0])**2
        distY = (self.y - punto[1])**2
        dist = math.sqrt(distX+distY)
        return int(dist)

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y



def calcularPromedio(datos):
    x = 0
    y = 0
    for tupla in datos:
        x = x + tupla[0]
        y = y + tupla[1]
    x = x//len(datos)
    y = y//len(datos)
    return (x,y)

def calcularVarianza(datos):
    mediaXY = calcularPromedio(datos)
    sumaX = 0
    sumaY = 0
    sumaXCuadrado = 0
    sumaYCuadrado = 0
    n = len(datos)
    for tupla in datos:
        sumaXCuadrado = sumaXCuadrado + (tupla[0]**2)
        sumaYCuadrado = sumaYCuadrado + (tupla[1]**2)
    varianzaX = (sumaXCuadrado//n) - mediaXY[0]**2
    varianzaY = (sumaYCuadrado//n) - mediaXY[1]**2
    return (varianzaX, varianzaY)

def calcularDesvio(datos):
    varianza = calcularVarianza(datos)
    return(int(math.sqrt(varianza[0])),int(math.sqrt(varianza[1])))

dataset = cl.leerTxt(cl.dir)
cantidadIndividuos = 2
individuos = []
datasetIndividuos = []

for i in range(len(dataset)):
    datasetIndividuos.append(Individuo())
    datasetIndividuos[i].setX = dataset[i][0]
    datasetIndividuos[i].setY = dataset[i][1]
    pl.scatter(datasetIndividuos[i].x,datasetIndividuos[i].y)

pl.show()

#por cada elemento calculo la distancia a los dos individuos y le asigno al mas cercano


#b = calcularPromedio(a)
#c = calcularVarianza(a)
#d = calcularDesvio(a)
#print(b, c, d)
'''x,y = zip(*a)
pl.scatter(x,y)
pl.scatter(ind.x, ind.y)
pl.show()'''
