"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
from datetime import datetime
import time
import tracemalloc



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    loadContent(catalog)
    # loadHashtagToSong(catalog)
    # loadHashtagdata(catalog)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return delta_time, delta_memory

def loadContent(catalog):
    contentfile = cf.data_dir + 'context_content_features-small.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for cancion in input_file:
        adaptado= {}
        adaptado["instrumentalness"]= float(cancion["instrumentalness"]) 
        adaptado["liveness"]= float(cancion["liveness"])
        adaptado["speechiness"]= float(cancion["speechiness"])
        adaptado["danceability"]= float(cancion["danceability"])
        adaptado["valence"]= float(cancion["valence"])        
        adaptado["loudness"]= float(cancion["loudness"])
        adaptado["tempo"]= float(cancion["tempo"])
        adaptado["acousticness"]= float(cancion["acousticness"])
        adaptado["energy"]= float(cancion["energy"])
        adaptado["artist_id"]= cancion["artist_id"]
        adaptado["track_id"] = cancion["track_id"]
        date_string = cancion["created_at"][11:]
        date_string1= model.horamilitar(date_string)
        adaptado["created_at"] =  datetime.strptime(date_string1, "%H:%M:%S")
        model.addSong(catalog, adaptado)
       
def loadHashtagToSong(catalog):   
     contentfile = cf.data_dir + 'user_track_hashtag_timestamp-small.csv'
     input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
     for cancion in input_file:
         adaptado={}
         date_string = cancion["created_at"][11:]
         date_string1= model.horamilitar(date_string)
         adaptado["created_at"] =  datetime.strptime(date_string1, "%H:%M:%S")
         adaptado["track_id"]= cancion["track_id"]
         adaptado['hashtag']= cancion['hashtag'].lower()
         model.addHT(catalog, adaptado)

def loadHashtagdata(catalog):
     contentfile= cf.data_dir + 'sentiment_values.csv'
     input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
     for hashtag in input_file:
         filtro={}
         if hashtag["vader_avg"] != "":
             filtro["hashtag"]= hashtag['hashtag']
             filtro["vader_avg"]= hashtag["vader_avg"]
             model.addVader(catalog, hashtag)

# Funciones de ordenamiento

def sortByHashTags(lista):
    return model.sortByHashTags(lista)

def sortByNumberOfReproductions(lista):
    return model.sortByNumberOfReproductions(lista)

# Funciones de consulta sobre el catálogo

def indexSizeInstrumentalness(catalog):
    return model.indexSizeInstrumentalness(catalog)

def indexHeightInstrumentalness(catalog):
    return model.indexHeightInstrumentalness(catalog)

def consultaArtistas(catalog, categoria, rango_menor, rango_mayor):
    artistas = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
   
    artistas = model.consultaArtistas(catalog, categoria, rango_menor, rango_mayor)

    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (artistas)

def consultaCanciones(catalog, categoria, rango_menor, rango_mayor):
    return model.consultaCanciones(catalog, categoria, rango_menor, rango_mayor)

def consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):
    consulta = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    consulta = model.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (consulta)

def consultaReq4(catalog, genero):
    consulta = None
    delta_time = -1.0
    delta_memory = -1.0

    # inicializa el processo para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    consulta = model.consultaReq4(catalog, genero)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()

    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    print('Tiempo [ms]: ' + str(delta_time) + ' || ' + 'Memoria [kB]: ' + str(delta_memory))

    return (consulta)

def reproduccionesTotalesEnRangoHoras(catalog, rango_menor, rango_mayor):
    return model.reproduccionesTotalesEnRangoHoras(catalog, rango_menor, rango_mayor)

def consultaGenero(catalog, rango_menor, rango_mayor):
    return model.consultaGenero(catalog, rango_menor, rango_mayor)

def consultaTopGeneros(catalog, rango_menor, rango_mayor):
    return model.consultaTopGeneros(catalog, rango_menor, rango_mayor)

def crearListaGeneros(catalog, rango_menor, rango_mayor):
    return model.crearListaGeneros(catalog, rango_menor, rango_mayor)

def topCancionesPorGenero(catalog, rango_menor, rango_mayor):
    return model.topCancionesPorGenero(catalog, rango_menor, rango_mayor)

# ==========================================
# Funciones para medir el tiempo y memoria
# ==========================================

def getTime():
    """
    Devuelve el instante de tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter() * 1000)

def getMemory():
    """
    Toma una muestra de la memoria alocada en el instante de tiempo
    """
    return tracemalloc.take_snapshot()

def deltaMemory(start_memory, stop_memory):
    """
    Calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory