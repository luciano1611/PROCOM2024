import matplotlib.pyplot as plt



"""
La función de asignación de etiquetas fuerza a que 
se asignen las etiquetas solo si pertenecen al eje
Y de la primera columna, y si pertenecen al eje X 
de la ultima fila.
"""
def getLabels(row,rowIndex, colIndex, xLabel, yLabel):
    
    #Asigna etiqueta del eje Y solo al indico de las columnas
    if colIndex == 1:
        plt.ylabel(yLabel)

    #Asigna etiqueta del eje X solo al inicio de las filas
    if rowIndex == row:  
        plt.xlabel(xLabel)