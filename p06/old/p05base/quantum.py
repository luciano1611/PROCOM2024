import numpy as np
from tool._fixedInt import *

def quantum(rc, s=(8, 7), op='trunc'):
    """
    Calcula truncamiento/redondeo y saturación para cada elemento de rc.
    
    :param rc: Array de valores en punto flotante.
    :param s: Tuple con el formato de punto fijo (NBT, NBF).
    :param op: Operación a realizar ('trunc' para truncamiento, 'round' para redondeo).
    :return: Array de valores procesados.
    """
    NBT = s[0]          # Numero total de bits
    NBF = s[1]          # Numero de bits de la parte fraccionaria
    NBI = NBT - NBF     # Numero de bits de la parte entera

    # Verifica si la operación es válida
    if op not in ['trunc', 'round']:
        print('Error, valor de <op> no válido.')
        return None

    # Inicializa la lista para almacenar los valores cuantizados
    rc_x = []
    
    # Realiza la cuantización de cada valor en rc
    for val in rc:
        # Crear el objeto DeFixedInt con los parámetros especificados
        obj = DeFixedInt(NBT, NBF,'S',op,'saturate')
        obj.value = val  # Asigna el valor a cuantizar
        
        # Añadir el valor cuantizado a la lista
        rc_x.append(obj.fValue)

    # Convertir la lista a un array numpy para la salida
    return np.array(rc_x)



