import numpy as np
import matplotlib.pyplot as plt

# importa funciones auxiliares
from .get_data_vector import getDataVector
from .get_data_vector import readVectorData

"""
Funciones que se llaman por un medio de un bucle 
para cada sub-plot
"""

#[A]: función de ingreso de vectores de datos
def getVector(subPlotNum):
     #El usuario define la función del eje y
    print(f"\n**Ingreso de vectores de datos a graficar {subPlotNum}**")
    
    #Comunicación con el usuario: validación
    while True:
        # mensajes de la terminal
        print("\nIngrese: ")
        print("1- Si desea generar un gráfico de prueba.")
        print("2- Si desea tomar una función de los valores de un <archivo.log>.")

        # evaluación
        op = input("\nOpción: ")
        if op in ['1', '2']:
            break
        else:
            print("Ingrese una opción valida.\n")
    
    # evaluación del ingreso
    if op == '1':
        x, y = getDataVector()      # función que genera un vector de datos aleatorios en x e y para graficar
    else:
        x, y = readVectorData()     # función que lee un vector de datos de un archivo.log
    return x, y



#[B]: función de ingreso de 'typeGraf' 
def getTypeGraf(joinVec):
    # para indicar el usuario a cual gráfico hace referencia
    plotNum = len(joinVec)
    print(f"\nIngrese el tipo de trazo del gráfico {plotNum}.")
    
    # ingreso del usuario con validación
    while True:

        type = input("\nIngrese el tipo de gráfico 'stem' o 'plot': ")
        
        #valida que sea de tipo stem o plot
        if type in ['stem', 'plot']:
            # sale del bucle
            break

        else:
            # imprime mensaje de error
            print("Error en el ingreso.\n")

    # retorna la selección validada
    return type


#[C]: función de ingreso de 'xlim' y 'ylim' 
def getLim(subPlotNum, xy):
    # ingresa los limites del eje X o el eje Y: 'xy' se lo usa para indicar al usuario si se refiere al eje X o al eje Y
    print(f"\n*Limites del eje {xy}*")
    print("\nIngrese:") 
    print(f"'y' si desea establecer limites al eje {xy} de la función número {subPlotNum}.") 
    print("'n' para saltear este paso. \n")
    
    # comunicación con el usuario
    while True:
        # validación
        op = input("Opción: ")
        # evalúa si la opción ingresada es correcta
        if op in ['y', 'n']:
            # sale del bucle
            break
        # mensaje de error 
        print("Ingrese una opción valida.\n")
    # fin del bucle

    # si no desea ingresar limites, retorna None
    if op == 'n':
        return 0, 0     # Retorna 0, 0 para indicar que no se establece un limite
    
    # si se quiere ingresar limites
    else:
        # se valida el ingreso
        while True:
            # valida que los datos ingresados sean float
            try:
                start   = float(input("Ingrese limite superior: "))
                stop    = float(input("Ingrese limite inferior: "))
                
                # valida el ingreso
                if start < stop:
                    # sale del grupo
                    break
                # si no se cumple
                else:
                    # mensaje de error
                    print("\nIngrese un rango valido.")

            # ante un ingreso de un tipo de dato que no sea de tipo float
            except ValueError:
                # mensaje de error
                print("\nError, ingrese números reales.")
        
        # retorna el limite
        limit = (start, stop)
        return limit


#[D] ingreso de 'xlabel' e 'ylabel' 
def getLabel(subPlotNum, xy):
    # ingresa los labels del eje X o el eje Y: 'xy' se lo usa para indicar al usuario si se refiere al eje X o al eje Y
    print(f"\n*Labels del eje {xy}*")
    print("\nIngrese: ") 
    print(f"'y' si desea definir un Label para el eje {xy} de la función número {subPlotNum}.")
    print("'n' para saltear este paso.\n")
    
    # comunicación con el usuario
    while True:
        # validación
        op = input("\nOpción: ")
        if op in ['y', 'n']:
            break
        print("Ingrese una opción valida.")
    
    # si se ingresa 'n' se retorna None
    if op == 'n':
        return " "  #Leyenda vacía

    # si se ingresa 'y' se pide al usuario que ingrese una leyenda
    else:

        print(f"\nIngrese el Label del eje {xy} del gráfico {subPlotNum}.")

        # como es una string no se requiere validación 
        label = input("Leyenda: ")

    #retorna el label
    return label