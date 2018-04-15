import numpy as np
import matplotlib.pyplot as plt
import Clusters.clusterPrueba as cl
import random
import math



#Dominio de solucion


def poblacionInicial(n):
    for i in range(cantidadCentroides):
        x = random.randrange(0,maxX)
        y = random.randrange(0,maxY)
        centX.append(x)
        centY.append(y)
    return list(zip(centX,centY))

def evaluarFuncionFitness(centroide,datos):
    #por cada punto del data set
    valorFitness = 0
    for i in range(len(datos[0])):
        datosX = datos[0]
        datosY = datos[1]
        punto = ((datos[0][i]),(datos[1][i]))
        dist = distance(centroide,punto)
        distEscala = dist//100
        valorFitness = valorFitness + round(10/(1+distEscala**2))
    return valorFitness

def distance(a,b):
    x = (a[0] - b[0])
    y = (a[1] - b[1])
    return (round(math.hypot(x,y)))




dataset = cl.leerTxt(cl.dir)
listaDatos = zip(*dataset)

#DATASET INICIAL
listaDatos = list(listaDatos)

#LONGITUD DATASET
longitudLista = len(listaDatos[0])

coordsX = listaDatos[0]
coordsY = listaDatos[1]

maxX = max(coordsX)
maxY = max(coordsY)

plt.axis([0, maxX+20, 0, maxY+20])
plt.ion()

#CENTROIDES INICIALES Y CANTIDAD DE CENTROIDES
cantidadCentroides = 8
centX = []
centY = []
centroides = poblacionInicial(cantidadCentroides)

plt.scatter(coordsX,coordsY)

for i in range(cantidadCentroides):
    centroide = centroides[i]
    fitness = evaluarFuncionFitness(centroide,listaDatos)
    plt.scatter(centroide[0],centroide[1])



a = zip(*poblacionInicial(cantidadCentroides))
centroides = list(a)
centX = centroides[0]
centY = centroides[1]

print(evaluarFuncionFitness((600,220),listaDatos))




while True:
    plt.pause(0.05)