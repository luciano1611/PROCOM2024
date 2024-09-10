# librerías
import time
import serial


# [1]: función de comunicación con el usuario
def message():
	# mensajes para el usuario
	print('Menu de opciones: \n')
	print('1 : Ejecuta el script de calculadora.')
	print('2 : Ejecuta el script de gráficos.')
	print('3 : Para salir del programa.')

	# ingreso de opción del usuario <se valida en el receptor>
	data = input('Ingrese una opción >> ')

	# retorna el valor 
	return data


# [2]: función principal >> envio de datos por el puerto serie
def client_Tx(ser):		# recibe como parámetro un objeto de tipo "serial"
	# llama a la función de comunicación con el usuario
	data = message()

	# opción de salir del programa sin enviar ningún mensaje al receptor
	if data == '3':
		if ser.isOpen():
			ser.close()
		return True						# para salir del bucle del main

	# si no: se transmiten los datos
	else:
		# Tx: envio de datos al "server" <receptor>
		ser.write(data.encode())		# transmite los datos ingresados al puerto serie
		print('client >> Tx : ', data)	# imprime en patalea los datos enviados por el puerto serie
		return False					# retorna False para volver a iterar en el bucle


# [3]: función principal >> recepción de datos del puerto serie (enviados por el server)
def client_Rx(ser): 	# recibe como parámetro un objeto de tipo "serial"
	
	# Rx: recibe datos del "server" <receptor>
	rx_data = ''

	while ser.inWaiting() > 0:
		rx 		= ser.read(1)			# dato recibido
		rx_data	+= rx.decode()			# concatenación

	# si se recibio algun dato del servido
	if rx_data != '': 
		print('client >> Rx : ', rx_data)


# código para testing
if __name__ == '__main__':

	# crea un objeto de tipo 'serial'
	# se usa 'loop://' para crear un puerto serial virtual en modo "loopback" (para no usar hardware físico)
	ser = serial.serial_for_url('loop://', timeout=1) 

	# configuaración del puerto serial:
	ser.isOpen()        # verifica si el puerto está abierto
	ser.timeout = None  # config. sin tiempo de espera
	ser.flushInput()    # limpia los buffers de entrada
	ser.flushOutput()   # limpia los buffers de salida
	
	# comunicación con el usuario	
	print('____Comunicación por puerto serie virtual____\n'	)
	print('Ingrese "exit" para salir y presione Enter\n\n'	)

	while True:

		exit = client(ser)

		if exit is True:
			break

		# limpia los buffer
	    #ser.flushInput()
	    #ser.flushOutput()