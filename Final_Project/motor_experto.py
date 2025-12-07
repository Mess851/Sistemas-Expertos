import sqlite3

def conectar_bd():
    return sqlite3.connect("sistema_experto.db")

def motor_de_inferencia():
    print("--- BIENVENIDO AL ASISTENTE DE SELECCIÓN DE PC ---")
    
    # --- 1. ADQUISICIÓN DE HECHOS (Preguntas al usuario) ---
    try:
        presupuesto = float(input("1. ¿Cuál es tu presupuesto máximo? (Ej: 15000): "))
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return

    print("\n2. ¿Cuál será el uso PRINCIPAL del equipo?")
    print("   [1] Básico (Oficina, Tareas escolares, Navegación)")
    print("   [2] Profesional (Programación, Edición ligera, Multitarea)")
    print("   [3] Alto Rendimiento (Gaming AAA, Render 3D, Arquitectura)")
    uso = input("Selecciona una opción (1-3): ")

    # --- 2. BASE DE REGLAS (Traducción de necesidades a SQL) ---
    # Iniciamos la consulta base filtrando solo por dinero
    query = "SELECT * FROM computadoras WHERE precio <= ?"
    parametros = [presupuesto]

    # APLICAMOS REGLAS SEGÚN EL PERFIL:
    
    if uso == "1": # Perfil Básico
        # Regla: No necesitamos potencia excesiva, priorizamos precio.
        # No agregamos filtros técnicos extra, pero ordenamos por precio.
        query += " ORDER BY precio ASC"

    elif uso == "2": # Perfil Profesional
        # Regla: Necesita mínimo 16GB de RAM para multitarea.
        # Regla: El procesador debe ser decente (Puntos > 8000).
        print("\n>> Aplicando regla: Buscando equipos con 16GB RAM o más...")
        query += " AND ram_gb >= 16 AND cpu_puntos >= 8000"
        query += " ORDER BY cpu_puntos DESC" # Priorizar el procesador más fuerte

    elif uso == "3": # Perfil Gamer/Ingeniero
        # Regla CRÍTICA: Debe tener tarjeta gráfica dedicada (es_gpu_dedicada = 1).
        print("\n>> Aplicando regla: Filtrando solo equipos con Tarjeta de Video Dedicada...")
        query += " AND es_gpu_dedicada = 1"
        query += " ORDER BY gpu_puntos DESC" # Priorizar la mejor gráfica

    else:
        print("Opción no válida.")
        return

    # --- 3. EJECUCIÓN Y EXPLICACIÓN (Salida) ---
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    conexion.close()

    if not resultados:
        print("\nLo siento, no encontré ninguna computadora con ese presupuesto para ese uso.")
        print("Sugerencia: Intenta aumentar tu presupuesto un poco.")
    else:
        print(f"\n¡Encontré {len(resultados)} opciones ideales para ti!\n")
        print(f"{'MARCA Y MODELO':<25} | {'PRECIO':<10} | {'RAM':<5} | {'GPU'}")
        print("-" * 60)
        
        for pc in resultados:
            # Nota: Los índices dependen del orden de columnas en tu BD
            # 1:Marca, 2:Modelo, 4:Precio, 8:RAM, 12:Modelo GPU
            marca_modelo = f"{pc[1]} {pc[2]}"
            precio = f"${pc[4]}"
            ram = f"{pc[8]}GB"
            gpu = pc[12]
            
            print(f"{marca_modelo:<25} | {precio:<10} | {ram:<5} | {gpu}")

# Ejecutar el sistema
if __name__ == "__main__":
    motor_de_inferencia()