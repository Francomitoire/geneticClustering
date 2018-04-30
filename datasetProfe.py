import random
import math
import matplotlib.pyplot as pl
import random



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

def generarCentroides(cantidad,minx,maxx,miny,maxy):
    centroides = []
    for i in range(cantidad):
        x = random.randrange(minx,maxx)
        y = random.randrange(miny,maxy)
        centroides.append((x , y))

    return(centroides)

def calcularCentroide(punto,centroides):
    centroideMinimo = 0
    centroide = centroides[0]
    min = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
    for i in range(1,len(centroides)):
        centroide = centroides[i]
        dist = math.hypot(punto[0]-centroide[0],punto[1]-centroide[1])
        if (dist < min):
            min = dist
            centroideMinimo = i

    return(centroideMinimo)

def asignarCentroide(punto, centroides, puntosEnCentroide):
    posicionCentroide = calcularCentroide(punto,centroides)
    puntosEnCentroide[posicionCentroide].append(punto)
    return puntosEnCentroide



def funcionFitness(centroides, puntosEnCentroide):
    '''Recibe un conjunto de centroides y los puntos que pertenecen a ellos, y calcula la funcion fitness en base a la distancia euclidea '''
    distanciaTotal = 0
    #proceso un centroide
    for i in range(len(centroides)):
        centroide = centroides[i]
        puntos = puntosEnCentroide[i]
        distancia = 0
        for i in range(len(puntos)):
            punto = puntos[i]
            distancia = math.hypot(centroide[0]-punto[0],centroide[1]-punto[1])
            distanciaTotal = distanciaTotal + distancia
        fitness = distanciaTotal / len(puntos)
    return(fitness)

dataset = leerTxt("C:\\Users\\Mati\\PycharmProjects\\geneticClustering\\dataset01.txt")
x,y= zip(*dataset)


#-----------------------------------------------------------------

for i in range(1):

    centroides1 = generarCentroides(2,0,round(max(x)),0,round(max(y)))
    centroides2 =  generarCentroides(2,0,round(max(x)),0,round(max(y)))
    xCentroides,yCentroides = zip(*centroides1)
    xCentroides2,yCentroides2 = zip(*centroides2)

    puntosEnCentroide1 = []
    puntosEnCentroide2 = []

    for i in range(len(centroides1)):
        puntosEnCentroide1.append([])
        puntosEnCentroide2.append([])

    for i in range(len(dataset)):
        asignarCentroide(dataset[i], centroides1, puntosEnCentroide1)
        asignarCentroide(dataset[i],centroides2, puntosEnCentroide2)


    if funcionFitness(centroides1,puntosEnCentroide1) > funcionFitness(centroides2,puntosEnCentroide2):
        centroides = centroides1
        puntosEnCentroide = puntosEnCentroide1
    else:
        centroides = centroides2
        puntosEnCentroide = puntosEnCentroide2


for i in range(len(centroides)):
    if puntosEnCentroide[i]:
        puntosx, puntosy = zip(*puntosEnCentroide[i])
        graficarPuntos(puntosx,puntosy)

#print(funcionFitness(centroides,puntosEnCentroide))
#print(centroides[0])
#graficarPuntos(x,y)
#graficarPuntos(15,10)
graficarPuntos(xCentroides,yCentroides)

pl.show()