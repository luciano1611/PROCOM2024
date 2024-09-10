import struct

def encoder(data_in, device_id):
    """obtención de datos"""
    # convierte la cadena en bytes
    data        = data_in.encode('utf-8')

    # obtiene la cantidad de bytes de 'data'
    data_len    = len(data)

    # si la trama es LONG
    if data_len > (15 - 5):
        start_bit   = 0b1011 & 0x0F             # 101 con LS = 1
        stop_bit    = 0b0101 & 0x0F             # 010 con LS = 1
        s_size      = 0x00                      # no se usa en tramas LONG
        l_size_high = (data_len >> 8) & 0xFF    # toma los 8 bits mas significativos y los trunca con & 0xFF
        l_size_low  = data_len & 0xFF           # toma los 8 bits menos significativos y los trunca con & 0xFF

    # si la trama es SHORT
    else:
        start_bit   = 0b1010 & 0xFF             # 101 con LS = 0
        stop_bit    = 0b0100 & 0xFF             # 010 con LS = 0
        s_size      = data_len & 0xFF           # toma el tamaño de la trama y la trunca en 8 bits con 0xFF
        l_size_high = 0x00                      # no se usa en tramas SHORT
        l_size_low  = 0x00                      # no se usa en tramas SHORT

    # convierte la cadena en bytes: y trunca el valor con 0xFF
    device  = struct.pack('B', device_id) 

    """armado de la trama"""
    # inicio de trama
    header = struct.pack('B', (start_bit << 4) | s_size)
    # fin de trama
    footer = struct.pack('B', (stop_bit << 4 ) | s_size)
    # trama
    frame   = (
        header                          +   # start bit + LS + s_size
        struct.pack('B', l_size_high)   +   # l_size_high
        struct.pack('B', l_size_low)    +   # l_size_low
        device                          +   # device_ide
        data                            +   # data
        footer                              # stop bit + LS + s_size
        )

    #######################33
    # debug
    #print('ls       : ', start_bit  )
    #print('s_size   : ', s_size     )
    #print('l_size_h : ', l_size_high)
    #print('l_size_l : ', l_size_low )
    #######################


    # convierte la trama en una lista para transmitirla como vector
    frame_list = list(frame)

    # retrona la lista
    return frame_list

"""codigo para testing"""
if __name__ == '__main__':

    """trama corta"""
    # ejemplo de datos
    data    = 'short'
    device  = 0x00

    print('dato        : ', data    )
    print('dispositivo : ', device  )

    # llamado a la función
    frame   = encoder(data, device)

    print('trama de datos : \n', frame)


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



#start_bit   = 0b1011
#s_size      = 0x00
#
#header1  = start_bit << 4 | struct.pack('B', s_size)
#
#s_size   = data_len & 0xFF
#header2  = start_bit << 4 | struct.pack('B', s_size)