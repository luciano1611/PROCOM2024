import numpy as np
import matplotlib.pyplot as plt

from functions import *


### [1]: funcion de ploteo de respuesta al impulso de caida cosenoidal
def plot_rcosine(t, rc, beta):

    plt.figure(figsize=[14,7])
    plt.plot(t, rc, 'ro-', linewidth=2.0, label=f'$\\beta={beta}$')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Magnitud')
    plt.title(f'Respuesta al impulso Raised Cosine - $\\beta={beta}$')
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



### [5]: funcion de ploteo de symbolos transmitidos
def plot_symb(zsymb_I, zsymb_Q):
    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.title('Simbolos a Transmitir completados con ceros')
    plt.plot(zsymb_I,'o')
    plt.xlim(0,20)
    plt.grid(True)
    plt.subplot(2,1,2)
    plt.plot(zsymb_Q,'o')
    plt.xlim(0,20)
    plt.grid(True)
    plt.show()



def plot_symb_out(symb_I, symb_Q, beta):
    
    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.title('Salida del filtro transmisor')
    plt.plot(symb_I, 'r-', linewidth=2.0, label=r'$\beta=%2.2f$'%beta)
    plt.xlim(0,20)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras en I')
    plt.ylabel('Magnitud')

    plt.subplot(2,1,2)
    plt.plot(symb_Q, 'r-', linewidth=2.0, label=r'$\beta=%2.2f$'%beta)
    plt.xlim(0,20)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras en Q')
    plt.ylabel('Magnitud')

    plt.show()
#symb_out0I = np.convolve(rc0,zsymbI,'same'); symb_out0Q = np.convolve(rc0,zsymbQ,'same')
#symb_out1I = np.convolve(rc1,zsymbI,'same'); symb_out1Q = np.convolve(rc1,zsymbQ,'same')
#symb_out2I = np.convolve(rc2,zsymbI,'same'); symb_out2Q = np.convolve(rc2,zsymbQ,'same')
#
#plt.figure(figsize=[10,6])
#plt.subplot(2,1,1)
#plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
#plt.plot(symb_out1I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
#plt.plot(symb_out2I,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
#plt.xlim(1000,1250)
#plt.grid(True)
#plt.legend()
#plt.xlabel('Muestras')
#plt.ylabel('Magnitud')
#
#plt.subplot(2,1,2)
#plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
#plt.plot(symb_out1Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
#plt.plot(symb_out2Q,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
#plt.xlim(1000,1250)
#plt.grid(True)
#plt.legend()
#plt.xlabel('Muestras')
#plt.ylabel('Magnitud')
#
#plt.figure(figsize=[10,6])
#plt.plot(np.correlate(symbolsI,2*(symb_out0I[3:len(symb_out0I):int(os)]>0.0)-1,'same'))
#
#plt.show()