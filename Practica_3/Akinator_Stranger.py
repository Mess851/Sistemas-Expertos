import json 
import os

# --- ESTRUCTURA DEL ÁRBOL DE DECISIÓN ---
class Nodo:
    # ... (La clase no cambia) ...
    def __init__(self, texto):
        self.texto = texto
        self.hijo_si = None
        self.hijo_no = None

    def es_hoja(self):
        return self.hijo_si is None and self.hijo_no is None

# --- TRADUCTORES (NUEVAS FUNCIONES) ---

def nodo_a_dict(nodo):
    """
    Función recursiva para convertir un árbol de Nodos a un diccionario.
    """
    if nodo.es_hoja():
        # Si es una hoja, es un simple diccionario con el texto.
        return {'texto': nodo.texto}
    
    # Si es una pregunta, crea un diccionario con el texto y sus hijos,
    # convirtiendo también a los hijos de forma recursiva.
    return {
        'texto': nodo.texto,
        'hijo_si': nodo_a_dict(nodo.hijo_si),
        'hijo_no': nodo_a_dict(nodo.hijo_no)
    }

def dict_a_nodo(diccionario):
    """
    Función recursiva para convertir un diccionario de vuelta a un árbol de Nodos.
    """
    # Crea el nodo actual a partir del texto del diccionario.
    nodo_actual = Nodo(diccionario['texto'])
    
    # Si el diccionario tiene hijos, significa que era una pregunta.
    if 'hijo_si' in diccionario:
        # Convierte los diccionarios hijos en Nodos de forma recursiva.
        nodo_actual.hijo_si = dict_a_nodo(diccionario['hijo_si'])
        nodo_actual.hijo_no = dict_a_nodo(diccionario['hijo_no'])
        
    return nodo_actual

# --- PERSISTENCIA DE DATOS (MODIFICADAS PARA JSON) ---

def guardar_conocimiento(nodo_raiz, archivo="conocimiento.json"):
    """
    Guarda el árbol de conocimiento en un archivo JSON.
    """
    diccionario_arbol = nodo_a_dict(nodo_raiz) # <-- Traduce el árbol a diccionario
    try:
        with open(archivo, "w", encoding='utf-8') as f:
            json.dump(diccionario_arbol, f, indent=4, ensure_ascii=False) # <-- Guarda el diccionario como JSON
        print("\n[Sistema: Conocimiento guardado en JSON.]")
    except Exception as e:
        print(f"\n[Error al guardar el conocimiento: {e}]")

def cargar_conocimiento(archivo="conocimiento.json"):
    """
    Carga el árbol de conocimiento desde un archivo JSON.
    """
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding='utf-8') as f:
                print("[Sistema: Cargando conocimiento desde JSON...]")
                diccionario_arbol = json.load(f) # <-- Carga el JSON a un diccionario
                return dict_a_nodo(diccionario_arbol) # <-- Traduce el diccionario a un árbol de Nodos
        except Exception as e:
            print(f"[Error al cargar el conocimiento, iniciando de cero: {e}]")
    
    print("[Sistema: No se encontró conocimiento previo. Creando uno nuevo.]")
    nodo_raiz = Nodo("¿Es un monstruo?")
    nodo_raiz.hijo_si = Nodo("demogorgon")
    nodo_raiz.hijo_no = Nodo("Once")
    return nodo_raiz

# --- MÓDULOS de aprender() y jugar() ---
# ... (Estas funciones no cambian en absoluto) ...
def aprender(nodo_actual):
    respuesta_incorrecta = nodo_actual.texto
    respuesta_correcta = ""
    while not respuesta_correcta:
        respuesta_correcta = input("¡Vaya, me rindo! ¿En qué estabas pensando? ").strip().capitalize()
    pregunta_nueva = ""
    while not pregunta_nueva:
        pregunta_nueva = input(f"Por favor, dame una pregunta que sea 'sí' para '{respuesta_correcta}' y 'no' para '{respuesta_incorrecta}': ").strip().capitalize()
    nodo_actual.texto = pregunta_nueva
    nodo_actual.hijo_si = Nodo(respuesta_correcta)
    nodo_actual.hijo_no = Nodo(respuesta_incorrecta)
    print("\n¡Gracias! He aprendido algo nuevo. Mi conocimiento ha crecido.")
    return True

def jugar(nodo_raiz):
    nodo_actual = nodo_raiz
    hubo_aprendizaje = False
    while not nodo_actual.es_hoja():
        respuesta = input(f"{nodo_actual.texto} (si/no): ").strip().lower()
        while respuesta not in ['si', 's', 'no', 'n']:
            respuesta = input("Por favor, responde 'si' o 'no': ").strip().lower()
        if respuesta in ['si', 's']:
            nodo_actual = nodo_actual.hijo_si
        else:
            nodo_actual = nodo_actual.hijo_no
    respuesta_final = input(f"¿Estás pensando en '{nodo_actual.texto}'? (si/no): ").strip().lower()
    if respuesta_final in ['si', 's']:
        print("\n¡Genial! ¡He adivinado! Soy el mejor. 🤖")
    else:
        hubo_aprendizaje = aprender(nodo_actual)
    return hubo_aprendizaje

# --- INICIO DEL PROGRAMA ---
if __name__ == "__main__":
    nodo_raiz = cargar_conocimiento()
    print("==============================================")
    print("¡Bienvenido al Simulador de Adivinación!")
    print("Piensa en algo y yo intentaré adivinarlo.")
    print("==============================================")
    while True:
        if jugar(nodo_raiz):
            guardar_conocimiento(nodo_raiz)
        jugar_de_nuevo = input("\n¿Quieres jugar otra vez? (si/no): ").strip().lower()
        if jugar_de_nuevo not in ['si', 's']:
            break
    guardar_conocimiento(nodo_raiz)
    print("¡Hasta la próxima!")