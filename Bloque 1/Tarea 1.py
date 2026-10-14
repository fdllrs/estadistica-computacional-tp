from codigo_base import *

rng = np.random.default_rng(4)   # cada grupo usa su propia semilla

posiblesPermutaciones = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
# Armamos la lista de permutaciones
frecuenciaPermutaciones = [0] * 6
for i in range (6000):
    permutacion = permutacion_aleatoria(3, rng)
    frecuenciaPermutaciones[posiblesPermutaciones.index(permutacion)] += 1
    

print(frecuenciaPermutaciones)

#

