import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # <-- Importamos Pillow
import json
import os

# --- 1. LÓGICA DEL ÁRBOL Y JSON (Tu código original) ---

class Nodo:
    def __init__(self, texto):
        self.texto = texto
        self.hijo_si = None
        self.hijo_no = None

    def es_hoja(self):
        return self.hijo_si is None and self.hijo_no is None

def nodo_a_dict(nodo):
    if nodo.es_hoja():
        return {'texto': nodo.texto}
    return {
        'texto': nodo.texto,
        'hijo_si': nodo_a_dict(nodo.hijo_si),
        'hijo_no': nodo_a_dict(nodo.hijo_no)
    }

def dict_a_nodo(diccionario):
    nodo_actual = Nodo(diccionario['texto'])
    if 'hijo_si' in diccionario:
        nodo_actual.hijo_si = dict_a_nodo(diccionario['hijo_si'])
        nodo_actual.hijo_no = dict_a_nodo(diccionario['hijo_no'])
    return nodo_actual

def cargar_conocimiento(archivo="conocimiento.json"):
    """
    Carga el árbol de conocimiento desde un archivo JSON.
    """
    if os.path.exists(archivo):
        try:
            with open(archivo, "r", encoding='utf-8') as f:
                print("[Sistema: Cargando conocimiento desde JSON...]")
                diccionario_arbol = json.load(f)
                return dict_a_nodo(diccionario_arbol)
        except Exception as e:
            print(f"[Error al cargar, iniciando de cero: {e}]")
    
    # Este es tu árbol inicial, pero recomiendo usar el JSON que te pasé
    print("[Sistema: No se encontró JSON o falló la carga. Creando uno nuevo.]")
    nodo_raiz = Nodo("¿Es un monstruo?")
    nodo_raiz.hijo_si = Nodo("Demogorgon")
    nodo_raiz.hijo_no = Nodo("Once")
    return nodo_raiz

def guardar_conocimiento(nodo_raiz, archivo="conocimiento.json"):
    """
    Guarda el árbol de conocimiento en un archivo JSON.
    """
    diccionario_arbol = nodo_a_dict(nodo_raiz)
    try:
        with open(archivo, "w", encoding='utf-8') as f:
            json.dump(diccionario_arbol, f, indent=4, ensure_ascii=False)
        print("\n[Sistema: Conocimiento guardado en JSON.]")
    except Exception as e:
        print(f"\n[Error al guardar el conocimiento: {e}]")


# --- 2. CLASE DE LA INTERFAZ GRÁFICA (AkinatorGUI) ---

class AkinatorGUI:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Adivinador de Stranger Things")
        self.root.geometry("500x600") # Ancho x Alto
        self.root.resizable(False, False)

        # Cargar el conocimiento
        self.nodo_raiz = cargar_conocimiento()
        self.nodo_actual = self.nodo_raiz

        # --- Widgets (Componentes visuales) ---

        # Etiqueta para el texto (preguntas y adivinanzas)
        self.texto_label = tk.Label(self.root, text="¡Piensa en un personaje!", 
                                    font=("Helvetica", 14, "bold"), wraplength=450, justify="center")
        self.texto_label.pack(pady=20) # padding (espacio) vertical

        # Canvas para mostrar la imagen
        self.canvas_imagen = tk.Canvas(self.root, width=350, height=350, bg="gray")
        self.canvas_imagen.pack(pady=10)

        # Frame (contenedor) para los botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=20)

        # Botón SÍ
        self.boton_si = tk.Button(frame_botones, text="Sí", font=("Helvetica", 12), width=10, 
                                  command=lambda: self.procesar_respuesta('si'))
        self.boton_si.grid(row=0, column=0, padx=15) # padx = espacio horizontal

        # Botón NO
        self.boton_no = tk.Button(frame_botones, text="No", font=("Helvetica", 12), width=10, 
                                  command=lambda: self.procesar_respuesta('no'))
        self.boton_no.grid(row=0, column=1, padx=15)

        # Iniciar el juego
        self.actualizar_ui()

    def mostrar_imagen(self, nombre_personaje):
        """Intenta cargar y mostrar una imagen desde la carpeta 'images'."""
        self.canvas_imagen.delete("all") # Limpiar imagen anterior
        
        # Intentar cargar .png y .jpg
        for extension in ['.png', '.jpg', '.jpeg']:
            # --- ¡AQUÍ ESTÁ EL CAMBIO! ---
            # Le decimos a Python que busque dentro de la carpeta "images"
            ruta_imagen = f"images/{nombre_personaje}{extension}" 
            # -----------------------------
            
            if os.path.exists(ruta_imagen):
                try:
                    # Abrir con Pillow
                    img_pil = Image.open(ruta_imagen)
                    # Redimensionar
                    img_pil = img_pil.resize((350, 350), Image.LANCZOS)
                    # Convertir para Tkinter
                    self.tk_image = ImageTk.PhotoImage(img_pil) # IMPORTANTE: guardar referencia
                    
                    self.canvas_imagen.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
                    return # Salir si se encontró la imagen
                except Exception as e:
                    print(f"Error al cargar imagen {ruta_imagen}: {e}")
                    self.canvas_imagen.create_text(175, 175, text=f"Error al\ncargar imagen", font=("Helvetica", 12))
                    return

        # Si no se encontró ningún archivo de imagen
        print(f"No se encontró imagen en 'images/' para: {nombre_personaje}")
        self.canvas_imagen.create_text(175, 175, text=f"Imagen no encontrada:\n{nombre_personaje}", 
                                        font=("Helvetica", 12), justify="center")


    def actualizar_ui(self):
        """Actualiza el texto y la imagen en la ventana."""
        if self.nodo_actual.es_hoja():
            # Es una respuesta (hoja) -> Mostrar adivinanza y foto del personaje
            texto = f"¿Estás pensando en '{self.nodo_actual.texto}'?"
            imagen_a_mostrar = self.nodo_actual.texto # ej: "Once"
        else:
            # Es una pregunta (nodo) -> Mostrar pregunta y foto del adivino
            texto = self.nodo_actual.texto
            imagen_a_mostrar = "adivino" # La imagen genérica
        
        # Actualizar los widgets
        self.texto_label.config(text=texto)
        self.mostrar_imagen(imagen_a_mostrar)

    def procesar_respuesta(self, respuesta):
        """Maneja el clic del usuario en 'Sí' o 'No'."""
        
        if self.nodo_actual.es_hoja():
            # Estábamos en una adivinanza final
            if respuesta == 'si':
                # ¡Adivinó!
                messagebox.showinfo("¡Gané!", "¡Genial! He adivinado.")
                self.reiniciar_juego()
            else:
                # Falló -> Llamar a aprender
                self.aprender()
        else:
            # Estábamos en una pregunta -> Navegar por el árbol
            if respuesta == 'si':
                self.nodo_actual = self.nodo_actual.hijo_si
            else:
                self.nodo_actual = self.nodo_actual.hijo_no
            
            # Actualizar la pantalla con la nueva pregunta/respuesta
            self.actualizar_ui()

    def aprender(self):
        """Usa ventanas emergentes para aprender."""
        respuesta_incorrecta = self.nodo_actual.texto
        
        # Pedir respuesta correcta
        respuesta_correcta = simpledialog.askstring("¡Me rindo!", 
                                                   f"¡Tú ganas! ¿En qué personaje estabas pensando?")
        if not respuesta_correcta: # Si el usuario presiona "Cancelar"
            return
        respuesta_correcta = respuesta_correcta.strip().capitalize() # Limpiar y estandarizar

        # Pedir pregunta nueva
        pregunta_nueva = simpledialog.askstring("¡Enséñame!", 
                                                f"Dame una pregunta (Sí/No) que sea 'Sí' para '{respuesta_correcta}' y 'No' para '{respuesta_incorrecta}':")
        if not pregunta_nueva: # Si presiona "Cancelar"
            return
        pregunta_nueva = pregunta_nueva.strip()
        if not pregunta_nueva.endswith("?"):
            pregunta_nueva += "?"

        # Modificar el árbol (la "cirugía")
        self.nodo_actual.texto = pregunta_nueva
        self.nodo_actual.hijo_si = Nodo(respuesta_correcta)
        self.nodo_actual.hijo_no = Nodo(respuesta_incorrecta)
        
        # Guardar el nuevo conocimiento en el JSON
        guardar_conocimiento(self.nodo_raiz)
        
        messagebox.showinfo("¡Aprendido!", f"¡Gracias! Ahora ya sé cómo diferenciar a '{respuesta_correcta}'.\nJuguemos de nuevo.")
        self.reiniciar_juego()

    def reiniciar_juego(self):
        """Vuelve al inicio del árbol para una nueva partida."""
        self.nodo_actual = self.nodo_raiz
        self.actualizar_ui()


# --- 3. INICIO DEL PROGRAMA (El código que se ejecuta) ---

if __name__ == "__main__":
    root = tk.Tk() # 1. Crea la ventana principal
    app = AkinatorGUI(root) # 2. Crea nuestra aplicación y la pone en la ventana
    
    # 3. Al cerrar la ventana, llama a guardar_conocimiento
    def al_cerrar():
        print("Cerrando y guardando...")
        guardar_conocimiento(app.nodo_raiz)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", al_cerrar)
    
    root.mainloop() # 4. Inicia el bucle de la aplicación