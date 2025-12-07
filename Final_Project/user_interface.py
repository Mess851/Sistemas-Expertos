import customtkinter as ctk
import sqlite3

# --- CONFIGURACIÓN VISUAL (Tu "Figma" en código) ---
ctk.set_appearance_mode("Dark")  # Opciones: "System" (estándar), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Opciones: "blue" (estándar), "green", "dark-blue"

class SistemaExpertoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Sistema Experto de Hardware")
        self.geometry("900x600")
        
        # Configurar Grid (Diseño de 2 columnas)
        # Columna 0: Panel lateral de controles
        # Columna 1: Área de resultados
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_widgets()

    def crear_widgets(self):
        # --- PANEL LATERAL (CONTROLES) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1) # Espaciado

        # Título Lateral
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CONFIGURADOR\nPC MASTER", 
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 1. LISTA DESPLEGABLE (USO)
        self.lbl_uso = ctk.CTkLabel(self.sidebar_frame, text="1. Uso Principal:", anchor="w")
        self.lbl_uso.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.opciones_uso = ["Básico (Oficina/Escuela)", "Profesional (Dev/Diseño)", "Gamer / Arquitectura"]
        self.menu_uso = ctk.CTkOptionMenu(self.sidebar_frame, values=self.opciones_uso)
        self.menu_uso.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # 2. SLIDER (PRESUPUESTO)
        self.lbl_presupuesto = ctk.CTkLabel(self.sidebar_frame, text="2. Presupuesto Máximo:", anchor="w")
        self.lbl_presupuesto.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")

        # Label dinámico del precio
        self.lbl_valor_precio = ctk.CTkLabel(self.sidebar_frame, text="$15,000", 
                                             font=ctk.CTkFont(size=16, weight="bold"), text_color="#3B8ED0")
        self.lbl_valor_precio.grid(row=4, column=0, padx=20, sticky="w")

        self.slider_presupuesto = ctk.CTkSlider(self.sidebar_frame, from_=5000, to=50000, number_of_steps=45, command=self.actualizar_precio)
        self.slider_presupuesto.set(15000)
        self.slider_presupuesto.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")

        # 3. BOTÓN DE ACCIÓN
        self.btn_buscar = ctk.CTkButton(self.sidebar_frame, text="BUSCAR EQUIPO", 
                                        height=40, font=ctk.CTkFont(size=14, weight="bold"),
                                        command=self.buscar_recomendacion)
        self.btn_buscar.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        # --- ÁREA PRINCIPAL (RESULTADOS) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.lbl_resultado = ctk.CTkLabel(self.main_frame, text="Resultados de la búsqueda:", 
                                          font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_resultado.pack(anchor="w", pady=(0, 10))

        # Caja de texto grande para mostrar resultados
        self.textbox_resultados = ctk.CTkTextbox(self.main_frame, width=500, font=ctk.CTkFont(family="Consolas", size=14))
        self.textbox_resultados.pack(fill="both", expand=True)
        self.textbox_resultados.insert("0.0", "Selecciona tus preferencias y presiona Buscar.\n\nEl sistema experto analizará la base de datos...")

    # --- LÓGICA DEL SISTEMA ---
    def actualizar_precio(self, value):
        self.lbl_valor_precio.configure(text=f"${int(value):,.0f}")

    def buscar_recomendacion(self):
        # 1. Obtener datos de la GUI
        uso_seleccionado = self.menu_uso.get()
        presupuesto = self.slider_presupuesto.get()

        # 2. Conectar BD
        try:
            conexion = sqlite3.connect("sistema_experto.db")
            cursor = conexion.cursor()
            
            # 3. Motor de Inferencia (Igual que antes, pero integrado en la clase)
            query = "SELECT marca, modelo, precio, ram_gb, gpu_modelo, cpu_puntos FROM computadoras WHERE precio <= ?"
            params = [presupuesto]

            if "Básico" in uso_seleccionado:
                query += " ORDER BY precio ASC"
            elif "Profesional" in uso_seleccionado:
                query += " AND ram_gb >= 16 AND cpu_puntos >= 8000 ORDER BY cpu_puntos DESC"
            elif "Gamer" in uso_seleccionado:
                query += " AND es_gpu_dedicada = 1 ORDER BY gpu_puntos DESC"

            cursor.execute(query, params)
            resultados = cursor.fetchall()
            conexion.close()

            # 4. Mostrar en GUI
            self.mostrar_en_texto(resultados)
            
        except sqlite3.Error as e:
            self.textbox_resultados.delete("0.0", "end")
            self.textbox_resultados.insert("0.0", f"Error de Base de Datos:\n{e}")

    def mostrar_en_texto(self, lista):
        self.textbox_resultados.delete("0.0", "end")
        
        if not lista:
            self.textbox_resultados.insert("end", "❌ No se encontraron equipos con esos criterios.\n\nIntenta aumentar el presupuesto.")
            return

        encabezado = f"{'EQUIPO':<30} | {'PRECIO':<10} | {'RAM':<5} | {'GPU'}\n"
        self.textbox_resultados.insert("end", encabezado + "="*65 + "\n")

        for pc in lista: # pc = (marca, modelo, precio, ram, gpu, cpu_pts)
            nombre = f"{pc[0]} {pc[1]}"
            precio = f"${pc[2]:,.0f}"
            ram = f"{pc[3]}GB"
            gpu = pc[4]
            
            linea = f"{nombre:<30} | {precio:<10} | {ram:<5} | {gpu}\n"
            self.textbox_resultados.insert("end", linea + "-"*65 + "\n")

if __name__ == "__main__":
    app = SistemaExpertoApp()
    app.mainloop()