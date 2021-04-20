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
                "Avance RBT": None, # Tabla de Hash en la que las llaves son
                                        # los nombres de las características y los
                                        # valores son un árbol Rojo-Negro.
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='CHAINING',
                                           loadfactor=4.0,
                                           comparefunction=compareKeys                                              
                                          )
    
    catalog['Avance RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValuesInstrumentalness)

    return catalog


# "instrumentalness","liveness","speechiness","danceability","valence","loudness","tempo","acousticness","energy","mode","key"
# Funciones para agregar información al catalogo

def addSong(catalog, cancion):
    addSongToTree(catalog['Avance RBT'], cancion)
    return catalog

def addSongToTreeInstrumentalness(mapt, cancion):
    instrumentalness = cancion['\ufeff"instrumentalness"']
    entry = om.get(mapt, instrumentalness)
    if entry is None:
        dataentry = newDataEntry(cancion)
        om.put(mapt, instrumentalness, dataentry)
    else:
        dataentry = me.getValue(entry)
    addValueIndex(dataentry, cancion)
    return mapt

def addValueIndex(dataentry, cancion):
    caracteristica = 'instrumentalness'
    cancionesInst = dataentry[caracteristica]
    artentry = mp.get(cancionesInst, cancion['artist_id'])
    if (artentry is None):
        entry = newArtEntry(caracteristica, cancion['artist_id'], cancion)
        lt.addLast(entry['canciones'], cancion['track_id'])
        mp.put(cancionesInst, 'información', entry)
    else:
        entry = me.getValue(artentry)
        lt.addLast(entry['canciones'], cancion['track_id'])
    return dataentry

def newDataEntry(cancion):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'instrumentalness': None}
    entry['instrumentalness'] = mp.newMap(numelements=10,
                                          maptype='CHAINING',
                                          loadfactor=4.0,
                                          comparefunction=compareArtist)

    return entry

def newArtEntry(caracteristica, artista, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    artentry = {'caracteristica': None, 'artista': None , 'canciones': None}
    artentry['caracteristica'] = caracteristica
    artentry['artista'] = artista
    artentry['canciones'] = lt.newList('ARRAY_LIST', compareCanciones)
    return artentry

# Funciones para creacion de datos

# Funciones de consulta

def indexHeght(catalog):
    return om.height(catalog['Avance RBT'])

def indexSize(catalog):
    return om.size(catalog['Avance RBT'])

def intentoConsulta(catalog, categoria, rango_menor, rango_mayor):
    arbol = catalog['Avance RBT']
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_tamaño = 0
    i = 0

    while i <= tamaño_tabla:
        tabla = lt.getElement(valores, i)
        tablaHash = tabla[categoria]
        key_value = mp.get(tablaHash, 'información')
        value = me.getValue(key_value)
        lista = value['canciones']
        tamaño = lt.size(lista)
        total_tamaño += tamaño
        i += 1

    return total_tamaño

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

def compareArtist(artist1, artist2):
    """
    Compara dos tipos de crimenes
    """
    artist = me.getKey(artist2)
    if (artist1 == artist):
        return 0
    elif (artist1 > artist):
        return 1
    else:
        return -1

def compareCanciones(cancion1, cancion2):
    """
    Compara dos tipos de crimenes
    """
    cancion = me.getKey(cancion2)
    if (cancion1 == cancion):
        return 0
    elif (cancion1 > cancion):
        return 1
    else:
        return -1

# Funciones de ordenamiento
