import random

import math


class Individuo(object):

    def __init__(self):
        self.valor = None
        self.fitness = None
        self.centroide = None

    def setValor(self,cantidad,minx,maxx,miny,maxy):
        individuo = []
        for i in range(cantidad):
            x = random.randrange(minx, maxx)
            y = random.randrange(miny, maxy)
            individuo.append((x, y))
        self.valor = individuo

    def setFitness(self,dataset,puntosEnIndividuo):
        for i in range(len(self.valor)):
            fitness = 0
            alelo = self.valor[i]
            distancia = 0
            puntos = puntosEnIndividuo[i]

            # puntosEnIndividuo[j] es un punto de todos los puntos que pertenecen al individuo i

            for j in range(len(puntos)):
                punto = puntos[j]
                distancia = distancia + math.hypot(alelo[0] - punto[0], alelo[1] - punto[1])
            errorIndividuo = distancia / len(puntosEnIndividuo)
            fitness = fitness + errorIndividuo





