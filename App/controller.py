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
    contentfile = cf.data_dir + 'context_content_features-chiquitín.csv'
    input_file = csv.DictReader(open(contentfile, encoding='utf-8'))
    for cancion in input_file:
        adaptado= {}
        adaptado["instrumentalness"]= float(cancion['\ufeff"instrumentalness"']) 
        adaptado["liveness"]= float(cancion["liveness"])
        adaptado["speechiness"]= float(cancion["speechiness"])
        adaptado["danceability"]= float(cancion["danceability"])
        adaptado["valence"]= float(cancion["valence"])        
        adaptado["loudness"]= float(cancion["loudness"])
        adaptado["tempo"]= float(cancion["tempo"])
        adaptado["acousticness"]= float(cancion["acousticness"])
        adaptado["energy"]= float(cancion["energy"])
        adaptado["mode"] = cancion['mode']
        adaptado["key"]= cancion["key"]
        adaptado["artist_id"]= cancion["artist_id"]
        adaptado["tweet_lang"]= cancion["tweet_lang"]
        adaptado["track_id"] = cancion["track_id"]
        adaptado["created_at"]= cancion["created_at"]
        adaptado["lang"]= cancion["lang"]
        adaptado["time_zone"]= cancion["time_zone"]
        adaptado["user_id"]= int(cancion["user_id"])
        adaptado["id"]= int(cancion["id"])
        model.addSong(catalog, adaptado)
        #model.addToTrackIdMap(catalog, adaptado)
        
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def indexSizeInstrumentalness(catalog):
    return model.indexSizeInstrumentalness(catalog)

def indexHeightInstrumentalness(catalog):
    return model.indexHeightInstrumentalness(catalog)

def consultaReq1(catalog, categoria, rango_menor, rango_mayor):
    return model.consultaReq1(catalog, categoria, rango_menor, rango_mayor)

def consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):
    return model.consultaReq2(catalog, categoria_1, categoria_2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2)