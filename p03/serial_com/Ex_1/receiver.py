# librerías
import time
import serial 

# instanciación de los tp 1 y 2
from tp1.main		import menuCalculator 
from tp2.graficar  	import graficar


# [1]: llamada a las funciones de los tp 1 y 2
def call_func(op):

	# según la elección recibida del cliente
	if   op == '1':
		menuCalculator()					# llama a la función principal del tp 1

	elif op == '2':
		graficar()							# llama a la función principal del tp 2


# [2]: función de validación de datos recibidos
def validate_data(data):

	# según el valor de data se asigna una string a 'val'
	if data in ['1', '2']:
		val = 'correcto'					# respuesta al cliente
	
	else:
		val = 'incorrecto'					# respuesta al cliente

	return val 	# retorna la respuesta


# [3]: función principal 
def server(ser):	# recibe como parámetro un objeto "serial"

	# Rx: recepción de datos
	data = ''
	while ser.inWaiting() > 0:
		rx 		= ser.read(1)				# dato recibido
		data 	+= rx.decode()				# concatenación

	# si se recibe algún dato del cliente
	if data != '':
		# recepción:
		print('server >> Rx : ', data)		# imprime el dato recibido del cliente en pantalla
		tx_data = validate_data(data)		# recibe mensaje a enviar "correcto" o "incorrecto"
		
		# transmisión:
		ser.write(tx_data.encode())			# envía el mensaje por el puerto serie al cliente
		print('server >> Tx : ', tx_data)	# imprime el mensaje transmitido en pantalla

		# si el dato recibido es una opción valida
		if tx_data == 'correcto':
			call_func(data)					# llama a la funciones de los tp 1 y/o 2


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
	print('____Comunicación por puerto serie virtual____\n'	)
	print('Ingrese "exit" para salir y presione Enter\n\n'	)


	while True:
	    data = input("Ingrese datos a enviar (escriba 'exit' para salir): ")
	    
	    # si se ingresa "exit" sale del programa
	    if data == 'exit':
	        if ser.isOpen():
	            ser.close()
	        break
	    
	    # si no:
	    else:
	    	# Tx: envía datos por el puerto serie del lado del cliente
        	ser.write(data.encode())        

        	# Rx: recepción de datos del lado del server
	        server(ser)

	        # limpia los buffer
	        #ser.flushInput()
	        #ser.flushOutput()
