from principal import *
from configuracion import *

import random
import math

def cargarseg(letra,numpos,listaizq,listamedio,listader):
#Esta funcion toma una letra y la carga en un segmento de la pantalla
    if numpos==1:
        listaizq.append(letra)
        return 1
    elif numpos==2:
        listamedio.append(letra)
        return 2
    elif numpos==3:
        listader.append(letra)
        return 3

def estaCerca(elem, lista):
    #es opcional, se usa para evitar solapamientos
    for pos in range(0,len(lista)):                #Recorre la lista y si algun elemento tiene una distancia menor al modulo de 15..
        if (elem-lista[pos][0])>-15 and (elem-lista[pos][0])<15:  #..retorna verdadero si no hay ninguno cerca retorna falso
            return True
    return False

def cargarpos(letra,numpos,posizq,posmedio,posder,aux):
                                #Esta funcion toma la letra y el segmento al que pertenece y le asigna..
    if numpos==1:                             #..un valor numerico perteneciente al propio segmento
        x1=random.randrange(5,(800//3)-5)
        y=12
        while estaCerca(x1,aux)==True:       #Mientras que la posx este cerca de otra sigue buscando un numero
            x1=random.randrange(5,(800//3)-5)
        posizq.append([x1,y])                #Se appendean los numeros asignados a la letra a la lista de posiciones
        aux.append([x1,y])
    elif numpos==2:
        x2=random.randrange((800//3)+5,(2*(800//3))-5)
        y=random.randrange(1,30)
        while estaCerca(x2,aux)==True:
            x2=random.randrange((800//3)+5,(2*(800//3))-5)
        posmedio.append([x2,y])
        aux.append([x2,y])
    elif numpos==3:
        x3=random.randrange(2*(800//3)+5,795)
        y=random.randrange(1,30)
        while estaCerca(x3,aux)==True:
            x3=random.randrange(2*(800//3)+5,795)
        posder.append([x3,y])
        aux.append([x3,y])

def cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer):
    #elige una palabra de la lista y la carga en las 3 listas
    # y les inventa una posicion para que aparezca en la columna correspondiente
    indice=random.randrange(0,len(lista))     #Elige un indice al azar
    pal=lista[indice]
    segmento=1                       #Con el indice elige una palabra de la lista
    limite=4
    posaux=[]
    for letra in pal:                                 #Recorre la palabra y con la funcion asigna cada letra a un segmento
        if len(posaux)<2:               #si posaux tiene menos de dos elementos la letra se asigna directamente al primer cuadrante
            limite=2
        elif len(posaux)<4:            #si posaux tiene menos de cuatro elementos la letra tiene como limite el segundo cuadrante
            limite=3
        else:                         #si tiene cuatro o mas elementos la letra puede asignarse hasta el cuarto cuadrante
            limite=4
        numpos=random.randrange(segmento,limite)
        segmento=cargarseg(letra,numpos,listaIzq,listaMedio,listaDer)
        cargarpos(letra,numpos,posicionesIzq,posicionesMedio,posicionesDer,posaux)

def donde(elem,lista):               #Funcion para saber en que indice se encuentra un elemento
    for x in range(0,len(lista)):
        if lista[x]==elem:
            return x

def elimina(letra,lista,posiciones):
        indice=donde(letra,lista)
        lista.pop(indice)
        posiciones.pop(indice)


def bajar(lista, posiciones):
    # hace bajar las letras y elimina las que tocan el piso
    for x in range(0,len(posiciones)):
        posiciones[x][1]+=6
    for letra in lista:
        indice=donde(letra,lista)
        if posiciones[indice][1] > ALTO-80:
            elimina(letra,lista,posiciones)


def actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer):
    ## llama a otras funciones para bajar bajar las letras, eliminar las que tocan el piso y
    ## cargar nuevas letras a la pantalla (esto puede no hacerse todo el tiempo para que no se llene de letras la pantalla)
    bajar(listaIzq,posicionesIzq)
    bajar(listaMedio,posicionesMedio)
    bajar(listaDer,posicionesDer)
    if posicionesIzq[-1][1]==180:
        cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer)


def puntos(candidata):
    voc = 0
    consonante = 0
    consonanteDF = 0
    for i in candidata:
        if i in "aeiouAEIOU":
            voc = voc + 1
        elif i in "bcdfghlmnprstv":
            consonante = consonante + 1
        elif i in "jkqwxyzJKQWXYZ":
            consonanteDF = consonanteDF + 1
    puntaje=(voc*1)+(consonante*2)+(consonanteDF*5)
    return puntaje

def noesta(elem,lista):  #Busca si un elemento no esta en una lista
    bandera=True
    for palabra in lista:
        if palabra==elem:
            bandera=False
    return bandera


def procesar(lista, candidata, listaIzq, listaMedio, listaDerecha):
    #chequea que candidata sea correcta en cuyo caso devuelve el puntaje y 0 si no es correcta
    listaerror=[pygame.mixer.Sound("sonido/error2.ogg"),pygame.mixer.Sound("sonido/error3.ogg")]
    listaacierto=[pygame.mixer.Sound("sonido/valid1.ogg"),pygame.mixer.Sound("sonido/valid2.ogg"),pygame.mixer.Sound("sonido/valid3.ogg"),pygame.mixer.Sound("sonido/valid4.ogg")]
    if esValida(lista, candidata, listaIzq, listaMedio, listaDerecha):
        indice=donde(candidata,lista)
        lista.pop(indice)
        listaacierto[random.randrange(0,4)].play()
        return puntos(candidata)
    else:
        listaerror[random.randrange(0,2)].play()
        return 0

def esta(elem,lista):     #Busaca si un elemento esta en una lista
    for letra in lista:
        if letra==elem:
            return True
    return False


def esValida(lista, candidata, listaIzq, listaMedio, listaDerecha):
    #devuelve True si candidata cumple con los requisitos
    aux=""
    seg=1
    if esta(candidata,lista):          #recorre a candidata
        for letra in candidata:
            if esta(letra,listaIzq) and seg<=1:   #si la letra esta en el primer segmento y el seg es menor o..
                aux+=letra                        #..igual a 1 se agrega la letra a a aux
            elif esta(letra,listaMedio) and seg<=2:  #si la letra esta en el segundo segmento y el seg es menor..
                aux+=letra                           #o igual a 2 se agrega la letra a aux y se cambia el seg a 2
                seg=2
            elif esta(letra,listaDerecha) and seg<=3:  #si la letra esta en el tercer segmento y el seg es menor..
                aux+=letra                           #o igual a 3 se agrega la letra a aux y se cambia el seg a 3
                seg=3
        if aux==candidata:                      #finalmente si el aux coincide con la candidata es valida
            return True
    else:
        return False






