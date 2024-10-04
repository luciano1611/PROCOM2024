import numpy as np
#import matplotlib.pyplot as plt
from tool._fixedInt import *

### funcion de grafica
from plot import *


### [1]: funcion de calculo de respuesta al impulso
def rcosine(beta, T, oversampling, n_baud, norm = False):

    t_start = -(n_baud / 2) * T                           # inicio de vector de tiempo
    t_stop  =  (n_baud / 2) * T                           # fin de vector de tiempo
    t_step  = float(T)  / oversampling                     # paso del vector

    # generacion del vector
    t_vec   = np.arange(t_start, t_stop, t_step)

    y_vec = []
    for t in t_vec:
        sinc    = np.sinc(t / T)                           # termino sinc
        cos     = np.cos(np.pi * beta * t / T)             # termino cosenoidal
        den     = 1 - (4.0 * beta**2 * t**2 / (T ** 2))    # denominador
        y_vec.append(sinc * (cos / den))

    # respuesta al impulso
    y_vec   = np.array(y_vec)

    # normalizacion si se lo indica
    if norm is True:
        return t_vec, (y_vec / sum(y_vec))
    else:
        return t_vec, y_vec


### [2]: funcion de calculo de respuesta en frecuencia
def freq_resp(y_vec, Ts, n_freq):

    H       = []            # lista para valores de magnitud
    A       = []            # lista para valores de fase
    y_len   = len(y_vec)

    # calculo de vector de frecuencias
    start   = 0
    stop    = 1.0 / (2.0 * Ts)
    step    = n_freq
    f_vec   = np.matrix(np.linspace(start, stop, step))
    
    # calculo de la freq. mas baja
    low_seq = 20.0 / (f_vec[0, 1] * Ts)

    # calculo del vector de tiempo
    t_vec   = np.matrix(np.arange(0, low_seq)) * Ts

    # calculo de la matriz de 2 pi fTn
    w_vec   = 2.0j * np.pi * (t.transpose() * y_vec)

    # valuacion de la exp. compx. en todo el rango de freq
    fin     = np.exp(w_vec)

    # sumatoria de convolucion con cada una de la exp. compx. 
    for i in range(0, np.size(fin, 1)):
        exp     = np.squeeze(np.array(fin[:,i].transpose()))    # Extrae la exponencial compleja para la frecuencia 'i' y la convierte en un array adecuado
        fout    = np.convolve(exp, y_vec)                       # Realiza la convolución entre la exponencial compleja y el filtro FIR
        m_fout  = abs       (fout [y_len:len(fout) - y_len])    # Extrae la parte "steady state" de la magnitud (omitiendo transitorios iniciales y finales)
        a_fout  = np.angle  (fout [y_len:len(fout) - y_len])    # Extrae la parte "steady state" de la fase (omitiendo transitorios iniciales y finales)
        H.append(m_fout.sum() / len(m_fout))                    # Calcula y almacena la magnitud promedio para la frecuencia 'i'
        A.append(a_fout.sum() / len(a_fout))                    # Calcula y almacena la fase promedio para la frecuencia 'i'

    f_vec   = list(np.squeeze(np.array(f_vec)))

    return H, A, f_vec


### para testing
if __name__ == '__main__':

    ### variables globales
    beta    = 0.5           # Roll-Off
    freq    = 100e6         # frecuencia de 100MHz
    T       = 1 / freq      # periodo en baudios
    n_baud  = 8             # numero de baudios
    n_freq  = 256           # numero de freq
    os      = 8             # oversampling
    norm    = True          # normalizacion
    Ts      = T / os        # tasa de muestreo


    ### respuesta al impulso
    t, rc   = rcosine(beta, T, os, n_baud, norm)

    ### trasa de la respuesta al impulso
    plot_rcosine(t, rc, beta)

    ### frespuesta en frecuencia
    H, A, f = freq_resp(rc, Ts, n_freq)

    ### trasa de la respuesta en frecuencia
    plot_freqresp(f, H, A, beta)