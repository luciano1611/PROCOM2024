Trabajo Práctico N°3: Operaciones con el Puerto UART - Python


**Objetivo:**
Utilizar la librería pyserial para enviar y recibir datos a través del puerto UART.

# Parte A:
Tomando como referencia los scripts `Python_UART.py` y `Python_UART_vector.py`, se 
deben enviar tres comandos por el puerto y, del lado del receptor, ejecutar alguna 
de las siguientes tareas:

- `1`: Ejecuta el script de la calculadora.
- `2`: Ejecuta el script de gráficos.
- `exit`: Termina el programa sin enviar ningún mensaje por el puerto serie.

En caso de introducir un comando incorrecto, se debe volver a pedir al usuario que 
ingrese alguna de las opciones válidas.


*** Desarrollo ***
Los códigos necesarios para esta consigna se encuentran en la carpeta `Ex_1`, que 
contiene los archivos `main.py`, `transmitter.py` y `receiver.py`, junto con las 
carpetas de los TP1 y TP2. El sistema se basa en una comunicación entre un cliente 
(transmitter) y un servidor (receiver). El cliente envía por el puerto serie los 
datos ingresados por la terminal, y el servidor los evalúa y devuelve una respuesta 
de mensaje correcto o incorrecto. Si el mensaje es correcto (evaluado en el receptor), 
se ejecutan los scripts de los TP1 y TP2.


# Parte B:
Utilizando el mismo criterio de diseño anterior, se reemplazan los comandos `1` y `2` 
por las palabras "Calculadora" y "Graficar". Por lo tanto, el receptor debe verificar 
la correcta recepción de los comandos mencionados.

- `Calculadora`: Ejecuta el script de la calculadora.
- `Graficar`: Ejecuta el script de gráficos.
- `exit`: Verifica la recepción y termina el script.

En caso de introducir un comando incorrecto, se debe volver a pedir al usuario que ingrese 
alguna de las opciones válidas.

*** Desarrollo ***
El desarrollo realiza la misma función que en el ejercicio A, solo que en este caso se 
envían cadenas de caracteres para realizar la evaluación en el receptor.


# Parte C:
Utilizando el esquema de trama detallado en la página 8 de las filminas, enviaremos el 
comando dentro del campo data, donde cada carácter será un byte de información. Es decir, 
la longitud de cada comando es "Calculadora" (11), "Graficar" (8) y "exit" (4).

- En el transmisor (TX), armamos la trama colocando el valor [0x00] en los campos `L.SIZE(HIGH)`, 
`L.SIZE(LOW)` y `DEVICE`, y completando el resto con los valores correspondientes.

- En el receptor (RX), desarmamos la trama, verificamos que sea correcta y ejecutamos el comando.

En caso de introducir un comando incorrecto, se debe volver a pedir al usuario que ingrese 
alguna de las opciones válidas.

### Detalles Técnicos:
Se busca sustituir las funciones `.encode()` y `.decode()` de pyserial por funciones propias 
llamadas `encoder()` y `decoder()` a las que se les envía los datos en formato string y devuelve 
una lista con los elementos de la trama a enviar en formato byte (cada celda contiene 1 byte).

- La función `encoder()` recibe una trama de datos (en formato string), la convierte a una lista 
de bytes y añade los campos `START_BIT`, `LS`, `S_SHORT`, `L_SIZE_HIGH`, `L_SIZE_LOW` y `STOP_BIT` 
detallados en el esquema de trama de las filminas. El campo de ID de dispositivo no se usa en la 
comunicación, por lo que en el código se le asigna un valor fijo.
  - `LS` determina si la trama es larga (LONG) o corta (SHORT). Si es corta (menor a 10 bytes), se 
    define su tamaño con el campo `s_size` (4 bits), sino se define el tamaño con `l_size_high` (8 bits) 
    y `l_size_low` (8 bits).
  
  - Los datos se concatenan en una variable llamada `frame`, que luego se convierte en una lista `
    frame_list` para realizar la comunicación según el script `Python_UART_vector.py`.

- En el receptor, se evalúa la trama:
  1. Se evalúan los campos de `START_BIT` y `STOP_BIT`. Si son incorrectos, se retorna un mensaje de error.

  2. Se verifica que los datos en los 4 bits menos significativos del primer byte y último byte de la trama 
    sean iguales (sistema de verificación). Si no lo son, se retorna un mensaje de error.

  3. Si los datos de la trama son válidos, se extraen los datos según el tamaño especificado por los campos 
    mencionados, se convierten de una lista de bytes a una string y se retornan al receptor.

El receptor evalúa los datos recibidos del `decoder()`, envía una respuesta al cliente (usando el mismo 
sistema de codificación `encoder()`) y, en caso de ser válida la opción del usuario, ejecuta los scripts 
del TP1 y TP2. El cliente decodifica los datos tal como lo hace el servidor y los imprime en pantalla.
