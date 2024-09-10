import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

"""
Genera un diagrama de ojo a partir de una señal dada.

Parametros:
    - signal: La señal de entrada.
    - samples_per_symbol: Número de muestras por símbolo.
    - num_symbols: Número de símbolos a mostrar en el diagrama.

Retorno:
    - None. (La función muestra una gráfica del diagrama de ojo).
"""

### [5]: funcion para graficar el diagrama de ojo
def eye_diagram(data, n, offset, T):
    
    span    = 2 * n                         # define el rango de muestras a visualizar
    segments= int(len(data) / span)         # calculo del número de segmentos posibles 
    xmax    = (n - 1) * T                   # def. el límite máximo en el eje x
    xmin    = -(n - 1) * T                  # def. el límite mínimo en el eje x    
    x       = list(np.arange(-n, n) * T)    # valores del eje x: de -n a n segun el periodo
    xoff    = offset                        # def. de offset

    ### ploteo
    plt.figure()
    # bucle para trazar cada segmento de los datos en el diagrama de ojo
    for i in range(0, segments - 1):
        # traza los datos para el segmento actual con el desplazamiento aplicado
        plt.plot(x, data[(i * span + xoff):((i + 1) * span + xoff)], 'b')
    
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.show()
