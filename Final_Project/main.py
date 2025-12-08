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
        self.geometry("1024x696")
        self.resizable(False, False) # Bloqueamos para que no se descuadre la imagen

        # 2. CARGAR FONDO ESTÁTICO (Sin redimensionado dinámico = 0 Lag)
        try:
            # Ruta de la imagen de fondo
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_fondo = os.path.join(directorio_actual, "images", "fondo_design.png")
            
            # Cargar imagen
            pil_bg = Image.open(ruta_fondo)
            # Definimos el tamaño exacto de la ventana
            bg_image = ctk.CTkImage(light_image=pil_bg, dark_image=pil_bg, size=(1024, 696))
            
            # Ponerla en un Label al fondo
            self.bg_label = ctk.CTkLabel(self, text="", image=bg_image)
            self.bg_label.place(x=0, y=0) # Coordenadas fijas 0,0

        except Exception as e:
            self.configure(fg_color="#E0F7FA") # Color de respaldo
            print(f"⚠️ Error cargando fondo: {e}")

        # Crear los controles
        self.crear_controles()

    def crear_controles(self):
        # --- CONFIGURACIÓN DE POSICIONES (CALIBRACIÓN) ---
        # Ajusta estos números para mover los bloques completos
        
        POS_X = 0.08           # Qué tan a la izquierda están todos los controles (0.08 = 8%)
        
        # Alturas (Vertical)
        Y_PRECIO   = 0.20      # Altura del texto "$15,000"
        Y_SLIDER   = 0.24      # Altura de la barrita slider
        Y_LISTA    = 0.40      # Altura de la lista desplegable
        Y_BOTON    = 0.80     # Altura del botón Analizar

        # -----------------------------------------------------

        # 1. VALOR DINÁMICO ($15,000)
        self.lbl_valor = ctk.CTkLabel(self.bg_label, 
                                      text="$15,000", 
                                      font=("Arial", 22, "bold"), text_color="#009688",
                                      fg_color="transparent")
        self.lbl_valor.place(relx=POS_X, rely=Y_PRECIO)

        # 2. SLIDER
        self.slider = ctk.CTkSlider(self.bg_label, 
                                    from_=5000, to=50000, 
                                    width=280, height=20, number_of_steps=45,
                                    button_color="#009688", progress_color="#4DB6AC", fg_color="#CFD8DC",
                                    bg_color="transparent", 
                                    command=self.actualizar_precio)
        self.slider.set(15000)
        self.slider.place(relx=POS_X, rely=Y_SLIDER)

        # 3. LISTA DESPLEGABLE
        self.menu_uso = ctk.CTkOptionMenu(self.bg_label, 
                                          values=["Básico", "Profesional", "Gamer"],
                                          width=280, height=45, corner_radius=15,
                                          fg_color="white", 
                                          bg_color="transparent",
                                          button_color="#ECEFF1", button_hover_color="#CFD8DC",
                                          text_color="#455A64", dropdown_fg_color="white", dropdown_text_color="#455A64",
                                          font=("Arial", 16))
        self.menu_uso.set("Gamer")
        self.menu_uso.place(relx=POS_X, rely=Y_LISTA)

        # 4. BOTÓN ANALIZAR
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_btn = os.path.join(directorio_actual, "images", "btn_analizar.png")
        
        try:
            pil_btn = Image.open(ruta_btn)
            self.img_btn_final = ctk.CTkImage(light_image=pil_btn, dark_image=pil_btn, size=(220, 60))

            self.btn_analizar = ctk.CTkLabel(self.bg_label, 
                                             text="", 
                                             image=self.img_btn_final,
                                             fg_color="transparent",
                                             cursor="hand2")
            
            self.btn_analizar.place(relx=POS_X, rely=Y_BOTON)
            self.btn_analizar.bind("<Button-1>", lambda event: self.buscar_recomendacion())
            
        except Exception:
            self.btn_analizar = ctk.CTkButton(self.bg_label, text="Analizar", 
                                              font=("Arial", 20, "bold"), height=50, width=220,
                                              command=self.buscar_recomendacion)
            self.btn_analizar.place(relx=POS_X, rely=Y_BOTON)

    def actualizar_precio(self, val):
        self.lbl_valor.configure(text=f"${int(val):,.0f}")

    def buscar_recomendacion(self):
        # Frame de Resultados
        self.frame_resultados = ctk.CTkScrollableFrame(self, width=500, height=550, 
                                                       fg_color="white", corner_radius=20, 
                                                       label_text="Mejores Opciones", label_text_color="#546E7A")
        
        # --- CORRECCIÓN DE ESPACIO ---
        # Antes: relx=0.55, relwidth=0.40
        # Ahora: relx=0.50 (más a la izquierda), relwidth=0.45 (más ancho)
        self.frame_resultados.place(relx=0.50, rely=0.1, relwidth=0.45, relheight=0.8) 

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
        card.pack(pady=10, padx=5, fill="x") # padx=5 da más espacio lateral interno

        # Imagen del producto (Reducida ligeramente para dar espacio)
        try:
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            ruta_producto = os.path.join(directorio_actual, "images", img_file)
            
            pil_img = Image.open(ruta_producto)
            # Antes size=(110, 80) -> Ahora (100, 70) para ganar espacio
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 75))
            
            ctk.CTkLabel(card, text="", image=ctk_img).pack(side="left", padx=(10, 5), pady=10)
        except:
            ctk.CTkLabel(card, text="[IMG]", width=100, height=75, fg_color="#DDD", corner_radius=10).pack(side="left", padx=10)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=5)
        
        # Usamos wraplength para que si el nombre es muy largo, baje de renglón
        ctk.CTkLabel(info, text=f"{marca} {modelo}", font=("Arial", 16, "bold"), text_color="#37474F", anchor="w", wraplength=150).pack(fill="x")
        ctk.CTkLabel(info, text=f"{ram}GB RAM | {gpu}", text_color="#78909C", anchor="w", font=("Arial", 12)).pack(fill="x")
        
        # Precio
        ctk.CTkLabel(card, text=f"${precio:,.0f}", font=("Arial", 18, "bold"), text_color="#009688").pack(side="right", padx=10)
if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.mainloop()