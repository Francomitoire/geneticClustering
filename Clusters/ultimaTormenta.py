import random
import math
import matplotlib.pyplot as pl
import random
import numpy as np
import easygui

class Individuo(object):
    """
    El atributo valor es un conjunto de centroides
    """
    #ESTE ATRIBUTO TIENE QUE TENER EL MAYOR FITNESS DE TODA LA POBLACION EN TO DO MOMENTO
    mayorFitness = 0

    def __init__(self):
        self.valor = None
        self.fitness = None
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
        #arreglar fitnes, colocar fitness = 99999 y colocar los if si no procesa ningun dato que quede esa fitness
        fitness = 0

        #por cada centroide..
        for i in range(len(self.valor)):
            errorCentroide = 0
            alelo = self.valor[i]
            distancia = 0
            puntos = self.puntos[i]

            # puntos[j] es un punto de todos los puntos que pertenecen al individuo i
            for j in range(len(puntos)):
                punto = puntos[j]
                distancia = distancia + math.hypot(alelo[0] - punto[0], alelo[1] - punto[1])

            errorCentroide = distancia / len(self.puntos)
            #print('error centroide '+str(i)+ ' :'+str(errorCentroide))
            fitness = fitness + errorCentroide
            #print('Fitness: ' + str(fitness))

        if fitness > Individuo.mayorFitness:
            Individuo.mayorFitness = fitness
        self.fitness = round(fitness,2)
        #print('Fitness: ' + str(fitness))

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
        return(salida)

def graficarPuntos(x, y):
    '''Recibe como paraemtro todas las coords x, luego todas los coords y, y las grafica'''
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

    return(centroideMinimo)


def seleccionControlada(poblacion):
    n = len(poblacion)
    totalFitness = 0

    for ind in poblacion:
        totalFitness = totalFitness + ind.fitness

    promFitness = totalFitness / n
    c = []
    copias = []

    for i in range(len(poblacion)):
        c.append(poblacion[i].fitness/promFitness)
        copias.append(int(c[i]))

    while sum(copias) !=  len(poblacion):

        for i in range(len(poblacion)):
            probabilidad = abs(c[i])-abs(int(c[i]))
            copia = 0
            if random.uniform(0,1) <= probabilidad:
                copia = 1
            copias[i] = copias[i] + copia
            if sum(copias) == len(poblacion):
                break



dataset = leerTxt("C:\\Franco\\Facultad\\IA\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))
cantidadIndividuos = 1000
tamanoIndividuo = 2


poblacion  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,minx,maxx,miny,maxy)




for ind in poblacion:
    ind.setFitness()

poblacion.sort(key = lambda individuo: individuo.fitness)


seleccionControlada(poblacion)



print(poblacion[len(poblacion)-1].fitness)

ind = poblacion[0]
ind2 = poblacion[len(poblacion)-1]

fig1 = pl.figure()
fig2 = pl.figure()
ax1 = fig1.add_subplot(111)
ax1.set_title('Mejor individuo, Fitness: '+str(ind.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))

ax2 = fig2.add_subplot(111)
ax2.set_title('Peor individuo, Fitness: '+str(ind2.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))
print(ind.fitness)


for i in range(len(ind.puntos)):
    if ind.puntos[i]:
        px,py = zip(*ind.puntos[i])
        ax1.scatter(px,py)

for centroide in ind.valor:
    px,py = centroide
    ax1.scatter(px,py)


for i in range(len(ind2.puntos)):
    if ind2.puntos[i]:
        px,py = zip(*ind2.puntos[i])
        ax2.scatter(px,py)

for centroide in ind.valor:
    px,py = centroide
    ax2.scatter(px,py)



pl.show()
