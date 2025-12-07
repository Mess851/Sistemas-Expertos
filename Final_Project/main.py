from tkinter import Tk, Canvas, Button, PhotoImage, messagebox, ttk
import sqlite3
from ctypes import windll

# --- CONFIGURACIÓN DE NITIDEZ PARA WINDOWS ---
try:
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# ===================================================================
# 1. LÓGICA DEL CEREBRO (Tu Motor de Inferencia)
# ===================================================================
def realizar_diagnostico():
    presupuesto_txt = combo_presupuesto.get()
    uso_txt = combo_uso.get()

    if not presupuesto_txt or not uso_txt:
        messagebox.showwarning("Faltan datos", "Por favor selecciona presupuesto y uso.")
        return

    # Convertir texto a números
    limite = 999999
    if "Bajo" in presupuesto_txt: limite = 10000
    elif "Medio" in presupuesto_txt: limite = 20000
    elif "Alto" in presupuesto_txt: limite = 30000
    
    try:
        conn = sqlite3.connect("laptops.db")
        cursor = conn.cursor()
        query = "SELECT marca, modelo, precio FROM laptops WHERE uso_recomendado = ? AND precio <= ?"
        resultados = cursor.execute(query, (uso_txt, limite)).fetchall()
        conn.close()
        
        if resultados:
            top = resultados[0]
            mensaje = f"✅ ¡RECOMENDACIÓN ENCONTRADA!\n\nModelo: {top[0]} {top[1]}\nPrecio: ${top[2]}\n\nPerfecta para: {uso_txt}"
            messagebox.showinfo("Resultado", mensaje)
        else:
            messagebox.showerror("Sin resultados", "No hay laptops con ese presupuesto para ese uso.")
            
    except sqlite3.Error as e:
        messagebox.showerror("Error BD", f"Error conectando a la base de datos:\n{e}")

# ===================================================================
# 2. INTERFAZ GRÁFICA (Montaje Manual Estilizado)
# ===================================================================
window = Tk()
window.title("Sistema Experto Laptops")
window.geometry("1512x982")
window.resizable(False, False)
# Ponemos el fondo negro de la ventana para evitar bordes blancos
window.configure(bg="#1E1E1E") 

# --- A. PONER EL FONDO DE FIGMA ---
canvas = Canvas(window, bg="#1E1E1E", height=982, width=1512, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

try:
    # Asegúrate que fondo.png sea LA IMAGEN COMPLETA de tu diseño (con textos y rectángulos)
    img_fondo = PhotoImage(file="fondo.png")
    canvas.create_image(0, 0, image=img_fondo, anchor="nw")
except Exception:
    canvas.create_text(500, 350, text="Error: Falta fondo.png", fill="white")

# --- CONFIGURACIÓN DE ESTILO "DARK MODE" ---
style = ttk.Style()
style.theme_use('clam') # Usamos un tema que permite cambiar colores

# Colores que imitan el diseño oscuro de Figma
COLOR_FONDO_OSCURO = "#333333"  # Un gris oscuro para las cajas
COLOR_TEXTO = "white"
COLOR_SELECCION = "#555555"

# Configuramos el estilo de los Combobox (Menús) para que sean oscuros
style.configure("TCombobox",
                fieldbackground=COLOR_FONDO_OSCURO, # Color de la caja
                background=COLOR_FONDO_OSCURO,      # Color de la flecha/borde
                foreground=COLOR_TEXTO,             # Color del texto
                arrowcolor=COLOR_TEXTO,             # Color de la flechita
                bordercolor=COLOR_FONDO_OSCURO)

# Estilo para cuando despliegas el menú
window.option_add('*TCombobox*Listbox.background', COLOR_FONDO_OSCURO)
window.option_add('*TCombobox*Listbox.foreground', COLOR_TEXTO)
window.option_add('*TCombobox*Listbox.selectBackground', COLOR_SELECCION)

# --- B. PONER LOS MENÚS DESPLEGABLES (YA ESTILIZADOS) ---
# Ajusta x, y, width, height para que calcen perfecto sobre tus rectángulos de Figma

# Menú 1: Presupuesto
valores_pres = ["Bajo ($10000)", "Medio ($20,000)", "Alto (30000)"]
combo_presupuesto = ttk.Combobox(window, values=valores_pres, state="readonly", font=("Arial", 12))
# 👇 AJUSTA ESTAS COORDENADAS 👇
combo_presupuesto.place(x=125, y=276, width=465, height=104)

# Menú 2: Uso
valores_uso = ["Oficina", "Gaming", "Diseno", "Programacion"]
combo_uso = ttk.Combobox(window, values=valores_uso, state="readonly", font=("Arial", 12))
# 👇 AJUSTA ESTAS COORDENADAS 👇
combo_uso.place(x=125, y=418, width=465, height=104)

# --- C. PONER EL BOTÓN (Con Imagen Superpuesta) ---
try:
    # 1. Cargamos la imagen (Asegúrate de que 'boton.png' incluya el texto 'Analizar' adentro)
    img_boton = PhotoImage(file="boton.png")
    
    btn_action = Button(
        window,
        image=img_boton,        # Aquí ponemos tu diseño
        command=realizar_diagnostico,
        
        # TRUCOS DE ESTILO PARA QUE SE VEA TRANSPARENTE:
        bg="#1E1E1E",           # Mismo color que el fondo de la ventana (ajusta si es necesario)
        activebackground="#1E1E1E", # Para que no parpadee blanco al dar clic
        borderwidth=0,          # Quita el borde 3D
        highlightthickness=0,   # Quita el recuadro de enfoque
        relief="flat",          # Lo hace plano
        cursor="hand2"          # Pone la manita al pasar el mouse
    )
    
    # 2. Colocación Exacta
    # Ve a Figma, selecciona tu grupo "Button" y mira las coordenadas X e Y.
    # Pon esos números exactos aquí:
    btn_action.place(x=183, y=760, width=320, height=104) # <--- ¡Ajusta esto!

except Exception as e:
    print(f"Error cargando imagen del botón: {e}")
    # Botón de respaldo por si falla la imagen
    btn_action = Button(window, text="ANALIZAR", command=realizar_diagnostico)
    btn_action.place(x=183, y=760)

window.mainloop()   