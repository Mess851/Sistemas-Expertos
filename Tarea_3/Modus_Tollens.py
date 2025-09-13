# Mantenemos las mismas proposiciones (P y Q)
# P = El sistema está en línea.
# Q = Se puede acceder a la base de datos.

def check_system_status():
  """
  Esta función representa la regla (Premisa 1):
  Si el sistema está en línea (P), entonces la base de datos es accesible (Q).
  """
  # En una situación real, aquí habría código que verifica el estado del sistema.
  # Para este ejemplo, simularemos que el sistema está caído.
  system_is_online = False
  
  if system_is_online:
    return "Base de datos accesible."
  else:
    return "Error: No se puede conectar a la base de datos."

# Establecemos nuestro hecho (Premisa 2):
# Observamos que la base de datos NO es accesible. (Negamos el consecuente Q)
database_status = check_system_status()
print(f"Observación: Estado de la base de datos -> '{database_status}'")

# Realizamos la inferencia lógica basada en la observación
conclusion = None
if database_status != "Base de datos accesible.": # Si Q es falso...
  conclusion = "El sistema NO está en línea."     # ...entonces P debe ser falso.

# Imprimimos la conclusión
print(f"Conclusión: {conclusion}")
# Resultado esperado: El sistema NO está en línea.