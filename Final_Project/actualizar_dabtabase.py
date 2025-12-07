import sqlite3

def actualizar_bd_con_imagenes():
    conn = sqlite3.connect("sistema_experto.db")
    cursor = conn.cursor()

    # 1. Agregar columna nueva (si no existe)
    try:
        cursor.execute("ALTER TABLE computadoras ADD COLUMN imagen_archivo TEXT")
    except sqlite3.OperationalError:
        print("La columna 'imagen_archivo' ya existía, continuando...")

    # 2. Asignar nombres de archivos
    # Lista de tuplas: (Nombre_Imagen, Texto_a_buscar)
    actualizaciones = [
        ('hp_notebook.png', 'HP'),          # Buscará "HP" en marca
        ('dell_inspiron.png', 'Dell'),      # Buscará "Dell" en marca
        ('acer_nitro.png', 'Acer'),         # Buscará "Acer" en marca
        ('lenovo_legion.png', 'Legion'),    # Buscará "Legion" en MODELO
        ('lenovo_desktop.png', 'ThinkCentre') # Buscará "ThinkCentre" en MODELO
    ]

    for archivo, termino_busqueda in actualizaciones:
        # CORRECCIÓN AQUÍ:
        # Usamos "modelo" en lugar de "marca_modelo"
        # La lógica es: Actualiza si la marca coincide O si el modelo contiene el texto
        cursor.execute('''
            UPDATE computadoras 
            SET imagen_archivo = ? 
            WHERE marca = ? OR modelo LIKE ?
        ''', (archivo, termino_busqueda, f"%{termino_busqueda}%"))

    conn.commit()
    conn.close()
    print(f"Base de datos actualizada con éxito. Se asignaron {len(actualizaciones)} imágenes.")

if __name__ == "__main__":
    actualizar_bd_con_imagenes()