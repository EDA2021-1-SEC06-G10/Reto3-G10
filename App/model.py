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
    catalog = {'caracteristicas': None,
                "Avance RBT": None # Tabla de Hash en la que las llaves son
                                        # los nombres de las características y los
                                        # valores son un árbol Rojo-Negro.
               'árbol rbt': None
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='CHAINING',
                                           loadfactor=4.0,
                                           comparefunction=compareKeys                                              
                                          )
    
    catalog['árbol_rbt_instrumentalness'] = om.newMap(omaptype='RBT', comparefunction=compareValuesInstrumentalness)

    return catalog

# Funciones para agregar información al catalogo

def addThingsToTree(catalog, musica):
    arbol = catalog['árbol_rbt_instrumentalness']
    llave = musica['\ufeff"instrumentalness"']
    entry = om.get(arbol, llave)
    if entry is None:
        valorEntrada = newEntryValue(llave, musica)
        om.put(arbol, llave, valorEntrada)
    else:
        valorEntrada = me.getValue(entry)
    addValueIndex(valorEntrada, musica)
    print(om.get(arbol, '0.0'))

def addValueIndex(dict, musica):


def newEntryValue(valor, musica):
    entry = {'artist_id': None, 'track_id': None}
    entry['artist_id'] = 1 #lt.newList('ARRAY_LIST')
    entry['track_id'] = 2 #lt.newList('ARRAY_LIST')
    #addArtist(entry['artist_id'], musica)
    #addTrack(entry['track_id'], musica)
    return entry

def addArtist(lista, musica):
    lt.addLast(lista, musica['artist_id'])

def addTrack(lista, musica):
    lt.addLast(lista, musica['track_id'])


# ============================ o =================================

#def addIntrumentalness(catalog, musica):
#    caracteristicas = catalog['caracteristicas']
#    llavecaract = '\ufeff"instrumentalness"'
#     existcaract = mp.contains(catalog['caracteristicas'], llavecaract)
#    if not existcaract:
#        valorarbol = om.newMap(omaptype='RBT', comparefunction=compareValuesInstrumentalness)
#        mp.put(caracteristicas, llavecaract, valorarbol)
#        addTablas(valorarbol, musica, llavecaract)

def addIntrumentalness2(catalog, musica):
    caracteristicas = catalog['Avance RBT']
    llavecaract = '\ufeff"instrumentalness"'
    existcaract = mp.contains(catalog['caracteristicas'], llavecaract)
    if not existcaract:
        valorarbol = om.newMap(omaptype='RBT', comparefunction=compareValuesInstrumentalness)
        mp.put(caracteristicas, llavecaract, valorarbol)
        addTablas(valorarbol, musica, llavecaract)
    #entry = mp.get(caracteristicas, llavecaract)
    #caracter = me.getValue(entry)
    #print(catalog['caracteristicas'])

#def addTablas(arbol, musica, caracteristica):
#    llavecaract = musica[caracteristica]
#    existcaract = om.contains(arbol, llavecaract)
#    if not existcaract:
#        valormap = mp.newMap(2, maptype='CHAINING', loadfactor=0.5)
#        om.put(arbol, llavecaract, valormap)
    #addArtistsKey(valormap, musica)
    #addTracksKey(valormap, musica)

    #entry = mp.get(arbol, llavecaract)
    #caracter = me.getValue(entry)

#def addArtistsKey(tabla, musica):
#    lista = lt.newList('ARRAY_LIST', cmpfunction=compareArtistIds)
#    llavecaract = 'artist_id'
#    existcaract = mp.contains(tabla, llavecaract)
#    if existcaract == False or existcaract == True:
#        mp.put(tabla, llavecaract, lista)
    #addArtist(lista, musica)
    
    #entry = mp.get(tabla, llavecaract)
    #caracter = me.getValue(entry)

#def addTracksKey(tabla, musica):
#    lista = lt.newList('ARRAY_LIST', cmpfunction=compareTrackIds)
#    llavecaract = 'track_id'
#    existcaract = mp.contains(tabla, llavecaract)
#    if existcaract == False or existcaract == True:
#        mp.put(tabla, llavecaract, lista)
    #addTrack(lista, musica)
    
    #entry = mp.get(tabla, llavecaract)
    #caracter = me.getValue(entry)

#def addArtist(lista, musica):
#    lt.addLast(lista, musica['artist_id'])

#def addTrack(lista, musica):
#    lt.addLast(lista, musica['track_id'])


# Funciones para creacion de datos

# Funciones de consulta

def intentoConsulta(catalog):
    arbol = catalog['árbol_rbt_instrumentalness']
    llaves = om.keys(arbol, '0.0', '0.2')
    valores = om.values(arbol, '0.0', '0.2')

    return llaves

# Funciones utilizadas para comparar elementos dentro de una lista

def compareArtistIds(musica, artist_id):
    result = (artist_id == musica['artist_id'])
    return result


def compareTrackIds(musica, track_id):
    result = (track_id == musica['track_id'])
    return result

def compareKeys(musica1, musica2):
    return None

def compareValuesInstrumentalness(valor1, valor2):
    if valor1 > valor2:
        return 1
    elif valor1 == valor2:
        return 0
    else:
        return -1

# Funciones de ordenamiento
