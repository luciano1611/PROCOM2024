import numpy as np
import matplotlib.pyplot as plt



### [1]: funcion de ploteo de respuesta al impulso de caida cosenoidal
def plot_rcosine(t, rc, beta):
   
    plt.figure(figsize=[14,7])
    plt.plot(t,rc,'ro-',linewidth=2.0,label=f'$beta={beta}$')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.show()



### [2]: funcion de ploteo de respuesta en frecuencia
def plot_freqresp(freq, M, A, beta):

    dB      = 20 * np.log10(M)
    phase   = A 
    #ph  = A  * (180 / np.pi)   # corregir ?? A no es float 

    # Magnitud en decibelios (dB)
    plt.subplot(2, 1, 1)  # Subgráfico 1: Magnitud
    plt.semilogx(freq, dB, 'r', linewidth=2.0, label=f'Magnitud (beta={beta})')
    plt.legend(loc='best')
    plt.grid(True)
    plt.ylim(-100, 50)
    plt.xlim(freq[0], freq[-1])
    plt.ylabel('Magnitud [dB]')
    plt.title('Respuesta en Frecuencia - Magnitud y Fase')

    # Fase en grados
    plt.subplot(2, 1, 2)  # Subgráfico 2: Fase
    plt.semilogx(freq, phase, 'b', linewidth=2.0, label=f'Fase (beta={beta})')
    plt.legend(loc='best')
    plt.grid(True)
    plt.xlim(freq[0], freq[-1])
    plt.xlabel('Frecuencia [Hz]')
    plt.ylabel('Fase [grados]')

    plt.tight_layout()
    plt.show()



### [3]: funcion de ploteo de diagrama del ojo
def plot_eye(data, n, offset, T):
    
    # variables auxiliares 
    span     = 2 * n                        # span
    segments = int(len(data) / span)        # cantidad de segmentos de span que se pueden extraer de data
    xmax     =  (n-1) * T                   # limite superior en x
    xmin     = -(n-1) * T                   # limite inferior en x
    x        = list(np.arange(-n,n,) * T)   # valores del eje x (lista de -n a n por T)
    xoff     = offset                       # offser para el despalzamiento de la signal

    # ploteo
    plt.figure()
    for i in range(0,segments-1):
        plt.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')       
    plt.grid(True)
    plt.xlim(xmin, xmax)
    plt.show()



### [4]: funcion de ploteo de diagrama de constelacion
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
