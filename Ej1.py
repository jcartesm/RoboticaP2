import matplotlib as plt
import math as mt

nEstados = 9
#aEstados = [i for i in range(0,9)] # Estados
nIter = 100 # Iteracions
aDir = ["N","S","W","E"] # Direccion 
aRec = [] # Recorrido
nError = 0

def Reward(s):
    if s == 0:
        return 1
    if s == 8:
        return 1
    if s == 3:
        return -1
    if s == 6:
        return -1
    return 0

for i in range(0,nIter):
    aRec.append([0 for x in range(nEstados)])

nV = 0
aV = []

# Value Iteration
for i in range(1,nIter):
    for s in range(0,nEstados):
        for j in range(0,nEstados):
            nV += T1[s][j] * mt.exp(-Ld * at[j])*aRec[i-1][j]
