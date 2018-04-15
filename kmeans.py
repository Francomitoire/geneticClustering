import random
import Clusters.clusterPrueba as cl
import math
import matplotlib.pyplot as pl


#Funciones ------------------------------------

def distancia(a, b):
    x = (a[0]-b[0])**2
    y = (a[1]-b[1])**2
    return (int(math.sqrt(x+y)))

#calcula el promedio(centroide) de un conjunto
def calcularPromedio(datos):
    x = 0
    y = 0
    for tupla in datos:
        x = x + tupla[0]
        y = y + tupla[1]
    x = x//len(datos)
    y = y//len(datos)
    return (x,y)

def calcularCentroideMenorDistancia(punto,centroides):
    '''Devuelve el centroide mas cercano'''
    min = distancia(punto,centroides[0])
    centroide = 0
    for i in range(1,len(centroides)):
        dist = distancia(punto,centroides[i])
        if dist < min:
            min = dist
            centroide = i
    return centroide

#---------------------------------------
#parametros


cantidadCentroides = 12
dataset = cl.leerTxt(cl.dir)
centroides = []
puntosEnCentroide = []


#---------------------------------------

for i in range(10):

    for i in range(cantidadCentroides):
        puntosEnCentroide.append([])

    #print(puntosEnCentroide)

    for i in range(cantidadCentroides):
        centroides.append((random.randrange(0,999),random.randrange(0,999)))

    for tuple in dataset:
        centroideDeTupla = calcularCentroideMenorDistancia(tuple,centroides)
        puntosEnCentroide[centroideDeTupla].append(tuple)

    #centroides[0] = calcularPromedio(puntosEnCentroide[0])
    #centroides[1] = calcularPromedio(puntosEnCentroide[1])


    x = [0]*cantidadCentroides
    y = [0]*cantidadCentroides



    for i in range(cantidadCentroides):
        #print('Centroide:' +str(i)+ str(puntosEnCentroide[i]))
        if(puntosEnCentroide[i]):
            a,b = zip(*puntosEnCentroide[i])
            #Cada posicion de los arreglos x e y tienen todas las cords x e y respectivamente, pertenecientes al centroide i
            x[i] = a
            y[i] = b
            #calculo los nuevos centroides de los conjuntos obtenidos anteriormente
            centroides[i] = calcularPromedio(puntosEnCentroide[i])


#grafico cada conjunto de puntos pertenecientes al centroide i, junto a su centroide, por separado del resto de puntos y centroides
for i in range(cantidadCentroides):
    pl.scatter(x[i], y[i])
    pl.scatter(centroides[i][0], centroides[i][1])

pl.show()

'''x,y= zip(*dataset)
pl.scatter(x,y)
prom = calcularPromedio(dataset)
pl.scatter(prom[0],prom[1])
pl.show()'''


