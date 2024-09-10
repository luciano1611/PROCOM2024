import numpy as np

"""
[1]:    función que obtiene matriz para mostrar las 
        posiciones disponibles de la figura
"""
def getMatrix(row, col):
    """
    Esta función genera una matriz en la cual, en 
    cada celda, se coloca el valor de la posición 
    de la misma. La misma se hace con las dimensiones
    especificadas por el usuario.

    Ejemplo de matriz: 
    row = 3
    col = 4

    matrix =    [[ 1,  2,  3,  4],
                 [ 5,  6,  7,  8],
                 [ 9, 10, 11, 12]]

    Este es el modelo de matriz que devuelve la función.
    Conforme se ocupen las posiciones de la matriz (que 
    indican la ubicación de los sub-plots de la figura), 
    se llenan las mismas con 0. Esto se realiza en otra
    función. 
    """
    # crea un vector con los valores consecutivos de 1 hasta (row*col) + 1 
    array   = np.arange(1, (row*col) + 1)
    
    # reagrupa el array en formato de matriz de dos dimensiones
    matrix  = array.reshape(row, col)

    #print("Celdas disponibles para gráficos.") 
    #print(matrix)

    # devuelve la matriz
    return matrix

"""
[2]:    Validación del valor de posición de celda ingresado por el usuario. 
        Al ocupar una posición de la matriz la celda se la rellena con '0'.
        Si el usuario elige una posición que contiene un '0' imprime un 
        mensaje de Error.
"""
def validPos(pos, matrix):
    
    # obtiene cantidad de filas
    rowNum = len(matrix)

    # obtiene cantidad de columnas
    colNum = len(matrix[0])

    # si la posición ingresada esta dentro del rango de la matriz 
    if(pos > 0) and (pos <= rowNum*colNum):
        
        # recorre la matriz por un bucle for
        for i in range(rowNum):
            for j in range(colNum):

                # si la posición No esta ocupada (es decir que es distinta de '0').  Previamente se valida que pos > 0    
                if (matrix[i][j] == pos):   # como pos contiene el valor de la celda, se la compara directamente con la celda
                    
                    # se inserta un 0 en la posición seleccionada
                    matrix[i][j] = 0
                    
                    # devuelve la matriz actualizada
                    return matrix

    # si la posición esta fuera del rango de la matriz, o ya fue ocupada:
    print("Posición no valida.")
    return None


"""
[3]:    Validación del valor de posición de tupla ingresado por el usuario, 
        Al ocupar mas de una posición de la matriz se la rellena con '0' en 
        todo el sub-vector ocupado. Si el usuario elige una posición que contiene 
        al menos un '0' dentro del sub-vector indicado por la tupla, se imprime 
        un mensaje de Error.
"""
def validTuple(pos, matrix):
    start, end = pos               # Inicio y fin de la posición
    row = len(matrix)              # Cantidad de filas
    col = len(matrix[0])           # Cantidad de columnas
    limit = row * col              # Cantidad máxima de elementos en la matriz

    # a) Si los valores ingresados están fuera de rango:
    if (start < 1 or end < 1) or (start > limit or end > limit) or (start > end):
        print("Error, posición fuera de rango.")
        return None
    
    # b) Si el sub plot está en la misma fila o columna:
    rowStart    = (start - 1) // col    # Índice de fila para el inicio
    rowEnd      = (end   - 1) // col    # Índice de fila para el final
    colStart    = (start - 1) %  col    # Índice de columna para el inicio
    colEnd      = (end   - 1) %  col    # Índice de columna para el final
   
    vecPos = []

    #Si 'pos' está en una misma fila:
    if rowStart == rowEnd:
        vecPos = matrix[rowStart][colStart:colEnd + 1]
    
    #Si 'pos' está en una misma columna:
    elif colStart == colEnd:
        vecPos = [matrix[i][colStart] for i in range(rowStart, rowEnd + 1)]
    
    #Si no está en la misma fila o columna:
    else:
        print("Error, el rango no está en la misma fila o columna")
        return None

    # c) Verificar si algún elemento de vecPos es 0
    for element in vecPos:
        if element == 0:
            print("Posición invalida, hay celdas intermedias ocupadas.")
            return None
    
    #Reemplaza los elementos de la posición elegida por 0 si la validación es correcta
    if rowStart == rowEnd:
        for j in range(colStart, colEnd + 1):
            matrix[rowStart][j] = 0
    
    elif colStart == colEnd:
        for i in range(rowStart, rowEnd + 1):
            matrix[i][colStart] = 0
    
    #Devuelve la matriz actualizada
    return matrix