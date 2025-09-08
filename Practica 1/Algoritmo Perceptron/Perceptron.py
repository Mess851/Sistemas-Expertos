import numpy as np

class Perceptron:
    def __init__(self, tasa_aprendizaje=0.1, n_iteraciones=10):
        self.tasa_aprendizaje = tasa_aprendizaje
        self.n_iteraciones = n_iteraciones
        self.pesos = None
        self.sesgo = None

    def fit(self, X, y):
        # Inicializar pesos y sesgo
        n_caracteristicas = X.shape[1]
        self.pesos = np.zeros(n_caracteristicas)
        self.sesgo = 0

        # Aprender de los datos
        for _ in range(self.n_iteraciones):
            for i, x_i in enumerate(X):
                condicion = np.dot(x_i, self.pesos) + self.sesgo
                prediccion = 1 if condicion >= 0 else 0
                actualizacion = self.tasa_aprendizaje * (y[i] - prediccion)
                self.pesos += actualizacion * x_i
                self.sesgo += actualizacion

    def predict(self, X):
        condicion = np.dot(X, self.pesos) + self.sesgo
        return 1 if condicion >= 0 else 0

# --- Aplicación al caso de la vida diaria ---

# Datos de entrenamiento: [¿Nublado?, ¿Pronóstico Lluvia?]
X_entrenamiento = np.array([[1, 1], [1, 0], [0, 1], [0, 0]])
# Resultados esperados: [Llevar Paraguas (1) o No (0)]
y_entrenamiento = np.array([1, 1, 1, 0])

# Crear y entrenar el modelo
perceptron = Perceptron()
perceptron.fit(X_entrenamiento, y_entrenamiento)

# --- Arrojar un resultado ---
# Pregunta: ¿Qué hago si NO está nublado (0) pero el pronóstico SÍ dice que lloverá (1)?
nueva_situacion = np.array([0, 1])
prediccion = perceptron.predict(nueva_situacion)

# Imprimir resultado
print("--- Algoritmo Perceptrón: Decisión de llevar paraguas ---")
decision = "Sí, llevar paraguas." if prediccion == 1 else "No, no llevar paraguas."
print(f"Situación: No está nublado, pero el pronóstico dice que lloverá.")
print(f"Predicción del algoritmo: {decision}")