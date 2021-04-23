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
from DISClib.Algorithms.Sorting import mergesort as mer
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
                "intrumentalness_RBT": None,
                'liveness_RBT': None,
                'speechiness_RBT': None,
                'danceability_RBT': None,
                'valence_RBT': None,
                'loudness_RBT': None,
                'tempo_RBT': None,
                'acousticness_RBT': None,
                'energy_RBT': None,
                'mode_RBT': None,
                'key_RBT': None,  

                'tracks': None   
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='CHAINING',
                                           loadfactor=4.0,
                                           #comparefunction=compareKeys                                              
                                          )
    
    catalog['instrumentalness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['liveness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['speechiness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['danceability_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['valence_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['loudness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['tempo_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['acousticness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['energy_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['mode_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['key_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['tracks'] = mp.newMap(4,
                                  maptype='CHAINING',
                                  loadfactor=4.0                                    
                                 )

    return catalog


# Funciones para agregar información al catalogo


def addSong(catalog, cancion):
    addInstrumentalnessTreesToHashTable(catalog, cancion)
    addLivenessTreesToHashTable(catalog, cancion)
    addSpeechinessTreesToHashTable(catalog, cancion)
    addDanceabilityTreesToHashTable(catalog, cancion)
    addValenceTreesToHashTable(catalog, cancion)
    addLoudnessTreesToHashTable(catalog, cancion)
    addTempoTreesToHashTable(catalog, cancion)
    addAcousticnessTreesToHashTable(catalog, cancion)
    addEnergyTreesToHashTable(catalog, cancion)
    addModeTreesToHashTable(catalog, cancion)
    addKeyTreesToHashTable(catalog, cancion)

    return catalog


# ================
# Intrumentalness
# ================

def addInstrumentalnessTreesToHashTable(catalog, cancion):
    categoria = 'instrumentalness'
    tabla = catalog['caracteristicas']
    arbol = catalog['instrumentalness_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeInstrumentalness(arbol, cancion)

    return tabla

def addSongToTreeInstrumentalness(mapt, cancion):
    caracteristica = 'instrumentalness'
    categoria = cancion["instrumentalness"]
    entry = om.get(mapt, categoria)
    filtrado = {} # Elina, Nicolás, 
                # por favor no nos bajen.
                # Carlos nos autorizó usar
                # este diccionaro.
    filtrado["track_id"] = cancion["track_id"]
    filtrado["instrumentalness"] = cancion["instrumentalness"]
    filtrado["tempo"] = cancion["tempo"]
    filtrado["danceability"] = cancion["danceability"]
    filtrado["energy"] = cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
    return mapt

# def addValueIndexInstrumentalness(dataentry, cancion):
#     caracteristica = 'instrumentalness'
#     cancionesInst = dataentry['caracteristica']
#     artentry = mp.get(cancionesInst, cancion['artist_id'])
#     if (artentry is None):
#         entry = newArtEntry(caracteristica, cancion['artist_id'], cancion)
#         lt.addLast(entry['canciones'], cancion['track_id'])
#         mp.put(cancionesInst, 'información', entry)
#     else:
#         entry = me.getValue(artentry)
#         lt.addLast(entry['canciones'], cancion['track_id'])
#     return dataentry

# ==========
# Liveness
# ==========

def addLivenessTreesToHashTable(catalog, cancion):
    categoria = 'liveness'
    tabla = catalog['caracteristicas']
    arbol = catalog['liveness_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeLiveness(arbol, cancion)

    return tabla

def addSongToTreeLiveness(mapt, cancion):
    caracteristica = 'liveness'
    categoria = cancion["liveness"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# ============
# Speechiness
# ============

def addSpeechinessTreesToHashTable(catalog, cancion):
    categoria = 'ispeechiness'
    tabla = catalog['caracteristicas']
    arbol = catalog['speechiness_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeSpeechiness(arbol, cancion)

    return tabla

def addSongToTreeSpeechiness(mapt, cancion):
    caracteristica = 'speechiness'
    categoria = cancion["speechiness"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# =============
# Danceability
# =============

def addDanceabilityTreesToHashTable(catalog, cancion):
    categoria = 'danceability'
    tabla = catalog['caracteristicas']
    arbol = catalog['danceability_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeDanceability(arbol, cancion)

    return tabla

def addSongToTreeDanceability(mapt, cancion):
    caracteristica = 'danceability'
    categoria = cancion["danceability"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# ========
# Valence
# ========

def addValenceTreesToHashTable(catalog, cancion):
    categoria = 'valence'
    tabla = catalog['caracteristicas']
    arbol = catalog['valence_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeValence(arbol, cancion)

    return tabla

def addSongToTreeValence(mapt, cancion):
    caracteristica = 'valence'
    categoria = cancion["valence"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# =========
# Loudness
# =========

def addLoudnessTreesToHashTable(catalog, cancion):
    categoria = 'loudness'
    tabla = catalog['caracteristicas']
    arbol = catalog['loudness_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeLoudness(arbol, cancion)

    return tabla

def addSongToTreeLoudness(mapt, cancion):
    caracteristica = 'loudness'
    categoria = cancion["loudness"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# ======
# Tempo
# ======

def addTempoTreesToHashTable(catalog, cancion):
    categoria = 'tempo'
    tabla = catalog['caracteristicas']
    arbol = catalog['tempo_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeTempo(arbol, cancion)

    return tabla

def addSongToTreeTempo(mapt, cancion):
    caracteristica = 'tempo'
    categoria = cancion["tempo"]
    entry = om.get(mapt, categoria)
    filtrado = {} # Elina, Nicolás, 
                # por favor no nos bajen.
                # Carlos nos autorizó usar
                # este diccionaro.
    filtrado["track_id"] = cancion["track_id"]
    filtrado["instrumentalness"] = cancion["instrumentalness"]
    filtrado["tempo"] = cancion["tempo"]
    filtrado["danceability"] = cancion["danceability"]
    filtrado["energy"] = cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
    return mapt

# =============
# Acousticness
# =============

def addAcousticnessTreesToHashTable(catalog, cancion):
    categoria = 'acousticness'
    tabla = catalog['caracteristicas']
    arbol = catalog['acousticness_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeAcousticness(arbol, cancion)

    return tabla

def addSongToTreeAcousticness(mapt, cancion):
    caracteristica = 'acousticness'
    categoria = cancion["acousticness"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# =======
# Energy
# =======

def addEnergyTreesToHashTable(catalog, cancion):
    categoria = 'energy'
    tabla = catalog['caracteristicas']
    arbol = catalog['energy_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeEnergy(arbol, cancion)

    return tabla

def addSongToTreeEnergy(mapt, cancion):
    caracteristica = 'energy'
    categoria = cancion["energy"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
    return mapt

# =====
# Mode
# =====

def addModeTreesToHashTable(catalog, cancion):
    categoria = 'mode'
    tabla = catalog['caracteristicas']
    arbol = catalog['mode_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeMode(arbol, cancion)

    return tabla

def addSongToTreeMode(mapt, cancion):
    caracteristica = 'mode'
    categoria = cancion["mode"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# ====
# Key
# ====

def addKeyTreesToHashTable(catalog, cancion):
    categoria = 'key'
    tabla = catalog['caracteristicas']
    arbol = catalog['key_RBT']
    entry = mp.get(tabla, categoria)
    if entry is None:
        mp.put(tabla, categoria, arbol)
    addSongToTreeInstrumentalness(arbol, cancion)

    return tabla

def addSongToTreeKey(mapt, cancion):
    caracteristica = 'key'
    categoria = cancion["key"]
    entry = om.get(mapt, categoria)
    filtrado={}
    filtrado["track_id"]=cancion["track_id"]
    filtrado["instrumentalness"]= cancion["instrumentalness"]
    filtrado["tempo"]= cancion["tempo"]
    filtrado["danceability"]= cancion["danceability"]
    filtrado["energy"]= cancion["energy"]
    if entry is None:
        dataentry = newArtEntry(caracteristica, filtrado)
        om.put(mapt, categoria, dataentry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
        
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"] )
    return mapt

# def newDataEntry(cancion):
#     """
#     Crea una entrada en el indice por fechas, es decir en el arbol
#     binario.
#     """
#     entry = {'caracteristica': None}
#     entry['caracteristica'] = mp.newMap(numelements=10,
#                                           maptype='CHAINING',
#                                           loadfactor=4.0,
#                                           comparefunction=compareArtist)

#     return entry

# Funciones para creacion de datos

def newArtEntry(caracteristica, cancion):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    artentry = {'caracteristica': None, 'artistas': None , 'canciones': None, "reproducciones":None} # Elina, Nicolás, 
                                                                                                     # por favor no nos bajen.
                                                                                                     # Carlos nos autorizó usar
                                                                                                     # este diccionaro.
    artentry['caracteristica'] = caracteristica
    artentry['artistas'] = lt.newList('ARRAY_LIST', compareArtistas)
    artentry['canciones'] = lt.newList('ARRAY_LIST', compareCanciones)
    artentry["reproducciones"]= lt.newList('ARRAY_LIST')
    return artentry

# Funciones de consulta

def indexHeightInstrumentalness(catalog):
    return om.height(catalog['instrumentalness_RBT'])

def indexSizeInstrumentalness(catalog):
    return om.size(catalog['instrumentalness_RBT'])

def consultaReq1(catalog, categoria, rango_menor, rango_mayor):
    total_tamaño = 0
    hashTabla = catalog['caracteristicas']
    llaves = mp.get(hashTabla, categoria)
    arbol = me.getValue(llaves)
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_canciones = 0
    total_artistas = 0
    canciones = lt.newList('ARRAY_LIST')
    i = 1

    while i <= tamaño_tabla:
        tabla = lt.getElement(valores, i)
        lista_canciones = tabla['reproducciones']
        lista_artistas = tabla['artistas']
        lista_reproducciones = tabla['canciones']
        size_canciones = lt.size(lista_canciones)
        size_artistas = lt.size(lista_artistas)
        size_reproducciones = lt.size(lista_reproducciones)
        total_artistas += size_artistas
        total_canciones += size_canciones
        j = 1
        while j <= size_reproducciones:
            lista_canciones_unicas = lt.getElement(tabla['canciones'], j)
            lt.addLast(canciones, lista_canciones_unicas)
            j += 1
        i += 1
       
    return (total_canciones, total_artistas, canciones)

def consultaReq2(catalog, categoria1, categoria2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):

    lista = lt.newList('ARRAY_LIST', cmpfunction=compareTracksLista)
    #lista_tracks_unicos = lt.newList('ARRAY_LIST', cmpfunction=compareTracks)
    
    tupla_1 = consultaReq1(catalog, categoria1, rango_menor1, rango_mayor1)
    total_canciones1 = tupla_1[0]
    lista_canciones1 = tupla_1[2]
    size1 = lt.size(lista_canciones1)
    i = 0
    while i < size1:
        cancion = lt.getElement(lista_canciones1, i)
        track = cancion['track_id']
        esta_track = lt.isPresent(lista, track)
        if esta_track == 0:
            lt.addLast(lista, cancion)
        # esta_track = lt.isPresent(lista_tracks_unicos, track)
        # if esta_track == 0:
        #     lt.addLast(lista_tracks_unicos, track)
        #lt.addLast(lista, cancion)
        i += 1

    tupla_2 = consultaReq1(catalog, categoria2, rango_menor2, rango_mayor2)
    total_canciones2 = tupla_2[0]
    lista_canciones2 = tupla_2[2]
    size2 = lt.size(lista_canciones2)
    j = 0
    while j < size2:
        cancion = lt.getElement(lista_canciones2, j)
        track = cancion['track_id']
        esta_track = lt.isPresent(lista, track)
        if esta_track == 0:
            lt.addLast(lista, cancion)
        # esta_track = lt.isPresent(lista_tracks_unicos, track)
        # if esta_track == 0:
        #     lt.addLast(lista_tracks_unicos, track)
        #lt.addLast(lista, cancion)
        j += 1
    
    size = lt.size(lista)

    return (size, lista)

# Funciones utilizadas para comparar elementos dentro de una lista

# def compareArtistIds(musica, artist_id):
#     result = (artist_id == musica['artist_id'])
#     return result

# def compareTrackIds(musica, track_id):
#     result = (track_id == musica['track_id'])
#     return result

def compareValues(valor1, valor2):
    if valor1 > valor2:
        return 1
    elif valor1 == valor2:
        return 0
    else:
        return -1

def compareArtistas(artist1, cancion):
    if artist1 == cancion:
        return 0
    elif artist1 > cancion:
        return 1
    else:
        return -1

def compareCanciones(cancion1, cancion):
    if cancion1 == cancion['track_id']:
        return 0
    elif cancion1 > cancion['track_id']:
        return 1
    else:
        return -1

def compareTracks(track1, track2):
    if track1 == track2:
        return 0
    elif track1 > track2:
        return 1
    else:
        return -1

def compareTracksLista(track1, track2):
    if track1 == track2['track_id']:
        return 0
    elif track1 > track2['track_id']:
        return 1
    else:
        return -1
    
# def compareArtist(artist1, artist2):
#     """
#     Compara dos tipos de artistas
#     """
#     artist = me.getKey(artist2)
#     if (artist1 == artist):
#         return 0
#     elif (artist1 > artist):
#         return 1
#     else:
#         return -1

# def compareCanciones(cancion1, cancion2):
#     """
#     Compara dos tipos de canciones
#     """
#     cancion = me.getKey(cancion2)
#     if (cancion1 == cancion):
#         return 0
#     elif (cancion1 > cancion):
#         return 1
#     else:
#         return -1

# Funciones de ordenamiento

def artistasUnicos(lista):
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    sorted_list = mer.sort(sub_list, compareArtistas)
    print(sorted_list)
    size_sorted_list = lt.size(sorted_list)
    i = 0
    while i < size_sorted_list:
        if i != size_sorted_list:
            artista1 = lt.getElement(sorted_list, i)
            artista2 = lt.getElement(sorted_list, i + 1)
          
            if (artista1 == artista2):
                lt.deleteElement(sorted_list, i)
            i += 1
        else:
            if i == size_sorted_list:
                break

    sub_list = None
    return sorted_list

def cancionesUnicas(lista):
    size = lt.size(lista)
    sub_list = lt.subList(lista,0,size)
    sub_list = sub_list.copy()
    sorted_list = mer.sort(sub_list, compareCancion)
    print(sorted_list)
    # size_sorted_list = lt.size(sorted_list)
    # i = 0
    # while i < size_sorted_list:
    #     if i != size_sorted_list:
    #         artista1 = lt.getElement(sorted_list, i)
    #         artista2 = lt.getElement(sorted_list, i + 1)
          
    #         if (artista1 == artista2):
    #             lt.deleteElement(sorted_list, i)
    #         i += 1
    #     else:
    #         if i == size_sorted_list:
    #             break

    sub_list = None
    return sorted_list