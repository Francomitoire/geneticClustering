import random
import math
import matplotlib.pyplot as pl
import random


#formato de la solucion o individuo: [(2,3),(5,1)(3,14)]


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
        return(salida)

def graficarPuntos(x, y):
    '''Recibe como paraemtro todas las coords x, luego todas los coords y, y las grafica'''
    pl.scatter(x,y)

def generarIndividuo(cantidad,minx,maxx,miny,maxy):
    '''Genera un conjunto de centroides dado por la cantidad'''
    individuo = []
    for i in range(cantidad):
        x = random.randrange(minx,maxx)
        y = random.randrange(miny,maxy)
        individuo.append((x , y))
    return(individuo)

def generarPobaclionInicial(tamanoPoblacion,tamanoIndividuo,minx,maxx,miny,maxy):
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = generarIndividuo(tamanoIndividuo,minx,maxx,miny,maxy)
        poblacion.append(individuo)
    return poblacion

def calcularCentroide(punto,individuo):
    centroideMinimo = 0
    centroide = individuo[0]
    min = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
    for i in range(1,len(individuo)):
        centroide = individuo[i]
        dist = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
        if (dist < min):
            min = dist
            centroideMinimo = i

    return(centroideMinimo)

def asignarCentroide(punto, individuo, puntosEnIndividuo):
    posicionCentroide = calcularCentroide(punto,individuo)
    puntosEnIndividuo[posicionCentroide].append(punto)
    return puntosEnIndividuo

def evaluarFitness(individuo, puntosEnIndividuo):
    #recorro todos los puntos

    for i in range(len(individuo)):
        fitness = 0
        alelo = individuo[i]
        distancia = 0
        puntos = puntosEnIndividuo[i]
        # puntosEnIndividuo[j] es un punto de todos los puntos que pertenecen al individuo i

        for j in range(len(puntos)):
            punto = puntos[j]
            distancia = distancia + math.hypot(alelo[0]-punto[0],alelo[1]-punto[1])
        errorIndividuo = distancia / len(puntosEnIndividuo)
        fitness = fitness + errorIndividuo
    return fitness


dataset = leerTxt("C:\\Users\\Mati\\PycharmProjects\\geneticClustering\\Clusters\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))
tamanoIndividuo = 3

poblacion = generarPobaclionInicial(10,tamanoIndividuo,minx,maxx,miny,maxy)

puntosEnIndividuo = []
for i in range(tamanoIndividuo):
    puntosEnIndividuo.append([])

mejor = poblacion[0]
fitnesMejor= evaluarFitness(poblacion[0],puntosEnIndividuo)
puntosMejor = puntosEnIndividuo


for i in range(len(poblacion)):
    individuo = poblacion[0]

    for i in range(len(dataset)):
        punto = dataset[i]
        asignarCentroide(punto,individuo,puntosEnIndividuo)
        fitness = evaluarFitness(individuo,puntosEnIndividuo)

    if fitness < fitnesMejor:
        mejor = individuo
        fitnesMejor = fitness
        puntosMejor = puntosEnIndividuo

for i in range(len(mejor)):
    if puntosMejor[i]:
        puntosx, puntosy = zip(*puntosMejor[i])
        graficarPuntos(puntosx,puntosy)


xCentroides,yCentroides = zip(*individuo)
graficarPuntos(xCentroides,yCentroides)

pl.show()
