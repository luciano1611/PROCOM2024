import numpy as np
import matplotlib.pyplot as plt

# se importa figPlot de figPlot.py
from figPlot                            import figPlot

# se importan las funciones auxiliares para validación de datos ingresados por el usuario
from func_ejercicio_B.get_row_col       import getRowCol
from func_ejercicio_B.get_joinVec       import getJoinVec
from func_ejercicio_B.get_num_plot      import getNumPlot
from func_ejercicio_B.get_show          import getShow
from func_ejercicio_B.get_subPlot_data  import getVector
from func_ejercicio_B.get_subPlot_data  import getTypeGraf
from func_ejercicio_B.get_subPlot_data  import getLim
from func_ejercicio_B.get_subPlot_data  import getLabel


# *variables globales* #
x           = []
y           = []
typeGraf    = []
xLim        = []
yLim        = []
xLabel      = []
yLabel      = []

#[1]: Función auxiliar para signar los datos a cada sub-plot
def getPlots(joinVec):
    global x, y, xLim, yLim, xLabel, yLabel

    # obtiene la cantidad de sub-plots a generar de la cantidad de elementos de joinVec
    subPlotNum  = len(joinVec)

    # bucle para registrar (pedir al usuario) cada sub-plot
    for i in range(subPlotNum):
        
        # para los vectores de datos:
        xData, yData    = getVector(i)

        # se concatenan los nuevos valores a los vectores de datos
        x       .append(xData)
        y       .append(yData)
        # para las demás listas se usa append para adjuntar los nuevos datos
        typeGraf.append(getTypeGraf (joinVec))
        xLim    .append(getLim      (i, 'X' ))   
        yLim    .append(getLim      (i, 'Y' ))
        xLabel  .append(getLabel    (i, 'X' ))        
        yLabel  .append(getLabel    (i, 'Y' ))
    
    # fin del bucle
    print(xLim)
    print(yLim)

#[2]: Función principal que llama a las funciones axilares para hacer de interfaz con el usuario 
def graficar():
    global x, y, xLim, yLim, xLabel, yLabel

    # funciones generales: no requieren bucle
    row, col    = getRowCol ()
    joinVec     = getJoinVec(row, col)
    numPlot     = getNumPlot()
    show        = getShow   ()
    
    # función que asigna los datos a cada sub-plot por un bucle
    getPlots(joinVec)

    # llamado a la función figPlot() con los valores cargados por el usuario
    figPlot(
        x           , 
        y           ,  
        row         , 
        col         ,
        joinVec     ,
        numPlot     ,
        show        ,
        typeGraf    ,     
        xLim        ,  
        yLim        , 
        xLabel      ,
        yLabel  
        )

# para testing
if __name__ == "__main__":
    # se llama a la función principal
    graficar()