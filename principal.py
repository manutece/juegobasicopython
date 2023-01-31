#! /usr/bin/env python
import os, random, sys, math

import pygame
from pygame.locals import *

from configuracion import *
from funcionesVACIAS import *
from extras import *

#Funcion principal
def main():

        #Centrar la ventana y despues inicializar pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        #pygame.mixer.init()

        #Preparar la ventana
        pygame.display.set_caption("Armar palabras...")
        screen = pygame.display.set_mode((ANCHO, ALTO))

        #tiempo total del juego
        gameClock = pygame.time.Clock()
        totaltime = 0
        segundos = TIEMPO_MAX
        fps = FPS_inicial
       #musica
        pygame.mixer.music.load("sonido/musicafondo.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)


        puntos = 0
        candidata = ""
        listaIzq = []
        listaMedio = []
        listaDer = []
        posicionesIzq = []
        posicionesMedio = []
        posicionesDer = []
        lista = []

        archivo= open("lemario.txt","r")
        for linea in archivo.readlines():
            lista.append(linea[0:-1])

        #DIFICULTAD
        dif=int(input("Ingrese la dificultad a la que quiere jugar\n1=FACIL\n2=DESAFIO"))
        if dif==2:
            fps=10

        cargarListas(lista, listaIzq, listaMedio, listaDer, posicionesIzq , posicionesMedio, posicionesDer)
        dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq ,
                posicionesMedio, posicionesDer, puntos,segundos)

        while segundos > fps/1000:
        # 1 frame cada 1/fps segundos
            gameClock.tick(fps)
            totaltime += gameClock.get_time()

            if dif==1:
                fps+=0.03
            else:
                fps+=0.02

            #Buscar la tecla apretada del modulo de eventos de pygame
            for e in pygame.event.get():

                #QUIT es apretar la X en la ventana
                if e.type == QUIT:
                    pygame.quit()
                    return()

                #Ver si fue apretada alguna tecla
                if e.type == KEYDOWN:
                    letra = dameLetraApretada(e.key)
                    candidata += letra
                    if e.key == K_BACKSPACE:
                        candidata = candidata[0:len(candidata)-1]
                    if e.key == K_RETURN:
                        puntos += procesar(lista, candidata, listaIzq, listaMedio, listaDer)
                        candidata = ""

            segundos = TIEMPO_MAX - pygame.time.get_ticks()/1000

            #Limpiar pantalla anterior
            screen.fill(COLOR_FONDO)

            #Dibujar de nuevo todo
            dibujar(screen, candidata, listaIzq, listaMedio, listaDer, posicionesIzq ,
                posicionesMedio, posicionesDer, puntos,segundos)

            pygame.display.flip()

            actualizar(lista, listaIzq, listaMedio, listaDer, posicionesIzq,
                posicionesMedio, posicionesDer)
        while 1:
            #Esperar el QUIT del usuario
            if puntos>=100 and dif==2:
                fondo=pygame.image.load("ganaste.png")
                screen.blit(fondo,(0,0))
                pygame.display.update()
            elif puntos<100 and dif==2:
                fondo=pygame.image.load("perdiste.png")
                screen.blit(fondo,(0,0))
                pygame.display.update()

            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return

##Programa Principal ejecuta Main
if __name__ == "__main__":
    main()


