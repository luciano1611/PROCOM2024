import numpy as np

def quantum(rc, s=(8, 7), op='trunc'):
    """
    Calcula truncamiento/redondeo y saturación para cada elemento de `rc` en `t_vec`.
    
    :param rc: Array de valores en punto flotante.
    :param t_vec: Array que indica el tiempo o índice.
    :param s: Tuple con el formato de punto fijo (NBT, NBF).
    :param op: Operación a realizar ('trunc' para truncamiento, 'round' para redondeo).
    :return: Array de valores procesados.
    """
    NBT = s[0]   # Número total de bits
    NBF = s[1]   # Número de bits de la parte fraccionaria
    NBI = NBT - NBF  # Número de bits de la parte entera

    # Para cálculo de truncamiento/redondeo
    SCALE = 1 << NBF  # Factor de escala para parte fraccionaria

    # Para cálculo de saturación
    MAX_VAL = (1 << (NBI)) - (1 / SCALE)  # Valor máximo permitido
    MIN_VAL = -(1 << (NBI))  # Valor mínimo permitido

    # Array para almacenar los resultados
    result = np.zeros_like(rc)

    # Procesar cada elemento de rc usando un bucle for
    for i in range(len(rc)):
        if op == 'trunc':
            # Truncamiento
            value = (rc[i] * SCALE) // 1 / SCALE
        elif op == 'round':
            # Redondeo
            value = round(rc[i] * SCALE) / SCALE
        else:
            print('Error, ingreso de operación incorrecto.')
            return rc  # Retorna la misma entrada sin operar

        # Saturación
        value_saturated = max(MIN_VAL, min(value, MAX_VAL))

        # Almacenar el resultado
        result[i] = value_saturated

    return result

