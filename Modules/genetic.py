import matplotlib.pyplot as pl
import time
import random
import numpy as np
from copy import copy
import warnings
import plotly
import plotly.graph_objs as go
import pandas as pd
import sklearn.metrics


class Individuo(object):
    """El atributo valor representa la estructura del individuo. Es un conjunto de centroides"""


    def __init__(self):

        #el atributo valor contiene los falsos centroides mediante los cuales se asignan los puntos al mas cercano
        self.valor = None
        #el atributo centroides tiene los verdaderos centroides de las clases
        # self.centroides = None
        self.fitness = None
        # self.fitnessReal = None
        self.puntos = []
        self.ssw_centroides = []
        self.ssb_centroides = []

        # self.copias = 0

    def setValorRandom(self, tam, mins, maxs, dimensiones, dataset):
        '''Recibe como parametro el tamaño deseado del individuo, las coordenadas minimas y maximas de un dataset
        previamente cargadas, la cantidad de dimensiones, y el dataset
        de donde se cargaron las coordenadas minimas y maximas'''

        valor = []
        #En base al tamaño ingresado, crea una cantidad 'tam' de centroides
        for j in range(tam):
            cent_lt = []
            #En base al valor 'dimensiones', crea valores random dentro de un min y max para ese centroide
            for i in range(dimensiones):
                x = random.randrange(mins[i], maxs[i])
                cent_lt.append(x)
            cent = np.array(cent_lt)
            valor.append(cent)
        self.setValor(valor,dataset)


    def setValor(self,valor,dataset):
        '''Setea el valor del individuo y seguidamente agrupa los puntos'''
        self.valor = valor
        self.setPuntos(dataset)

    def setFitness(self,valor):
        self.fitness = round(valor,4)

    def calcularFitness(self,media,n):
        '''Calcula la fitness del individuo, para el cual se utilizo el indice Calinski y Harabasz
            Recibe como parametro la media del dataset y la cantidad de puntos y setea la fitness'''

        #Calculo la separacion inter clusters mediante 'suma de los cuadrados entre'
        ssb = self.calcularSsb(media)

        #Calculo la cohesion interna de los clusters mediante la 'suma de los cuadrados dentro'
        ssw = self.calcularSsw(self.valor)


        #Si algun centroide no contiene puntos, asigno la peor fitness al individuo
        if 0 in self.ssb_centroides:
            self.setFitness(0)
        #De lo contrario, calculo el indice Calinski y Harabasz
        else:
            #k es el numero de clusters
            k = len(self.puntos)
            a = ssb / (k-1)
            b = ssw / (n-k)
            fit = round(a/b,4)
            self.setFitness(fit)



    def calcularSsb(self,media):
        '''Medida de separacion para evaluar la distancia inter clusters. Sum of Squared Between
        Recibe como parametro la media del dataset y devuelve el SSB'''
        ssb = 0

        #por cada centroide calculo el 'Sum of squared between' y acumulo
        for i in range(len(self.valor)):
            #n es el numero de elementos en el cluster i
            n = len(self.puntos[i])
            centroide = self.valor[i]
            dist = np.linalg.norm(centroide-media)
            exp = n * (dist**2)
            self.ssb_centroides.append(exp)
            ssb = ssb + exp
        return ssb

    def calcularSsw(self,valores):
        '''Medida usada para evaluar la cohesion de los clusteres que el algoritmo ha generado
        Recibe como parametro los centroides y devuelve el SSW'''
        ssw = 0

        # por cada centroide
        for i in range(len(valores)):

            ssw_centroide = 0

            #punto 2 contiene el centroide i
            punto2 = valores[i]

            distancia2 = 0
            # puntos_en_centroide contiene los puntos asignados al centroide i
            puntos_en_centroide = self.puntos[i]

            #Si el centroide tiene al menos un punto, se calcula su SSW
            if (len(puntos_en_centroide) != 0):

                for j in range(len(puntos_en_centroide)):
                    punto1 = puntos_en_centroide[j]
                    dist = np.linalg.norm(punto2 - punto1)
                    distancia2 = distancia2 + (dist**2)

                ssw_centroide = distancia2
            else:
            #De lo contrario se le asigna 0
                ssw_centroide = 0

            self.ssw_centroides.append(ssw_centroide)
            ssw = ssw + ssw_centroide

        return ssw

    def setPuntos(self,dataset):
        '''Setea los puntos del dataset, agrupandolos al centroide mas cercano'''
        del self.puntos[:]

        #Crea una lista de arreglos en base a la cantidad de clusters
        for i in range(len(self.valor)):
            self.puntos.append([])

        #seteo de puntos con un desarrollo propio
        if uso_lib == 0:
            for i in range(len(dataset)):
                #punto representa un punto del dataset
                punto = dataset[i]
                posicionCentroide = calcularCentroide(punto,self)
                self.puntos[posicionCentroide].append(punto)

        #seteo de puntos con libreria SKLearn
        else:
            particion = sklearn.metrics.pairwise_distances_argmin(dataset, self.valor)
            for i in range(len(dataset)):
                punto = dataset[i]
                pos = particion[i]
                self.puntos[pos].append(punto)




#FUNCIONES EN GENERAL

def leerTxt(path):
    '''Lee un txt donde cada linea esta conformada por n dimensiones y convierte cada linea en un arreglo de n elementos'''
    with open(path, 'r') as file:
        data = file.read()
        lines = data.splitlines()
        salida = []
        for line in lines:
            line = line.split()
            lt = []
            for i in range(len(line)):
                num = float(line[i])
                lt.append(num)
            arr = np.array(lt)
            salida.append(arr)
        return(salida)


def calcularMedia(dataset):
    '''Recibe como parametro un dataset, y devuelve la media del mismo'''

    sum = 0
    for punto in dataset:
        sum = sum + np.array(punto)
    prom = sum/len(dataset)
    # tup = tuple(prom)
    arr = np.array(prom)
    return arr


def generarPoblacionInicial(tamanoPoblacion,tamanoIndividuo,mins,maxs,dimensiones,dataset):
    '''Recibe como parametro la cantidad de individuos, el tamaño de cada individuo, los valores minimos y maximos
    aceptados, la cantidad de dimensiones y el dataset. Devuelve una lista de individuos con coordenadas random'''
    poblacion = []
    for i in range(tamanoPoblacion):
        individuo = Individuo()
        individuo.setValorRandom(tamanoIndividuo,mins,maxs,dimensiones,dataset)
        poblacion.append(individuo)
    return poblacion


def calcularCentroide(punto,individuo):
    '''Recibe como parametro un punto y un individuo y devuelve el indice del centroide mas cercano'''
    centroideMinimo = 0
    centroide = individuo.valor[0]
    min = np.linalg.norm(centroide - punto)

    for i in range(1,len(individuo.valor)):
        centroide = individuo.valor[i]
        dist = np.linalg.norm(centroide - punto)
        if (dist < min):
            min = dist
            centroideMinimo = i

    return(centroideMinimo)

#OPERADORES

def seleccionRanking(pob):
    '''Recibe como parametro una lista de individuos que debe haber sido previamente ordenada por la fitness.
    La poblacion de entrada debe tener como minimo 6 elementos para que devuelva una cantidad igual de individuos, ya que
    la seleccion por ranking trabaja de esta forma.
    Devuelve una lista de individuos de la misma longitud que la lista de entrada'''

    pob_entrada = pob
    pob_salida = []
    #rmin es la cantidad de copias asignadas al peor individuo
    rmin = 0
    copias = []
    n = len(pob_entrada)
    for i in range(n):
    #Se asignan las parte entera de 'c' a los individuos
        indi = i+1
        #c es la cantidad de copias asignadas al individuo i
        c = rmin + 2*(n-indi)*(1-rmin)/(n-1)

        #cant guarda la parte entera del calculo 'c'
        cant = int(c)

        #La lista copias guarda la parte decimal de 'c' del individuo i
        copias.append((round(c-int(c),2)))

        #se asignan una cantidad igual a la parte entera de 'c' del individuo i a la poblacion de salida
        for j in range(cant):
            pob_salida.append(pob_entrada[i])

    faltante = len(pob_entrada) - len(pob_salida)
    #Para completar la longitud de la poblacion de entrada, se asignan individuos seleccionando los mas probables
    #La probabilidad utilizada es la parte decimal del calculo de 'c'
    for i in range(faltante):
        ind = copias.index(max(copias))
        pob_salida.append(pob_entrada[ind])
        copias[ind] = 0
    return pob_salida


def seleccion(poblacion,preservar,cant_seleccion):
    '''Recibe como parametro una lista de individuos, la cantidad de individuos que se desean preservar con seleccion
    elitista, y la cantidad total de seleccion.
    La cantidad a preservar debe ser menor o igual a cant_seleccion.
    Devuelve una lista de individuos de longitud cant_seleccion '''

    if cant_seleccion == 0:
        return []

    #cant es la cantidad de individuos a seleccionar
    cant = cant_seleccion
    pob_elitista = []

    if cant > preservar:
        for i in range(preservar):
            pob_elitista.append(poblacion[i])

        pob_controlada = seleccionRanking(poblacion[preservar:cant])

        #la poblacion de salida esta constituida por los individuos preservados y por los seleccionados pro ranking
        pob_salida = pob_elitista + pob_controlada
        return pob_salida

    #De los seleccionados, se preservar todos
    elif cant == preservar:
        pob_salida = poblacion[0:preservar]
        return pob_salida

    else:
        warnings.warn_explicit('La cantidad a preservar debe ser menor o igual a la cantidad total a seleccionar')



def mutacion(poblacion, cant_mutacion, mins, maxs, dataset):
    '''Recibe como parametro una lista de individuos, la cantidad deseada de individuos a mutar, los valores minimos y maximos
    dentro de los cuales pueden mutar, y el dataset.
    Devuelve como salida una lista de los individuos mutados de longitud cant_mutacion'''
    pob_salida = []
    cant_indiv = cant_mutacion

    #indices contiene numeros de 0 al total de la poblacion
    indices = lista_de_enteros(0, len(poblacion))
    lt = []

    #Por la cantidad de individuos a mutar, se almacena individuos aleatorios en una lista 'lt'
    for i in range(cant_indiv):
        x = random.choice(indices)
        indices = restar_listas(indices, [x])
        lt = lt + [x]

    #Por cada individuo seleccionado aleatoriamente se lo muta y se lo agrega a la poblacion de salida
    #hasta que no queden individuos por mutar en 'lt'
    while(True):
        rd = random.choice(lt)
        lt = restar_listas(lt, [rd])
        ind = (poblacion[rd])
        nuevo_ind = mutar(ind,mins,maxs,dataset)
        pob_salida.append((nuevo_ind))
        if not lt:
            break
    return pob_salida

def mutar(ind,mins,maxs,dataset):
    '''Mutacion simple de un punto.
    Recibe como parametro el individuo a mutar, los valores dentro de los cuales puede mutar, y el dataset.
    El dataset se recibe ya que una vez que cambian los centroides, se debe setear el dataset para ese individuo.
    Retorna un nuevo individuo que tiene un centroide mutado de diferencia con el individuo de entrada'''

    nuevo_ind = Individuo()
    valor = copy(ind.valor)
    cant_atributos = len(valor)
    #puntero es el punto de cruza
    puntero = random.randrange(0,cant_atributos)

    #cant_alelos tiene la cantidad de dimensiones de un centroide
    cant_alelos = len(valor[puntero])

    a = []
    #Se crea un nuevo centroide
    for i in range(0,cant_alelos):
        a.append(random.randrange(mins[i],maxs[i]))

    a = np.array(a)
    new_atributo = a

    #a la posicion 'puntero' del conjunto de centroides, se le asigna el nuevo centroide
    valor[puntero] = new_atributo

    nuevo_ind.setValor(valor,dataset)
    return nuevo_ind

def cruzaPoblacion(poblacion, cant_cruza, dataset):
    '''Recibe como parametro una lista de individuos, la cantidad deseada de individuos a cruzar, y el dataset.
    Devuelve una lista de individuos de longitud cant_cruza.
    El parametro cant_cruza debe ser par, ya que el algoritmo trabaja cruzando pares que no han sido cruzados'''

    if cant_cruza % 2 != 0 :
        warnings.warn_explicit('La cantidad a cruzar debe ser par')
    else:

        pob_salida = []
        cant_indiv = cant_cruza
        indices = lista_de_enteros(0, len(poblacion))
        lt = []
        for i in range(cant_indiv):
            x = random.choice(indices)
            indices = restar_listas(indices, [x])
            lt = lt + [x]
        while True:
            #selecciona aleatoriamente 2 individuos de la poblacion de entrada para cruzarlos y los elimina de la lista
            #para no volver a seleccionarlos
            rand1 = random.choice(lt)
            lt = restar_listas(lt, [rand1])
            rand2 = random.choice(lt)
            lt = restar_listas(lt, [rand2])
            ind1 = poblacion[rand1]
            ind2 = poblacion[rand2]
            ind1_cruzado, ind2_cruzado = cruzaUnPunto(ind1,ind2,dataset)
            pob_salida.append(ind1_cruzado)
            pob_salida.append(ind2_cruzado)
            if not lt:
                break
        return pob_salida

def cruzaUnPunto(i1, i2,dataset):
    '''Cruza simple con punto de cruza aleatorio.
    Recibe como parametro dos individuos.
    Devuelve dos nuevos individuos'''
    # print(ind1.valor)
    # print(ind2.valor)
    ind1 = Individuo()
    ind2 = Individuo()
    size = len(i1.valor)
    cxpoint = random.randrange(1, size)
    # print('punto de cruza: '+ str(cxpoint) )
    valor1 = (i1.valor[:cxpoint] + i2.valor[cxpoint:])
    valor2 = (i2.valor[:cxpoint] + i1.valor[cxpoint:])
    ind1.setValor(valor1,dataset)
    ind2.setValor(valor2,dataset)

    # ind1.valor[cxpoint:], ind2.valor[cxpoint:] = ind2.valor[cxpoint:], ind1.valor[cxpoint:]
    # print(ind1.valor)
    # print(ind2.valor)
    return ind1, ind2



def ordenarPoblacion(poblacion):
    '''Ordena la poblacion de mayor a menor en base a la fitness'''
    poblacion.sort(key=lambda individuo: individuo.fitness,reverse=True)


def setFitnessPoblacion(poblacion,media,n):
    '''Recibe como parametro una lista de individuos, la media del dataset y la cantidad de puntos del dataset.
    Setea la fitness de cada individuo que no haya sido seteado.'''
    for ind in poblacion:
        if not ind.fitness:
           ind.calcularFitness(media,n)




def imprimirPoblacion(pob):
    '''Ordena la poblacion e imprime los individuos, sus fitness, y la cantidad de individuos'''
    # copias = 0
    ordenarPoblacion(pob)
    for i in range(len(pob)):
        print('Valor: '+str(pob[i].valor) + ' Fitness: '+ str(pob[i].fitness))
    print('Cant individuos: ' + str(len(pob)))

def lista_de_enteros(a, b):
    '''Crea una lista de enteros de a y b, sin incluir b'''
    lt = []
    for i in range(a, b ):
        lt = lt + [i]
    return lt

def restar_listas(lt1, lt2):
    '''Resta de la lista lt1 la lista lt2'''
    a = lt1
    b = lt2
    a = [item for item in a if item not in b]
    return a

def setUsoLib(bool=0):
    '''Setear a 0 para no usar librerias, setear a uno para usar libreria SKLearn en setPuntos '''
    global uso_lib
    uso_lib = bool

def mainApp(cantidadIndividuos,iteraciones, tamanoIndividuo,dimx_graficar,dimy_graficar,lib,porc_seleccion,porc_cruza,porc_mutacion):
    '''Algoritmo principal. Recibe como parametro la cantidad de iteraciones, el tamaño deseado de individuos, las dimensiones a graficar,
    y 1 si se desea usar libreria, 0 en caso contrario.'''
    setUsoLib(lib)
    cantPreservar = 1

    porc_seleccion = porc_seleccion/100
    porc_cruza = porc_cruza/100
    porc_mutacion = porc_mutacion/100


    cant_seleccion = int(cantidadIndividuos * porc_seleccion)
    cant_cruza = int(cantidadIndividuos * porc_cruza)
    cant_mutacion = int(cantidadIndividuos * porc_mutacion)


    tic = time.clock()
    dataset = leerTxt("C:\\PythonProjects\\geneticClustering\\static\\archivos\\newdataset.txt")
    media_dataset = calcularMedia(dataset)
    n = len(dataset)
    puntos = list(zip(*dataset))
    puntos_a_graficar = []
    puntos_a_graficar.append(puntos[0])
    puntos_a_graficar.append(puntos[1])
    dimensiones = len(puntos)
    mins = []
    maxs = []
    for dim in range(len(puntos)):
        mins.append(round(min(puntos[dim])))
        maxs.append(round(max(puntos[dim])))


    if porc_mutacion + porc_cruza + porc_seleccion != 1:
        print("LOS PORCENTAJES ESTAN MAL")

    if cant_cruza % 2 != 0:
        # print('se ha forzado la cruza')
        cant_cruza = cant_cruza + 1
        cantidadIndividuos = cantidadIndividuos + 1


    pob_anterior = generarPoblacionInicial(cantidadIndividuos, tamanoIndividuo, mins, maxs, dimensiones, dataset)
    pob_siguiente = []
    setFitnessPoblacion(pob_anterior, media_dataset, n)


    ordenarPoblacion(pob_anterior)
    ind_viejo = copy(pob_anterior[0])

    for i in range(iteraciones):
        pob_sel = seleccion(pob_anterior, cantPreservar, cant_seleccion)

        pob_cru = cruzaPoblacion(pob_anterior, cant_cruza,dataset)

        pob_mut = mutacion(pob_anterior, cant_mutacion, mins, maxs, dataset)

        pob_siguiente = pob_sel + pob_cru + pob_mut

        setFitnessPoblacion(pob_siguiente, media_dataset, n)

        pob_anterior = pob_siguiente
        ordenarPoblacion(pob_anterior)

    ordenarPoblacion(pob_siguiente)
    ind_nuevo = pob_siguiente[0]
    # print('ssb por centroide', ind_nuevo.ssb_centroides)
    # print('ssw por centroide', ind_nuevo.ssw_centroides)
    #
    # for grupo in ind_nuevo.puntos:
    #     print(len(grupo))

    # ------------------------------ Graficos
    toc = time.clock()
    tiempo = round(toc - tic, 2)

    #TABLA--------------------------------------------------

    columns = []
    for i in range(tamanoIndividuo):
        columns.append('Clase ' + str(i + 1))
    #
    # trace = go.Table(
    #     header=dict(values=columns,
    #                 fill=dict(color='#C2D4FF'),
    #                 align=['left'] * 5),
    #     cells=dict(values=ind_nuevo.puntos,
    #                fill=dict(color='#F5F8FF'),
    #                align=['left'] * 5))
    #
    # data = [trace]
    # plotly.offline.plot(data, filename='tabla_cluster.html')

    #-----

    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    colors = []
    for i in range(len(ind_nuevo.puntos[i])):
        if i%2 == 0:
            colors.append(rowEvenColor)
        else:
            colors.append(rowOddColor)
    trace = go.Table(
        type='table',
        header=dict(
            values=columns,
            line=dict(color='#506784'),
            fill=dict(color=headerColor),
            align=['center'],
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=ind_nuevo.puntos,
            line=dict(color='#506784'),
            fill=dict(color=[colors]),
            align=['center'],
            font=dict(color='#506784', size=11)
        ))

    data = [trace]
    plotly.offline.plot(data, filename='tabla_cluster.html')


    #GRAFICO------------------------------------------------

    data2 = []
    tracei = []
    for i in range(len(ind_nuevo.puntos)):
        if ind_nuevo.puntos[i]:
            puntos_por_dimension1 = zip(*ind_nuevo.puntos[i])
            puntos_por_dimension1 = list(puntos_por_dimension1)
            px1 = puntos_por_dimension1[dimx_graficar]
            py1 = puntos_por_dimension1[dimy_graficar]

            tracei.append(go.Scatter(
                x=px1,
                y=py1,
                name=columns[i],
                mode='markers',
                marker=dict(
                    size=10,
                    line=dict(
                        width=2,
                        color='rgb(0, 0, 0)'
                    )
                )
            ))

            data2.append(tracei[i])



    layout = dict(title='Fitness Solución: ' + str(ind_nuevo.fitness) + ' -' + ' Individuos: ' + str(cantidadIndividuos)+' - '+' Generaciones: '+str(iteraciones)+' Tiempo consumido: '+str(tiempo)+' segs.' ,
                  yaxis=dict(zeroline=False),
                  xaxis=dict(zeroline=False)
                  )


    fig = dict(data=data2, layout=layout)



    fig1 = dict(data=data2, layout=layout)
    plotly.offline.plot(fig1, filename='grafico_clusters.html')




# setUsoLib(1)
#
# tic = time.clock()
# mainApp(1,4,0,1,0,10,80,10)
# toc = time.clock()
# print(toc-tic)


# dataset = leerTxt("C:\\Users\\Franco\\PycharmProjects\\prueba\\algoritmosGeneticos\\Clusters\\static\\archivos\\newdataset.txt")
# tic = time.clock()
# calcularMedia(dataset)
# toc = time.clock()
# print(toc-tic)


