import math
import matplotlib.pyplot as pl
import random
import numpy as np


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


    def setValorRandom(self,cantidad,minx,maxx,miny,maxy,dataset):
        individuo = []
        for i in range(cantidad):
            x = random.randrange(minx, maxx)
            y = random.randrange(miny, maxy)
            individuo.append((x, y))
        self.valor = individuo
        self.setPuntos(dataset)

    def setValor(self,valor,dataset):
        self.valor = valor
        self.setPuntos(dataset)

    def setFitness(self):
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
        self.fitness = 1000 - round(fitness,2)
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


def generarPoblacionInicial(tamanoPoblacion,tamanoIndividuo,minx,maxx,miny,maxy,dataset):
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = Individuo()
        individuo.setValorRandom(tamanoIndividuo,minx,maxx,miny,maxy,dataset)
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


def seleccionControlada(pob):
    poblacion = pob
    pob_salida = []
    n = len(poblacion)
    totalFitness = 0

    for ind in poblacion:
        totalFitness = totalFitness + ind.fitness

    promFitness = totalFitness / n
    c = []
    copias = []

    for i in range(len(poblacion)):
        c.append(poblacion[i].fitness/promFitness)
        cant= int(c[i])
        copias.append(int(cant))
        for j in range(cant):
            indiv = Individuo()
            indiv = poblacion[i]
            pob_salida.append(indiv)

    while sum(copias) !=  len(poblacion):

        for i in range(len(poblacion)):
            probabilidad = abs(c[i])-abs(int(c[i]))
            copia = 0
            if random.uniform(0,1) <= probabilidad:
                copia = 1
                indiv = Individuo()
                indiv = poblacion[i]
                pob_salida.append(indiv)
            copias[i] = copias[i] + copia
            if sum(copias) == len(poblacion):
                break
    print('copias' + str(copias))
    return pob_salida

def seleccion(poblacion,preservar,porcentaje):
    cant = int(len(poblacion)*porcentaje)
    if cant > preservar:
        pob_elitista = poblacion[0:preservar]
        pob_controlada = seleccionControlada(poblacion[preservar:cant])
        pob_salida = pob_elitista + pob_controlada
        ordenarPoblacion(pob_salida,'fitness')
        return pob_salida
    elif cant == preservar:
        pob_salida = poblacion[0:preservar]
        ordenarPoblacion(pob_salida, 'fitness')
        return pob_salida
    else:
        print('La cantidad a preservar debe ser menor o igual a la cantidad total a seleccionar')


def cruzaUnPunto(ind1, ind2):
    # print(ind1.valor)
    # print(ind2.valor)
    size = len(ind1.valor)
    cxpoint = random.randint(1, size - 1)
    valor1 = ind1.valor[:cxpoint] + ind2.valor[cxpoint:]
    valor2 = ind2.valor[:cxpoint] + ind1.valor[cxpoint:]
    ind1.setValor(valor1,dataset)
    ind2.setValor(valor2,dataset)
    # ind1.valor[cxpoint:], ind2.valor[cxpoint:] = ind2.valor[cxpoint:], ind1.valor[cxpoint:]
    # print(ind1.valor)
    # print(ind2.valor)


    return ind1, ind2

def ordenarPoblacion(poblacion, atr):
    if atr == 'fitness':
        poblacion.sort(key=lambda individuo: individuo.fitness, reverse=True)
    if atr == 'copias':
        poblacion.sort(key=lambda individuo: individuo.copias, reverse=True)

def evaluarFitness(poblacion):
    for ind in poblacion:
        ind.setFitness()

    ordenarPoblacion(poblacion, 'fitness')

    # for ind in poblacion:
    #     ind.corregirFitness()

def cruzaPoblacion(pob):
    poblacion = pob
    while True:
        ordenarPoblacion(poblacion,'copias')

        if poblacion[0].copias != 0:
            cruzaUnPunto(poblacion[0],poblacion[1])
            poblacion[0].copias = poblacion[0].copias - 1
            poblacion[1].copias = poblacion[1].copias - 1
        else:
            break
    return poblacion

def imprimirPoblacion(pob):
    # copias = 0
    ordenarPoblacion(pob,'fitness')
    for i in range(len(pob)):
        print('Fitness: '+ str(pob[i].fitness))
        # copias = copias + pob[i].copias
    print('Cant individuos: ' + str(len(pob)))
    # print('Cant copias: ' + str(copias))


dataset = leerTxt("C:\\Franco\\Facultad\\IA\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))
cantidadIndividuos = 10
tamanoIndividuo = 3
cantPreservar = 0
iteraciones = 1





pob_anterior  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,minx,maxx,miny,maxy,dataset)
pob_siguiente = []

evaluarFitness(pob_anterior)
imprimirPoblacion(pob_anterior)

for i in range(iteraciones):
    pob_siguiente = seleccion(pob_anterior,0,1)

print()
imprimirPoblacion(pob_siguiente)


# p = ''
# f = ''
#
#
# for ind in poblacion:
#     p = p + str(ind.valor)
#     f = f + str(ind.fitness) + '/'
# print(p)
# print(f)
# print(poblacion[0].valor)
# print(poblacion[0].fitness)
#




# p = ''
# f = ''
# for i in poblacion:
#     p = p + str(i.valor)
#     f = f + str(i.fitness) +'/'
# print(p)
# print(f)
# print(poblacion[0].valor)
# print(poblacion[0].fitness)

#
# ordenarPoblacion(poblacion, 'copias')
# pob = ''
# copias = ''
# fitness = ''
# for ind in poblacion:
#     pob = pob + str(ind.valor) + '////'
#     copias = copias + str(ind.copias) + '////'
#     fitness = fitness +  str(ind.fitness)+ '////'
# print(pob)
# print(copias)
# print(fitness)
# cruzaPoblacion(poblacion)
# pob = ''
# copias = ''
# fitness = ''
# evaluarFitness(poblacion)
# for ind in poblacion:
#     pob = pob + str(ind.valor) + '////'
#     copias = copias + str(ind.copias) + '////'
#     fitness = fitness + str(ind.fitness) + '////'
# print(pob)
# print(copias)
# print(fitness)












#------------------------------ Graficos

# individuo2 = pob_siguiente[0]
# individuo1 = pob_siguiente[len(pob_siguiente)-1]
#
# fig1 = pl.figure()
# fig2 = pl.figure()
# ax1 = fig1.add_subplot(111)
# ax1.set_title('Peor individuo, Fitness: '+str(individuo1.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))
#
# ax2 = fig2.add_subplot(111)
# ax2.set_title('Mejor individuo, Fitness: '+str(individuo2.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))
#
#
#
# for i in range(len(individuo1.puntos)):
#     if individuo1.puntos[i]:
#         px,py = zip(*individuo1.puntos[i])
#         ax1.scatter(px,py)
#
#
# for centroide in individuo1.valor:
#     px,py = centroide
#     ax1.scatter(px,py)
#
#
# for i in range(len(individuo2.puntos)):
#     if individuo2.puntos[i]:
#         px,py = zip(*individuo2.puntos[i])
#         ax2.scatter(px,py)
#
#
# for centroide in individuo2.valor:
#     px,py = centroide
#     ax2.scatter(px,py)
#
# pl.show()
