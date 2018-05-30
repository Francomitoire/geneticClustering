import math
import platform

import matplotlib.pyplot as pl
import random
import numpy as np
from copy import copy
import warnings


class Individuo(object):
    """
    El atributo valor es un conjunto de centroides
    """
    #ESTE ATRIBUTO TIENE QUE TENER EL MAYOR FITNESS DE TODA LA POBLACION EN TO DO MOMENTO
    # mayorFitness = 0


    def __init__(self):
        self.valor = None
        self.fitness = None
        self.puntos = []
        # self.copias = 0

    def setValorRandom(self, tam, mins, maxs, dimensiones, dataset):
        valor = []
        # para cada centroide del individuo
        for j in range(tam):
            cent_lt = []
            # para cada elemento del centroide seteo un valor random
            for i in range(dimensiones):
                x = random.randrange(mins[i], maxs[i])
                cent_lt.append(x)
            cent = tuple(cent_lt)
            valor.append(cent)
        self.valor = valor
        self.setPuntos(dataset)

    def setValor(self,valor):
        self.valor = valor

    def setFitness(self,valor):
        self.fitness = round(valor,4)

    def calcularError(self):
        #arreglar fitnes, colocar fitness = 99999 y colocar los if si no procesa ningun dato que quede esa fitness
        fitness = 0

        #por cada centroide..
        for i in range(len(self.valor)):
            errorCentroide = 0
            alelo = self.valor[i]
            # distancia = 0
            distancia2 = 0
            puntos = self.puntos[i]

            # puntos[j] es un punto de todos los puntos que pertenecen al individuo i
            for j in range(len(puntos)):
                punto = puntos[j]
                # distancia = distancia + math.hypot(alelo[0] - punto[0], alelo[1] - punto[1])
                punto1 = np.array(punto)
                punto2 = np.array(alelo)
                distancia2 = distancia2 + np.linalg.norm(punto2 - punto1)
            # print('dist1 '+ str(distancia) )
            # print('dist2 ' + str(distancia2) )
            errorCentroide = distancia2 / len(self.puntos)
            #print('error centroide '+str(i)+ ' :'+str(errorCentroide))
            fitness = fitness + errorCentroide
            #print('Fitness: ' + str(fitness))

        # if fitness > Individuo.mayorFitness:
        #     Individuo.mayorFitness = round(fitness,2)
        self.setFitness(fitness)
        #print('Fitness: ' + str(fitness))

    # def corregirFitness(self):
    #     self.fitness = 9999 - self.fitness

    def setPuntos(self,dataset):
        del self.puntos[:]
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
            lt = []
            for i in range(len(line)):
                num = float(line[i])
                lt.append(num)
            tupla = tuple(lt)
            salida.append(tupla)
        return(salida)

def graficarPuntos(x, y):
    '''Recibe como paraemtro todas las coords x, luego todas los coords y, y las grafica'''
    pl.scatter(x,y)


def generarPoblacionInicial(tamanoPoblacion,tamanoIndividuo,mins,maxs,dimensiones,dataset):
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = Individuo()
        individuo.setValorRandom(tamanoIndividuo,mins,maxs,dimensiones,dataset)
        poblacion.append(individuo)
    return poblacion


def calcularCentroide(punto,individuo):
    centroideMinimo = 0
    centroide = individuo.valor[0]
    punto1 = np.array(punto)
    punto2 = np.array(centroide)
    min = np.linalg.norm(punto2 - punto1)
    for i in range(1,len(individuo.valor)):
        centroide = individuo.valor[i]
        punto2 = np.array(centroide)
        dist = np.linalg.norm(punto2 - punto1)
        if (dist < min):
            min = dist
            centroideMinimo = i

    return(centroideMinimo)


def seleccionControlada(pob):
    poblacion = pob
    pob_salida = []
    n = len(poblacion)
    totalFitness = 0
    #print('len pob entrada')
    #print(len(pob))
    #calculo promedio fitness
    for ind in poblacion:
        totalFitness = totalFitness + ind.fitness
    promFitness = totalFitness / n
    #------------
    # si promfitnes == 0  quiere decir que hay solo un individuo y es el peor, entonces lo pasamos directo CHARLARLO CON MATI
    if promFitness == 0 :
        pob_salida = poblacion
        return pob_salida
    c = []
    copias = []

    for i in range(len(poblacion)):
        #guardo la parte entera del fitness sobre el promedio de fitness
        c.append(poblacion[i].fitness/promFitness)
        cant = int(c[i])
        #asigno esa parte entera en copias
        copias.append(cant)
        for j in range(cant):
            indiv = poblacion[i]
            pob_salida.append(indiv)


    while sum(copias) !=  len(poblacion):

        for i in range(len(poblacion)):
            probabilidad = abs(c[i])-abs(int(c[i]))
            copia = 0
            if random.uniform(0,1) <= probabilidad:
                copia = 1
                indiv = poblacion[i]
                pob_salida.append(indiv)

            copias[i] = copias[i] + copia
            if sum(copias) == len(poblacion):
                break
    # print('copias' + str(copias))
    return pob_salida

def seleccion(poblacion,preservar,porcentaje):


    if porcentaje == 0:
        return []

    cant = int(len(poblacion)*porcentaje)
    pob_elitista = []

    if cant > preservar:
        for i in range(preservar):
            pob_elitista.append(poblacion[i])

        pob_controlada = seleccionControlada(poblacion[preservar:cant])
        pob_salida = pob_elitista + pob_controlada
        return pob_salida

    elif cant == preservar:
        pob_salida = poblacion[0:preservar]
        return pob_salida

    else:
        warnings.warn_explicit('La cantidad a preservar debe ser menor o igual a la cantidad total a seleccionar')

def ordenarPoblacion(poblacion, atr):
    if atr == 'fitness':
        poblacion.sort(key=lambda individuo: individuo.fitness, reverse=True)
    if atr == 'copias':
        poblacion.sort(key=lambda individuo: individuo.copias, reverse=True)
    if atr == 'valor':
        poblacion.sort(key=lambda individuo: individuo.valor, reverse=True)



#SECCION FITNESS POBLACION ----------------------

def setFitnessPoblacion(poblacion):
    for ind in poblacion:
        ind.calcularError()

def calcularMayorFitness(poblacion):
    may = 0
    for ind in poblacion:
        # print(ind.fitness)

        if ind.fitness > may:
            may = ind.fitness
    return may

def corregirFitness(poblacion,mayor):
    for ind in poblacion:
        val = 1 - ind.fitness/mayor
        ind.setFitness(val)
        # print(ind.fitness)



def evaluarFitness(poblacion):
    setFitnessPoblacion(poblacion)
    may = calcularMayorFitness(poblacion)
    # print()
    corregirFitness(poblacion,may)

#-------------------------

def cruzaPoblacion(poblacion, porcentaje):
    #arreglar, que si la cantidad a cruzar es 4, no busque solo en [0,1,2,3] sino en toda la poblacion [0,...,len(pob)]
    '''Elegir siempre un porcentaje que de una cantidad par de individuos'''
    # poblacion = copy(pob)
    pob_salida = []
    cant_indiv = int(len(poblacion) * porcentaje)
    indices = lista_de_enteros(0, len(poblacion))
    lt = []
    for i in range(cant_indiv):
        x = random.choice(indices)
        indices = restar_listas(indices, [x])
        lt = lt + [x]
    while True:
        rand1 = random.choice(lt)
        lt = restar_listas(lt, [rand1])
        rand2 = random.choice(lt)
        lt = restar_listas(lt, [rand2])
        ind1 = copy(poblacion[rand1])
        ind2 = copy(poblacion[rand2])
        cruzaUnPunto(ind1,ind2)
        pob_salida.append(ind1)
        pob_salida.append(ind2)
        if not lt:
            break

    return pob_salida



def cruzaUnPunto(i1, i2):
    '''Cruza simple con punto de cruza aleatorio'''
    # print(ind1.valor)
    # print(ind2.valor)
    ind1 = i1
    ind2 = i2
    size = len(ind1.valor)
    cxpoint = random.randrange(1, size)
    # print('punto de cruza: '+ str(cxpoint) )
    valor1 = ind1.valor[:cxpoint] + ind2.valor[cxpoint:]
    valor2 = ind2.valor[:cxpoint] + ind1.valor[cxpoint:]
    ind1.setValor(valor1)
    ind2.setValor(valor2)
    # ind1.valor[cxpoint:], ind2.valor[cxpoint:] = ind2.valor[cxpoint:], ind1.valor[cxpoint:]
    # print(ind1.valor)
    # print(ind2.valor)
    return ind1, ind2

def imprimirPoblacion(pob):
    # copias = 0
    ordenarPoblacion(pob,'fitness')
    for i in range(len(pob)):
         print('Valor: '+str(pob[i].valor) + ' Fitness: '+ str(pob[i].fitness))
        # copias = copias + pob[i].copias
    #print('Cant individuos: ' + str(len(pob)))
    # print('Cant copias: ' + str(copias))

def lista_de_enteros(a, b):
    lt = []
    for i in range(a, b ):
        lt = lt + [i]
    return lt

def restar_listas(lt1, lt2):
    a = lt1
    b = lt2
    a = [item for item in a if item not in b]
    return a
def mainApp(cantidadIteraciones,tamanoIndividuo):

    if platform.system() == 'Windows':
        dataset = leerTxt("C:\\PythonProjects\\geneticClustering\\static\\archivos\\newdataset.txt")
    elif platform.system() =='Linux':
        dataset = leerTxt("\\Users\\geneticClustering\\Clusters\\static\\archivos\\newdataset.txt")
    puntos = []
    puntos = list(zip(*dataset))
    puntos_a_graficar = []
    puntos_a_graficar.append(puntos[0])
    puntos_a_graficar.append(puntos[1])
    cantidadIndividuos = 60
    dimensiones = len(puntos)
    mins = []
    maxs = []
    for dim in range(len(puntos)):
        mins.append(round(min(puntos[dim])))
        maxs.append(round(max(puntos[dim])))

    # cantidadIndividuos = 10
    # tamanoIndividuo = 3
    iteraciones = 2
    cantPreservar = 1
    porc_seleccion = 1
    porc_cruza = 0.2
    porc_mutacion = 0
    dimx_graficar = 0
    dimy_graficar = 1


    pob_anterior = []
    pob_siguiente = []



    mins = []
    maxs = []
    for dim in range(len(puntos)):
        mins.append(round(min(puntos[dim])))
        maxs.append(round(max(puntos[dim])))


    pob_anterior  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,mins,maxs,dimensiones,dataset)
    evaluarFitness(pob_anterior)
    # imprimirPoblacion(pob_anterior)
    ind_viejo = copy(pob_anterior[0])

    # tratar convergencia( ver si fitness no modifica % del anterior, si no mejora un % converge > return )
    for i in range(cantidadIteraciones):
        # print('iteracion '+str(i))
        pob_siguiente = seleccion(pob_anterior,1,porc_seleccion)
        evaluarFitness(pob_siguiente)
        pob_anterior = pob_siguiente

    imprimirPoblacion(pob_siguiente)
    ind_nuevo = pob_siguiente[0]
    #print(pob_sig[0].valor)
    #print(pob_anterior[0].valor)
    # return ind_nuevo, ind_viejo

    #------------------------------ Graficos


    ind = ind_nuevo
    ind2 = ind_viejo


    fig1 = pl.figure()
    fig2 = pl.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_title('Nuevo individuo, Fitness: '+str(ind.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))

    ax2 = fig2.add_subplot(111)
    ax2.set_title('Viejo individuo, Fitness: '+str(ind2.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))





    for i in range(len(ind.puntos)):
        if ind.puntos[i]:
            puntos_por_dimension = zip(*ind.puntos[i])
            puntos_por_dimension = list(puntos_por_dimension)
            px = puntos_por_dimension[dimx_graficar]
            py = puntos_por_dimension[dimy_graficar]
            ax1.scatter(px,py)

    for centroide in ind.valor:
        px = centroide[dimx_graficar]
        py = centroide[dimy_graficar]
        ax1.scatter(px,py)



    for i in range(len(ind2.puntos)):
        if ind2.puntos[i]:
            puntos_por_dimension = zip(*ind2.puntos[i])
            puntos_por_dimension = list(puntos_por_dimension)
            px = puntos_por_dimension[dimx_graficar]
            py = puntos_por_dimension[dimy_graficar]
            ax2.scatter(px,py)

    for centroide in ind2.valor:
        px = centroide[dimx_graficar]
        py = centroide[dimy_graficar]
        ax2.scatter(px,py)


    pl.show()

#  asd