# -*- coding: utf-8 -*-
from operator import add
import Clusters.clusterPrueba as funciones
"""
Introducción a los Algoritmos Geneticos
Autor: Guillermo Izquierdo
Este código es para fines educativos exclusivamente.

"""

geneSet = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ '
target = 'Matias Zaracho'

import datetime
import random

random.seed(2)
startTime = datetime.datetime.now()


# Funcion para generar de manera aleatoria una muestra de genes
def generate_parent(length):
    genes = []  # Lista donde se almacenan las secuencia aleatoria
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet)) # Eligo la longitud minima entre la ingresada y la longitud de mi geneSet
        #print("SampleSize: " + str(sampleSize))
        genes.extend(random.sample(geneSet, sampleSize))  # Obtención de la muestra aleatoria, extiendo el array con el string aleatorio generado
        #print(random.sample(geneSet,sampleSize))
        #print(genes)
        #print(random.sample(geneSet, sampleSize))
        #print(genes)
    return ''.join(genes)  # Regresamos una cadena


# Funcion de optimización, si el nuestra muestra aleatoria tiene un caracter igual y en la misma posicion a nuestro target
def get_fitness(guess):
    return sum(1 for expected, actual in zip(target, guess) if expected == actual) #lista por comprension zip('ho,'ch) = (h,c), (o,h)


# Funcion para mutar a nuestra cadena original o padre
# Muta un string de entrada. Ej: Entrada = Franco, Salida = FTanco
def mutate(parent):
    index = random.randrange(0, len(parent)) # index es el lugar donde se realizara la mutacion
    #print('Index: ' + str(index))
    childGenes = list(parent)
    #print('childGenes: '+ str(childGenes))
    newGene, alternate = random.sample(geneSet, 2)
    #print('newGene: '+ newGene + ' alternate: ' + alternate)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    #print(childGenes)
    #print('---------------------')
    return ''.join(childGenes)


# Funcion para imprimir en pantalla los resultados
def display(guess):
    timeDiff = datetime.datetime.now() - startTime
    fitness = get_fitness(guess)
    print('{}\t{}\t{}'.format(guess, fitness, timeDiff))


# Inicializamos nuestros parametros

bestParent = generate_parent(len(target))
print('bestParen: '+ bestParent + ' Longitud: '+ str(len(bestParent)))
bestFitness = get_fitness(bestParent)
print('bestFitness: ' + str(bestFitness))
display(bestParent)

# Creamos un ciclo para iterar nuestras funciones
# Hasta obtener nuestro target
while True:
    child = mutate(bestParent)
    childFitness = get_fitness(child)
    #si nuestro Fitness padre es mejor que el hijo, simplemente descartamos el hijo
    if bestFitness >= childFitness:
        continue
    display(child)
    #Si el fitness es 100% es decir, se muto a la palabra buscada, entonces termina to do.
    if childFitness >= len(bestParent) :
        break
    bestFitness = childFitness
    bestParent = child

#print(funciones.leerTxt(funciones.dir))





