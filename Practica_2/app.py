import json
from flask import Flask, request, jsonify
from flask import Flask, request, jsonify, render_template # Añade render_template

# Inicializar la aplicación Flask
app = Flask(__name__)

# Nombre del archivo que usaremos como base de conocimiento
DB_FILE = "conocimiento.json"

# --- Funciones Auxiliares para manejar la "Base de Datos" ---

def cargar_conocimiento():
    """Carga la base de conocimiento desde el archivo JSON."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, retorna un diccionario vacío.
        return {}

def guardar_conocimiento(data):
    """Guarda los datos actualizados en el archivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# --- Lógica Central del Chatbot ---

# Esta variable guardará la última pregunta que no se supo responder.
# En una aplicación real, esto se manejaría de forma más robusta (ej. por sesión de usuario).
pregunta_sin_respuesta = None

@app.route('/chat', methods=['POST'])
def chat():
    global pregunta_sin_respuesta

    # Obtener el mensaje del usuario desde la petición
    # Usamos .get() para evitar errores si no se envía el 'mensaje'
    mensaje_usuario = request.json.get('mensaje', '').lower().strip()

    # Cargar la base de conocimiento actual
    conocimiento = cargar_conocimiento()

    # --- MODO APRENDIZAJE ---
    # Si hay una pregunta pendiente y el usuario envía un mensaje,
    # asumimos que es la respuesta a esa pregunta.
    if pregunta_sin_respuesta:
        # Añadimos el nuevo conocimiento
        conocimiento[pregunta_sin_respuesta] = mensaje_usuario
        guardar_conocimiento(conocimiento)
        
        respuesta_bot = "¡Perfecto! Gracias, he aprendido algo nuevo."
        
        # Limpiamos la variable para que la próxima pregunta no entre aquí.
        pregunta_sin_respuesta = None
        
        return jsonify({"respuesta": respuesta_bot})

    # --- MODO NORMAL ---
    # Buscar una coincidencia perfecta en nuestra base de conocimiento
    if mensaje_usuario in conocimiento:
        respuesta_bot = conocimiento[mensaje_usuario]
        return jsonify({"respuesta": respuesta_bot})
    else:
        # --- INICIO DEL MODO ADQUISICIÓN DE CONOCIMIENTO ---
        # No se encontró una respuesta, guardamos la pregunta y pedimos ayuda.
        pregunta_sin_respuesta = mensaje_usuario
        
        # Esta es la pregunta que designamos para ingresar conocimiento nuevo
        pregunta_para_aprender = f"No sé qué responder a '{mensaje_usuario}'. ¿Qué debería haberte contestado?"
        
        return jsonify({"respuesta": pregunta_para_aprender})

@app.route('/')
def home():
    """Esta ruta servirá nuestra página de chat (index.html)."""
    return render_template('index.html')

# --- Punto de entrada para ejecutar la aplicación ---
if __name__ == '__main__':
    # debug=True permite que el servidor se reinicie automáticamente con cada cambio.
    # ¡No uses debug=True en un entorno de producción!
    app.run(debug=True)
