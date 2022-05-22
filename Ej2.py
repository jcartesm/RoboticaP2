import numpy as np
import sys, pygame
from pygame.locals import *
from random import randint
import math as mt
import random as ra

nEstados    = 13
nIter       = 1000 # Iteracions
Lamda       = 0.95
e           = 0.0001
e           = e*(1-Lamda)/2*Lamda
k           = 1
aDir        = ["N","S","E","O"] # Direccion 
JOptimo     = [[0 for i in range(0,nEstados)]] # Jota Optimo (J*)
aP          = ["?" for i in range(0,nEstados)] # Acciones a tomar en estado
RecxAcc     = [0,0,0,0] # Reward x Accion
nError      = 0 # Error
aRec        = [] # matriz con las Iteraciones
nMax        = 0 # Maximo
nPos        = 0

nV1 = 0 ; nV2 = 0 
nV3 = 0 ; nV4 = 0 

                                     
#            0      1      2      3      4      5      6      7      8      9      10     11     12  Estado
mTNorte = [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 0
           [0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 1
           [0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 2
           [0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 3
           [0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 4
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 5
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 6
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 7
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 8
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.00 , 0.15 , 0.00 , 0.00 , 0.00],  # 9
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00],  # 10
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00],  # 11
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00],] # 12

                                     
#           0      1      2      3      4      5      6      7      8      9      10     11     12  Estado
mTSur = [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 0
         [0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 1
         [0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 2
         [0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 3
         [0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 4
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 5
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 6
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.00 , 0.85 , 0.00 , 0.00 , 0.00],  # 7
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 8
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00],  # 9
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],  # 10
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00],  # 11
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00],] # 12

                                      
#           0      1      2      3      4      5      6      7      8      9      10     11     12  Estado
mTEste = [[0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 0
         [0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 1
         [0.00 , 0.00 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00],  # 2
         [0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 3
         [0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 4
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 5
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 6
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 7
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85 , 0.00 , 0.00 , 0.00],  # 8
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.00 , 0.85 , 0.00],  # 9
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],  # 10
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.85],  # 11
         [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00],] # 12

                                     
#             0      1      2      3      4      5      6      7      8      9      10     11     12  Estado
mTOeste = [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 0
           [0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 1
           [0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 2
           [0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 3
           [0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 4
           [0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 5
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 6
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],  # 7
           [0.00 , 0.00 , 0.85 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.15 , 0.00 , 0.00 , 0.00 , 0.00],  # 8
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15 , 0.00 , 0.00 , 0.00],  # 9
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],  # 10
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.00 , 0.15 , 0.00],  # 11
           [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.85 , 0.15],] # 12

###############################################################################################################

                            #               Acciones

###############################################################################################################
# Accion     N     S         E     O Estado
ac1 =     [[0.0  , 0.0  ,  0.0  , 0.0 ],  # 0
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 1
           [0.0  , 0.0  , -1.0  , 0.0 ],  # 2
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 3
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 4
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 5
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 6
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 7
           [-1.0 , -1.0 ,  0.0  , 0.0 ],  # 8
           [0.0  , -1.0 ,  0.0  , -1.0],  # 9
           [0.0  , -1.0 ,  -1.0 , -1.0],  # 10
           [0.0  , 0.0  ,  0.0  , 0.0 ],  # 11
           [1.0  , 1.0  ,  1.0  , 0.0 ]]  # 12

# RecompenEstadosa por estado
# Estado s    0    1     2     3     4     5      6     7     8     9     10    11     12
aRwd =    [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -4.0 , 0.0 , -1.0 , 0.0 , +1.0 ]
acN =     [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -1.0 , 0.0 , 0.0 , 0.0 , +1.0 ]
acS =     [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -1.0 , -1.0 , -1.0 , 0.0 , +1.0 ]
acE =     [0.0 , 0.0 , -1.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -1.0 , 0.0 , +1.0 ]
acO =     [0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , 0.0 , -1.0 , -1.0 , 0.0 , 0.0 ]


def Norma(aA,aB):
    return (max([abs(aA[i]-aB[i]) for i in range(0,nEstados)]))

# Funcion Reward
def Reward(Estado,Accion):
    if Accion == 0: # Norte
        return (sum([mTNorte[Estado][i] * aRwd[i] for i in range(0,nEstados)]))
    if Accion == 1: # Sur
        return (sum([mTSur[Estado][i] * aRwd[i] for i in range(0,nEstados)]))
    if Accion == 2: # Este
        return (sum([mTEste[Estado][i] * aRwd[i] for i in range(0,nEstados)]))
    if Accion == 3: # Oeste
        return (sum([mTOeste[Estado][i] * aRwd[i] for i in range(0,nEstados)]))


# LLenar matriz de recorrido con 0
for i in range(0,nIter):
    aRec.append([0 for x in range(nEstados)])
aRR = []
maxRwd = 1
Q = np.zeros((nEstados,4))

# Value Iteration
for i in range(1,nIter):
    for s in range(nEstados):
        for j in range(nEstados):
            nV1 += mTNorte[s][j] *  aRec[i-1][j] #* mt.exp(-Lamda * acN[j])# * aRec[i-1][j] # Norte #aRec[i-1][j]
            nV2 += mTSur[s][j]   *  aRec[i-1][j] #* mt.exp(-Lamda * acS[j])# * aRec[i-1][j]   # Sur #aRec[i-1][j]
            nV3 += mTEste[s][j]  *  aRec[i-1][j] #* mt.exp(-Lamda * acE[j])# * aRec[i-1][j]  # Este #aRec[i-1][j]
            nV4 += mTOeste[s][j] *  aRec[i-1][j] #* mt.exp(-Lamda * acO[j])# * aRec[i-1][j] # Oeste #aRec[i-1][j]
            
        RecxAcc[0] = Reward(s,0) + (nV1 * Lamda)
        RecxAcc[1] = Reward(s,1) + (nV2 * Lamda)
        RecxAcc[2] = Reward(s,2) + (nV3 * Lamda)
        RecxAcc[3] = Reward(s,3) + (nV4 * Lamda)

        aRec[i][s] = max(RecxAcc)
        
        nV1 = 0 ; nV2 = 0 
        nV3 = 0 ; nV4 = 0 
        
        nMax = max(RecxAcc)
        nPos = RecxAcc.index(nMax)
        aP[s] = aDir[nPos]
    
    nError = Norma(aRec[i][:],aRec[i-1][:])
    #print("Recorrido en i = ",aRec[i])
    #print(nError)
    if nError < e: # almacenar el J* Optimo
        for k in range(0,nEstados):
            JOptimo[0][k] = aRec[i][k]
        print(" k optimo  = ", i , " , error => ", nError, " , J* Optimo => ",JOptimo)
        break

print('-'*87,
      '-'*87)
for s in range(0,nEstados):
 print ("En S_"+str(s)," => ",aP[s])    
print('='*87)

######################################################################################

#                              PYGAME SIMULATION

######################################################################################

pygame.init()
ventana = pygame.display.set_mode((875, 500))
pygame.display.set_caption('Value Iteration')
WHITE = (255, 255, 255)
ventana.fill(WHITE)
fondo = pygame.image.load("img/fondo.png")
fondo = pygame.transform.scale(fondo, [875, 500])
ventana.blit(fondo,[0,0])

pygame.display.flip()

# Cargado de Imagenes a ocupar
robot = pygame.image.load("img/robot.png")
robot = pygame.transform.scale(robot, [50, 50])

casilla = pygame.image.load("img/normal.png")
casilla = pygame.transform.scale(casilla, [125, 125])

casilla_win = pygame.image.load("img/win.png")
casilla_win = pygame.transform.scale(casilla_win, [125, 125])

casilla_bad = pygame.image.load("img/lose.png")
casilla_bad = pygame.transform.scale(casilla_bad, [125, 125])

def RestFondo():
    ventana.fill(WHITE)
    ventana.blit(fondo,[0,0])
    for i in range(0,7):  
        if i == 2:
            ventana.blit(casilla,[125*i,0])
            ventana.blit(casilla,[125*i,125])
        if i == 3:
            ventana.blit(casilla,[125*i,0])
        if i == 4:
            ventana.blit(casilla_bad,[125*i,375])
            ventana.blit(casilla_bad,[125*(i-1),250])
            ventana.blit(casilla,[125*i,0])
            ventana.blit(casilla,[125*i,125])  
        if i == 6:
            ventana.blit(casilla_win,[125*i,250])
        else:
            ventana.blit(casilla,[125*i,250])

def Mover(posActual,mov):
    x = posActual[0]
    y = posActual[1]
    if mov == "N":
        for i in range(25):
            if x > 784:
                return [x,y]
            y = y - 5
            RestFondo()
            ventana.blit(robot,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        return [x,y]
    if mov == "S":
        for i in range(25):
            y = y + 5
            #if y > 210:
            #    return [x,y-5]
            RestFondo()
            ventana.blit(robot,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        return [x,y]
    if mov == "E":
        for i in range(25):
            x = x + 5
            RestFondo()
            ventana.blit(robot,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        return [x,y]
    if mov == "O":
        for i in range(25):
            x = x - 5
            RestFondo()
            ventana.blit(robot,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        return [x,y]
    
RestFondo()

# Posicion inicial aleatoria del robot
Estado_Robot = [[35,285],[160,285],[285,285],[285,160],[285,35],[410,35],
                [535,35],[535,160],[410,285],[535,285],[535,410],[660,285],[785,285]]
indexIni =  ra.randint(0,3)
posRobot = Estado_Robot[indexIni]
ventana.blit(robot,[posRobot[0],posRobot[1]])

    
pygame.display.update()

is_running = True
while is_running:
    posRobot = Mover(posRobot,aP[indexIni])
    indexIni = Estado_Robot.index(posRobot)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

pygame.quit()