import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import os

# --- Configuración Base ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
imagenes_cargadas = {} 

# --- Datos del Juego (Personajes, Armas, Lugares) ---
personajes = {
    "Alicia Vega": {"genero": "Femenino", "img": "alicia.png"},
    "Bruno Salas": {"genero": "Masculino", "img": "bruno.png"},
    "Camila Ríos": {"genero": "Femenino", "img": "camila.png"},
    "Diego Torres": {"genero": "Masculino", "img": "diego.png"},
    "Elena Cruz": {"genero": "Femenino", "img": "elena.png"}
}
armas = {
    "Cuchillo": {"tipo": "Contacto", "img": "cuchillo.png"},
    "Llave inglesa": {"tipo": "Contacto", "img": "llave.png"},
    "Pistola": {"tipo": "Distancia", "img": "pistola.png"},
    "Veneno": {"tipo": "Distancia", "img": "veneno.png"},
    "Bate de béisbol": {"tipo": "Contacto", "img": "bate.png"}
}
lugares = {
    "Biblioteca": {"zona": "Interior", "img": "biblioteca.jpg"},
    "Cocina": {"zona": "Interior", "img": "cocina.jpg"},
    "Jardín": {"zona": "Exterior", "img": "jardin.jpg"},
    "Estudio": {"zona": "Interior", "img": "estudio.jpg"},
    "Garaje": {"zona": "Exterior", "img": "garaje.jpg"}
}
# Historia para la pantalla de victoria
historias = {
    ("Alicia Vega", "Cuchillo", "Cocina"): "🍴 Alicia fue encontrada en la cocina con su cuchillo de chef. La ira fue su peor receta.",
    ("Bruno Salas", "Pistola", "Estudio"): "🔫 Bruno, el detective, usó su pistola para silenciar a su víctima en el estudio.",
    ("Camila Ríos", "Veneno", "Biblioteca"): "☠️ La doctora Camila mezcló veneno en el vino. El crimen ocurrió en la biblioteca.",
    ("Diego Torres", "Llave inglesa", "Garaje"): "🔧 Diego perdió el control en el garaje con una llave inglesa.",
    ("Elena Cruz", "Bate de béisbol", "Jardín"): "⚾ Elena golpeó con el bate bajo la lluvia, entre las flores del jardín."
}

# --- NUEVA Base de Conocimiento (Pistas y Coartadas) ---
coartadas = {
    "Alicia Vega": "Alicia jura que pasó toda la noche en la biblioteca, organizando sus libros de recetas.",
    "Bruno Salas": "Bruno dice que estaba en el garaje, reparando una llanta de su auto que encontró ponchada.",
    "Camila Ríos": "Camila afirma haber estado en el jardín, tomando aire fresco después de una larga llamada.",
    "Diego Torres": "Diego testifica que estaba en el estudio, terminando un reporte de trabajo urgente.",
    "Elena Cruz": "Elena dice que estaba en la cocina, preparando un postre complicado que le llevó horas."
}
pistas_lugares = {
    "Biblioteca": "Las cámaras de la biblioteca muestran que la única persona que entró fue Alicia. No se ve nada sospechoso.",
    "Cocina": "Se encontró un cuchillo de chef (distinto al arma homicida) tirado en el suelo. Parece que hubo un forcejeo.",
    "Jardín": "Hay huellas de zapatos deportivos cerca de los rosales. Elena y Camila suelen usar ese tipo de calzado.",
    "Estudio": "La computadora de Diego está encendida. El último archivo guardado fue un reporte a las 8 PM.",
    "Garaje": "Hay una llanta ponchada junto al auto de Bruno, pero la herramienta está limpia. No parece que la haya usado."
}
pistas_armas = {
    "Cuchillo": "El cuchillo pertenece a un set de la cocina. Faltaba desde la mañana.",
    "Llave inglesa": "Esta herramienta es del garaje. Tiene manchas de grasa... y algo que parece ser sangre.",
    "Pistola": "Es la pistola registrada de Bruno Salas, pero él reportó que se la robaron de su estudio hace dos días.",
    "Veneno": "Este frasco fue comprado por internet. La dirección de entrega fue la de la casa, a nombre de 'C. Ríos'.",
    "Bate de béisbol": "El bate es de Elena. Dice que lo usa para practicar en el jardín."
}

# --- Variables Globales del Juego ---
culpable = None
arma = None
lugar = None
oportunidades = 5
pistas_descubiertas = [] # (Por si se quiere usar en el futuro)

# --- Variables Globales de la GUI ---
root = tk.Tk()
lbl_oportunidades = None
cuadro_pistas = None
sel_personaje = tk.StringVar()
sel_arma = tk.StringVar()
sel_lugar = tk.StringVar()


# --- Funciones de Utilidad ---

def cargar_imagen(nombre, tamaño=(70, 70)):
    ruta = os.path.join(BASE_DIR, "img", nombre)
    if not os.path.exists(ruta):
        print(f"⚠️ Imagen no encontrada: {ruta}")
        return None
    try:
        img = Image.open(ruta).resize(tamaño, Image.LANCZOS)
        foto = ImageTk.PhotoImage(img)
        imagenes_cargadas[nombre] = foto 
        return foto
    except Exception as e:
        print(f"⚠️ Error al cargar {nombre}: {e}")
        return None

def seleccionar_solucion():
    """Elige una nueva combinación ganadora."""
    global culpable, arma, lugar
    culpable = random.choice(list(personajes.keys()))
    arma = random.choice(list(armas.keys()))
    lugar = random.choice(list(lugares.keys()))
    print(f"SOLUCIÓN SECRETA: {culpable}, {arma}, {lugar}") # Para depuración

def limpiar_pantalla():
    """Destruye todos los widgets en la ventana root."""
    for widget in root.winfo_children():
        widget.destroy()

# --- FLUJO DEL JUEGO ---

# --- Pantalla 1: Inicio ---
def pantalla_inicio():
    limpiar_pantalla()

    fondo = cargar_imagen("fondo.jpg", tamaño=(900, 750))
    if fondo:
        fondo_lbl = tk.Label(root, image=fondo)
        fondo_lbl.image = fondo
        fondo_lbl.place(x=0, y=0) 

    frame_central = tk.Frame(root, bg="#1B2631")
    frame_central.place(relx=0.5, rely=0.5, anchor="center")

    logo_img = cargar_imagen("logo.png", tamaño=(200, 200))
    if logo_img:
        logo_lbl = tk.Label(frame_central, image=logo_img, bg="#1B2631")
        logo_lbl.pack(pady=20)
        logo_lbl.image = logo_img
    
    tk.Button(frame_central, text="🎮 Comenzar juego", command=mostrar_pantalla_juego,
              font=("Arial", 16, "bold"), bg="#27AE60", fg="white", 
              width=20, height=2, relief="flat").pack(pady=10)

# --- Pantalla 2: Investigación ---
def mostrar_pantalla_juego():
    limpiar_pantalla()
    construir_pantalla_juego()

def construir_tarjetas_investigacion(opciones, tipo_pista, frame_padre, fila_inicio):
    """Crea botones que al hacer click llaman a 'investigar'."""
    col = 0
    for nombre, info in opciones.items():
        foto = cargar_imagen(info['img'])
        btn = tk.Button(frame_padre, image=foto, text=nombre, compound="top",
                        width=100, height=120, fg="white", font=("Arial", 9),
                        bg="#273746", relief="flat", activebackground="#34495E",
                        highlightthickness=2, highlightbackground="#5D6D7E")
        btn.image = foto
        # El comando ahora llama a 'investigar'
        btn.config(command=lambda n=nombre, t=tipo_pista, b=btn: investigar(n, t, b))
        
        # ASEGÚRATE QUE ESTA LÍNEA USE .grid()
        btn.grid(row=fila_inicio, column=col, padx=8, pady=8)
        col += 1

def construir_pantalla_juego():
    global lbl_oportunidades, cuadro_pistas, oportunidades
    
    # Ajustar altura de la ventana para el cuadro de pistas
    root.geometry("900x850") # Aumentamos la altura

    # --- Widgets hijos de 'root' (Usan .pack()) ---
    titulo = tk.Label(root, text="🕵️ ¿Quién fue? Tienes 5 oportunidades para investigar.", 
                      font=("Arial", 15, "bold"), bg="#1B2631", fg="white")
    titulo.pack(pady=10)

    lbl_oportunidades = tk.Label(root, text=f"Oportunidades restantes: {oportunidades}", 
                                 font=("Arial", 12, "bold"), bg="#1B2631", fg="#F4D03F")
    lbl_oportunidades.pack(pady=5)

    contenedor_juego = tk.Frame(root, bg="#1B2631")
    contenedor_juego.pack()
    
    # --- FIN de widgets hijos de 'root' ---


    # --- Widgets hijos de 'contenedor_juego' (DEBEN usar .grid()) ---
    tk.Label(contenedor_juego, text="👤 Sospechosos", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=0, column=0, columnspan=5)
    construir_tarjetas_investigacion(personajes, "coartada", contenedor_juego, 1) 

    tk.Label(contenedor_juego, text="🔪 Armas", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=2, column=0, columnspan=5, pady=(10,0))
    construir_tarjetas_investigacion(armas, "arma", contenedor_juego, 3)

    tk.Label(contenedor_juego, text="📍 Lugares", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=4, column=0, columnspan=5, pady=(10,0))
    construir_tarjetas_investigacion(lugares, "lugar", contenedor_juego, 5)
    # --- FIN de widgets hijos de 'contenedor_juego' ---
    

    # --- Widgets hijos de 'root' (Usan .pack() de nuevo) ---
    tk.Label(root, text="--- Pistas Descubiertas ---", font=("Arial", 11, "bold"), 
             bg="#1B2631", fg="white").pack(pady=(10,2))
    
    cuadro_pistas = tk.Text(root, height=8, width=100, bg="#212F3C", fg="#AED6F1", 
                            font=("Arial", 10), relief="flat", wrap="word")
    cuadro_pistas.pack()
    cuadro_pistas.insert(tk.END, "Haz clic en cualquier tarjeta para investigarla...\n")
    cuadro_pistas.config(state="disabled")

    tk.Button(root, text="Hacer Acusación Final", command=mostrar_pantalla_acusacion, 
              font=("Arial", 13, "bold"), bg="#E74C3C", fg="white", 
              width=25, height=2, relief="flat").pack(pady=10)

def investigar(nombre_tarjeta, tipo_pista, boton):
    global oportunidades, pistas_descubiertas, cuadro_pistas

    if oportunidades <= 0:
        messagebox.showwarning("Sin oportunidades", "Ya no te quedan oportunidades de investigar. Debes resolver el crimen.")
        return

    oportunidades -= 1
    lbl_oportunidades.config(text=f"Oportunidades restantes: {oportunidades}")

    pista = ""
    if tipo_pista == "coartada":
        pista = coartadas[nombre_tarjeta]
    elif tipo_pista == "arma":
        pista = pistas_armas[nombre_tarjeta]
    elif tipo_pista == "lugar":
        pista = pistas_lugares[nombre_tarjeta]

    cuadro_pistas.config(state="normal")
    cuadro_pistas.insert(tk.END, f"\n🔎 [Investigando {nombre_tarjeta}]:\n{pista}\n")
    cuadro_pistas.see(tk.END) # Auto-scroll
    cuadro_pistas.config(state="disabled")

    boton.config(state="disabled", bg="#17202A") 
    
    if oportunidades == 0:
        cuadro_pistas.config(state="normal")
        cuadro_pistas.insert(tk.END, "\n--- ¡SE ACABARON LAS OPORTUNIDADES! --- \nPresiona 'Hacer Acusación Final'.\n")
        cuadro_pistas.see(tk.END)
        cuadro_pistas.config(state="disabled")

# --- Pantalla 3: Acusación Final ---
def mostrar_pantalla_acusacion():
    limpiar_pantalla()
    construir_pantalla_acusacion()

def construir_tarjetas_seleccion(opciones, variable, frame_padre, fila_inicio):
    """Crea botones que SELECCIONAN (resaltado azul)"""
    col = 0
    grupo_botones = [] 
    color_borde = "#5D6D7E" 
    color_normal = "#273746"
    color_seleccion = "#3498DB" 

    def on_select(btn_presionado, nombre_sel, var_sel):
        for btn in grupo_botones:
            btn.config(bg=color_normal, relief="flat", highlightthickness=2) 
        btn_presionado.config(bg=color_seleccion, relief="solid", highlightthickness=0)
        var_sel.set(nombre_sel)

    for nombre, info in opciones.items():
        foto = cargar_imagen(info['img'])
        btn = tk.Button(frame_padre, image=foto, text=nombre, compound="top",
                        width=100, height=120, fg="white", font=("Arial", 9),
                        bg=color_normal, relief="flat", activebackground="#34495E",
                        highlightthickness=2, highlightbackground=color_borde)
        btn.image = foto
        btn.config(command=lambda b=btn, n=nombre, v=variable: on_select(b, n, v))
        btn.grid(row=fila_inicio, column=col, padx=8, pady=8)
        grupo_botones.append(btn)
        col += 1

def construir_pantalla_acusacion():
    global sel_personaje, sel_arma, sel_lugar
    
    # Restaurar tamaño de ventana
    root.geometry("900x650") 

    titulo = tk.Label(root, text="Basado en tus pistas, haz tu acusación final", 
                      font=("Arial", 15, "bold"), bg="#1B2631", fg="white")
    titulo.pack(pady=15)

    contenedor_juego = tk.Frame(root, bg="#1B2631")
    contenedor_juego.pack()

    sel_personaje = tk.StringVar()
    sel_arma = tk.StringVar()
    sel_lugar = tk.StringVar()

    # --- Sección de Selección (.grid()) ---
    tk.Label(contenedor_juego, text="👤 Sospechoso", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=0, column=0, columnspan=5)
    construir_tarjetas_seleccion(personajes, sel_personaje, contenedor_juego, 1)

    tk.Label(contenedor_juego, text="🔪 Arma", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=2, column=0, columnspan=5, pady=(10,0))
    construir_tarjetas_seleccion(armas, sel_arma, contenedor_juego, 3)

    tk.Label(contenedor_juego, text="📍 Lugar", font=("Arial", 13, "bold"), 
             bg="#1B2631", fg="#F4D03F").grid(row=4, column=0, columnspan=5, pady=(10,0))
    construir_tarjetas_seleccion(lugares, sel_lugar, contenedor_juego, 5)
    
    tk.Button(root, text="¡CONFIRMAR ACUSACIÓN!", command=verificar_acusacion, 
              font=("Arial", 13, "bold"), bg="#27AE60", fg="white", 
              width=25, height=2, relief="flat").pack(pady=20)

# --- Pantallas 4 y 5: Resultado (Victoria / Derrota) ---

def verificar_acusacion():
    """Comprueba la acusación final."""
    p, a, l = sel_personaje.get(), sel_arma.get(), sel_lugar.get()

    if not p or not a or not l:
        messagebox.showwarning("Acusación Incompleta", "Debes seleccionar un personaje, un arma y un lugar.")
        return

    if (p, a, l) == (culpable, arma, lugar):
        historia = historias.get((p, a, l), "Has descubierto la verdad.")
        mostrar_resultado(historia)
    else:
        mostrar_game_over()

def mostrar_resultado(historia):
    """Pantalla de Victoria."""
    limpiar_pantalla()
    root.geometry("900x600")

    foto = cargar_imagen(personajes[culpable]['img'], tamaño=(180, 180))
    if foto:
        lbl_img = tk.Label(root, image=foto, bg="#1B2631")
        lbl_img.pack(pady=15)
        lbl_img.image = foto 

    tk.Label(root, text="🎯 ¡HAS RESUELTO EL CASO!", font=("Arial", 18, "bold"), 
             fg="#2ECC71", bg="#1B2631").pack(pady=10)
    tk.Label(root, text=historia, wraplength=700, font=("Arial", 13), 
             fg="white", bg="#1B2631").pack(pady=20)
    tk.Button(root, text="🔁 Jugar de nuevo", command=reiniciar, bg="#3498DB", 
             fg="white", font=("Arial", 12), width=15, relief="flat").pack(pady=10)
    tk.Button(root, text="🚪 Salir", command=root.destroy, bg="#E74C3C", 
             fg="white", font=("Arial", 12), width=15, relief="flat").pack(pady=5)

def mostrar_game_over():
    """Pantalla de Derrota."""
    limpiar_pantalla()
    root.geometry("900x600")

    foto = cargar_imagen("logo.png", tamaño=(150, 150)) # Imagen genérica
    if foto:
        lbl_img = tk.Label(root, image=foto, bg="#1B2631")
        lbl_img.pack(pady=15)
        lbl_img.image = foto 

    tk.Label(root, text="❌ CASO NO RESUELTO", font=("Arial", 18, "bold"), 
             fg="#E74C3C", bg="#1B2631").pack(pady=10)
    
    solucion_texto = f"La solución correcta era:\n\nCulpable: {culpable}\nArma: {arma}\nLugar: {lugar}"
    tk.Label(root, text=solucion_texto, wraplength=700, font=("Arial", 13), 
             fg="white", bg="#1B2631").pack(pady=20)
    
    tk.Button(root, text="🔁 Jugar de nuevo", command=reiniciar, bg="#3498DB", 
             fg="white", font=("Arial", 12), width=15, relief="flat").pack(pady=10)
    tk.Button(root, text="🚪 Salir", command=root.destroy, bg="#E74C3C", 
             fg="white", font=("Arial", 12), width=15, relief="flat").pack(pady=5)

# --- Función de Reinicio ---
def reiniciar():
    global oportunidades, pistas_descubiertas
    
    # Resetear variables del juego
    oportunidades = 5
    pistas_descubiertas = []
    seleccionar_solucion()
    
    # Volver a la pantalla de investigación
    mostrar_pantalla_juego()

# --- Ejecución Principal ---
if __name__ == "__main__":
    root.title("🕵️ CLUE - Modo Detective 🕵️")
    root.geometry("900x750") # Tamaño inicial
    root.resizable(False, False)
    root.config(bg="#1B2631")

    seleccionar_solucion() 
    pantalla_inicio()      
    root.mainloop()