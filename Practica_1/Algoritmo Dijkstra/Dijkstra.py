import heapq

# La data que representa nuestro mapa
mapa_ciudad = {
    'Trabajo': {'Cafetería': 5, 'Gimnasio': 10},
    'Cafetería': {'Trabajo': 5, 'Supermercado': 8},
    'Gimnasio': {'Trabajo': 10, 'Supermercado': 4, 'Casa': 15},
    'Supermercado': {'Cafetería': 8, 'Gimnasio': 4, 'Casa': 7},
    'Casa': {'Gimnasio': 15, 'Supermercado': 7}
}

# Implementación del algoritmo
def dijkstra(grafo, inicio, fin):
    cola = [(0, inicio, [])]
    visitados = set()

    while cola:
        (tiempo, actual, ruta) = heapq.heappop(cola)
        if actual not in visitados:
            visitados.add(actual)
            ruta = ruta + [actual]
            if actual == fin:
                return (tiempo, ruta)
            for vecino, tiempo_viaje in grafo[actual].items():
                if vecino not in visitados:
                    heapq.heappush(cola, (tiempo + tiempo_viaje, vecino, ruta))
    return float("inf"), []

# --- Arrojar un resultado ---
inicio_ruta = 'Trabajo'
fin_ruta = 'Casa'
tiempo_final, ruta_optima = dijkstra(mapa_ciudad, inicio_ruta, fin_ruta)

print("\n--- Algoritmo de Dijkstra: Ruta más rápida a casa ---")
print(f"La ruta óptima es: {' -> '.join(ruta_optima)}")
print(f"El tiempo total de viaje es: {tiempo_final} minutos.")