import numpy as np
import matplotlib.pyplot as plt

"""
Función para obtener el número de plot
"""

def getNumPlot():

    # comunicación con el usuario
    print("\nIngrese el número (entero) del plot, el cual sera incluido en la figura general.")

    # validación del ingreso del usuario
    while True: 
        # valida que numPlot sea un entero
        try:    
            numPlot = int(input('Ingreso = '))
            # si es valido sale del bucle
            break
        # en caso de ingreso incorrecto
        except ValueError:
            # mensaje de error
            print("Error, debe ingresar un número entero.")
    
    # fin del bucle

    # devuelve el valor de numPlot validado
    return numPlot
        