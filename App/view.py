"""
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
import time
from datetime import datetime

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

def print_Req1(tamaño, categoria, rango_menor, rango_mayor):
    if tamaño == -1:
        print('La categoría ingresada no existe en el archivo cargado.')
    else:
        print('*' * 50)
        print('Para la caracerística ' + str(categoria) + ':')
        print('En el rango de ' + str(rango_menor) + ' a ' + str(rango_mayor) + ' han habido: ' + str(tamaño[1]) + ' canciones.')
        print('En el rango de ' + str(rango_menor) + ' a ' + str(rango_mayor) + ' hay ' + str(tamaño[0]) + ' artistas.')
        print('*' * 50)

def print_Req2y3(tupla, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):
    size = tupla[0]
    i = 0
    print('\n')
    print('Entre ' + str(rango_menor1) + ' y ' + str(rango_mayor1) + ' para ' + str(categoria1) + '.')
    print('Entre ' + str(rango_menor2) + ' y ' + str(rango_mayor2) + ' para ' + str(categoria2) + '.')
    print('Hay un total de: ' + str(tupla[0]) + ' canciones únicas.\n')
    print('+' * 50 + '\n')
    print('5 canciones random: ')

    while i < 5:
        numero = random.randint(0, (size - 1))
        track = lt.getElement(tupla[1], numero)
        print('Track ' + str(i + 1) + ': ' + str(track['track_id']) + ' con ' + str(track[str(categoria_1)]) + ' de ' + str(categoria1) + ' y ' + str(track[str(categoria_2)]) + ' de ' + str(categoria2) + '.')
        i += 1
    print('+' * 50 + '\n')

def print_Req4(tupla, genero, rango):
    print(("-" * 10) + genero + ("-" * 10))
    print("Para " + genero + " el tempo esta entre: " + str(rango[0]) + " y " + str(rango[1])+ " BPM")
    print("Las reproducciones de "+ genero + " son: " + str(tupla[1]))
    print('Algunos artistas son: ')
    print('\n')
    i = 1
    while i <= 10:
        artista = lt.getElement(tupla[2], i)
        print("Artista #" + str(i) + ": " + artista )
        i += 1

def print_Req5_1(lista, reproducciones, rango_menor, rango_mayor):
    print('Hay un total de ' + str(reproducciones) + ' reproducciones entre las ' + str(rango_menor) + ' y ' + str(rango_mayor) + '\n')
    print('=' * 25 + ' TOP DE GÉNEROS ' + '=' * 25 + '\n')
    print('(NOTA: Tenga en cuenta que una canción puede pertenecer a diferentes\ngéneros por el tempo que tiene.)\n')

    size_lista = lt.size(lista[1])
    i = 1
    while i <= size_lista:
        elemento = lt.getElement(lista[1], i)
        print('TOP ' + str(i) + ': ' + str(elemento['key']) + ' con ' + str(elemento['value']) + ' reproducciones.')
        i += 1

def print_Req5_2(lista1, lista2):
    top = lt.getElement(lista1[1], 1)
    print('El GÉNERO TOP es ' + str(top['key']) + ' con ' + str(top['value']) + '.')
    print('=' * 25 + ' ' + str(top['key']) + ' ANÁLISIS ' + '=' * 25)
    print(str(top['key']) + ' tiene ') # AQUÍ VAN LOS TRACKS ÚNICOS DEL GÉNERO TOP
    print('Las primeras 10 canciones son: ')
    
    size_lista2 = lt.size(lista2)
    i = 1
    while i <= size_lista2:
        elemento = lt.getElement(lista2, i)
        if i <= 10:
            print('TOP ' + str(i) + ': ' + str(elemento['key']) + ' con ' + str(elemento['value'][0]) + ' hashtags y VADER promedio de: ' + str(elemento['value'][1]))
        i += 1

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
        answer = controller.loadData(catalog)
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")
        print('Elementos en el árbol: ' + str(controller.indexSizeInstrumentalness(catalog)))
        print('Altura del árbol: ' + str(controller.indexHeightInstrumentalness(catalog)))
        

    elif int(inputs[0]) == 2:
        categoria = input('Ingrese la categoría de la que quiere ver información: ')
        categoria = categoria.lower()
        rango_menor = float(input('Ingrese el rango menor de valores que quiere ver: '))
        rango_mayor = float(input('Ingrese el rango mayor de valores que quiere ver: '))
        canciones = controller.consultaArtistas(catalog, categoria, rango_menor, rango_mayor)
        print_Req1(canciones, categoria, rango_menor, rango_mayor)

    elif int(inputs[0]) == 3:
        categoria1 = 'Energy'
        categoria_1 = categoria1.lower()
        categoria2 = 'Danceability'
        categoria_2 = categoria2.lower()
        # rango_menor1 = 0.6
        # rango_mayor1 = 1
        # rango_menor2 = 0.6
        # rango_mayor2 = 1
        rango_menor1 = float(input('Ingrese el rango menor de Energy: '))
        rango_mayor1 = float(input('Ingrese el rango mayor de Energy: '))
        rango_menor2 = float(input('Ingrese el rango menor de Danceability: '))
        rango_mayor2 = float(input('Ingrese el rango mayor de Danceability: '))

        canciones = controller.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)
        print_Req2y3(canciones, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)

    elif int(inputs[0]) == 4:
        categoria1 = 'Instrumentalness'
        categoria_1 = categoria1.lower()
        categoria2 = 'Tempo'
        categoria_2 = categoria2.lower()
        # rango_menor1 = 0.0
        # rango_mayor1 = 0.3
        # rango_menor2 = 90
        # rango_mayor2 = 120
        rango_menor1 = float(input('Ingrese el rango menor de Instrumentalness: '))
        rango_mayor1 = float(input('Ingrese el rango mayor de Instrumentalness: '))
        rango_menor2 = float(input('Ingrese el rango menor de Tempo: '))
        rango_mayor2 = float(input('Ingrese el rango mayor de Tempo: '))
        canciones = controller.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)
        print_Req2y3(canciones, categoria1, categoria2, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)

    elif int(inputs[0]) == 5:
        generos = int(input("Ingrese la cantidad de generos que desea consultar (max 3): "))
        i = 1
        while i <= generos:
            print("Genero #" + str(i))
            creacion = bool(int(input("Si desea consultar un genero desconocido, digite 1. De lo contrario, digite 0: "))) 
            if creacion == True:
                rangotemp_sup = int(input("Ingrese el valor superior del tempo del genero desconocido: "))
                rangotemp_inf = int(input("Ingrese el valor inferior del tempo del genero desconocido: "))
                rango = (rangotemp_inf, rangotemp_sup)
                result = controller.consultaArtistas(catalog, 'tempo', rangotemp_inf, rangotemp_sup)
                print(result[2])
                #print_Req4(result, 'desconocido', rango)
            else:
                generoX = input("Ingrese el genero que desea consultar: ")
                generoX = generoX.lower()
                resultado = controller.consultaReq4(catalog, generoX)
                rango = resultado[3]
                print_Req4(resultado[:3], generoX, rango)
            print("\n")
            i += 1
        
    elif int(inputs[0]) == 6:
        genero = ''
        rango_menor_str = '07:15:00'
        rango_menor = datetime.strptime(rango_menor_str, "%H:%M:%S")
        rango_mayor_str = '09:45:00'
        rango_mayor = datetime.strptime(rango_mayor_str, "%H:%M:%S")
        reproducciones = controller.reproduccionesTotalesEnRangoHoras(catalog, rango_menor, rango_mayor)
        lista = controller.consultaTopGeneros(catalog, rango_menor, rango_mayor)
        ordenada1 = controller.sortByHashTags(lista)
        print_Req5_1(ordenada1, reproducciones, rango_menor, rango_mayor)
        top = controller.topCancionesPorGenero(catalog, rango_menor, rango_mayor, genero)
        ordenada2 = controller.sortByNumberOfReproductions(top)
        
        print_Req5_2(ordenada2, top)
    else:
        sys.exit(0)
sys.exit(0)
