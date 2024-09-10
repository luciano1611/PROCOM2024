import matplotlib.pyplot as plt

# importación de funciones de otros códigos:
from .tuple_validation import tupleValidation

"""
La función getSubPlot genera cada sub-plot ya sea
ingresado por una única posición o por una tupla (mas
de una posición). Esta función evalúa la tupla por medio
de tuple_validation
"""
def getSubPlot(row, col, pos):

    #[A] Si 'pos' es una tupla (ocupa más de una celda):
    if isinstance(pos, tuple):

        #Llama a tupleValidation para evaluar 'pos'
        if tupleValidation(row, col, pos):
            #Genera el sub-plot
            plt.subplot(row, col, pos)

        else:
            #En caso de una 'pos' invalida
            return False

    #[B] Si 'pos' ocupa una única celda:
    else:

        #Se evalúa si la posición dentro de la cuadrilla es valida
        if(pos > 0) and (pos <= row*col):
            #Genera el sub-plot
            plt.subplot(row, col, pos)

        else:
            #En caso de que se encuentre fuera d ela cuadrilla
            return False

    # si se cumple [A] o [B] retorna True
    return True
