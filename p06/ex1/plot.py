import numpy as np
import matplotlib.pyplot as plt


def plot_rcosine(t, rc, beta):
   
    plt.figure(figsize=[14,7])
    plt.plot(t,rc,'ro-',linewidth=2.0,label=f'$beta={beta}$')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.show()


def plot_freqresp(f, M, A, beta):

    dB  = 20 * np.log10(M)
    ph  = A  * (180 / np.pi)

    plt.figure(figsize=[14,6])
    plt.semilogx(f, dB, 'r', linewidth = 2.0, label = f'beta={beta}')
    plt.semilogx(f, ph, 'b', linewidth = 2.0, label = f'beta={beta}')
    plt.legend(loc=3)
    plt.grid(True)
    plt.ylim(-100, 50)
    plt.xlim(F[2][1],F[2][len(F[2])-1])
    plt.xlabel('Frequencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.title('Respuesta en Frecuencia')
    plt.show()


