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



"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    loadContent(catalog)

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
    
 

def loadHashtagdata(catalog):
    contentfile= cf.data_dir + 'sentiment_values.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for hashtag in input_file:
        filtro={}
        if hashtag["vader_avg"] != "":
            filtro["hashtag"]= hashtag['hashtag']
            filtro["vader_avg"]= hashtag["vader_avg"]

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def indexSizeInstrumentalness(catalog):
    return model.indexSizeInstrumentalness(catalog)

def indexHeightInstrumentalness(catalog):
    return model.indexHeightInstrumentalness(catalog)

def consultaArtistas(catalog, categoria, rango_menor, rango_mayor):
    return model.consultaArtistas(catalog, categoria, rango_menor, rango_mayor)

def consultaCanciones(catalog, categoria, rango_menor, rango_mayor):
    return model.consultaCanciones(catalog, categoria, rango_menor, rango_mayor)

def consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):
    return model.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)

def consultaReq4(catalog, genero):
    return model.consultaReq4(catalog,genero)

