# --- La Data: (costo, colonia1, colonia2) ---
conexiones_posibles = [
    (2, 'C', 'D'),
    (3, 'B', 'C'),
    (4, 'A', 'B'),
    (5, 'A', 'C'),
    (6, 'D', 'E'),
    (7, 'B', 'E'),
    (8, 'C', 'E'),
    (10, 'A', 'D')
]

# --- Implementación del algoritmo de Kruskal ---
parent = {nodo: nodo for nodo in ['A', 'B', 'C', 'D', 'E']}

def find_set(v):
    if v == parent[v]:
        return v
    parent[v] = find_set(parent[v])
    return parent[v]

def union_sets(a, b):
    a = find_set(a)
    b = find_set(b)
    if a != b:
        parent[b] = a

# --- Arrojar un resultado ---
arbol_expansion_minima = []
costo_total = 0

# Ordenar las conexiones de la más barata a la más cara
conexiones_posibles.sort()

for costo, u, v in conexiones_posibles:
    if find_set(u) != find_set(v):
        union_sets(u, v)
        arbol_expansion_minima.append((u, v))
        costo_total += costo

print("\n--- Algoritmo de Kruskal (Árbol de Expansión Mínima): Red de Fibra Óptica ---")
print("Las conexiones a realizar para minimizar el costo son:")
for u, v in arbol_expansion_minima:
    print(f"- Conectar Colonia {u} con Colonia {v}")
print(f"El costo total mínimo para conectar todas las colonias es: ${costo_total},000 USD")