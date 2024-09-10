import matplotlib.pyplot as plt

"""
Esta función se usa para validar el valor de posición
pasado por tupla, la cual se usa cuando la posición
ocupa mas de una celda en el gráfico.
"""
def tupleValidation(row, col, pos):
    # se extrae el rango de la tupla dentro de la figura:
    start, end  = pos           #Inicio y fin del sub-plot
    limit       = row * col     #Limite de número de celdas

    # se evalúa que el rango no exceda el tamaño de la figura
    if (start < 1) or (end < 1) or (start > limit) or (end > limit):

        print("Error, posición fuera de rango")
        return False

    # verifica que el sub-plot este en una misma fila o columna:
    startRow    = (start - 1) // col    # el resultado de la division es el mismo si pertenecen a la misma fila
    endRow      = (end   - 1) // col    # el resultado de la division es el mismo si pertenecen a la misma fila
    startCol    = (start - 1) %  col    # el resto de la division indica si la posición esta en la misma columna
    endCol      = (end   - 1) %  col    # el resto de la division indica si la posición esta en la misma columna

    # si el gráfico esta en la misma fila o columna
    if (startRow == endRow) or (startCol == endCol):

        # devuelve True
        return True

    # Si no, se imprime un mensaje de error
    print(f"Error, la posición {start},{end} es No valida.")
    # devuelve False
    return False
