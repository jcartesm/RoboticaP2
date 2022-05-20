import numpy as np

# vector de probabilidades historicas
Apriori = [0.7, 0.2, 0.1]  # produccion, mantencion,reparacion

#S     P     M     R       S
P = np.array([[0.90, 0.07, 0.03], # P
            [0.85, 0.10, 0.05], # M
            [0.60, 0.10, 0.30]]) # R


P_x_7d = np.dot(Apriori,np.linalg.matrix_power(P,7))
print("Probabilidad que la maquina funcione durante 7 dias => ",P_x_7d[0], " %")

M_in_3d = np.dot(Apriori,np.linalg.matrix_power(P,3))
print("Probabilidad que la maquina entre en mantencion en 3 dias => ",M_in_3d[1], " %")

R_in_5d = np.dot(Apriori,np.linalg.matrix_power(P,5))
print("Probabilidad que la maquina entre en reparacion en 5 dias => ",R_in_5d[2], " %")

