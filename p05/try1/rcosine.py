import numpy as np
from tool._fixedInt import *

### [1]: funcion de respuesta al impulso del pulso de caída cosenoidal 
def rcosine(beta, t_baud, oversampling, n_baud, norm=False):
    """ Respuesta al impulso del pulso de caída cosenoidal """
    # vector de tiempo
    t_vec = np.arange(-0.5 * n_baud * t_baud,
                      0.5 * n_baud * t_baud,
                      float(t_baud) / oversampling)
    
    # vector de respuesta al impulso
    y_vec = []

    # para cada muestra de tiempo se calcula la respuesta al impulso
    for t in t_vec:
        sinc = np.sinc(t / t_baud)
        cos = np.cos(np.pi * beta * t / t_baud)
        den = 1 - (4.0 * beta**2 * t**2 / (t_baud**2))
        if den == 0:  # evitar división por cero
            y_vec.append(0.0)
        else:
            y_vec.append((sinc * cos) / den)

    # conversión a array
    y_vec = np.array(y_vec)

    if norm:
        return t_vec, (y_vec / np.sqrt(np.sum(y_vec ** 2)))
    else:
        return t_vec, y_vec


### [2]: funcion de cuantizacion de las respuestas de filtros en formato de punto fijo
def quantization(rc0, rc1, rc2, op='1'):
    # listas para almacenar los valores cuantificados de cada filtro
    rc0_0 = []
    rc1_1 = []
    rc2_2 = []

    # almacenamiento de las señales en una lista para recorrer con un 'for'
    filters = [rc0, rc1, rc2]
    aux = []

    # validacion de la opcion
    if op not in ['1', '2', '3', '4', '5', '6']:
        return None
    
    # definicion de los parametros segun la opcion seleccionada
    if op == '1':
        # primera opción: cuantificación truncada con saturación en punto fijo S(8,7)
        print("trunc/sat. en punto fijo S(8,7)")
        params = (8, 7, 'trunc')
    elif op == '2':
        # segunda opción: cuantificación redondeada con saturación en punto fijo S(8,7)
        print("round/sat. en punto fijo S(8,7)")
        params = (8, 7, 'round')
    elif op == '3':
        # tercera opción: cuantificación truncada con saturación en punto fijo S(3,2)
        print("trunc/sat. en punto fijo S(3,2)")
        params = (3, 2, 'trunc')
    elif op == '4':
        # cuarta opción: cuantificación redondeada con saturación en punto fijo S(3,2)
        print("round/sat. en punto fijo S(3,2)")
        params = (3, 2, 'round')
    elif op == '5':
        # quinta opción: cuantificación truncada con saturación en punto fijo S(6,4)
        print("trunc/sat. en punto fijo S(6,4)")
        params = (6, 4, 'trunc')
    elif op == '6':
        # sexta opción: cuantificación redondeada con saturación en punto fijo S(6,4)
        print("round/sat. en punto fijo S(6,4)")
        params = (6, 4, 'round')

    # para cada respuesta al impulso
    for f in filters:

        #arrayFixedInt(8, 7, rc0, signedMode='S', roundMode='trunc', saturateMode='saturate') #S (8,7) Trunc con saturacion
        aux.append(arrayFixedInt(params[0], params[1], f, signedMode='S', roundMode=params[2], saturateMode='saturate'))

    # se llenan las listas con los valores cuantificados (fValue) correspondientes
    for ptr in range(len(rc0)):
        # almacenamiento de los valores cuantificados de rc0 en rc0_0
        rc0_0.append(aux[0][ptr].fValue)

    for ptr in range(len(rc1)):
        # almacenamiento de los valores cuantificados de rc1 en rc1_1
        rc1_1.append(aux[1][ptr].fValue)

    for ptr in range(len(rc2)):
        # almacenamiento de los valores cuantificados de rc2 en rc2_2
        rc2_2.append(aux[2][ptr].fValue)

    # conversion de las listas en arrays
    rc0 = np.array(rc0_0)
    rc1 = np.array(rc1_1)
    rc2 = np.array(rc2_2)

    # retorno de los arrays cuantificados
    return rc0, rc1, rc2
