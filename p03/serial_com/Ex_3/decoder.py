# librerias
import struct   # para convertir la cadena de bytes en una string
# para testing
from encoder    import encoder

"""función para decodificar los datos"""
def decoder(frame):
    
    """obtención de datos de la trama"""
    # obtiene el inicio y fin de la trama
    header      = frame[  0  ]
    footer      = frame[ -1  ] 

    # obtiene los 3 bits mas significativos
    start       = header >> 5   
    stop        = footer >> 5

    # si hay un error en el start_bit o el stop_bit
    if (start != 0b101) or (stop != 0b010):
        # mensaje de error
        return 'Error, inicio o fin de trama incorrecto.'
    
    # si LS + S_SIZE del inicio y fin de trama son distintos
    if (header & 0x0F) != (footer & 0x0F):
        # mensaje de error
        return 'Error, tamaño de trama no validado.'


    # obtiene los datos de tamaño de trama
    ls          = (header & 0b00010000) >> 4    # extrae solo LS
    s_size      = header & 0x0F                 # extrae solo S_SIZE
    l_size_high = frame[  1  ]                  # extrae L_SIZE_HIGH de la trama
    l_size_low  = frame[  2  ]                  # extrae L_SIZE_LOW de la trama


    # si LS es 1, el dato es LONG
    if ls == 0b1:
        # tamaño descripto por variable 'int' de 16 bits
        size    = (l_size_high << 8) | l_size_low
    # si LS es 0 el dato es SHORT
    else:
        # tamaño descripto por variable 'int' de 8 bits
        size    = s_size


    """extracción de los datos de la trama"""
    # dispositivo
    device      = frame[  3  ]
    # datos
    data_bytes  = frame[4:4+size] 

    """decodificación de los datos"""
    data_str    = bytes(data_bytes).decode('utf-8')

    return data_str, device

"""codigo para testing"""
if __name__ == '__main__':

    """trama corta"""
    # ejemplo de datos
    data    = 'short'
    device  = 0x00

    print('dato        : ', data    )
    print('dispositivo : ', device  )

    # llamado a la función de codificación
    frame   = encoder(data, device)
    print('trama de datos : \n', frame)

    # llamado a la función de decodificación
    data_d  = decoder(frame)
    print('datos decodificados : ', data_d)


    """trama larga"""
    """trama corta"""
    # ejemplo de datos
    data    = 'long: ejemplo de trama larga'
    device  = 0x00
    
    print('dato        : ', data    )
    print('dispositivo : ', device  )
    
    # llamado a la función
    frame   = encoder(data, device)
    print('trama de datos : \n', frame)

    # llamado a la función de decodificación
    data_d  = decoder(frame)
    print('datos decodificados : ', data_d)
