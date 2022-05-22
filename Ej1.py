import matplotlib.pyplot as plt
import math as mt
import pygame
import numpy as np
import random as ra

nEstados    = 9
nIter       = 1000 # Iteracions
Lamda       = 0.98
e           = 0.001
k           = 1
aDir        = ["N","S","E","O"] # Direccion 
JOptimo     = [[0 for i in range(0,nEstados)]] # Jota Optimo (J*)
aP          = ["?" for i in range(0,nEstados)] # Acciones a tomar en estado
RwdxAcc     = [0,0,0,0] # Reward x Accion
nError      = 0 # Error
aRec        = [] # matriz con las Iteraciones
nMax        = 0 # Maximo
nPos        = 0

nV1 = 0 ; nV2 = 0 
nV3 = 0 ; nV4 = 0

arNorte = []; arSur = []; arEste = []; arOeste = []
arNorteJ = []; arSurJ = []; arEsteJ = []; arOesteJ = []

#Estado        0      1      2      3      4      5      6      7      8   Estado
mTNorte=   [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 0
            [0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 1
            [0.00 , 0.00 , 0.10 , 0.90 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 2
            [0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 3
            [0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00],# 4
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00],# 5
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.90 , 0.10 , 0.00 , 0.00],# 6
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00],# 7
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00]]# 8

#Estado        0      1      2      3      4      5      6      7      8   Estado
mTSur=     [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 0
            [0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 1
            [0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 2
            [0.00 , 0.00 , 0.90 , 0.10 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 3
            [0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00],# 4
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.10 , 0.90 , 0.00 , 0.00],# 5
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],# 6
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00],# 7
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00]]# 8

#Estado        0      1      2      3      4      5      6      7      8   Estado
mTEste=    [[0.10 , 0.90 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 0
            [0.00 , 0.10 , 0.90 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 1
            [0.00 , 0.00 , 0.10 , 0.00 , 0.90 , 0.00 , 0.00 , 0.00 , 0.00],# 2
            [0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 3
            [0.00 , 0.00 , 0.00 , 0.00 , 0.10 , 0.90 , 0.00 , 0.00 , 0.00],# 4
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.10 , 0.00 , 0.90 , 0.00],# 5
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],# 6
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.10 , 0.90],# 7
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00]]# 8

#Estado        0      1      2      3      4      5      6      7      8   Estado
mTOeste=   [[1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 0
            [0.90 , 0.10 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 1
            [0.00 , 0.90 , 0.10 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 2
            [0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00],# 3
            [0.00 , 0.00 , 0.90 , 0.00 , 0.10 , 0.00 , 0.00 , 0.00 , 0.00],# 4
            [0.00 , 0.00 , 0.00 , 0.00 , 0.90 , 0.10 , 0.00 , 0.00 , 0.00],# 5
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 1.00 , 0.00 , 0.00],# 6
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.90 , 0.10 , 0.00],# 7
            [0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.00 , 0.90 , 0.10]]# 8

# Recompensa por estado
# Estado s    0    1     2      3     4     5      6     7     8
aRwd =     [1.0 , 0.0 , 0.0 , -1.0 , 0.0 , 0.0 , -1.0 , 0.0 , 1.0 ]

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


#Comprobar que la suma de transicion de 1
# for i in mTranOeste:
#      porcentaje = 0.0
#      for k in i:
#          porcentaje += k
#      print(porcentaje)

# Norma
def Norma(aA,aB):
    return (max([abs(aA[i]-aB[i]) for i in range(0,nEstados)]))

# LLenar matriz de recorrido con 0
for i in range(0,nIter):
    aRec.append([0 for x in range(nEstados)])

# Value Iteration
for i in range(1,nIter):
    for s in range(0,nEstados):
        for j in range(0,nEstados):
            nV1 += mTNorte[s][j] *  aRec[i-1][j]  #mt.exp(-nDesc * aRwd[j])*aRec[i-1][j] # Norte
            nV2 += mTSur[s][j]   *  aRec[i-1][j]  #mt.exp(-nDesc * aRwd[j])*aRec[i-1][j]   # Sur
            nV3 += mTEste[s][j]  *  aRec[i-1][j]  #mt.exp(-nDesc * aRwd[j])*aRec[i-1][j]  # Este
            nV4 += mTOeste[s][j] *  aRec[i-1][j]  #mt.exp(-nDesc * aRwd[j])*aRec[i-1][j] # Oeste
            
        RwdxAcc[0] = aRwd[s] + (nV1 * Lamda)  
        RwdxAcc[1] = aRwd[s] + (nV2 * Lamda)
        RwdxAcc[2] = aRwd[s] + (nV3 * Lamda) 
        RwdxAcc[3] = aRwd[s] + (nV4 * Lamda) 

        arNorte.append(RwdxAcc[0])
        arSur.append(RwdxAcc[1])
        arEste.append(RwdxAcc[2])
        arOeste.append(RwdxAcc[3])
        
        aRec[i][s] = max(RwdxAcc)
        
        nV1 = 0 ; nV2 = 0 
        nV3 = 0 ; nV4 = 0 
        
        #print(RwdxAcc)
        nMax = max(RwdxAcc)
        nPos = RwdxAcc.index(nMax)
        aP[s] = aDir[nPos]

    nError = Norma(aRec[i],aRec[i-1])
    #print("Recorrido en i = ",aRec[i])
    #print(nError)
    if nError < e: # almacenar el J* Optimo
        for k in range(0,nEstados):
            JOptimo[0][k] = aRec[i][k]
        print(" k optimo  = ", i , " , error => ", nError, " , J* Optimo => ",JOptimo)
        break
# Calculo de la Mejor Accion a tomar en los Estados S(i) segun JOptimo (J*).-
for s in range(0,nEstados):
    for j in range(0,nEstados):
        nV1 += mTNorte[s][j] * JOptimo[0][j]  
        nV2 += mTSur[s][j]   * JOptimo[0][j]
        nV3 += mTEste[s][j]  * JOptimo[0][j]
        nV4 += mTOeste[s][j] * JOptimo[0][j]
   
    RwdxAcc[0] = aRwd[s] + (nV1 * Lamda) # Accion 1-Norte
    RwdxAcc[1] = aRwd[s] + (nV2 * Lamda) # Accion 2-Sur
    RwdxAcc[2] = aRwd[s] + (nV3 * Lamda) # Accion 3-Este
    RwdxAcc[3] = aRwd[s] + (nV4 * Lamda) # Accion 4-Oeste

    arNorteJ.append(RwdxAcc[0])
    arSurJ.append(RwdxAcc[1])
    arEsteJ.append(RwdxAcc[2])
    arOesteJ.append(RwdxAcc[3])

    nV1 = 0; nV2 = 0; nV3 = 0; nV4 = 0 
    #print 'Estado[%d] Reward Accion [N]: %0.3f Reward Accion [S]: %0.3f Reward Accion [E]: %0.3f Reward Accion [O]: %0.3f' %(s,nA[0],nA[1],nA[2],nA[3])   

    nMax = max(RwdxAcc)
    nPos = RwdxAcc.index(nMax)
    aP[s] = aDir[nPos]

    
print('-'*87,
      '-'*87)
for s in range(0,nEstados):
 print ("En S_"+str(s)," => ",aP[s])    
print('='*87)


######################################################################################

#                              Graficas Matplotlib

######################################################################################


fig_E, ax_Vs = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
plt.suptitle("Valores de V(s) por accion")

fig_V, ax_VsJ = plt.subplots(nrows=2, ncols=2, figsize=(10,10))
plt.suptitle("Valores de V(s) por accion con JOptimo")

x = np.arange(0,3087)
x_2 = np.arange(0,9)

ax_Vs[0, 0].plot(x,arNorte,'b',linewidth = 2)
ax_Vs[0, 0].set_xlabel('t')
ax_Vs[0, 0].set_ylabel('valores')
ax_Vs[0, 0].set_title("A Norte")
ax_Vs[0, 0].grid()

ax_Vs[0, 1].plot(x,arSur,'r',linewidth = 2)
ax_Vs[0, 1].set_xlabel('t')
ax_Vs[0, 1].set_ylabel('valores')
ax_Vs[0, 1].set_title("A Sur")
ax_Vs[0, 1].grid()

ax_Vs[1, 0].plot(x,arEste,'y',linewidth = 2)
ax_Vs[1, 0].set_xlabel('t')
ax_Vs[1, 0].set_ylabel('valores')
ax_Vs[1, 0].set_title("A Este")
ax_Vs[1, 0].grid()

ax_Vs[1, 1].plot(x,arOeste,'g',linewidth = 2)
ax_Vs[1, 1].set_xlabel('t')
ax_Vs[1, 1].set_ylabel('valores')
ax_Vs[1, 1].set_title("A Oeste")
ax_Vs[1, 1].grid()

ax_VsJ[0, 0].plot(x_2,arNorteJ,'r',linewidth = 2)
ax_VsJ[0, 0].set_xlabel('t')
ax_VsJ[0, 0].set_ylabel('valores')
ax_VsJ[0, 0].set_title("A Norte")
ax_VsJ[0, 0].grid()

ax_VsJ[0, 1].plot(x_2,arSurJ,'b',linewidth = 2)
ax_VsJ[0, 1].set_xlabel('t')
ax_VsJ[0, 1].set_ylabel('valores')
ax_VsJ[0, 1].set_title("A Sur")
ax_VsJ[0, 1].grid()

ax_VsJ[1, 0].plot(x_2,arEsteJ,'y',linewidth = 2)
ax_VsJ[1, 0].set_xlabel('t')
ax_VsJ[1, 0].set_ylabel('valores')
ax_VsJ[1, 0].set_title("A Este")
ax_VsJ[1, 0].grid()

ax_VsJ[1, 1].plot(x_2,arOesteJ,'g',linewidth = 2)
ax_VsJ[1, 1].set_xlabel('t')
ax_VsJ[1, 1].set_ylabel('valores')
ax_VsJ[1, 1].set_title("A Oeste")
ax_VsJ[1, 1].grid()


plt.show()

######################################################################################

#                              PYGAME SIMULATION

######################################################################################

# Seteo de la ventana
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
            ventana.blit(casilla_bad,[125*i,50])
        if i == 4:
            ventana.blit(casilla_bad,[125*i,300])  
        if i == 0 or i == 6:
            ventana.blit(casilla_win,[125*i,175])
        else:
            ventana.blit(casilla,[125*i,175])

def Mover(posActual,mov):
    x = posActual[0]
    y = posActual[1]
    if mov == "N":
        for i in range(25):
            y = y - 5
            if y < 210:
                return [x,y+5]
            RestFondo()
            ventana.blit(robot,[x,y])
            pygame.display.update()                            
            pygame.time.delay(40)
        return [x,y]
    if mov == "S":
        for i in range(25):
            y = y + 5
            if y > 210:
                return [x,y-5]
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
Estado_Robot = [[35,210],[160,210],[285,210],[285,85],[410,210],[535,210],[535,335],[660,210],[785,210]]
indexIni =  ra.randint(2,6)
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







