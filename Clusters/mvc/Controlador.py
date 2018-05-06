from Individuo import Individuo
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


def generarPoblacionInicial(tamanoPoblacion,tamanoIndividuo,minx,maxx,miny,maxy):
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = Individuo()
        individuo.setValorRandom(tamanoIndividuo,minx,maxx,miny,maxy)
        individuo.setPuntos(dataset)
        poblacion.append(individuo)
    return poblacion


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
    for i in range(len(poblacion)):
        poblacion[i].copias = copias[i]

def seleccionElitista(poblacion,preservar):
    seleccionControlada(poblacion)
    pobElitista = poblacion[0:preservar]
     # p = ''
     # for ind in pobElitista:
     #     p = p + str(ind.valor)
     # print(p)
    pobCruzar = poblacion[preservar:]
     # p = ''
     # for ind in pobCruzar:
     #     p = p + str(ind.valor)
     # print(p)
    pobCruzada = cruzaPoblacion(pobCruzar)
     # p = ''
     # for ind in pobCruzada:
     #     p = p + str(ind.valor)
     # print(p)
    pob = pobElitista + pobCruzada
     # p = ''
     # for ind in pob:
     #     p = p + str(ind.valor)
     # print(p)
    return pob


def cruzaUnPunto(ind1, ind2):
    size = len(ind1.valor)
    cxpoint = random.randint(1, size - 1)
    ind1.valor[cxpoint:], ind2.valor[cxpoint:] = ind2.valor[cxpoint:], ind1.valor[cxpoint:]


    return ind1, ind2

def ordenarPoblacion(poblacion, atr):
    if atr == 'fitness':
        poblacion.sort(key=lambda individuo: individuo.fitness)
    if atr == 'copias':
        poblacion.sort(key=lambda individuo: individuo.copias, reverse=True)

def evaluarFitness(poblacion):
    for ind in poblacion:
        ind.setFitness()

    ordenarPoblacion(poblacion, 'fitness')

    for ind in poblacion:
        ind.corregirFitness()

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


dataset = leerTxt("C:\\Franco\\Facultad\\IA\\dataset01.txt")
x, y = zip(*dataset)
maxx = round(max(x))
maxy = round(max(y))
minx = round(min(x))
miny = round(min(y))
cantidadIndividuos = 2000
tamanoIndividuo = 2
cantPreservar = 0
iteraciones = 20




poblacion  = generarPoblacionInicial(cantidadIndividuos,tamanoIndividuo,minx,maxx,miny,maxy)

evaluarFitness(poblacion)
print('primer mejor' + str(poblacion[0].fitness))

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


for ind in range(iteraciones):
    poblacion = seleccionElitista(poblacion,cantPreservar)


evaluarFitness(poblacion)

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





individuo2 = poblacion[0]
individuo1 = poblacion[len(poblacion)-1]
print(poblacion[0].fitness)

fig1 = pl.figure()
fig2 = pl.figure()
ax1 = fig1.add_subplot(111)
ax1.set_title('Peor individuo, Fitness: '+str(individuo1.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))

ax2 = fig2.add_subplot(111)
ax2.set_title('Mejor individuo, Fitness: '+str(individuo2.fitness)+' -'+' Individuos: '+str(cantidadIndividuos))



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
