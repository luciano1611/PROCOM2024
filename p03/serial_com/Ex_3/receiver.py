# librerías
import time
import serial 

# instanciación de los tp 1 y 2
from tp1.main     import menuCalculator 
from tp2.graficar import graficar

# importar las funciones de encoder y decoder
from encoder import encoder
from decoder import decoder

# [1]: llamada a las funciones de los tp 1 y 2
def call_func(op):

    # según la elección recibida del cliente
    if op == 'Calculadora':
        menuCalculator()  # llama a la función principal del tp 1
    
    elif op == 'Graficar':
        graficar()  # llama a la función principal del tp 2


# [2]: función de validación de datos recibidos
def validate_data(data):
    
    # según el valor de data se asigna una string a 'val'
    if data in ['Calculadora', 'Graficar']:
        val = 'correcto'  # respuesta al cliente
    else:
        val = 'incorrecto'  # respuesta al cliente
    
    return val  # retorna la respuesta


# [3]: función principal 
def server(ser):  # recibe como parámetro un objeto "serial"
    
    """recepción de datos"""
    frame = []

    while ser.inWaiting() > 0:
        # cada byte se convierte en un entero y se concatena en 'frame'
        frame.append(int.from_bytes(ser.read(1), byteorder='big'))

    # si se recibió algún dato del cliente
    if frame:
        try:
            # decodificación de los datos
            decoded_data = decoder(frame)
            # imprime la decodificación para depuración
            print('Decoded Data:', decoded_data)  

            # Verifica el tamaño de `decoded_data` antes de desempacar
            if len(decoded_data) != 2:
                print("Error: Decoded data has incorrect length")
                return

            data, device    = decoded_data
            print('server >> Rx : ', data)  # imprime el dato recibido del cliente en pantalla


            """envía una respuesta al cliente"""
            tx_data         = validate_data(data)  # recibe mensaje a enviar "correcto" o "incorrecto"
            
            # codificación de los datos
            frame_to_send   = encoder(tx_data, device)
            
            # transmisión
            for byte in frame_to_send:
                ser.write(byte.to_bytes(1, byteorder='big'))
            
            print('server >> Tx : ', tx_data)  # imprime el mensaje transmitido en pantalla

            # si el dato recibido es una opción válida
            if tx_data == 'correcto':
                call_func(data)  # llama a la función de los tp 1 y/o 2
        
        except Exception as e:
            print("Error during decoding or processing:", str(e))


# código para testing
if __name__ == '__main__':
    # crea un objeto de tipo 'serial'
    # se usa 'loop://' para crear un puerto serial virtual en modo "loopback" (para no usar hardware físico)
    ser = serial.serial_for_url('loop://', timeout=1) 
    
    # configuración del puerto serial:
    ser.isOpen()        # verifica si el puerto está abierto
    ser.timeout = None  # config. sin tiempo de espera
    ser.flushInput()    # limpia los buffers de entrada
    ser.flushOutput()   # limpia los buffers de salida

    # comunicación con el usuario:
    print('____Comunicación por puerto serie virtual____\n')
    print('Ingrese "exit" para salir y presione Enter\n\n')

    while True:
        data = input("Ingrese datos a enviar (escriba 'exit' para salir): ")
        
        # si se ingresa "exit" sale del programa
        if data == 'exit':
            if ser.isOpen():
                ser.close()
            break
        
        # si no:
        else:
            # Tx: codifica los datos y envíalos por el puerto serie
            frame = encoder(data, 0x01)
            for byte in frame:
                ser.write(byte.to_bytes(1, byteorder='big'))

            # Rx: recepción de datos del lado del server
            server(ser)

            # limpia los buffer
            # ser.flushInput()
            # ser.flushOutput()
