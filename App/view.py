﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
import random
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Música dependiendo de tus gustos: ")
    print("3- ¡Música para festejar! (Energy y Danceability): ")
    print("4- Música para estudiar (Instrumentalness y Tempo): ")
    print("5- Reproducciones según un género musical: ")
    print("6- Género más escuchado en un rango de horas del día: ")
    print("0- Salir")

def print_Req1(tamaño, rango_menor, rango_mayor):
    if tamaño == -1:
        print('La categoría ingresada no existe en el archivo cargado.')
    else:
        print('\n')
        print('En el rango de ' + str(rango_menor) + ' a ' + str(rango_mayor) + ' han habido: ' + str(tamaño[0]) + ' canciones.')
        print('En el rango de ' + str(rango_menor) + ' a ' + str(rango_mayor) + ' hay ' + str(tamaño[1]) + ' artistas.')
        #print('Un tímido: ' + str(tamaño[2]))
        print('\n')

def print_Req2y3(tupla, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):
    size = tupla[0]
    i = 0
    print('\n')
    print('Entre ' + str(rango_menor1) + ' y ' + str(rango_mayor1) + ' para ' + str(categoria1) + '.')
    print('Entre ' + str(rango_menor2) + ' y ' + str(rango_mayor2) + ' para ' + str(categoria2) + '.')
    print('Hay un total de: ' + str(tupla[0]) + ' canciones únicas.\n')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    print('5 canciones random: ')

    while i < 5:
        numero = random.randint(0, (size - 1))
        track = lt.getElement(tupla[1], numero)
        print('Track ' + str(i + 1) + ': ' + str(track['track_id']) + ' con ' + str(track[str(categoria_1)]) + ' de ' + str(categoria1) + ' y ' + str(track[str(categoria_2)]) + ' de ' + str(categoria2) + '.')
        i += 1

    print('\n')

def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData = controller.loadData(catalog)
        print('Elementos en el árbol: ' + str(controller.indexSizeInstrumentalness(catalog)))
        print('Altura del árbol: ' + str(controller.indexHeightInstrumentalness(catalog)))


    elif int(inputs[0]) == 2:
        categoria = 'instrumentalness'#input('Ingrese la categoría de la que quiere ver información: ')
        categoria = categoria.lower()
        rango_menor = 0.0 #input('Ingrese el rango menor de valores que quiere ver: ')
        rango_mayor = 0.3 #input('Ingrese el rango mayor de valores que quiere ver: ')
        canciones = controller.consultaReq1(catalog, categoria, rango_menor, rango_mayor)
        print_Req1(canciones, rango_menor, rango_mayor)

    elif int(inputs[0]) == 3:
        categoria1 = 'Energy'
        categoria_1 = categoria1.lower()
        categoria2 = 'Danceability'
        categoria_2 = categoria2.lower()
        rango_menor1 = 0.6
        rango_mayor1 = 1
        rango_menor2 = 0.0
        rango_mayor2 = 0.1
        #rango_menor1 = input('Ingrese el rango menor de Energy: ')
        #rango_mayor1 = input('Ingrese el rango mayor de Energy: ')
        #rango_menor2 = input('Ingrese el rango menor de Danceability: ')
        #rango_mayor2 = input('Ingrese el rango mayor de Danceability: ')
        canciones = controller.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)
        print_Req2y3(canciones, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)

    elif int(inputs[0]) == 4:
        categoria1 = 'Instrumentalness'
        categoria_1 = categoria1.lower()
        categoria2 = 'Tempo'
        categoria_2 = categoria2.lower()
        rango_menor1 = 0.6
        rango_mayor1 = 1
        rango_menor2 = 90
        rango_mayor2 = 120
        #rango_menor1 = input('Ingrese el rango menor de Instrumentalness: ')
        #rango_mayor1 = input('Ingrese el rango mayor de Instrumentalness: ')
        #rango_menor2 = input('Ingrese el rango menor de Tempo: ')
        #rango_mayor2 = input('Ingrese el rango mayor de Tempo: ')
        canciones = controller.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)
        print_Req2y3(canciones, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)

    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    else:
        sys.exit(0)
sys.exit(0)
