import numpy as np
from tool._fixedInt import *

"""
    Aplicacion e interpolacion de un filtro de media móvil a la señal PRBS.
    
    Parametros:

    - prbs: Señal de entrada de tipo PRBS.
    - K: Tamaño del filtro de media móvil.
    - upsample_factor: Factor de interpolación (upsampling).
    
    Retorno:
    - Señal PRBS filtrada e interpolada.
    """

### [4]: funcion para aplicar un filtro a al señal PRBS en fase I & Q
def PRBS_process(prbs, k, upsample_factor):

    # def. de un filtro para aplicar a la señal PRBS 
    filter_k        = np.ones(k) / k
    
    # convolucion del filtro con la señal PRBS
    prbs_filtred    = np.convolve(prbs, filter_k, mode = 'same')

    # interpolacion por unsampling: repite cada valor 'upsample_factor' veces
    prbs_upsampled  = np.repeat(prbs_filtred, upsample_factor)
    
    # normalizacion de la PRBS en un rango de -1 y 1
    prbs_norm       = 2 * (prbs_upsampled - 0.5)
    
    # retorno de la PRBS procesada
    return prbs_norm
    
