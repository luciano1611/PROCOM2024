import numpy as np
from tool._fixedInt import *


### [1]: Funcion de calculo de respuesta al impulso
def rcosine(beta, T, oversampling, n_baud, norm = False):

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
    

### [2]: Funcion de calculo de respuesta en frecuencia
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


### [3]: Funcion para calculo de diagrama de ojo
def eye_diagram(rc, os, symb_I, symb_Q, n_symb):

    ### Version 1: sin prbs usando funcion random de numpy
    # simbolos de I y Q
    #symb_I  = 2 * (np.random.uniform(-1, 1, n_symb) > 0.0) -1
    #symb_Q  = 2 * (np.random.uniform(-1, 1, n_symb) > 0.0) -1
 

    # zeros para muestreo
    zsymb_I = np.zeros(os * n_symb)
    zsymb_I[1:len(zsymb_I):int(os)] = symb_I
    
    zsymb_Q = np.zeros(os * n_symb)
    zsymb_Q[1:len(zsymb_Q):int(os)] = symb_Q

    # convolucion del filtro con los simbolos
    conv_I  = np.convolve(rc, zsymb_I, 'same')
    conv_Q  = np.convolve(rc, zsymb_Q, 'same')

    # datos para trasa de diagrama de ojo
    #data_I  = conv_I[100 : len(conv_I)-100]
    #data_Q  = conv_Q[100 : len(conv_Q)-100]

    data_I  = conv_I[100:100 + n_symb]
    data_Q  = conv_Q[100:100 + n_symb]

    return np.array(data_I), np.array(data_Q)




