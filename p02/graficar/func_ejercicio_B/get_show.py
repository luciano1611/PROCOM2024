"""
función pra validar el ingreso del usuario 
al seleccionar si mostrar o no el gráfico 
"""

def getShow():

    # comunicación con el usuario 
    while True:
        
        print("\nIngrese 'y' para mostrar el plot completo ó 'n' para no mostrarlo.")
        op = input("Opción: ")
        
        # valida el ingreso
        if op in ['y', 'n']:
            # sale del bucle
            break
        print("\nIngrese una opción valida.")

    # retorna true o false según la elección del usuario
    if op == 'y':
        return True
    else:
        return False