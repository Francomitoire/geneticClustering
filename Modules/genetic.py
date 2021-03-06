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
from scipy import sparse


class Individuo(object):
    """
    El atributo valor es un conjunto de centroides GATOOOOOO
    """
    #ESTE ATRIBUTO TIENE QUE TENER EL MAYOR FITNESS DE TODA LA POBLACION EN TO DO MOMENTO
    # mayorFitness = 0


    def __init__(self):

        #el atributo valor contiene los falsos centroides mediante los cuales se asignan los puntos al mas cercano
        self.valor = None
        #el atributo centroides tiene los verdaderos centroides de las clases
        self.centroides = None
        self.fitness = None
        self.fitnessReal = None
        self.puntos = []
        self.ssw_centroides = []
        self.ssb_centroides = []

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
            # cent = tuple(cent_lt)
            #ACA cent_lt
            cent = np.array(cent_lt)
            valor.append(cent)
        self.setValor(valor,dataset)


    def setValor(self,valor,dataset):
        self.valor = valor
        self.setPuntos(dataset)

    def setFitness(self,valor):
        self.fitness = round(valor,4)

    def setFitnessReal(self,valor):
        self.fitnessReal = round(valor,4)


    # def calcularVerdaderosCentroides(self):
    #     #para el conjunto de puntos totales
    #     centroides = []
    #
    #     for clase in self.puntos:
    #
    #         sum = 0
    #
    #         if len(clase) != 0 :
    #             for punto in clase:
    #                 sum = sum + np.array(punto)
    #
    #             prom = sum/len(clase)
    #             print(prom)
    #
    #             tup = tuple(prom)
    #             centroides.append(tup)
    #         else:
    #             centroides.append((0,0))
    #
    #     self.centroides = centroides

    def calcularDistanciaPromedio(self,valores):
        '''recibe como parametro los centroides a los cuales se desea calcular la distancia promedio de su cluster'''
        fitness = 0

        # por cada centroide..
        for i in range(len(valores)):

            errorCentroide = 0
            # alelo = [(2,3),(5,8),(1,5)]
            alelo = valores[i]

            # distancia = 0
            distancia2 = 0
            # puntos_en_centroide = [(4,2),(4,3),(6,7),(8,7),(2,3),(5,1)]
            puntos_en_centroide = self.puntos[i]
            print(type(alelo),'alelo')
            punto2 = np.array(alelo)
            # por cada punto que pertenece (es cercano) a ese centroide...
            if (len(puntos_en_centroide) != 0):

                for j in range(len(puntos_en_centroide)):
                    punto = puntos_en_centroide[j]
                    punto1 = np.array(punto)
                    dist = np.linalg.norm(punto2 - punto1)
                    distancia2 = distancia2 + dist

                errorCentroide = distancia2 / len(puntos_en_centroide)
            else:
                errorCentroide = errorCentroide + 50
            fitness = fitness + errorCentroide
            # fitness = fitness/len(self.valor)


        # fitness = fitness / len(self.valor)
        return fitness

    def calcularFitness(self,media,n):
        # fitness = self.calcularDistanciaPromedio(self.valor)
        # self.setFitness(fitness)
        # fitness_real = self.calcularDistanciaPromedio(self.centroides)
        # self.setFitnessReal(fitness_real)

        ssb = self.calcularSsb(media)
        ssw = self.calcularSsw(self.valor)

        if 0 in self.ssb_centroides:
            self.setFitness(0)
        else:
            k = len(self.puntos)
            a = ssb / (k-1)
            b = ssw / (n-k)
            fit = round(a/b,4)
            self.setFitness(fit)



    def calcularSsb(self,media):
        #medida de separacion para evaluar la distancia inter clusters. Sum of Squared Between
        ssb = 0
        # media = np.array(media)
        for i in range(len(self.valor)):
            n = len(self.puntos[i])
            # centroide = np.array(self.valor[i])
            centroide = self.valor[i]
            dist = np.linalg.norm(centroide-media)
            exp = n * (dist**2)
            self.ssb_centroides.append(exp)
            ssb = ssb + exp
        return ssb

    def calcularSsw(self,valores):
        #recibe los centroides como parametro.  Sum of Squared Within
        ssw = 0

        # por cada centroide..
        for i in range(len(valores)):

            ssw_centroide = 0
            # alelo = [(2,3),(5,8),(1,5)]
            punto2 = valores[i]
            # distancia = 0
            distancia2 = 0
            # puntos_en_centroide = [(4,2),(4,3),(6,7),(8,7),(2,3),(5,1)]
            puntos_en_centroide = self.puntos[i]
            # punto2 = np.array(alelo)
            # por cada punto
            if (len(puntos_en_centroide) != 0):

                for j in range(len(puntos_en_centroide)):
                    punto1 = puntos_en_centroide[j]
                    dist = np.linalg.norm(punto2 - punto1)
                    distancia2 = distancia2 + (dist**2)

                ssw_centroide = distancia2
            else:
                ssw_centroide = 1
            self.ssw_centroides.append(ssw_centroide)
            ssw = ssw + ssw_centroide


        # fitness = fitness / len(self.valor)
        return ssw


    # def mostrarFitnessCentroides(self):
    #     print(self.valor)
    #     print(self.fitnessCentroides)
    #     # for cent_y_fit in self.fitnessCentroides:
    #     #     print(cent_y_fit)


    def setPuntos(self,dataset):
        # particion = sklearn.metrics.pairwise(dataset,self.valor)
        del self.puntos[:]
        for i in range(len(self.valor)):
            self.puntos.append([])
        if uso_lib == 0:
            # print('usando propio')
            for i in range(len(dataset)):
                punto = dataset[i]
                posicionCentroide = calcularCentroide(punto,self)
                # print(posicionCentroide)
                self.puntos[posicionCentroide].append(punto)
        else:
            # print('usando libreria')
            particion = sklearn.metrics.pairwise_distances_argmin(dataset, self.valor)

            for i in range(len(dataset)):
                punto = dataset[i]
                pos = particion[i]
                self.puntos[pos].append(punto)



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
            # tupla = tuple(lt)
            arr = np.array(lt)
            # salida.append(a)
            salida.append(arr)
        return(salida)

def calcularMedia(dataset):
    sum = 0
    for punto in dataset:
        sum = sum + np.array(punto)
    prom = sum/len(dataset)
    # tup = tuple(prom)
    arr = np.array(prom)
    return arr

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
    # print(type(punto), punto)
    min = np.linalg.norm(centroide - punto)
    for i in range(1,len(individuo.valor)):
        centroide = individuo.valor[i]
        punto2 = np.array(centroide)
        dist = np.linalg.norm(centroide - punto)
        if (dist < min):
            min = dist
            centroideMinimo = i

    return(centroideMinimo)

#OPERADORES ---------------------------------------------------------

def seleccionRanking(pob):
    '''La poblacion de entrada debe tener como minimo 6 elementos para que devuelva una cantidad igual'''
    pob_entrada = pob
    # ordenarPoblacion(pob_entrada)
    pob_salida = []
    rmin = 0
    copias = []
    n = len(pob_entrada)
    for i in range(n):
        indi = i+1
        c = rmin + 2*(n-indi)*(1-rmin)/(n-1)
        cant = int(c)
        copias.append((round(c-int(c),2)))
        for j in range(cant):
            pob_salida.append(pob_entrada[i])
    faltante = len(pob_entrada) - len(pob_salida)
    for i in range(faltante):
        ind = copias.index(max(copias))
        pob_salida.append(pob_entrada[ind])
        copias[ind] = 0
    return pob_salida


def seleccion(poblacion,preservar,porcentaje):

    if porcentaje == 0:

        return []

    cant = int(len(poblacion)*porcentaje)
    pob_elitista = []

    if cant > preservar:
        for i in range(preservar):
            pob_elitista.append(poblacion[i])

        pob_controlada = seleccionRanking(poblacion[preservar:cant])
        pob_salida = pob_elitista + pob_controlada
        return pob_salida


    elif cant == preservar:
        pob_salida = poblacion[0:preservar]
        return pob_salida

    else:
        warnings.warn_explicit('La cantidad a preservar debe ser menor o igual a la cantidad total a seleccionar')



def mutacion(poblacion, porc_mutacion,mins,maxs,dataset):
    pob_salida = []
    cant_indiv = int(len(poblacion) * porc_mutacion)
    indices = lista_de_enteros(0, len(poblacion))
    lt = []
    for i in range(cant_indiv):
        x = random.choice(indices)
        indices = restar_listas(indices, [x])
        lt = lt + [x]
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
    nuevo_ind = Individuo()
    valor = copy(ind.valor)
    # print('valor', valor)
    cant_atributos = len(valor)
    # print('cant atributos', cant_atributos)
    puntero = random.randrange(0,cant_atributos)
    # print('///')
    # print (puntero, 'Puntero del atributo del individuo')
    atributo = ind.valor[puntero]
    # print(atributo)
    #mutar
    cant_alelos = len(valor[puntero])
    # print(cant_alelos, 'Cantidad de alelos del atributo')
    a = []
    for i in range(0,cant_alelos):
        a.append(random.randrange(mins[i],maxs[i]))
    # a = tuple(a)
    a = np.array(a)
    new_atributo = a
    # print(new_atributo, 'Generador de nuevo atributo')
    valor[puntero] = new_atributo
    nuevo_ind.setValor(valor,dataset)
    # print('valor', valor)
    # print(ind.valor, 'Injeccion en el individuo del atributo generado')
    return nuevo_ind

def cruzaPoblacion(poblacion, porcentaje,dataset):
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
        ind1 = poblacion[rand1]
        ind2 = poblacion[rand2]
        ind1_cruzado, ind2_cruzado = cruzaUnPunto(ind1,ind2,dataset)
        pob_salida.append(ind1_cruzado)
        pob_salida.append(ind2_cruzado)
        if not lt:
            break
    return pob_salida

def cruzaUnPunto(i1, i2,dataset):
    '''Cruza simple con punto de cruza aleatorio'''
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
    poblacion.sort(key=lambda individuo: individuo.fitness,reverse=True)




#SECCION FITNESS POBLACION ----------------------

def setFitnessPoblacion(poblacion,media,n):
    for ind in poblacion:
        #VER SI ES RAZONABLE, HABLARLO CON MATI
        if not ind.fitness:
           ind.calcularFitness(media,n)



#---------------------------



def imprimirPoblacion(pob):
    # copias = 0
    ordenarPoblacion(pob)
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

def setUsoLib(bool=0):
    '''Setear a 0 para no usar librerias, setear a uno para usar librerias'''
    global uso_lib
    uso_lib = bool

def mainApp(iteraciones, tamanoIndividuo,dimx_graficar,dimy_graficar,opcion1):
    setUsoLib(opcion1)
    cantidadIndividuos = 60
    cantPreservar = 1
    porc_seleccion = 0.5
    porc_cruza = 0.3
    porc_mutacion = 0.2
    dataset = leerTxt("C:\\PythonProjects\\geneticClustering\\static\\archivos\\newdataset.txt")
    media_dataset = calcularMedia(dataset)
    n = len(dataset)
    puntos = []
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

    pob_anterior = generarPoblacionInicial(cantidadIndividuos, tamanoIndividuo, mins, maxs, dimensiones, dataset)
    pob_siguiente = []

    setFitnessPoblacion(pob_anterior, media_dataset, n)

    ordenarPoblacion(pob_anterior)
    ind_viejo = copy(pob_anterior[0])

    for i in range(iteraciones):
        pob_sel = seleccion(pob_anterior, cantPreservar, porc_seleccion)

        pob_cru = cruzaPoblacion(pob_anterior, porc_cruza,dataset)

        pob_mut = mutacion(pob_anterior, porc_mutacion, mins, maxs, dataset)

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



    #TABLA--------------------------------------------------

    columns = []
    for i in range(tamanoIndividuo):
        columns.append('Clase ' + str(i + 1))

    trace = go.Table(
        header=dict(values=columns,
                    fill=dict(color='#C2D4FF'),
                    align=['left'] * 5),
        cells=dict(values=ind_nuevo.puntos,
                   fill=dict(color='#F5F8FF'),
                   align=['left'] * 5))

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





    layout = dict(title='Fitness Solución: ' + str(ind_nuevo.fitness) + ' -' + ' Individuos: ' + str(cantidadIndividuos)+' -'+' Generaciones: '+str(iteraciones),
                  yaxis=dict(zeroline=False),
                  xaxis=dict(zeroline=False)
                  )


    fig = dict(data=data2, layout=layout)



    fig1 = dict(data=data2, layout=layout)
    plotly.offline.plot(fig1, filename='grafico_clusters.html')




# setUsoLib(0)
#
# tic = time.clock()
# mainApp(10,2,0,1,0)
# toc = time.clock()
# print(toc-tic)