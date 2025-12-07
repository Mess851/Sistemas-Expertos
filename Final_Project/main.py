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

        self.title("Sistema Experto PC Master - Design Edition")
        self.geometry("1000x650")
        self.resizable(False, False)

        # 1. CARGAR IMAGEN DE FONDO
        try:
            # Tu diseño limpio de Figma (sin textos ni botones, solo arte)
            bg_image_data = Image.open("fondo_design.png")
            self.bg_image = ctk.CTkImage(bg_image_data, size=(1000, 650))
            
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            self.configure(fg_color="#E0F7FA") # Fondo de respaldo
            print("⚠️ No encontré 'fondo_design.png'.")

        # 2. INTERFAZ
        self.crear_controles()

    def crear_controles(self):
        # Frame transparente para agrupar controles a la izquierda
        self.frame_izquierdo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_izquierdo.place(x=50, y=100) # <--- MUEVE ESTO si tus botones no calzan

        # --- SECCIÓN PRESUPUESTO ---
        lbl_presu = ctk.CTkLabel(self.frame_izquierdo, text="Presupuesto", 
                                 font=("Arial Rounded MT Bold", 24, "bold"), text_color="#5F7D8B")
        lbl_presu.pack(anchor="w", pady=(0, 0))

        # Etiqueta dinámica que cambia con el slider
        self.lbl_valor = ctk.CTkLabel(self.frame_izquierdo, text="$15,000", 
                                      font=("Arial", 20, "bold"), text_color="#009688")
        self.lbl_valor.pack(anchor="w", pady=(0, 5))

        # EL SLIDER (Restaurado)
        self.slider = ctk.CTkSlider(self.frame_izquierdo, from_=5000, to=50000, 
                                    width=250, height=20,
                                    number_of_steps=45,
                                    button_color="#009688",      # Verde azulado (Teal)
                                    button_hover_color="#00796B",
                                    progress_color="#4DB6AC",    # Barra llena
                                    fg_color="#CFD8DC",          # Barra vacía (Gris)
                                    command=self.actualizar_precio)
        self.slider.set(15000)
        self.slider.pack(pady=(0, 30))

        # --- SECCIÓN USO ---
        lbl_uso = ctk.CTkLabel(self.frame_izquierdo, text="Uso", 
                               font=("Arial Rounded MT Bold", 24, "bold"), text_color="#5F7D8B")
        lbl_uso.pack(anchor="w", pady=(0, 5))

        self.menu_uso = ctk.CTkOptionMenu(self.frame_izquierdo, 
                                          values=["Básico", "Profesional", "Gamer"],
                                          width=250, height=40,
                                          corner_radius=15,
                                          fg_color="white", 
                                          button_color="#ECEFF1", button_hover_color="#CFD8DC",
                                          text_color="#455A64", 
                                          dropdown_fg_color="white", dropdown_text_color="#455A64",
                                          font=("Arial", 16))
        self.menu_uso.pack(pady=(0, 50))
        self.menu_uso.set("Gamer")

        # --- BOTÓN ANALIZAR ---
        self.btn_analizar = ctk.CTkButton(self.frame_izquierdo, text="Analizar", 
                                          width=200, height=50,
                                          corner_radius=20,
                                          font=("Arial Rounded MT Bold", 20),
                                          fg_color="#CFD8DC", hover_color="#B0BEC5",
                                          text_color="#546E7A", border_color="white", border_width=2,
                                          command=self.buscar_recomendacion)
        self.btn_analizar.pack()

    def actualizar_precio(self, val):
        self.lbl_valor.configure(text=f"${int(val):,.0f}")

    def buscar_recomendacion(self):
        # Frame de resultados (aparece a la derecha)
        self.frame_resultados = ctk.CTkScrollableFrame(self, width=500, height=500, 
                                                       fg_color="white", corner_radius=20, 
                                                       label_text="Mejores Opciones", label_text_color="#546E7A")
        self.frame_resultados.place(x=420, y=50) 

        # Limpiar
        for widget in self.frame_resultados.winfo_children(): widget.destroy()

        # Lógica
        uso = self.menu_uso.get()
        presu = self.slider.get() # <--- Tomamos valor del slider
        
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
                ctk.CTkLabel(self.frame_resultados, text="❌ Sin resultados.\nSube el presupuesto.", 
                             text_color="#546E7A", font=("Arial", 16)).pack(pady=50)
                return

            for pc in resultados:
                self.crear_tarjeta_clara(pc)

        except sqlite3.Error as e:
            ctk.CTkLabel(self.frame_resultados, text=f"Error BD: {e}", text_color="red").pack()

    def crear_tarjeta_clara(self, pc):
        marca, modelo, precio, ram, gpu, img_file = pc[0], pc[1], pc[2], pc[3], pc[4], pc[5]

        card = ctk.CTkFrame(self.frame_resultados, fg_color="#F5F5F5", corner_radius=15, border_width=1, border_color="#E0E0E0")
        card.pack(pady=10, padx=10, fill="x")

        # Imagen
        try:
            ruta = os.path.join("imagenes", img_file)
            pil_img = Image.open(ruta)
            ctk_img = ctk.CTkImage(pil_img, size=(110, 80))
            ctk.CTkLabel(card, text="", image=ctk_img).pack(side="left", padx=10, pady=10)
        except:
            ctk.CTkLabel(card, text="[IMG]", width=110, height=80, fg_color="#DDD", corner_radius=10).pack(side="left", padx=10)

        # Datos
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(info, text=f"{marca} {modelo}", font=("Arial", 16, "bold"), text_color="#37474F", anchor="w").pack(fill="x")
        ctk.CTkLabel(info, text=f"{ram}GB RAM | {gpu}", text_color="#78909C", anchor="w", font=("Arial", 12)).pack(fill="x")
        
        # Precio
        ctk.CTkLabel(card, text=f"${precio:,.0f}", font=("Arial", 18, "bold"), text_color="#009688").pack(side="right", padx=15)

if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.mainloop()