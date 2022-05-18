import matplotlib as plt
import math as mt

nEstados    = 9
nIter       = 1000 # Iteracions
Lamda       = 0.98
e           = 0.001
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
            
        RecxAcc[0] = aRwd[s] + (nV1 * Lamda)  
        RecxAcc[1] = aRwd[s] + (nV2 * Lamda)
        RecxAcc[2] = aRwd[s] + (nV3 * Lamda) 
        RecxAcc[3] = aRwd[s] + (nV4 * Lamda) 
        
        aRec[i][s] = max(RecxAcc)
        
        nV1 = 0 ; nV2 = 0 
        nV3 = 0 ; nV4 = 0 
        
        print(RecxAcc)
        nMax = max(RecxAcc)
        nPos = RecxAcc.index(nMax)
        aP[s] = aDir[nPos]

    nError = Norma(aRec[i],aRec[i-1])
    #print("Recorrido en i = ",aRec[i])
    print(nError)
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
   
    RecxAcc[0] = aRwd[s] + (nV1 * Lamda) # Accion 1-Norte
    RecxAcc[1] = aRwd[s] + (nV2 * Lamda) # Accion 2-Sur
    RecxAcc[2] = aRwd[s] + (nV3 * Lamda) # Accion 3-Este
    RecxAcc[3] = aRwd[s] + (nV4 * Lamda) # Accion 4-Oeste

    nV1 = 0; nV2 = 0; nV3 = 0; nV4 = 0 
    #print 'Estado[%d] Reward Accion [N]: %0.3f Reward Accion [S]: %0.3f Reward Accion [E]: %0.3f Reward Accion [O]: %0.3f' %(s,nA[0],nA[1],nA[2],nA[3])   

    nMax = max(RecxAcc)
    nPos = RecxAcc.index(nMax)
    aP[s] = aDir[nPos]

    
print('-'*87,
      '-'*87)
for s in range(0,nEstados):
 print ("En S_"+str(s)," => ",aP[s])    
print('='*87)
        
