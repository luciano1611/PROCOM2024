# librerias
import time		
import serial	# para manejo de puerto serie
# funciones externas
from transmitter	import client_Tx
from transmitter	import client_Rx
from receiver		import server


# objeto de tipo serial 
ser = serial.serial_for_url('loop://', timeout=1)	# se usa 'loop://' para puerto serie virtual

# objeto de tipo serial: comunicación física
# crear: ser_tx para el transmisor
# crear: ser_rx para el receptor

# ejemplo:
# ser = serial.Serial(
#     port     = '/dev/ttyUSB1',      #Configurar con el puerto
#     baudrate = 9600,
#     parity   = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )

# configuración del puerto serie:
ser.isOpen()		# verifica si el puerto está abierto
ser.timeout = None	# config. sin tiempo de espera
ser.flushInput()	# limpia los buffers de entrada
ser.flushOutput()	# limpia los buffers de salida

# comunicación con el usuario
print('#### TP3: Operaciones con el puerto UART ####')
print('#### Ejercicio N°1 ####\n')

# bucle principal
while True:

	# Cliente: transmisión de datos
	exit = client_Tx(ser)

	# si el cliente devuelve True <exit == True> 
	if exit is True:
		break 	# se sale del bucle sin enviar datos por el puerto serie

	# Servidor: Recepción de datos enviados del cliente y Transmisión de respuesta <correcto / incorrecto>
	server(ser)

	# Cliente: Recepción de respuesta enviados del Servidor
	client_Rx(ser)
