# Definimos nuestras proposiciones (P y Q)
# P = El usuario es un administrador.
# Q = El usuario tiene acceso a todos los archivos.

def check_access(is_admin):
  """
  Esta función representa la regla (Premisa 1):
  Si el usuario es un administrador (P), entonces tiene acceso total (Q).
  """
  if is_admin:
    return "Acceso total concedido."
  else:
    return "Acceso de usuario estándar."

# Establecemos nuestro hecho (Premisa 2):
# El usuario ES un administrador. (Afirmamos el antecedente P)
user_is_admin = True

# Realizamos la inferencia llamando a la función con nuestro hecho
conclusion = check_access(user_is_admin)

# Imprimimos el resultado
print(f"Premisa: ¿El usuario es administrador? {user_is_admin}")
print(f"Conclusión: {conclusion}") 
# Resultado esperado: Acceso total concedido.