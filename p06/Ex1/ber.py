import numpy as np

def bit_error_rate(tx_bits, rx_bits):

    # evalua que ambas listas tengan el mismo tamaño
    if len(tx_bits) != len(rx_bits):
        print('Error, el tamaño de las listas de bits transmitidos y recibidos no coincide.')
        return None
    
    len_bits    = len(tx_bits)  # == len(rx_bits)
    bit_error   = 0             

    # comparacion de bit a bit de las listas
    for i in range(len_bits):
    
        if tx_bits[i] != rx_bits[i]:
            # si los bits son diferentes, incrementa el contador de errores
            bit_error = bit_error +1

    # calculo de la BER (tasa de error)
    tot_bits    = len(tx_bits)
    ber         = bit_error / tot_bits

    return ber
