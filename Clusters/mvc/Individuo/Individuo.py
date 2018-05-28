import math
import random

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
        self.copias = 0

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
            Individuo.mayorFitness = round(fitness,2)
        self.fitness = round(fitness,2)
        #print('Fitness: ' + str(fitness))

    def corregirFitness(self):
        self.fitness = 9999 - self.fitness

    def setPuntos(self,dataset):
        for i in range(len(self.valor)):
            self.puntos.append([])

        for i in range(len(dataset)):
            punto = dataset[i]
            posicionCentroide = calcularCentroide(punto,self)
            self.puntos[posicionCentroide].append(punto)

def calcularCentroide(punto, individuo):
    centroideMinimo = 0
    centroide = individuo.valor[0]
    min = math.hypot(punto[0] - centroide[0], punto[1] - centroide[1])
    for i in range(1, len(individuo.valor)):
        centroide = individuo.valor[i]
        dist = math.hypot(punto[0] - centroide[0], punto[1] - centroide[1])
        if (dist < min):
            min = dist
            centroideMinimo = i

    return (centroideMinimo)