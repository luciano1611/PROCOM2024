#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

# Parametros generales
freq    = 100e6         # Frecuencia 
T       = 1.0 / freq    # Periodo de baudio
n_symb  = 1000          # Número de símbolos
os      = 4             # Oversampling

# Parametros de la respuesta en frecuencia
n_freq  = 256           # Cantidad de frecuencias

# Parametros del filtro de caida cosenoidal
beta    = 0.5           # Roll-Off (solo un valor)
n_baud  = 8             # Cantidad de baudios del filtro

# Frecuencia de muestreo
Ts      = T / os

# Valores de PRBS
seed_I  = 0b110101010   # I = 9'0xh1AA
seed_Q  = 0b111111110   # Q = 9'0xh1FE

# Para debug
plot    = True


#********** Muestra los valores por pantalla **************#
print( "*********************************")
print(f"Valor de frecuencia     : {freq     }Hz")
print(f"Valor de Roll-Off       : {beta     }")
print(f"Numero de baudios       : {n_baud   }")
print(f"NUmero de simbolos      : {n_symb   }")
print(f"Oversampling            : {os       }")
print(f"Numero de frecuencias   : {n_freq   }")


############################################################
#**************** Respuesta al Impulso ********************#
### [1]: Funcion de calculo de respuesta al impulso
def rcosine(beta, T, oversampling, n_baud, norm=False):

    # definicion del vector de tiempo
    start   = -0.5 * n_baud * T                     # inicio
    stop    =  0.5 * n_baud * T                     # fin 
    step    = float(T) / oversampling               # paso
    t_vec   = np.arange(start, stop, step)          # definicion del 't_vec'

    # definicion de la respuesta al impulso en cada 't'
    y_vec   = []                                    # declaracion
    for t in t_vec:
        
        sinc    = np.sinc(t/T)                      # termino sinc
        cos     = np.cos(np.pi*beta*t/T)            # termino cosenoidal
        den     = 1 - (4.0*beta*beta*t*t/(T*T))     # denominador
        y_vec.append(sinc*(cos/den))                # respuesta al impulso en 't'

    # conversion de lista a np.array
    y_vec   = np.array(y_vec)

    # normalizacion si se lo indica
    if norm is True:
        return t_vec, (y_vec / sum(y_vec))
    else:
        return t_vec, y_vec      

### [2]: Funcion de ploteo de respuesta al impulso
def plot_rcosine(t, rc, beta, os, n_bauds, show_plot=True):

    # Gráfica del pulso
    plt.figure(figsize=[14, 7])
    plt.plot(t, rc, 'gs-', linewidth=2.0, label=r'Pulso $\beta={}$'.format(beta))
    plt.legend()
    plt.grid(True)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    # Convolución del pulso con bits
    symb        = np.zeros(int(os) * 3 + 1)
    symb[os : len(symb) - 1 : int(os)] = 1.0
    rcSymb      = np.convolve(rc, symb)

    offsetPot   = os * ((n_bauds // 2) - 1) + int(os / 2) * (n_bauds % 2) + 0.5 * (os % 2 and n_bauds % 2)

    # Gráfica de la convolución
    plt.figure(figsize=[14, 7])
    plt.plot(np.arange(0, len(rc)), rc, 'r.-', linewidth=2.0, label=r'Pulso $\beta={}$'.format(beta))
    plt.plot(np.arange(os, len(rc) + os), rc, 'k.-', linewidth=2.0, label=r'Pulso $\beta={}$'.format(beta))
    plt.stem(np.arange(offsetPot, len(symb) + offsetPot), symb, label='Bits')
    plt.plot(rcSymb[os::], '--', linewidth=3.0, label='Convolución')
    plt.legend()
    plt.grid(True)
    plt.ylim(-0.2, 1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.title('Rcosine - OS: %d' % int(os))

    if show_plot is True:
        plt.show()
    
# Llamada a la funcion de calculo de respuesta al impulso
t, rc   = rcosine(beta, T, os, n_baud, norm=False)

# Llamada a la función de ploteo
if plot: 
    plot_rcosine(t, rc, beta, os, n_baud, show_plot=True)


############################################################
#**************** Respuesta en Frecuencia *****************#
### [3]: Funcion de calculo de respuesta en frecuencia
def freq_resp(y_vec, Ts, n_freq):

    H       = []  # lista para valores de magnitud
    A       = []  # lista para valores de fase
    y_len   = len(y_vec)

    # Genero el vector de frecuencias
    f_vec = np.matrix(np.linspace(0, 1.0 / (2.0 * Ts), n_freq))
    
    # Calculo cuantas muestras necesito para 20 ciclos de la frecuencia más baja (diferente de cero)
    low_seq = 20.0 / (f_vec[0, 1] * Ts)

    # Genero el vector de tiempo
    t_vec = np.matrix(np.arange(0, low_seq)) * Ts

    # Genero la matriz de 2πfTn
    Omega = 2.0j * np.pi * (t_vec.transpose() * f_vec)

    # Evaluación de la exponencial compleja en todo el rango de frecuencias
    fin = np.exp(Omega)

    # Suma de convolución con cada una de las exponenciales complejas
    for i in range(0, np.size(fin, 1)):
        exp     = np.squeeze(np.array(fin[:, i].transpose()))   # Extraigo la exponencial compleja para la frecuencia 'i' y la convierto en array
        fout    = np.convolve(exp, y_vec)                       # Convolución entre la exponencial compleja y el filtro FIR
        m_fout  = abs(fout[y_len:len(fout) - y_len])            # Extraigo la parte "steady state" de la magnitud
        a_fout  = np.angle(fout[y_len:len(fout) - y_len])       # Extraigo la parte "steady state" de la fase
        H.append(m_fout.sum() / len(m_fout))                    # Almaceno la magnitud promedio para la frecuencia 'i'
        A.append(a_fout.sum() / len(a_fout))                    # Almaceno la fase promedio para la frecuencia 'i'

    # Devuelvo los valores de magnitud, fase y el vector de frecuencias
    return H, A, list(np.squeeze(np.array(f_vec)))

### [4]: Funcion de ploteo de respuesta en frecuencia
def plot_resp_freq(F, H, beta, Ts):

    plt.figure(figsize=[14, 6])
    plt.semilogx(F, 20 * np.log10(H), 'r', linewidth=2.0, label=r'$\beta={}$'.format(beta))
    
    # Línea vertical en la frecuencia de Nyquist (1 / (2 * Ts))
    plt.axvline(x=(1. / Ts) / 2., color='k', linewidth=2.0)
    
    # Línea horizontal en -6 dB (representa 0.5 en escala lineal)
    plt.axhline(y=20 * np.log10(0.5), color='k', linewidth=2.0)
    
    # Configuración del gráfico
    plt.legend(loc=3)
    plt.grid(True, which="both", ls="--")
    plt.xlim(F[1], F[-1])  # Ajuste del rango de frecuencias
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.title(f'Respuesta en frecuencia para $\\beta={beta}$')
    plt.show()

# Cálculo de la respuesta en frecuencia para un solo pulso
H, A, F = freq_resp(rc, Ts, n_freq)

# Llamada a la función de ploteo
if plot: 
    plot_resp_freq(F, H, beta=0.5, Ts=Ts)


############################################################
#************* Calculo de simbolos por PRBS ***************#
### [5]: Funcion de calculo de PRBS
def prbs9(seed=0b111100001, length=20):

    # Conversion de los bits a una lista
    sh_reg  = [int(bit) for bit in bin(seed)[2:].zfill(9)]

    # Lista de PRBS
    prbs    = []

    # Bucle para generar la prbs, a base del shift register
    for i in range(length):

        # añade un bit a la PRBS
        prbs.append(sh_reg[0])             # sh_reg[-1] es el bit 9 (ultimo de la lista sh_reg)

        # calculo de XOR y corrimiento
        xor     = sh_reg[8]  ^ sh_reg[4]
        sh_reg  = sh_reg[1:] + [xor]     # Realiza un corrimeinto a la izquierda

    return prbs

# Bits de I y Q de la PRBS0
prbs_I      = prbs9(seed=seed_I, length=n_symb)
prbs_Q      = prbs9(seed=seed_Q, length=n_symb)

#print(prbs_I)
#print(prbs_Q)

# Conversion de bits 1:0 a simbolos -1:1
symb_I_Tx   = [1 if symb == 0 else -1 for symb in prbs_I]   # La señal Tx (symb a transmitir) es la entrada del filtro
symb_Q_Tx   = [1 if symb == 0 else -1 for symb in prbs_Q]   #            

# Aplicacion de Up-Sampling (zeros)
zsymb_I     = np.zeros(os * n_symb)                         # Genera un vector de zeros de tamaño n_symb
zsymb_I[1 : len(zsymb_I) : int(os)] = symb_I_Tx             # Combina el vector con los simbolos de la prbs cada OS=4 espacios

zsymb_Q     = np.zeros(os * n_symb)                         # Genera un vector de zeros de tamaño n_symb
zsymb_Q[1 : len(zsymb_Q) : int(os)] = symb_Q_Tx             # Combina el vector con los simbolos de la prbs cada OS=4 espacios


### [6]: Funcion de plot de symb en I y Q
def plot_symbols(symbolsI, symbolsQ, label='Símbolos'):

    plt.figure(figsize=[14, 6])

    # Histograma para los símbolos del canal I
    plt.subplot(1, 2, 1)
    plt.hist(symbolsI, bins=20, color='blue', edgecolor='black', label=label)
    plt.legend()
    plt.xlabel('Símbolos - Canal I')
    plt.ylabel('Repeticiones')
    plt.title('Distribución de Símbolos en I')

    # Histograma para los símbolos del canal Q
    plt.subplot(1, 2, 2)
    plt.hist(symbolsQ, bins=20, color='red', edgecolor='black', label=label)
    plt.legend()
    plt.xlabel('Símbolos - Canal Q')
    plt.ylabel('Repeticiones')
    plt.title('Distribución de Símbolos en Q')

    plt.tight_layout()  # Ajusta el diseño para evitar solapamiento de gráficos
    plt.show()

### [7]: Funcion de plot de zsymb
def plot_symbols_sequence(zsymb_I, zsymb_Q, xlim=(0, 20)):
    plt.figure(figsize=[10, 6])

    # Gráfico para la secuencia de símbolos en el canal I
    plt.subplot(2, 1, 1)
    plt.stem(zsymb_I, linefmt='b-', markerfmt='bo', basefmt='k')  # Línea azul con puntos azules
    plt.xlim(xlim)
    plt.grid(True)
    plt.xlabel('Muestras')
    plt.ylabel('Símbolos - Canal I')
    plt.title('Secuencia de Símbolos en I')

    # Gráfico para la secuencia de símbolos en el canal Q
    plt.subplot(2, 1, 2)
    plt.stem(zsymb_Q, linefmt='r-', markerfmt='ro', basefmt='k')  # Línea verde con puntos verdes
    plt.xlim(xlim)
    plt.grid(True)
    plt.xlabel('Muestras')
    plt.ylabel('Símbolos - Canal Q')
    plt.title('Secuencia de Símbolos en Q')

    plt.tight_layout()  # Ajuste de diseño para evitar solapamiento
    plt.show()

### Llamada a la función de ploteo
if plot:
    plot_symbols(symb_I_Tx, symb_Q_Tx, label='Símbolos: %d' % n_symb)
    plot_symbols_sequence(zsymb_I, zsymb_Q, xlim=(0,250))


############################################################
#******** Convolucion de los Symb. con el Filtro **********#
### Convolucion de los simbolos luego de Up-Sampling con la funcion de tranferencia del filtro
symb_I_out  = np.convolve(rc, zsymb_I, 'same')              # Señal discreta (valore flotantes)
symb_Q_out  = np.convolve(rc, zsymb_Q, 'same')              # La señal symb__out es la salida del filtro


### [8]: Funcion de plot de los symb de salida del filtro
def plot_downsampled_signals(symb_out_I, symb_out_Q, beta, xlim=(0, 250)):
    plt.figure(figsize=[10, 6])

    # Gráfico para la señal I
    plt.subplot(2, 1, 1)
    plt.stem(symb_out_I, linefmt='r-', markerfmt='ro', basefmt=' ', label=r'$\beta=%2.2f$' % beta)
    plt.xlim(xlim)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.title('Canal I después de Downsampling')

    # Gráfico para la señal Q
    plt.subplot(2, 1, 2)
    plt.stem(symb_out_Q, linefmt='b-', markerfmt='bo', basefmt=' ', label=r'$\beta=%2.2f$' % beta)
    plt.xlim(xlim)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.title('Canal Q después de Downsampling')

    plt.tight_layout()  # Ajuste para evitar solapamientos
    plt.show()


### Llamada a la función de ploteo
if plot:
    plot_downsampled_signals(symb_I_out, symb_Q_out, beta, xlim=(0, 250))


###########################################################
#****************** Diagrama del Ojo *********************#
### [9]: Funcion de plot de diagrama de ojo
def eye_diagram(data, n, offset, period):
    span     = 2*n
    segments = int(len(data)/span)
    xmax     = (n-1)*period
    xmin     = -(n-1)*period
    x        = list(np.arange(-n,n,)*period)
    xoff     = offset

    plt.figure()
    for i in range(0,segments-1):
        plt.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')       
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.show()

# Llamada a la funcion de ploteo en I y Q
if plot:
    eye_diagram(symb_I_out[100 : len(symb_I_out)-100 ], os, 4, n_baud)
    eye_diagram(symb_Q_out[100 : len(symb_Q_out)-100 ], os, 4, n_baud)


###########################################################
#************** Diagrama del Constelacion ****************#
### [10]: Funcion de plot de diagrama de constelacion
def plot_constellation(data_I, data_Q, os, beta, offset=6):

    plt.figure(figsize=[6,6])
    
    # Graficar las señales recortadas con el desplazamiento y sobremuestreo
    plt.plot(data_I[100+offset:len(data_I)-(100-offset):int(os)],
             data_Q[100+offset:len(data_Q)-(100-offset):int(os)],
             '.', linewidth=2.0)
    
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    plt.title(f'Diagrama de Constelación - Roll-Off {beta}')
    plt.show()

# Offset obtenido en forma empirica del grafico de diagrama de ojo
offset = 16

# Llamada a la funcion de ploteo en I y Q
if plot: 
    plot_constellation(symb_I_out, symb_Q_out, os, beta, offset=6)


###########################################################
#******************Systema de Recepcion*******************#
### [11]: Funcion de recepcion de datos
### Extrae los datos de la salida del filtro
def rx_system(data, os, n_baud, T, offset):

    # Calculo de tamaño de señal de salida
    out_len     = int(len(data) / os)

    # Inicializacion de array de salida
    out_data    = np.zeros(out_len)

    # Offset de muestas
    offset      = int(0.5 * n_baud * T) + offset

    for i in range(out_len):
        # Inidice para recorrer las muestras de entrada (data)
        idx     = os * i + offset

        if idx < (out_len * os):
            out_data[i] = data[idx]                             # Extraccion de valores por Down-Sampling
            out_data[i] = -1 if(out_data[i] <= 0.0) else 1      # Conversion a symbolos -1:1

        else:
            break

    return out_data

# Offset obtenido en forma empirica
offset      = 2
# Obtencion de las tramas receptadas
symb_I_Rx   = rx_system(symb_I_out, os, n_baud, T, offset)
symb_Q_Rx   = rx_system(symb_Q_out, os, n_baud, T, offset)

#plot_symbols_sequence(symb_I_Tx, symb_I_Rx, xlim=(0,1000))

###########################################################
#*********************Bit Error Rate**********************#

def bit_error_rate(data_Tx, data_Rx):
    
    # Verificar si las listas tienen el mismo tamaño
    if len(data_Tx) != len(data_Rx):
        raise ValueError("Las listas deben tener el mismo tamaño.")

    # Contar el numero de errores
    error   = 0
    for i in range(len(data_Tx)):
        # Por cada bit distinto
        if data_Tx[i] != data_Rx[i]:
            # Incrementa el contador de error
            error = error + 1
    
    # Calcular la Bit Error Rate (BER)
    ber = (error / len(data_Tx)) * 100  # Convertir a porcentaje

    return ber


ber_I   = bit_error_rate(symb_I_Rx, symb_I_Tx)
ber_Q   = bit_error_rate(symb_Q_Rx, symb_Q_Tx)

print( "*********************************")
print(f"Bit Error Rate en I: {ber_I}%")
print(f"Bit Error Rate en Q: {ber_Q}%")
print( "*********************************")