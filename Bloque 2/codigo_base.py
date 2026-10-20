import json
import numpy as np


# ---------------------------------------------------------------------------
# Algoritmos instrumentados
# ---------------------------------------------------------------------------
def insertion_sort(lista):
    """Ordena una copia de `lista` por inserción.

    Devuelve (swaps, comparaciones). El elemento a[i] se lleva hacia la
    izquierda con swaps adyacentes mientras sea menor que su vecino.
    """
    a = list(lista)
    swaps = comparaciones = 0
    for i in range(1, len(a)):
        j = i
        while j > 0:
            comparaciones += 1
            if a[j - 1] > a[j]:
                a[j - 1], a[j] = a[j], a[j - 1]
                swaps += 1
                j -= 1
            else:
                break
    return swaps, comparaciones


def selection_sort(lista):
    """Ordena una copia de `lista` por selección.

    Devuelve (swaps, comparaciones). Solo se hace swap si el mínimo encontrado
    no está ya en su lugar.
    """
    a = list(lista)
    swaps = comparaciones = 0
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comparaciones += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            swaps += 1
    return swaps, comparaciones


def quicksort(lista, pivote="primero"):
    """Ordena una copia de `lista` con quicksort (partición de Lomuto).

    pivote = "primero": el pivote es el primer elemento del subarreglo.
    pivote = "medio":   el elemento del medio se lleva al principio y se usa
                        como pivote (ese movimiento previo NO cuenta como swap).

    Cada partición de un subarreglo de largo L hace exactamente L-1
    comparaciones (cada elemento contra el pivote). Se usa una pila explícita
    en lugar de recursión para no romper el límite de Python con listas
    ordenadas (peor caso).

    Devuelve (swaps, comparaciones).
    """
    a = list(lista)
    swaps = comparaciones = 0
    pila = [(0, len(a) - 1)]
    while pila:
        lo, hi = pila.pop()
        if lo >= hi:
            continue
        if pivote == "medio":
            m = (lo + hi) // 2
            a[lo], a[m] = a[m], a[lo]
        p = a[lo]
        i = lo
        for j in range(lo + 1, hi + 1):
            comparaciones += 1
            if a[j] < p:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps += 1
        a[lo], a[i] = a[i], a[lo]
        swaps += 1
        pila.append((lo, i - 1))
        pila.append((i + 1, hi))
    return swaps, comparaciones


ALGORITMOS = {
    "insertion": insertion_sort,
    "selection": selection_sort,
    "quick_primero": lambda l: quicksort(l, "primero"),
    "quick_medio": lambda l: quicksort(l, "medio"),
}


# ---------------------------------------------------------------------------
# Generadores de entradas aleatorias
# ---------------------------------------------------------------------------
def permutacion_aleatoria(n, rng):
    """Permutación uniforme de 0..n-1 (las n! tienen la misma probabilidad)."""
    return [int(v) for v in rng.permutation(n)]


def lista_desordenada(n, k, rng):
    """Lista ordenada 0..n-1 a la que se aplican k transposiciones al azar.

    En cada paso se eligen dos posiciones i, j uniformes e independientes en
    {0, ..., n-1} (pueden coincidir, en cuyo caso no cambia nada) y se
    intercambian. k = 0 es la lista ordenada; k grande se parece a una
    permutación uniforme.
    """
    a = list(range(n))
    for i, j in rng.integers(0, n, size=(k, 2)):
        a[i], a[j] = a[j], a[i]
    return a


# ---------------------------------------------------------------------------
# Medición
# ---------------------------------------------------------------------------
def medir(experimento, algoritmos, n, N, rng, k=None):
    """Corre cada algoritmo sobre las MISMAS N listas aleatorias de tamaño n.

    k=None usa permutaciones uniformes; k entero usa `lista_desordenada`.
    Devuelve una lista de diccionarios, uno por (lista, algoritmo). El campo
    `lista` identifica la entrada (útil para comparaciones apareadas) y
    `experimento` es una etiqueta para separar las distintas corridas.
    """
    filas = []
    for r in range(N):
        if k is None:
            entrada = permutacion_aleatoria(n, rng)
        else:
            entrada = lista_desordenada(n, k, rng)
        for nombre in algoritmos:
            swaps, comps = ALGORITMOS[nombre](entrada)
            filas.append({"experimento": experimento, "algoritmo": nombre,
                          "n": n, "k": k, "lista": r,
                          "swaps": swaps, "comparaciones": comps})
    return filas


def guardar_jsonl(filas, archivo):
    with open(archivo, "w") as f:
        for fila in filas:
            f.write(json.dumps(fila) + "\n")


if __name__ == "__main__":
    rng = np.random.default_rng(2026)   # cada grupo usa su propia semilla
    filas = []

    # 1) permutaciones uniformes, n = 100
    filas += medir("uniforme", ["insertion", "selection", "quick_primero", "quick_medio"],
                   n=100, N=2000, rng=rng)
    # 2) distintos tamaños de lista (complejidad)
    for n in [10, 20, 50, 100, 200, 500, 1000]:
        filas += medir("tamanos", ["insertion", "quick_primero"], n=n, N=200, rng=rng)
    # 3) listas con desorden controlado, n = 100
    for k in [0, 5, 10, 25, 50, 100, 150, 200, 300, 500]:
        filas += medir("desorden", ["insertion", "quick_primero"], n=100, N=300,
                       rng=rng, k=k)

    guardar_jsonl(filas, "conteos.jsonl")
    print(f"{len(filas)} mediciones guardadas en conteos.jsonl")
