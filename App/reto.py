"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from time import process_time 
from Sorting import insertionsort   
from Sorting import mergesort  
from Sorting import quicksort   
from Sorting import selectionsort  
from Sorting import shellsort 

def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking")
    print("7- encontrar peliculas buenas")
    print("0- Salir")

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1

def loadCSVFile (file, cmpfunction):
    lst=lt.newList("ARRAY_LIST", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(  cf.data_dir + file, encoding="utf-8") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst


def loadMovies ():
    lst = loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def rankingPeliculas(function, lst, criteria, elements):
    """
    Retorna el ranking de películas con base en los parámetros
     Args:
        function
            Función de ordenamiento que se va a usar
        column:: str
            Columna que se usa para realiza el ordenamiento (vote_average o vote_count)   
        lst
            Lista encadenada o arreglo     
        criteria:: str
            Critero para ordenar (less o greater)
        elements:: int
            Cantidad de elementos para el ranking
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    t1_start = process_time() #tiempo inicial
    if function == "selectionsort":
       selectionsort.selectionSort(lst, criteria)
    if function == "insertionsort":
       insertionsort.insertionSort(lst, criteria)
    if function == "mergesort":
       mergesort.mergesort(lst, criteria)
    if function == "quicksort":
       quicksort.quickSort(lst, criteria)
    if function == "shellsort":
       shellsort.shellSort(lst, criteria)
    i = 0
    ordenado = []
    while i < elements:
       i += 1
       pelicula = lt.getElement(lst,i)
       ordenado.append(pelicula)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos")       
    return ordenado

def entenderGenero(genero, lst):
    """
    Retorna la lista, el número y el promedio de votos de las películas de un género cinematográfico
     Args:
        genero
            Género cinematográfico
        column:: str
            Columna que se usa para realiza el ordenamiento (vote_average o vote_count)   
        lst
            Lista encadenada o arreglo     
        criteria:: str
            Critero para ordenar (less o greater)
        elements:: int
            Cantidad de elementos para el ranking
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """   
    asociadas = [] 
    total = 0
    votos = 0
    for pelicula in lst["elements"]:
        genre = pelicula["genres"]
        if genero.lower() in genre.lower():
           asociadas.append(pelicula)
           total += 1
           votos += int(pelicula["vote_count"])
    prom_votos = votos / total       
    res = asociadas, total, prom_votos
    return res

def conocerDirector(director,datos):
    r=0
    numero_peliculas=0
    lista=[]
    id_peliculas=[]
    while r<len(datos):
        p=datos[r]
        if p["director_name"]== director:
            numero_peliculas+=1
            lista.append(p)
            id_peliculas.append(p["id"])
        r+=1
    return numero_peliculas,lista,id_peliculas
def votos_media(id_peliculasa,lista):
    r=0
    suma=0
    promedio=0
    while r<len(lista):
        p=lista[r]
        for i in id_peliculasa:
            if i == p["id"]:
                suma+=float(p["vote_average"])
        r+=1
    if suma > 0:
        promedio=suma/len(id_peliculasa)
    return promedio   
def encontrar_peliculas_buenas(lista1,lista2,nombre):
    promedio=0
    lista2_elementos=lista2["elements"]
    lista1_elementos=lista1["elements"]
    
    fila=0
    ids=[]
    suma=0
    cantidad_peliculas=0
    while fila < len(lista2_elementos):
        if lista2_elementos[fila]["director_name"] == nombre:
            ids.append(lista2_elementos[fila]["id"]) 
        fila+=1
    fila=0
    while fila < len(lista1_elementos):
        for i in ids:
            if lista1_elementos[fila]["id"] == i:
                o=lista1_elementos[fila]["vote_average"]
                if float(o) >= 6:
                    suma+=float(o)
                    cantidad_peliculas+=1
        fila+=1
    if cantidad_peliculas >0:
        promedio=suma/cantidad_peliculas
    return (promedio,cantidad_peliculas)

def conocer_actor(lista1,lista2,nombre):
    lista2_elementos=lista2["elements"]
    lista1_elementos=lista1["elements"]
    nombre_prueba="Jean-Louis Barrault"
    fila=0
    lista_peliculas=[]
    directores=[]
    peliculas=0
    ids=[]
    directores_dict={}
    mayor=0
    directores_final=[]
    while fila < len(lista2_elementos):
        if lista2_elementos[fila]['actor1_name'] == nombre:
            peliculas+=1
            ids.append(lista2_elementos[fila]['id'])
            lista_peliculas.append(lista2_elementos[fila])
            directores.append(lista2_elementos[fila]["director_name"])
        elif lista2_elementos[fila]['actor2_name'] == nombre:
            peliculas+=1
            ids.append(lista2_elementos[fila]['id'])
            lista_peliculas.append(lista2_elementos[fila])
            directores.append(lista2_elementos[fila]["director_name"])
        elif lista2_elementos[fila]['actor3_name'] == nombre:
            peliculas+=1
            ids.append(lista2_elementos[fila]['id'])
            lista_peliculas.append(lista2_elementos[fila])
            directores.append(lista2_elementos[fila]["director_name"])
        elif lista2_elementos[fila]['actor4_name'] == nombre:
            peliculas+=1
            ids.append(lista2_elementos[fila]['id'])
            lista_peliculas.append(lista2_elementos[fila])
            directores.append(lista2_elementos[fila]["director_name"])
        elif lista2_elementos[fila]['actor5_name'] == nombre:
            peliculas+=1
            ids.append(lista2_elementos[fila]['id'])
            lista_peliculas.append(lista2_elementos[fila])
            directores.append(lista2_elementos[fila]["director_name"])
        fila+=1
    fila=0
    promedio=0
    while fila < len(lista1_elementos):
        for i in ids:
            if lista1_elementos[fila]['id'] == i:
                promedio+=float(lista1_elementos[fila]["vote_average"])
        promedio=promedio/peliculas
        fila+=1
    for t in directores:
        if t not in directores_dict:
            directores_dict[t]=1
        elif t in directores_dict:
            y=directores_dict[t]
            w=float(y)+1
            directores_dict[t]=w
    for h in directores_dict:
        if directores_dict[h] >mayor:
            directores_final=[]
            mayor=directores_dict[h]
            directores_final.append(h)
        elif directores_dict[h] == mayor:
            directores_final.append(h)
    
    return (promedio,peliculas,directores_final,lista_peliculas)
            
def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs[0])==1: #opcion 1
                lstmovies = loadMovies()

            elif int(inputs[0])==2: #opcion 2
                lista = lstmovies
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:   
                    print("Hay 5 algoritmos de ordenamiento: \ninsertionsort\nmergesort\nquicksort\nselectionsort\nshellsort")    
                    ## Pide los parámetros al usuario
                    algoritmo = input("Escriba el algoritmo de ordenamiento que desee usar: ")
                    columna = input("Escriba la columna a utilizar (vote_average o vote_count): ")  
                    criteria = input("Escriba el criterio a utilizar (less o greater): ") 
                    elements = int(input("¿Cuántas películas quiere ver en el ranking?: "))
                    def less(element1, element2, column=columna): # Agregué "column" para poder escoger, por ejemplo, entre vote_average y vote_count
                        if float(element1[column]) < float(element2[column]):
                           return True
                        return False
                    def greater(element1, element2,column=columna):
                        if float(element1[column]) > float(element2[column]):
                           return True
                        return False  
                    if criteria == "less":
                       lista = rankingPeliculas(algoritmo, lista, less, elements)
                    elif criteria == "greater":
                       lista = rankingPeliculas(algoritmo, lista, greater, elements)
                    print("Películas ordenadas: \n")   
                    print(lista)        
                pass

            elif int(inputs[0])==3: #opcion 3
                lista = lstmovies
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")
                else:       
                    lista = lstmovies
                    director = input("Escriba el director: ")
                    e = conocerDirector(director,lista)
                    w=votos_media(e[2],lstmovies)
                    print(w)
                    print("El numero de peliculas dirigidas por {0} fueron {1} con un promedio de {2}".format(t,e[0],w))
                    print("La lista de las peliculas dirigidas son {o}")
                    print(e[1])
                    print("La lista esta vacía")    

            elif int(inputs[0])==4: #opcion 4
                lista1=loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds)
                lista2=loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds)
                nombre=input("¿que actor deseas buscar?\n")
                p=conocer_actor(lista1,lista2,nombre)
                if len(p[2]) > 1:
                    print("El actor {0} ha colaborado con {1} directores la misma cantidad de veces, \nlos nombres de los directores son {2}".format(nombre,len(p[2]),p[2]))
                    print("el numero de peliculas en las que aparece el actor son {0}, con un promedio de {1}".format(p[1],p[0]))
                    print("la lista de peliculas en las que participo son:")
                    print(p[3])
                elif len(p[2]) == 0:
                    print("El actor {0} no ha actuado con ningun director".format(nombre))
                elif len(p[2]) == 1:
                    print("El actor {0} ha actuado con {1} mas veces que con cualquier otro dircetor".format(nombre,p[2],))
                    print("el numero de peliculas en las que aparece el actor son {0}, con un promedio de {1}".format(p[1],p[0]))
                    print("la lista de peliculas en las que participo son:")
                    print(p[3])
                pass

            elif int(inputs[0])==5: #opcion 5
                lista = lstmovies
                if lista==None or lista['size']==0: #obtener la longitud de la lista
                    print("La lista esta vacía")    
                else:
                    genero = input("Escriba el género cinematográfico: ")
                    res_genero = entenderGenero(genero, lstmovies)
                    lista_genero = res_genero[0]
                    numero = res_genero[1]
                    votos = res_genero[2]
                print("Lista de peliculas:",lista_genero,"\n")
                print("Numero de peliculas:",numero,"\n") 
                print("Promedio de votos:",votos,"\n")    
                pass

            elif int(inputs[0])==6: #opcion 6
                pass
            elif int(inputs[0])==7: #opcion 7 (Req 1)
                nombre_director=input("¿Qué director busca?: \n")
                lista1=loadCSVFile("theMoviesdb/SmallMoviesDetailsCleaned.csv",compareRecordIds)
                lista2=loadCSVFile("theMoviesdb/MoviesCastingRaw-small.csv",compareRecordIds)
                u=encontrar_peliculas_buenas(lista1,lista2,nombre_director)
                print("El director {0} tiene {1} peliculas buenas con un promedio de {2}".format(nombre_director,u[1],u[0]))
                pass

            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()