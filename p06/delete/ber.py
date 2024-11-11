import numpy as np

def bit_error_rate(tx_bits, rx_bits):

    # para debug
    #print('Input Bits  ', tx_bits)
    #print('Output Bits ', rx_bits)

    # verifica que el tamaño de ambas lista sea el mismo
    if len(tx_bits) != len(rx_bits):
        # mensaje de error
        print('Error, el tamaño de las listas de bits transmitidos y recibidos no coincide.')
        # sale de la funcion
        return None

    # compara bit a bit
    for i in range(len(tx_bits)):
        # por cada bit distinto
        if tx_bits[i] != rx_bits[i]:
            # incrementa el contador de BER
            ber_count   += 1

    # tasa de error
    ber = ber_count / len(tx_bits)
    return ber

