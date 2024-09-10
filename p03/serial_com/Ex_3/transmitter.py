# librerías
import time
import serial

# funciones
from encoder import encoder
from decoder import decoder

# [1]: función auxiliar
def message():
    """comunicación con el usuario"""
    print('Menu de opciones: \n')
    print('Calculadora : Ejecuta el script de calculadora.')
    print('Graficar    : Ejecuta el script de gráficos.')
    print('exit        : Para salir del programa.')

    # ingreso de opción del usuario <se valida en el receptor>
    data = input('Ingrese una opción >> ')

    # retorna el valor 
    return data

# [2]: función principal 
def client_Tx(ser):  # recibe como parámetro un objeto de tipo "serial"
    """función de transmisión de datos"""
    # llama a la función de comunicación con el usuario
    data = message()
    # como se trabaja con un puerto virtual
    device = 0x01

    # opción de salir del programa sin enviar ningún mensaje al receptor
    if data == 'exit':
        if ser.isOpen():
            ser.close()
        return True  # para salir del bucle del main

    # codificación de los datos
    frame = encoder(data, device)

    # se envía cada byte de 'frame'
    for byte in frame:
        ser.write(byte.to_bytes(1, byteorder='big'))

    return False

# [3]: función principal >> recepción de datos del puerto serie (enviados por el server)
def client_Rx(ser):  # recibe como parámetro un objeto de tipo "serial"
    """función de recepción de datos"""
    # recibe la trama por un vector con N celdas de 1 byte
    frame = []

    while ser.inWaiting() > 0:
        # cada byte (formato big-endian) se convierte en un entero y se concatena en 'frame'
        frame.append(int.from_bytes(ser.read(1), byteorder='big'))

    # una vez obtenida el vector, se lo decodifica extrayendo los datos
    data, device = decoder(frame)

    # se retornan los valores decodificados (strings)
    return data, device

"""código para testing"""
if __name__ == '__main__':
    # crea un objeto de tipo 'serial'
    # se usa 'loop://' para crear un puerto serial virtual en modo "loopback" (para no usar hardware físico)
    ser = serial.serial_for_url('loop://', timeout=1)

    # configuración del puerto serial:
    if ser.isOpen():
        ser.timeout = None  # config. sin tiempo de espera
        ser.flushInput()    # limpia los buffers de entrada
        ser.flushOutput()   # limpia los buffers de salida

        # comunicación con el usuario    
        print('____Comunicación por puerto serie virtual____\n')
        print('Ingrese "exit" para salir y presione Enter\n\n')

        while True:
            exit = client_Tx(ser)
            if exit:
                break

            # Llama a la función de recepción de datos
            data, device = client_Rx(ser)
            print(f'Datos recibidos: {data}, Dispositivo: {device}')

            # limpia los buffer
            ser.flushInput()
            ser.flushOutput()

        # Cerrar el puerto después de salir del bucle
        ser.close()
    else:
        print('Error: No se pudo abrir el puerto serial.')
