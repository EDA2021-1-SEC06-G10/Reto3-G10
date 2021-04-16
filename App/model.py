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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.ADT import orderedmap as om
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    catalog = {'caracteristicas': None, # Tabla de Hash en la que las llaves son
                                        # los nombres de las características y los
                                        # valores son un árbol Rojo-Negro.
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='CHAINING',
                                           loadfactor=4.0,
                                           comparefunction=compareKeys                                              
                                          )

    return catalog

def addIntrumentalness(catalog, musica):
    caracteristicas = catalog['caracteristicas']
    llavecaract = '\ufeff"instrumentalness"'
    existcaract = mp.contains(catalog['caracteristicas'], llavecaract)
    if not existcaract:
        valorarbol = om.newMap(omaptype='RBT', comparefunction=compareValues)
        mp.put(caracteristicas, llavecaract, valorarbol)

    print(musica.keys()['dict_keys'][0])
    entry = mp.get(caracteristicas, llavecaract)
    caracter = me.getValue(entry)
    #addTablas(catalog, caracter, musica, llavecaract)

def addTablas(arbol, musica, caracteristica):
    llavecaract = musica[caracteristica]
    existcaract = om.contains(arbol, llavecaract)
    if not existcaract:
        valormap = mp.newMap(2, maptype='CHAINING', loadfactor=0.5, comparefunction=compareKeys)
        om.put(arbol, llavecaract, valormap)

    entry = mp.get(arbol, llavecaract)
    caracter = me.getValue(entry)
    #addArtistAndTracks(arbol, caracter, musica, llavecaract)

def addArtistAndTracks(tabla, musica):
    llavecaract = 'artist_id'
    existcaract = mp.contains(tabla, llavecat)
    if not existcaract:
        lista = lt.newList('ARRAY_LIST', cmpfunction=compareIds, key=None)
        mp.put(tabla, llavecaract, lista)
    
    entry = mp.get(tabla, llavecaract)
    caracter = me.getValue(entry)

def addArtist(musica):
    lt.addLast(musica['artist_id'])

def addTrack(musica):
    lt.addLast(musica['track_id'])

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds():
    return None

def compareKeys(musica1, musica2):
    return None

def compareValues():
    return None

# Funciones de ordenamiento
