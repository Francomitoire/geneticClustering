import math
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


    def setValorRandom(self,cantidad,minx,maxx,miny,maxy,dataset):
        individuo = []
        for i in range(cantidad):
            x = random.randrange(minx, maxx)
            y = random.randrange(miny, maxy)
            individuo.append((x, y))
        self.valor = individuo
        self.setPuntos(dataset)

    def setValor(self,valor):
        self.valor = valor


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
        self.fitness = 2000 - round(fitness,2)
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

def evaluarFitness(poblacion):
    for ind in poblacion:
        ind.setFitness()


    # for ind in poblacion:
    #     ind.corregirFitness()

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
    print('Cant individuos: ' + str(len(pob)))
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


dataset = leerTxt("C:\\Franco\\Facultad\\IA\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))
cantidadIndividuos = 10
tamanoIndividuo = 2
iteraciones = 1000
cantPreservar = 1
porc_seleccion = 0.2
porc_cruza = 0.8
porc_mutacion = 0

#
# pob_anterior = []
# pob_siguiente = []
#
# pob_anterior  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,minx,maxx,miny,maxy,dataset)
# evaluarFitness(pob_anterior)
# print('Poblacion anterior')
# imprimirPoblacion(pob_anterior)
#
#
#
# print()
#
# for i in range(iteraciones):
#     pob_siguiente = seleccion(pob_anterior,cantPreservar,porc_seleccion)
#     pob_siguiente = pob_siguiente + cruzaPoblacion(pob_anterior,porc_cruza)
#     evaluarFitness(pob_siguiente)
#
#     pob_anterior = pob_siguiente
#
#
#
#
#
# print()
# print('pob sig')
# imprimirPoblacion(pob_siguiente)


pob_anterior  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,minx,maxx,miny,maxy,dataset)
evaluarFitness(pob_anterior)
imprimirPoblacion(pob_anterior)
ind_viejo = copy(pob_anterior[0])
print(ind_viejo.fitness)

for i in range(iteraciones):
    pob_sig = seleccion(pob_anterior,1,0.2) + cruzaPoblacion(pob_anterior,porc_cruza)
    evaluarFitness(pob_sig)
    pob_anterior = pob_sig



imprimirPoblacion(pob_sig)
ind_nuevo = pob_sig[0]
print(ind_nuevo.fitness)






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


individuo1 = ind_nuevo
individuo2 = ind_viejo

fig1 = pl.figure()
fig2 = pl.figure()
ax1 = fig1.add_subplot(111)
ax1.set_title('Nuevo individuo, Fitness: '+str(individuo1.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))

ax2 = fig2.add_subplot(111)
ax2.set_title('Viejo individuo, Fitness: '+str(individuo2.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))



for i in range(len(individuo1.puntos)):
    if individuo1.puntos[i]:
        px,py = zip(*individuo1.puntos[i])
        ax1.scatter(px,py)


for centroide in individuo1.valor:
    px,py = centroide
    ax1.scatter(px,py)


for i in range(len(individuo2.puntos)):
    if individuo2.puntos[i]:
        px,py = zip(*individuo2.puntos[i])
        ax2.scatter(px,py)


for centroide in individuo2.valor:
    px,py = centroide
    ax2.scatter(px,py)

pl.show()
