import numpy as np
import matplotlib.pyplot as plt

# importación de funciones de otros códigos:
from .func_ejercicio_A.tuple_validation     import tupleValidation
from .func_ejercicio_A.get_sub_plot         import getSubPlot
from .func_ejercicio_A.get_labels           import getLabels


# función principal:
def figPlot(
    x                   ,   # vector de datos de x   
    y                   ,   # vector de datos de y
    row                 ,   # cantidad de filas
    col                 ,   # cantidad de columnas
    joinVec             ,   # vector con la posición de cada sub-plot
    numplot             ,   # número de la figura   
    show                ,   # flag que indica si mostrar o no la figura  
    typeGraf    = None  ,   # indica si el sub-plot es de tipo stem o plot
    xlim        = None  ,   # define los limites en x del sub-plot   
    ylim        = None  ,   # define los limites en x del sub-plot   
    xLabel      = ' '   ,   # define los labels en x del sub-plot   
    yLabel      = ' '       # define los labels en y del sub-plot   
    ):

    # se define un tamaño en función de la cantidad de celdas de la figura
    pltSizeX    = 5                             
    pltSizeY    = 4
    pltSize     = (row*pltSizeX, col*pltSizeY)  # según el numero de row y col

    # se crea un plot con el numero 'numplot' y con tamaño pltSize
    plt.figure(numplot, figsize = pltSize)

    # se lee la cantidad de elementos de 'joinVec' para iterar en el bucle
    joinVecSize = len(joinVec)

    # bucle para generar cada sub-plot de la figura: itera en la cantidad de elementos de joinVec
    for i in range(joinVecSize):

        #[1] carga la posición actual de joinVec
        pos = joinVec[i]

        #[2] genera un plt.subplot(row,col,pos) validado
        if getSubPlot(row, col, pos) == False:

            print(f"Error en el sub-plot de posición {pos}")

        #[3] define el tipo de trazo: stem o plot
        if (typeGraf[i]) and (typeGraf[i] == 'stem'):
            # si es stem:
            plt.stem(x[i], y[i])
        
        else:
            # si no:
            plt.plot(x[i], y[i])

        #[4] añade los labels: solo para los gráficos que están en la primera columna o ultima fila:
        
        # si es una tupla: el gráfico ocupa mas de una celda
        if isinstance(pos, tuple):

            start, end  = pos
            rowIdx      = (end      - 1) // col
            colIdx      = (start    - 1) %  col

        # si no: el gráfico ocupa una única celda de la figura
        else:

            rowIdx      = (pos      - 1) // col
            colIdx      = (pos      - 1) %  col

        # se llama a la función encargada de asignar los labels:
        getLabels(row, rowIdx +1, colIdx +1, xLabel[i], yLabel[i])

        #[5] definición de los limites, si se lo indica
        # si se especifica un xlim
        if xlim and xlim[i] and (xlim[i] != (0,0)):
            plt.xlim(xlim[i])

        # si se especifica un ylim
        if ylim and ylim[i] and (ylim[i] != (0,0)):
            plt.ylim(ylim[i])       

    # fin del for

    #[6] si se lo indica, se muestra la figura en pantalla
    if show == True:
        plt.show()

# fin de la función 

# código para testing
if __name__ == '__main__':

    # definición de funciones para testing:
    t = np.linspace(0, 2 * np.pi, 400)
    # vectores de datos
    x = [t, t, t, t, t, t, t, t, t]
    y = [np.sin(t), np.cos(t), np.sin(2*t), np.cos(2*t), np.sin(3*t), np.cos(3*t), np.sin(4*t), np.cos(4*t), np.sin(5*t)]

    # llamada a la función con 3 filas y 3 columnas
    figPlot(
        x, 
        y, 
        row         = 3                                                 , 
        col         = 3                                                 , 
        joinVec     = [(1, 3), (4, 7), 5, 6, (8, 9)]                    , 
        numplot     = 1                                                 , 
        show        = True                                              ,   
        typeGraf    = ['plot', 'stem', 'stem', 'plot', '']              , 
        xlim        = None                                              , 
        ylim        = None                                              , 
        xLabel      = [ 't1', 't2','t3', 't4', 't5', 't6']              , 
        yLabel      = ['Amp1', 'Amp2', 'Amp3', 'Amp4', 'Amp5', 'Amp6'])


