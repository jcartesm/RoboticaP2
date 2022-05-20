import numpy as np
import sys, pygame
from pygame.locals import *
from random import randint
import math as mt

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



# # Creacion de Proceso principal de PyGame
# def main():
#     # Variables iniciales
#     Ancho = 160
#     Alto  = 240
#     # Colores Iniciales
#     CCeleste = (153,217,234)
#     CAzul = (63,72,204)
#     CRojo = (237,28,36)
#     CNegro = (0,0,0)

#     # Carga de assets
#     # Se carga el icono de flecha, los iconos de robots
#     # y se redimenEstadosionan
#     Flecha = pygame.image.load("assets/arrow.png")
#     Flecha = pygame.tranEstadosform.scale(Flecha, (38, 38))
#     Robot = pygame.image.load("assets/robot.png")
#     Robot = pygame.tranEstadosform.scale(Robot, (38, 38))
#     RobotAnt = pygame.image.load("assets/robot2.png")
#     RobotAnt = pygame.tranEstadosform.scale(RobotAnt, (38, 38))

#     # Creacion de Objeto Pantalla
#     pantalla = pygame.display.set_mode((Ancho,Alto))
#     # Fuentes de Texto
#     pygame.font.init()
#     myfont = pygame.font.SysFont('Romand', 10)
#     # Titulo
#     pygame.display.set_caption("Laboratorio 3")
#     # Relleno Pantalla
#     pantalla.fill(CNegro)


#     # Creacion de arreglos con posiciones de lineas
#     mPos = []
#     for y in range(0,201,40):
#         for x in range(0,121,40):
#             mPos.append([x,y])

#     # Con la cuadricula generada se dibujan los cuadrados
#     # Si corresponden a ciertas ubicaciones detalladas en el mapa
#     # se pintan del color respectivo
#     for Data in mPos:
#         if Data==[80,0] or Data==[80,80] or Data==[0,120]:
#             pygame.draw.rect(pantalla, CRojo ,[Data[0],Data[1],38,38],0)
#         elif Data==[120,0]:
#             pygame.draw.rect(pantalla, CAzul ,[Data[0],Data[1],38,38],0)
#         else:
#             pygame.draw.rect(pantalla, CCeleste ,[Data[0],Data[1],38,38],0)
    
#     # Se genera el camino con las politicas
#     for Data in sL:
#         # Angulo de giro
#         A=0
#         # Posicion actual
#         X=mPos[Data[0]][0]
#         Y=mPos[Data[0]][1]
#         # Se actualiza el angulo segun lo que indica la politica
#         if Data[1]=='N':
#             A=90
#         elif Data[1]=='E':
#             A=0
#         elif Data[1]=='S':
#             A=-90
#         elif Data[1]=='O':
#             A=-180
#         # Se gira la flecha y se muestra en la posicion del nuevo centro
#         FlechaR=pygame.tranEstadosform.rotate(Flecha,A)
#         FlechaP=FlechaR.get_rect(center = Flecha.get_rect(topleft = (X,Y)).center)
#         # Se escribe en el cuadrado la posicion en el mapa
#         Texto=myfont.render(str(Data[0]), False, (0, 0, 0))
#         # Se genera un nuevo blit con los objetos
#         pantalla.blit(FlechaR,FlechaP)
#         pantalla.blit(Texto,(X,Y))

#     # Se genera posicion aleatoria del robot
#     RS=randint(0,23)
#     # Se almacena la posicion en relacion al dato aleatorio
#     RoboPos=[mPos[RS],RS]
#     # Se muestra en pantalla
#     pantalla.blit(Robot,RoboPos[0])
#     pygame.display.update()
#     # Inicio ciclo del programa
#     while True:
#         # Retraso entre cada actualizacion
#         pygame.time.delay(500)
#         # Si el robot aun no llega a la meta
#         if RoboPos[1]!=3:
#             # Se suma la distancia de un cuadrado dependiendo
#             # de lo que indica la politica
#             if sL[RoboPos[1]][1]=='N':
#                 X=0
#                 Y=-40
#             elif sL[RoboPos[1]][1]=='E':
#                 X=40
#                 Y=0
#             elif sL[RoboPos[1]][1]=='S':
#                 X=0
#                 Y=40
#             elif sL[RoboPos[1]][1]=='O':
#                 X=-40
#                 Y=0
#             # Se marca la posicion antigua
#             pantalla.blit(RobotAnt,RoboPos[0])
#             # Se genera la nueva posicion
#             RoboPos[0]=SumT(RoboPos[0],(X,Y))
#             # Se busca el estado que coincida con la nueva posicion generada
#             # y se almacena dicho estado
#             for i in range(0,len(mPos)):
#                 if mPos[i][0]==RoboPos[0][0] and mPos[i][1]==RoboPos[0][1]:
#                     RoboPos[1]=i
#                     break
#             # Se genera la nueva posicion en pantalla
#             pantalla.blit(Robot,RoboPos[0])
#             # Se actualiza la pantalla
#             pygame.display.update()
#         for eventos in pygame.event.get():
#             if eventos.type == QUIT:
#                 sys.exit(0)
#     return 
 
# if __name__ == '__main__':
#     pygame.init()
#     main()