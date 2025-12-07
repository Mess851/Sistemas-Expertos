import customtkinter as ctk
import sqlite3
from PIL import Image
import os

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class SistemaExpertoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema Experto PC Master - Final")
        
        # 1. TAMAÑO FIJO (Coincide con tu imagen redimensionada)
        self.geometry("1100x750")
        self.resizable(False, False) # Bloqueamos para que no se descuadre la imagen

        # 2. CARGAR FONDO ESTÁTICO (Sin redimensionado dinámico = 0 Lag)
        try:
            # Ruta de la imagen de fondo
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_fondo = os.path.join(directorio_actual, "images", "fondo_design.png")
            
            # Cargar imagen
            pil_bg = Image.open(ruta_fondo)
            # Definimos el tamaño exacto de la ventana
            bg_image = ctk.CTkImage(light_image=pil_bg, dark_image=pil_bg, size=(1100, 750))
            
            # Ponerla en un Label al fondo
            self.bg_label = ctk.CTkLabel(self, text="", image=bg_image)
            self.bg_label.place(x=0, y=0) # Coordenadas fijas 0,0

        except Exception as e:
            self.configure(fg_color="#E0F7FA") # Color de respaldo
            print(f"⚠️ Error cargando fondo: {e}")

        # Crear los controles
        self.crear_controles()

    def crear_controles(self):
        # Frame transparente para agrupar controles
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izquierdo.place(relx=0.08, rely=0.25) 

        # --- SECCIÓN PRESUPUESTO ---
        lbl_presu = ctk.CTkLabel(self.frame_izquierdo, text="Presupuesto", 
                                 font=("Arial Rounded MT Bold", 26, "bold"), text_color="#5F7D8B")
        lbl_presu.pack(anchor="w")

        self.lbl_valor = ctk.CTkLabel(self.frame_izquierdo, text="$15,000", 
                                      font=("Arial", 22, "bold"), text_color="#009688")
        self.lbl_valor.pack(anchor="w", pady=(0, 5))

        self.slider = ctk.CTkSlider(self.frame_izquierdo, from_=5000, to=50000, 
                                    width=280, height=20, number_of_steps=45,
                                    button_color="#009688", progress_color="#4DB6AC", fg_color="#CFD8DC",
                                    command=self.actualizar_precio)
        self.slider.set(15000)
        self.slider.pack(pady=(0, 30))

        # --- SECCIÓN USO ---
        lbl_uso = ctk.CTkLabel(self.frame_izquierdo, text="Uso", 
                               font=("Arial Rounded MT Bold", 26, "bold"), text_color="#5F7D8B")
        lbl_uso.pack(anchor="w", pady=(0, 5))

        self.menu_uso = ctk.CTkOptionMenu(self.frame_izquierdo, 
                                          values=["Básico", "Profesional", "Gamer"],
                                          width=280, height=45, corner_radius=15,
                                          fg_color="white", button_color="#ECEFF1", button_hover_color="#CFD8DC",
                                          text_color="#455A64", dropdown_fg_color="white", dropdown_text_color="#455A64",
                                          font=("Arial", 16))
        self.menu_uso.pack(pady=(0, 50))
        self.menu_uso.set("Gamer")

        # --- BOTÓN ANALIZAR (IMAGEN - SOLUCIÓN DEFINITIVA HOVER) ---
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_btn = os.path.join(directorio_actual, "images", "btn_analizar.png")
        
        try:
            # 1. Cargar la imagen UNA SOLA VEZ y guardarla en la clase (self)
            # Esto es vital para que no desaparezca
            pil_btn = Image.open(ruta_btn)
            self.img_btn_final = ctk.CTkImage(light_image=pil_btn, dark_image=pil_btn, size=(220, 60))

            # 2. Crear el botón
            self.btn_analizar = ctk.CTkButton(self.frame_izquierdo, 
                                              text="", 
                                              image=self.img_btn_final, # Usamos la imagen guardada
                                              width=220, height=60,
                                              fg_color="transparent", 
                                              
                                              # IMPORTANTE: Lo volvemos a poner en None, el truco viene abajo
                                              hover_color=None,
                                              
                                              command=self.buscar_recomendacion)
            self.btn_analizar.pack(pady=(10,0))

            # --- EL TRUCO MÁGICO ---
            # Definimos dos funciones pequeñas que fuerzan a que la imagen se mantenga
            # cuando el mouse entra y sale, anulando el cuadro azul.
            def on_enter(e):
                self.btn_analizar.configure(image=self.img_btn_final)
            
            def on_leave(e):
                self.btn_analizar.configure(image=self.img_btn_final)

            # "Anclamos" estas funciones a los eventos del mouse
            self.btn_analizar.bind("<Enter>", on_enter)
            self.btn_analizar.bind("<Leave>", on_leave)
            # -----------------------

        except Exception as e:
            print(f"Error cargando botón imagen: {e}")
            self.btn_analizar = ctk.CTkButton(self.frame_izquierdo, text="Analizar", font=("Arial", 20, "bold"), width=220, height=55, command=self.buscar_recomendacion)
            self.btn_analizar.pack(pady=(10,0))

    def actualizar_precio(self, val):
        self.lbl_valor.configure(text=f"${int(val):,.0f}")

    def buscar_recomendacion(self):
        # Frame de Resultados
        self.frame_resultados = ctk.CTkScrollableFrame(self, width=500, height=550, 
                                                       fg_color="white", corner_radius=20, 
                                                       label_text="Mejores Opciones", label_text_color="#546E7A")
        
        # Ajusta esta posición según donde quieras que aparezca la lista
        self.frame_resultados.place(relx=0.55, rely=0.1, relwidth=0.40, relheight=0.8) 

        for widget in self.frame_resultados.winfo_children(): widget.destroy()

        uso = self.menu_uso.get()
        presu = self.slider.get()
        
        try:
            conn = sqlite3.connect("sistema_experto.db")
            cursor = conn.cursor()
            
            query = "SELECT marca, modelo, precio, ram_gb, gpu_modelo, imagen_archivo, cpu_puntos, gpu_puntos FROM computadoras WHERE precio <= ?"
            
            if "Básico" in uso: query += " ORDER BY precio ASC"
            elif "Profesional" in uso: query += " AND ram_gb >= 16 ORDER BY cpu_puntos DESC"
            elif "Gamer" in uso: query += " AND es_gpu_dedicada = 1 ORDER BY gpu_puntos DESC"

            cursor.execute(query, [presu])
            resultados = cursor.fetchall()
            conn.close()

            if not resultados:
                ctk.CTkLabel(self.frame_resultados, text="❌ Sin resultados.", text_color="gray").pack(pady=50)
                return

            for pc in resultados:
                self.crear_tarjeta_clara(pc)

        except sqlite3.Error as e:
            ctk.CTkLabel(self.frame_resultados, text=f"Error BD: {e}", text_color="red").pack()

    def crear_tarjeta_clara(self, pc):
        marca, modelo, precio, ram, gpu, img_file = pc[0], pc[1], pc[2], pc[3], pc[4], pc[5]

        card = ctk.CTkFrame(self.frame_resultados, fg_color="#F5F5F5", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card.pack(pady=10, padx=10, fill="x")

        # Imagen del producto
        try:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_producto = os.path.join(directorio_actual, "images", img_file)
            
            pil_img = Image.open(ruta_producto)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(110, 80))
            
            ctk.CTkLabel(card, text="", image=ctk_img).pack(side="left", padx=10, pady=10)
        except:
            ctk.CTkLabel(card, text="[IMG]", width=110, height=80, fg_color="#DDD", corner_radius=10).pack(side="left", padx=10)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(info, text=f"{marca} {modelo}", font=("Arial", 16, "bold"), text_color="#37474F", anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=f"{ram}GB RAM | {gpu}", text_color="#78909C", anchor="w", font=("Arial", 12)).pack(fill="x")
        
        ctk.CTkLabel(card, text=f"${precio:,.0f}", font=("Arial", 18, "bold"), text_color="#009688").pack(side="right", padx=15)

if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.mainloop()