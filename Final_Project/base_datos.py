import sqlite3

def inicializar_bd():
    # 1. Conectar (o crear) la base de datos
    conexion = sqlite3.connect("sistema_experto.db")
    cursor = conexion.cursor()

    # 2. Crear la tabla si no existe
    # Fíjate en los campos: cpu_puntos y es_gpu_dedicada son vitales para la lógica
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS computadoras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            tipo TEXT NOT NULL,           -- 'Laptop', 'Desktop', 'AIO'
            precio REAL NOT NULL,
            cpu_marca TEXT,               -- 'Intel', 'AMD', 'Apple'
            cpu_modelo TEXT,
            cpu_puntos INTEGER,           -- Puntaje de rendimiento (Benchmark)
            ram_gb INTEGER NOT NULL,
            almacenamiento_gb INTEGER,
            es_ssd BOOLEAN,               -- 1 para SSD, 0 para HDD
            es_gpu_dedicada BOOLEAN,      -- 1 Sí, 0 No (Clave para Gamers)
            gpu_modelo TEXT,
            gpu_puntos INTEGER            -- Puntaje gráfico
        )
    ''')

    # 3. Datos de prueba (El Conocimiento Inicial)
    # Limpiamos datos viejos para no duplicar si corres esto varias veces
    cursor.execute("DELETE FROM computadoras")

    computadoras_iniciales = [
        # (Marca, Modelo, Tipo, Precio, CPU_Marca, CPU_Mod, PuntosCPU, RAM, Alm, EsSSD, GPU_Ded, GPU_Mod, PuntosGPU)
        
        # 1. Económica para Estudiantes / Ofimática
        ('HP', 'Notebook 15', 'Laptop', 8500, 'Intel', 'Core i3-1115G4', 6000, 8, 256, 1, 0, 'Intel UHD', 1000),
        
        # 2. Gama Media Equilibrada (Programación Web / Diseño ligero)
        ('Dell', 'Inspiron 15', 'Laptop', 14500, 'AMD', 'Ryzen 5 5500U', 13000, 16, 512, 1, 0, 'Radeon Graphics', 2000),
        
        # 3. Gamer de Entrada / Arquitectura Estudiante
        ('Acer', 'Nitro 5', 'Laptop', 19000, 'Intel', 'Core i5-11400H', 16000, 16, 512, 1, 1, 'RTX 3050', 9000),
        
        # 4. Gama Alta Profesional / Gamer Hardcore
        ('Lenovo', 'Legion 5 Pro', 'Laptop', 32000, 'AMD', 'Ryzen 7 5800H', 21000, 32, 1000, 1, 1, 'RTX 3070', 16000),
        
        # 5. Desktop para Oficina
        ('Lenovo', 'ThinkCentre', 'Desktop', 11000, 'Intel', 'Core i5-10400', 12000, 8, 1000, 0, 0, 'Intel UHD', 1200)
    ]

    cursor.executemany('''
        INSERT INTO computadoras (marca, modelo, tipo, precio, cpu_marca, cpu_modelo, cpu_puntos, ram_gb, almacenamiento_gb, es_ssd, es_gpu_dedicada, gpu_modelo, gpu_puntos)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', computadoras_iniciales)

    conexion.commit()
    conexion.close()
    print("Base de datos creada y poblada con éxito.")

# Ejecutar la función
if __name__ == "__main__":
    inicializar_bd() 