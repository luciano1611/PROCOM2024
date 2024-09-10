import random
import numpy as np
import matplotlib.pyplot as plt
# *funciones para generar los vectores de datos* #

"""
[1]:    Para testeo se usa la siguiente función para generar 
        gráficos aleatorios. Esta se llama dentro de un bucle en el 
        código principal de graficar() para cada subPlot
"""
def getDataVector():
    
    t = np.linspace(0, 2 * np.pi, 400)
    x = t
    y = random.uniform(-10, 10) * np.sin(t + random.uniform(0, 2 * np.pi))
        
    return x, y


"""
[2]:    Para casos generales, se busca que el usuario ingrese las 
        funciones desde un <archivo.log> 
"""
# b) Función leída de un archivo
def readFile(fileName):

    # abre el archivo en modo lectura
    with open(fileName, 'r') as file:
        data = file.read()
    
    y = [int(value.strip()) for value in data.split(',')]
    
    x = list(range(len(y)))

    return x, y

# función para levanta el archivo indicado por el usuario
def readVectorData():
    # bucle para el ingreso del archivo
    while True:
        fileName = input("Ingrese el nombre del <archivo.log>: ")
        
        #Se verifica que se pueda leer correctamente el <archivo.log>
        try: 
            # devuelve los valores de 'x' e 'y' Leidos del archivo
            return readFile(fileName)
        
        except FileNotFoundError:
            print("No se pudo encontrar el archivo.")
        
        except Exception as e: 
            # imprime el error correspondiente.
            print("Error:", e)


# código para testing
if __name__ == "__main__":


    # Llamar a la función para leer los datos del archivo
    x, y = readVectorData()

    # Graficar los valores
    plt.plot(x, y)
    plt.title('Ploteo de readVectorData()')
    plt.xlabel('indice')
    plt.ylabel('valor')
    plt.grid(True)
    plt.show()

