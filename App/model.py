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
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Sorting import quicksort as qui
from DISClib.ADT import orderedmap as om
from datetime import datetime 
import time
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
                'info_VADER':None,
                'generos': None
               }

    catalog['caracteristicas'] = mp.newMap(20,
                                           maptype='PROBING',
                                           loadfactor=0.5,
                                           #comparefunction=compareKeys                                              
                                          )
    catalog['generos'] = mp.newMap(9,
                                  maptype='PROBING',
                                  loadfactor=0.5,
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
    addDateTree(catalog,cancion, lista)
    addToGenre(catalog, lista, cancion)
    lista.clear()
    return catalog

def addHT(catalog, cancion):
   
    existe= mp.contains(catalog['info_VADER'], cancion['hashtag'])
    if existe== False:
        lista = ['reggae','down-tempo',"chill-out","hip-hop","jazz and funk", "pop", "r&b", "rock", "metal"]
        addHTinfo(catalog, lista, cancion)
    lista.clear()
    
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

    entry= {'canciones': None, "reproducciones": 1}
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
    llenado(tabla_Gen['generos'], lista, cancion)
    return arbol

def llenado(tablaGen, lista, cancion):
    lista_hashtags = lt.newList('ARRAY_LIST')
    for llave in lista:
        existeGen = mp.contains(tablaGen, llave)
        if existeGen:
            entry = mp.get(tablaGen, llave)
            gen = me.getValue(entry)
            esta_cancion = mp.contains(gen['canciones'], cancion['track_id'])
            if esta_cancion == False:
                mp.put(gen['canciones'], cancion["track_id"], lista_hashtags)
                lt.addLast(lista_hashtags, cancion["hashtag"])
            else:
                mp.put(gen['canciones'], cancion["track_id"], lista_hashtags)
                lt.addLast(lista_hashtags, cancion["hashtag"]) 
    return tablaGen

# ================
# Hash para Vaders
# ================

def addVader(catalog, hashtag):
    hashtags = catalog["info_VADER"]
    llave = hashtag['hashtag']
    existeHT =  mp.contains(hashtags, llave)
    if existeHT== False:
        mp.put(hashtags, llave, hashtag["vader_avg"])


# ========================
# Organizacion por fechas
# ========================

def addDateTree(catalog, cancion, lista):
    fecha = cancion["created_at"]
    arbol= catalog['date_RBT']
    entry= om.get(arbol, fecha)
    if entry is None:
        dataentry=newGenEntry(cancion)
        om.put(arbol, fecha, dataentry)
        
    else:
        dataentry=me.getValue(entry)
    dataentry["fechaRepr"] += 1
    addGenre2(dataentry, lista, cancion)    
    return arbol

def newGenEntry(cancion):
    generosFecha={"fechaRepr": 0, "generos": None}
    generosFecha['generos']= mp.newMap(9,
                                  maptype='PROBING',
                                  loadfactor=0.5,
                                  comparefunction=compareGenre)
    return generosFecha

def addGenre2(dataentry, lista, cancion):
    generos = dataentry['generos']

    for llave in lista:
        existeGen = mp.contains(generos, llave)
        if existeGen:
            entry = mp.get(generos, llave)
            gen = me.getValue(entry)
            gen['reproducciones'] += 1
        else:
            gen = newGen2(llave)
            mp.put(generos, llave, gen)
                
        mp.put(gen['canciones'], cancion["track_id"], None)
    
# ================================
# Creación de árboles principales
# ================================

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

    #print(arbol)
    return tabla

def addSongToTreeInstrumentalness(mapt, cancion):
    caracteristica = 'instrumentalness'
    categoria = cancion["instrumentalness"]
    entry = om.get(mapt, categoria)
    #print(entry)
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

        # artistas_par = mp.get(dataentry, 'artistas')
        # artistas = me.getValue(artistas_par)
        # lt.addLast(artistas, cancion['artist_id'])

        # canciones_par = mp.get(dataentry, 'canciones')
        # canciones = me.getValue(canciones_par)
        # lt.addLast(canciones, cancion['track_id'])

        # reproducciones_par = mp.get(dataentry, 'reproducciones')
        # reproducciones = me.getValue(reproducciones_par)
        # lt.addLast(reproducciones, cancion['track_id'])

        lt.addLast(dataentry['canciones'], filtrado)
        lt.addLast(dataentry['artistas'], cancion["artist_id"])
        lt.addLast(dataentry["reproducciones"], cancion["track_id"])
       
    else:
        # dataentry = me.getValue(entry)
 
        # canciones_par = mp.get(dataentry, 'canciones')
        # canciones = me.getValue(canciones_par)
        # esta_track = lt.isPresent(canciones, filtrado['track_id'])
        # if esta_track == 0:
        #     lt.addLast(canciones, filtrado)

        # artistas_par = mp.get(dataentry, 'artistas')
        # artistas = me.getValue(artistas_par)
        # esta_artista = lt.isPresent(artistas, cancion['artist_id'])
        # if esta_artista == 0:
        #     lt.addLast(artistas, cancion["artist_id"])
        
        # reproducciones_par = mp.get(dataentry, 'reproducciones')
        # reproducciones = me.getValue(reproducciones_par)
        # lt.addLast(reproducciones, cancion["track_id"])

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

    # artentry = mp.newMap(8, maptype='PROBING', loadfactor=0.5) #, comparefunction=compareArtistas)

    # lista_artistas = lt.newList('ARRAY_LIST', compareArtistas)
    # lista_canciones = lt.newList('ARRAY_LIST', compareCanciones)
    # lista_reproducciones = lt.newList('ARRAY_LIST')

    # mp.put(artentry, 'caracteristica', caracteristica)
    # mp.put(artentry, 'artistas', lista_artistas)
    # mp.put(artentry, 'canciones', lista_canciones)
    # mp.put(artentry, 'reproducciones', lista_reproducciones)

    return artentry

# ======================
# Funciones de consulta
# ======================

def indexHeightInstrumentalness(catalog):
    return om.height(catalog['instrumentalness_RBT'])

def indexSizeInstrumentalness(catalog):
    return om.size(catalog['instrumentalness_RBT'])

    # ==================================
    # Funciones para el Requerimiento 1
    # ==================================

def consultaArtistas(catalog, categoria, rango_menor, rango_mayor):
    total_tamaño = 0
    hashTabla = catalog['caracteristicas']
    llaves = mp.get(hashTabla, categoria)
    arbol = me.getValue(llaves)
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_reproducciones = 0
    total_artistas = 0
    artistas_unicos = None
    mapaArtistas = mp.newMap(3000, maptype='CHAINING', loadfactor=4.0, comparefunction=compareArtistid)
    i = 1

    while i <= tamaño_tabla:
        tabla = lt.getElement(valores, i)

        # artistas_par = mp.get(tabla, 'artistas')
        # lista_artistas = me.getValue(artistas_par)

        # reproducciones_par = mp.get(tabla, 'reproducciones')
        # lista_reproducciones = me.getValue(reproducciones_par)
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

    return (total_artistas, total_reproducciones, artistas_unicos)

    # ========================================
    # Funciones para los Requerimientos 2 y 3
    # ========================================

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

    # ===================================
    # Funciones para el Requerimiento 4
    # ===================================

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

    # ==================================
    # Funciones para el Requerimiento 5
    # ==================================

        # ========
        # Parte 1
        # ========

def reproduccionesTotalesEnRangoHoras(catalog, rango_menor, rango_mayor):
    total_tamaño = 0
    arbol = catalog['date_RBT']
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_reproducciones = 0
    i = 1

    while i <= tamaño_tabla:
        diccionario = lt.getElement(valores, i)
        reproducciones = diccionario['fechaRepr']
        total_reproducciones += reproducciones
        i += 1
    
    return total_reproducciones

def crearListaGeneros(catalog, keyset, rango_menor, rango_mayor):
    total_tamaño = 0
    arbol = catalog['date_RBT']
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    total_reproducciones = 0
    lista_generos = lt.newList('ARRAY_LIST')
    size_generos = lt.size(keyset)
    j = 1
    while j <= size_generos:
        elemento = lt.getElement(keyset, j)
        esta_genero = lt.isPresent(lista_generos, elemento)
        if esta_genero == 0:
            lt.addLast(lista_generos, elemento)
        j += 1
        
    return lista_generos
    
def consultaGenero(catalog, rango_menor, rango_mayor):
    
    total_tamaño = 0
    arbol = catalog['date_RBT']
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    generos = mapaTempGen()
    i = 1
    while i <= tamaño_tabla:
        diccionario = lt.getElement(valores, i)
        tablaGeneros = diccionario['generos']
        keyset = mp.keySet(tablaGeneros)
        tamaño_diferentes_generos = lt.size(keyset)
        j = 1
        while j <= tamaño_diferentes_generos:
            genero = lt.getElement(keyset, j)
            elemento = mp.get(tablaGeneros, genero)
            if elemento != None:
                valor = me.getValue(elemento)
                reproducciones = valor['reproducciones']
                genero2=mp.get(generos,genero)
                value= me.getValue(genero2)
                value+=reproducciones
                mp.put(generos,genero, value)

            j += 1
        
        i += 1

    return generos

def mapaTempGen():
    lista = ['reggae','down-tempo',"chill-out","hip-hop","jazz and funk", "pop", "r&b", "rock", "metal"]
    i=0
    size= len(lista)
    mapa= mp.newMap(9, maptype='PROBING', loadfactor=0.5)

    while i < size:
        llave=lista[i]
        mp.put(mapa,llave, 0)
        i+=1
    return mapa

def consultaTopGeneros(catalog, rango_menor, rango_mayor):
    generos = consultaGenero(catalog, rango_menor, rango_mayor)
    lista = lt.newList('ARRAY_LIST')
    llaves = mp.keySet(generos)
    size_llaves = lt.size(llaves)
    k = 1
    while k <= size_llaves:
        elemento = lt.getElement(llaves, k)
        pareja = mp.get(generos, elemento)
        lt.addLast(lista, pareja)
        k += 1

    return lista

        # ========
        # Parte 2
        # ========

def crearPequeñaLista(lista_vieja, lista_nueva):
    size = lt.size(lista_vieja)
    i = 1
    while i <= size:
        elemento = lt.getElement(lista_vieja, i)
        lt.addLast(lista_nueva, elemento)
        i += 1
    return lista_nueva

def crearMapaTracks(catalog, rango_menor, rango_mayor, genero):
    arbol = catalog['date_RBT']
    valores = om.values(arbol, rango_menor, rango_mayor)
    tamaño_tabla = lt.size(valores)
    cancionesUnicas = mp.newMap(3000, maptype='CHAINING', loadfactor=4.0, comparefunction=compareArtistid)
    lista_hashtags = lt.newList('ARRAY_LIST')
    i = 1
    while i <= tamaño_tabla:
        diccionario = lt.getElement(valores, i)
        tablaGeneros = diccionario['generos']
        diccionario_2 = mp.get(tablaGeneros, genero)
        if diccionario_2 != None:
            tablaCanciones = diccionario_2['value']['canciones']
            llaves = mp.keySet(tablaCanciones)
            size_llaves = lt.size(llaves)
            j = 1
            while j <= size_llaves:
                elemento = lt.getElement(llaves, j)
                pareja = mp.get(tablaCanciones, elemento)
                llave = me.getKey(pareja)
                valor = me.getValue(pareja)
                esta = mp.contains(cancionesUnicas, llave)
                if esta == False:
                    mp.put(cancionesUnicas, llave, valor)
                    # k = 1
                    # while k <= lt.size(valor):
                    #     elemento = lt.getElement(valor, k)
                    #     lt.addLast(lista_hashtags, elemento)
                    #     #crearPequeñaLista(valor, lista_hashtags)
                    #     mp.put(cancionesUnicas, llave, lista_hashtags)
                else:
                    pareja = mp.get(cancionesUnicas, llave)
                    valor2 = me.getValue(pareja)
                    k = 1
                    while k <= lt.size(valor):
                        elemento = lt.getElement(valor, k)
                        esta = lt.isPresent(valor, elemento)
                        if esta == 0:
                            lt.addLast(valor2, elemento)
                        #crearPequeñaLista(valor, valor2)
                        #mp.put(cancionesUnicas, llave, valor2)
                        k += 1
                j += 1
        i += 1

    total = mp.keySet(cancionesUnicas)
    total_canciones_unicas = lt.size(total)
    return (cancionesUnicas, total_canciones_unicas)

def darthVaderPorUnaCancion(catalog, tabla, cancion_id, rango_menor, rango_mayor, genero):
    tablaCanciones = crearMapaTracks(catalog, rango_menor, rango_mayor, genero)
    pareja = mp.get(tablaCanciones[0], cancion_id)
    valor = me.getValue(pareja)
    size_hashtags = lt.size(valor)
  
    tablaHashtags = catalog['info_VADER']
  
    total_vader = 0
    i = 1
    while i <= size_hashtags:
        elemento = lt.getElement(valor, i)
        # esta = mp.contains(tablaHashtags, elemento)
        # if esta == True:
        pareja = mp.get(tablaHashtags, elemento)
        vader_avg = me.getValue(pareja)
        vader_avg= float(vader_avg)
        total_vader += vader_avg
        i += 1
  
    vader_promedio = total_vader / size_hashtags

    tupla = (size_hashtags, vader_promedio)
    return tupla

def vaderPromedioParaCadaCancion(catalog, rango_menor, rango_mayor, genero):
    tablaCanciones = crearMapaTracks(catalog, rango_menor, rango_mayor, genero)
    llaves = mp.keySet(tablaCanciones[0])
    size_llaves = lt.size(llaves)
    nueva_hash = mp.newMap(3000, maptype='CHAINING', loadfactor=4.0, comparefunction=compareArtistid)
    i = 1
    while i <= size_llaves:
        elemento = lt.getElement(llaves, i)
        tupla = darthVaderPorUnaCancion(catalog, tablaCanciones, elemento, rango_menor, rango_mayor, genero)
        mp.put(nueva_hash, elemento, tupla)
        i += 1
    return nueva_hash      

def topCancionesPorGenero(catalog, rango_menor, rango_mayor, genero):
    tablaGeneros = vaderPromedioParaCadaCancion(catalog, rango_menor, rango_mayor, genero)
    lista = lt.newList('ARRAY_LIST')
    llaves = mp.keySet(tablaGeneros)
    size_llaves = lt.size(llaves)
    i = 1
    while i <= size_llaves:
        elemento = lt.getElement(llaves, i)
        pareja = mp.get(tablaGeneros, elemento)
        lt.addLast(lista, pareja)
        i += 1
    return lista

# =================================================================
# Funciones utilizadas para comparar elementos dentro de una lista
# =================================================================

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

def compareByHashtags(hash1, hash2):
    result = hash1['value'][0] > hash2['value'][0]
    return result

def compareHashtags(hashtag1, hashtag2):
    result = hashtag1['value'] > hashtag2['value']
    return result    
    
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

# ==========================
# Funciones de ordenamiento
# ==========================

def sortByNumberOfReproductions(lista):
    size = lt.size(lista)
    sub_list = lt.subList(lista, 0, size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = qui.sort(sub_list, compareByHashtags)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)    

def sortByHashTags(lista):
    size = lt.size(lista)
    sub_list = lt.subList(lista, 0, size)
    sub_list = sub_list.copy()
    t1 = time.process_time()
    sorted_list = qui.sort(sub_list, compareHashtags)
    t2 = time.process_time()
    tiempo_ms = (t2-t1)*1000
    sub_list = None
    return (tiempo_ms, sorted_list)

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

#============================
# INTENTO DEL 5.2
#============================
