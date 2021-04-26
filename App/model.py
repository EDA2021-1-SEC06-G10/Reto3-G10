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
from datetime import datetime 
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
                'date_RBT':None,
                'info_VADER':None
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='CHAINING',
                                           loadfactor=4.0,
                                           #comparefunction=compareKeys                                              
                                          )
    catalog['generos'] = mp.newMap(9,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareGenre)
    catalog['info_VADER'] = mp.newMap(2500,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareGenre)
    
    catalog['instrumentalness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['liveness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['speechiness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['danceability_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['valence_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['loudness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['tempo_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['acousticness_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['energy_RBT'] = om.newMap(omaptype='RBT', comparefunction=compareValues)
    catalog['date_RBT'] =  om.newMap(omaptype='RBT', comparefunction=compareValues)
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
    lista = findGenre(catalog, cancion)
    lista2 = ['reggae','down-tempo',"chill-out","hip-hop","jazz and funk", "pop", "r&b", "rock", "metal"]
    addToGenre(catalog, lista, cancion)
    addDateTree(catalog,cancion, lista)
    addHTinfo(catalog, lista2, cancion)
    lista.clear()
    return catalog

# =================
# Para los géneros
# =================

def findGenre(catalog, cancion):
    lista=[]
    if (cancion["tempo"]>= 60) and (cancion['tempo']<= 90):
        lista.append("reggae")
    if (cancion["tempo"]>= 70) and (cancion['tempo']<= 100):
        lista.append("down-tempo")
    if (cancion["tempo"]>= 90) and (cancion['tempo']<= 120):
        lista.append("chill-out")
    if (cancion["tempo"]>= 85) and (cancion['tempo']<= 115):
        lista.append("hip-hop")
    if (cancion["tempo"]>= 120) and (cancion['tempo']<= 125):
        lista.append("jazz and funk")
    if (cancion["tempo"]>= 100) and (cancion['tempo']<= 130):
        lista.append("pop")
    if (cancion["tempo"]>=60) and (cancion['tempo']<= 80):
        lista.append("r&b")
    if (cancion["tempo"]>= 110) and (cancion['tempo']<= 140):
        lista.append("rock")
    if (cancion["tempo"]>= 100) and (cancion['tempo']<= 160):
        lista.append("metal")    
    return lista

def addToGenre(catalog, lista, cancion):
    try:

        generos = catalog['generos']
        for llave in lista:
        
            existeGen = mp.contains(generos, llave)
            if existeGen:
                entry = mp.get(generos, llave)
                gen = me.getValue(entry)
            else:
                gen = newGen(llave)
                mp.put(generos, llave, gen)
            
            mp.put(gen['artistas'], cancion["artist_id"],None)
            gen['reproducciones']+=1
    except Exception:
        return None


def newGen(genero):
    entry= {'artistas': None, "reproducciones":0}
    entry['artistas']= mp.newMap(3000,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareArtistid)
    return entry

def newGen2(genero):

    entry= {'canciones': None, "reproducciones":0}
    entry['canciones']= mp.newMap(3000,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareArtistid)
    return entry

# ================
# Meter hashtags por fechas
# ================

def addHTinfo(catalog, lista, cancion):
    arbol= catalog['date_RBT']
    fecha= cancion["created_at"]
    entry= om.get(arbol, fecha)
    tabla_Gen=me.getValue(entry)
    llenado(tablaGen,lista,cancion)
    return arbol

def llenado(tablaGen, lista, cancion):
    for llave in lista:
        existeGen = mp.contains(generos, llave)
        if existeGen:
            entry = mp.get(generos, llave)
            gen = me.getValue(entry)
            asociarHTcancion(entry,cancion) 
    return tablaGen

def asociar(entry, cancion):
    return

# ================
# Organizacion por fechas
# ================

def addDateTree(catalog, cancion, lista):
    fecha = cancion["created_at"]
    arbol= catalog['date_RBT']
    entry= om.get(arbol, fecha)
    if entry is None:
        dataentry=newGenEntry(cancion)
        om.put(arbol, fecha, dataentry)
        
    else:
        dataentry=me.getValue(entry)
    dataentry["fechaRepr"]+=1
    addGenre2(dataentry,lista,cancion)    
    return arbol

def newGenEntry(cancion):
    generosFecha={"fechaRepr": 0, "generos": None}
    generosFecha['generos']= mp.newMap(9,
                                  maptype='CHAINING',
                                  loadfactor=4.0,
                                  comparefunction=compareGenre)
    return generosFecha

def addGenre2(dataentry, lista, cancion):
    try:
        generos = dataentry['generos']
        for llave in lista:
        
            existeGen = mp.contains(generos, llave)
            if existeGen:
                entry = mp.get(generos, llave)
                gen = me.getValue(entry)
            else:
                gen = newGen2(llave)
                mp.put(generos, llave, gen)
            
            mp.put(gen['canciones'], cancion["track_id"],None)
            gen['reproducciones']+=1
    except Exception:
        return None
    
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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
        esta_track = lt.isPresent(dataentry['canciones'], filtrado['track_id'])
        if esta_track == 0:
            lt.addLast(dataentry['canciones'], filtrado)
        esta_artista = lt.isPresent(dataentry['artistas'], cancion['artist_id'])
        if esta_artista == 0:
            lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
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

# Funciones para creacion de datos

def newArtEntry(caracteristica, cancion):
    artentry = {'caracteristica': None, 'artistas': None , 'canciones': None, "reproducciones": None} # Elina, Nicolás, 
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

def consultaArtistas(catalog, categoria, rango_menor, rango_mayor):
    total_tamaño = 0
    hashTabla = catalog['caracteristicas']
    llaves = mp.get(hashTabla, categoria)
    arbol = me.getValue(llaves)
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_reproducciones = 0
    total_artistas = 0
    mapaArtistas = mp.newMap(22, maptype='CHAINING', loadfactor=4.0, comparefunction=compareArtistid)
    i = 1

    while i <= tamaño_tabla:
        tabla = lt.getElement(valores, i)

        lista_reproducciones = tabla['reproducciones']
        lista_artistas = tabla['artistas']
        size_lista_artistas = lt.size(lista_artistas)

        j = 1
        while j <= size_lista_artistas:
            elemento = lt.getElement(lista_artistas, j)
            mp.put(mapaArtistas, elemento, None)
            j += 1
        
        artistas_unicos = mp.keySet(mapaArtistas)
        total_artistas = lt.size(artistas_unicos)

        size_reproducciones = lt.size(lista_reproducciones)
        total_reproducciones += size_reproducciones

        i += 1

    return (total_reproducciones, total_artistas)

def consultaCanciones(catalog, categoria, rango_menor, rango_mayor):
    total_tamaño = 0
    hashTabla = catalog['caracteristicas']
    llaves = mp.get(hashTabla, categoria)
    arbol = me.getValue(llaves)
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_reproducciones = 0
    total_canciones = lt.newList('ARRAY_LIST')
    i = 1

    while i <= tamaño_tabla:
        tabla = lt.getElement(valores, i)

        lista_reproducciones = tabla['reproducciones']
        lista_canciones = tabla['canciones']
        size_lista_canciones = lt.size(lista_canciones)

        size_reproducciones = lt.size(lista_reproducciones)
        total_reproducciones += size_reproducciones

        j = 1
        while j <= size_lista_canciones:
            lista_canciones_unicas = lt.getElement(tabla['canciones'], j)
            lt.addLast(total_canciones, lista_canciones_unicas)
            j += 1

        i += 1
    
    #print(total_canciones)
    return (total_reproducciones, total_canciones)

def consultaReq2(catalog, categoria1, categoria2, rango_menor1, rango_mayor1, rango_menor2, rango_mayor2):

    lista_canciones_unicas = lt.newList('ARRAY_LIST', cmpfunction=compareTracksLista)

    tupla_1 = consultaCanciones(catalog, categoria1, rango_menor1, rango_mayor1)
    lista_canciones1 = tupla_1[1]
    size1 = lt.size(lista_canciones1)
    i = 1
    while i <= size1:
        cancion = lt.getElement(lista_canciones1, i)
        track = cancion['track_id']
        esta_track = lt.isPresent(lista_canciones_unicas, track)
        if esta_track == 0:
            if (cancion[categoria2] > rango_menor2) and (cancion[categoria2] < rango_mayor2):
                lt.addLast(lista_canciones_unicas, cancion)

        i += 1

    tupla_2 = consultaCanciones(catalog, categoria2, rango_menor2, rango_mayor2)
    lista_canciones2 = tupla_2[1]
    size2 = lt.size(lista_canciones2)
    j = 1
    while j <= size2:
        cancion = lt.getElement(lista_canciones2, j)
        track = cancion['track_id']
        esta_track = lt.isPresent(lista_canciones_unicas, track)
        if esta_track == 0:
            if (cancion[categoria1] > rango_menor1) and (cancion[categoria1] < rango_mayor1):
                lt.addLast(lista_canciones_unicas, cancion)

        j += 1
    
    #print(lista_canciones_unicas)
    size = lt.size(lista_canciones_unicas)

    return (size, lista_canciones_unicas)

def consultaReq4(catalog, genero):
    key_value = mp.get(catalog['generos'], genero)
    value = me.getValue(key_value)
    artistas = mp.keySet(value["artistas"])
    cantArt= lt.size(artistas)
    reproducciones= value["reproducciones"]
    rango= Rangos(genero)
    return cantArt, reproducciones, artistas, rango

def Rangos(genero):
    rango= 0
    if genero== "reggae":
        rango=(60,90)
    elif genero== "down-tempo":
        rango=(70,100)
    elif genero== "chill-out":
            rango=(90,120)
    elif genero== "hip-hop":
            rango=(85,115)
    elif genero== "jazz and funk":
            rango=(120, 125)
    elif genero== "pop":
            rango=(100, 130)
    elif genero== "r&b":
        rango=(60, 80)
    elif genero== "rock":
        rango=(110, 140)
    elif genero == "metal":
        rango=(100, 160)
    return rango

# Funciones utilizadas para comparar elementos dentro de una lista

def compareArtistid(Id, entry):
    """
    """
    identry= me.getKey(entry)
    if Id == identry:
        return 0
    elif Id > identry:
        return 1
    else:
        return -1

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

def compareGenre(Id, entry):
    """
    """
    identry= me.getKey(entry)
    if Id == identry:
        return 0
    elif Id > identry:
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

def horamilitar(stringAM):
    if "AM" in stringAM:
        stringAM = stringAM[:len(stringAM)-3]
    elif "PM" in stringAM:
        stringAM = stringAM[:len(stringAM)-3]
        if stringAM[1]==":":
            reemplazo= int(stringAM[0])+12
            stringAM[0]= str(reemplazo)
            print(stringAM)
        elif stringAM[2]==":":
            reemplazo= int(stringAM[0:2])+12
            stringAM[0]= str(reemplazo)+ stringAM[2:]
    stringAM= stringAM[:len(stringAM)-2]
    stringAM = stringAM+"00"
    return stringAM