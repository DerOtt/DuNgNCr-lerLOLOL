import pygame, sys, time, random
from pygame.locals import *
from threading import Thread, Semaphore

#constants, do not change other than to debug
GAMESIZEX = 800
GAMESIZEY = 600
CELLSIZE = 20
KEYBOARD_DELAY = 0.25
GAMETICK = 0.05

#letters used in the map
PLAYER = '@'
NPC = 'N'
TREE = 'T'
WALL = '0'
GRASS = '.'
CONCRETE_FLOOR = '_'

#initialize the surfaces
pygame.init()
pygame.font.init()

#the surface area to draw on
windowArea = pygame.display.set_mode((GAMESIZEX, GAMESIZEY),0,32)

#helpVars
keyboardSpam = 0 #debug setting on
killSwitch = 1
coordsXPlayer = 1
coordsYPlayer = 1
keyCommands = []
semKeys = Semaphore()


#levelArray, WIP NEEDS TO BE MODULAR LATER. THIS IS ONLY DEBUG
LEVEL1 = [['0','0','0','0','0','0'],
        ['0', '.','.','.','.','0'],
        ['0', '.','.','.','.','0'],
        ['0','0','0','0','0','0']]


#Thread that draws 60 times a second refreshing the screen (aka redrawing every active element)
def draw():
    global killSwitch
    global coordsXPlayer, coordsYPlayer
    while killSwitch:
        windowArea.fill((0,0,0))
        for i in range(0,len(LEVEL1)):
            for j in range(0,len(LEVEL1[0])):
                if not (j == coordsXPlayer and i == coordsYPlayer):
                    if LEVEL1[i][j] == '0':
                        pygame.draw.rect(windowArea, (200,200,200), (j*CELLSIZE, i*CELLSIZE,CELLSIZE,CELLSIZE))
                    if LEVEL1[i][j] == '.':
                        pygame.draw.rect(windowArea, (0,255,0), (j*CELLSIZE, i*CELLSIZE,CELLSIZE,CELLSIZE))
                else:
                    #print(str(i) + " " + str(j) + " caused to draw a player")
                    pygame.draw.rect(windowArea, (255,0,0), (j*CELLSIZE, i*CELLSIZE,CELLSIZE,CELLSIZE))
        pygame.display.update()
        time.sleep(0.05)



#Thread that handles Userinput and is responsible to move the player around
def fetchUserInput():
    global killSwitch
    global semKeys
    tmp = 0
    keys = []
    while killSwitch:
        semKeys.acquire()
        keys = pygame.key.get_pressed()
        if keyboardSpam:
            for n in keys:
                keyCommands.append(n)
        else:
            for n in keys:
                tmp=0
                for k  in keyCommands:
                    if keyCommands[n] == keys[k]:
                        tmp=1
                if tmp:
                    keyCommands.append(k)
        semKeys.release()

#Thread which handles NPC movement once a second
def npcHandler():
    print("WIP")


#Thread that detects keyboard hold down. 
def keyboardSpam():
    global killSwitch
    keys = []
    while killSwitch:
        print("WIP FUCK THIS")

    print("WIP")



#GameTicker?
def gameTickThread():
    global semKeys
    global killSwitch
    global coordsYPlayer
    global coordsXPlayer
    while killSwitch:
        semKeys.acquire()
        #execute one command every 10 ticks
        for n in keyCommands:
            if (n == K_w and not coordsYPlayer-20 < 0):
                coordsYPlayer -= 20
            if (n == K_s and not coordsYPlayer+20 > GAMESIZEY):
                coordsYPlayer += 20
            if (n == K_a and not coordsXPlayer-20 < 0):
                coordsXPlayer -= 20
            if (n == K_d and not coordsXPlayer+20 > GAMESIZEX):
                coordsXPlayer += 20
            #print("Keys were checked")
            keyCommands.pop(0)
        semKeys.release()
        time.sleep(GAMETICK)



#Thread that effectively kills the window and also stops all other while true loops
def breakWindow():
    global killSwitch
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                killSwitch=0
        time.sleep(1)

threadPrinter = Thread(target = draw)
threadKiller = Thread(target = breakWindow)
threadGameTick = Thread(target = gameTickThread)
threadInputFetcher = Thread(target = fetchUserInput)

threadPrinter.start()
threadKiller.start()
threadGameTick.start()
threadInputFetcher.start()

