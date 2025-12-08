import sqlite3

def poblar_base_datos():
    conn = sqlite3.connect("sistema_experto.db")
    cursor = conn.cursor()

    # 1. LIMPIEZA: Borramos todo lo anterior para empezar desde cero y evitar duplicados/errores
    cursor.execute("DELETE FROM computadoras")
    # Opcional: Reiniciar el contador de IDs (para que empiece en 1 de nuevo)
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='computadoras'")
    print("🧹 Base de datos limpiada.")

    # 2. NUEVA LISTA (Con extensión .jpg)
    # Verifica que tus archivos en la carpeta 'images' tengan estos nombres exactos.
    # --- LISTA CORREGIDA PARA llenar_bd.py ---
    nuevas_pcs = [
        # --- GAMA BAJA / ESTUDIANTES ---
        ('Acer', 'Aspire 3', 'Laptop', 7500, 'AMD', 'Ryzen 3 3250U', 4000, 8, 256, 1, 0, 'Radeon Vega', 1500, 'acer_aspire.jpg'),
        ('HP', 'Pavilion 15', 'Laptop', 10500, 'Intel', 'Core i3-1215U', 11000, 8, 512, 1, 0, 'Intel UHD', 2000, 'hp_pavilion.jpg'),
        ('Lenovo', 'IdeaPad Slim', 'Laptop', 9200, 'Intel', 'Core i3-1115G4', 6000, 8, 256, 1, 0, 'Intel UHD', 1000, 'lenovo_ideapad.jpg'),

        # --- GAMA MEDIA / PROFESIONAL ---
        ('Apple', 'MacBook Air M1', 'Laptop', 18000, 'Apple', 'M1 Chip', 15000, 8, 256, 1, 0, 'Apple GPU', 8000, 'macbook_air.jpg'),
        ('Dell', 'XPS 13', 'Laptop', 22000, 'Intel', 'Core i7-1165G7', 10500, 16, 512, 1, 0, 'Intel Iris Xe', 2800, 'dell_xps.jpg'),
        ('Microsoft', 'Surface Laptop 4', 'Laptop', 19500, 'AMD', 'Ryzen 5 Custom', 12000, 16, 512, 1, 0, 'Radeon Graphics', 2200, 'surface_laptop.jpg'),
        # CORREGIDO: Se cambió 'asus_tuf.jpg' por 'asus_vivobook.jpg'
        ('Asus', 'Vivobook Pro', 'Laptop', 21000, 'AMD', 'Ryzen 7 5800H', 21000, 16, 1000, 1, 1, 'RTX 3050', 9000, 'asus_vivobook.jpg'), # <--- CORREGIDO

        # --- GAMA GAMER / INGENIERÍA ---
        ('Asus', 'TUF Gaming F15', 'Laptop', 18500, 'Intel', 'Core i5-11400H', 16000, 16, 512, 1, 1, 'RTX 3050', 9500, 'asus_tuf.jpg'),
        ('MSI', 'Katana GF66', 'Laptop', 24500, 'Intel', 'Core i7-12700H', 26000, 16, 1000, 1, 1, 'RTX 3060', 13000, 'msi_katana.jpg'),
        # VERIFICAR: Asegúrate que tu archivo se llame exactamente 'acer_nitro.jpg'
        ('Acer', 'Predator Helios', 'Laptop', 29000, 'Intel', 'Core i7-11800H', 21000, 32, 1000, 1, 1, 'RTX 3060', 13000, 'acer_nitro.jpg'), # <--- VERIFICA EL NOMBRE

        # --- GAMA ULTRA / HARDCORE ---
        ('Asus', 'ROG Strix G16', 'Laptop', 38000, 'Intel', 'Core i9-13980HX', 45000, 32, 1000, 1, 1, 'RTX 4070', 22000, 'rog_strix.jpg'),
        ('Alienware', 'X15 R2', 'Laptop', 45000, 'Intel', 'Core i9-12900H', 30000, 32, 2000, 1, 1, 'RTX 3080 Ti', 24000, 'dell_xps.jpg'),
        ('PC', 'Gamer Xtreme VR', 'Desktop', 32000, 'Intel', 'Core i7-13700F', 32000, 32, 2000, 1, 1, 'RTX 4060 Ti', 19000, 'pc_gamer_xtreme.jpg'),
        ('PC', 'Ryzen Creator', 'Desktop', 42000, 'AMD', 'Ryzen 9 7900X', 48000, 64, 2000, 1, 1, 'RTX 4070', 22000, 'pc_gamer_creator.jpg')
    ]

    try:
        cursor.executemany('''
            INSERT INTO computadoras (marca, modelo, tipo, precio, cpu_marca, cpu_modelo, cpu_puntos, ram_gb, almacenamiento_gb, es_ssd, es_gpu_dedicada, gpu_modelo, gpu_puntos, imagen_archivo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', nuevas_pcs)
        
        conn.commit()
        print(f"✅ Se agregaron {len(nuevas_pcs)} computadoras nuevas (Versión JPG).")
    except sqlite3.Error as e:
        print(f"❌ Error al insertar: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    poblar_base_datos()