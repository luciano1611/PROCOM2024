import numpy as np


### [1]: Funcion de prbs9
def prbs9(seed=0b110101010, length=20, QPSK=True):
    
    ### pasaje a lista binaria
    aux     = bin(seed)[2:].zfill(9)    # quita prefijo 0b, zfill asegura que la longitud sea de 9 bits, si no rellena con zero 
    reg     = [int(bit) for bit in aux] # almacena cada bit en una lista
    # declararcion de lista de prbs
    prbs    = []

    for i in range(length):

        ### agrega 1 bit a la prbs
        simb    = -1 if (reg[8] == 1) else 1    # para simbolos -1 : 1
        bits    = reg[0]                        # para bits      0 : 1
        
        # segun la flag QPSK
        prbs.append(simb if (QPSK is True) else bits)

        ### shift register
        reg     = np.roll(reg, -1)  # 1 rotacion a la izquierda
        reg[8]  = reg[5] ^ reg[8]   # XOR del bit 5 con el bit 9 del registro (lista)

    # pasaje a array    
    print("IN",prbs)
    return np.array(prbs)


### [2]: Funcino de Bit Error Rate (BER)
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

    ber_count = 0

    # compara bit a bit
    for i in range(len(tx_bits)):
        # por cada bit distinto
        if tx_bits[i] != rx_bits[i]:
            # incrementa el contador de BER
            ber_count   += 1

    # tasa de error
    ber = ber_count / len(tx_bits)
    return ber



### [2]: Funcion de upsample
def upsample(signal, os, n_symb): 
    
    # zeros para muestreo: upsampling
    zsymb   = np.zeros(os * n_symb)
    zsymb[1:len(zsymb):int(os)] = signal

    
    print(zsymb.shape[0])
    
    return zsymb


### [3]: Funcion de downsample
def downsample(signal, os):
    
    signal_out = signal[::os]
    print("OUT",signal_out)

    return signal_out

