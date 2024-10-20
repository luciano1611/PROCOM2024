"""
PRBS9: Codigo de implementacion de la funcion de PRBS

Explicacion del codigo:

        ...
"""

def val_prbs9(seed):

    # si la semilla no es de 9 bits
    if len(seed) != 9:
        print("Error en el tamaño de la Semilla, debe ser de 9 bits.")
        return None

    # si el contenido de la semilla no es un binario
    if not all(bit in [0, 1] for bit in seed):
        print("Error en el contenido de la Semilla, debe contener solo numeros binarios.")
        return None 

    # si no
    return seed

'''
def prbs9(seed=0b110101010, length):
    
    aux_bin     = bin(seed)[2:] 
    reg_prbs    = [int(bit) for bit in aux_bin]



    for i in range(length):
'''