import numpy as np
#import matplotlib.pyplot as plt
from tool._fixedInt import *

### funcion de grafica
from plot import *


### [1]: funcion de calculo de respuesta al impulso
def rcosine(beta, Tbaud, oversampling, Nbauds, Norm=False):
    """ Respuesta al impulso del pulso de caida cosenoidal """
    t_vect = np.arange(-0.5*Nbauds*Tbaud, 0.5*Nbauds*Tbaud, 
                       float(Tbaud)/oversampling)

    y_vect = []
    for t in t_vect:
        y_vect.append(np.sinc(t/Tbaud)*(np.cos(np.pi*beta*t/Tbaud)/
                                        (1-(4.0*beta*beta*t*t/
                                            (Tbaud*Tbaud)))))

    y_vect = np.array(y_vect)

    if(Norm):
        return (t_vect, y_vect/np.sqrt(np.sum(y_vect**2)))
        #return (t_vect, y_vect/y_vect.sum())
    else:
        return (t_vect,y_vect)


### [2]: funcion de calculo de respuesta en frecuencia
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




def eye_diagram(rc, offset, n_symb):

    # simbolos de I y Q
    symb_I  = 2 * (np.random.uniform(-1, 1, n_symb) > 0.0) -1
    symb_Q  = 2 * (np.random.uniform(-1, 1, n_symb) > 0.0) -1

    # zeros para muestreo
    zsymb_I = np.zeros(os * n_symb)
    zsymb_I[1:len(zsymb_I):int(os)] = symb_I
    
    zsymb_Q = np.zeros(os * n_symb)
    zsymb_Q[1:len(zsymb_Q):int(os)] = symb_Q

    # convolucion del filtro con los simbolos
    conv_I  = np.convolve(rc, zsymb_I, 'same')
    conv_Q  = np.convolve(rc, zsymb_Q, 'same')

    # datos para trasa de diagrama de ojo
    data_I  = conv_I[100 : len(conv_I)-100]
    data_Q  = conv_Q[100 : len(conv_Q)-100]

    return data_I, data_Q
    


### para testing
if __name__ == '__main__':

    ### variables globales
    beta    = 0.5           # Roll-Off
    freq    = 100.0e6         # frecuencia de 100MHz
    T       = 1 / freq      # periodo en baudios
    n_symb  = 1000          # numero de simbolos
    n_baud  = 6             # numero de baudios
    n_freq  = 256           # numero de freq
    os      = 4             # oversampling
    norm    = True          # normalizacion
    Ts      = T / os        # tasa de muestreo
    offset  = 9             # offset para diagrama de ojo


    ### respuesta al impulso
    t, rc   = rcosine(beta, T, os, n_baud, norm)

    ### trasa de la respuesta al impulso
    plot_rcosine(t, rc, beta)

    ### respuesta en frecuencia
    H, A, f = freq_resp(rc, Ts, n_freq)

    ### trasa de la respuesta en frecuencia
    plot_freqresp(f, H, A, beta)

    ### diagrama de ojo
    data_I, data_Q = eye_diagram(rc, offset, n_symb)

    ### trasa de diagrama de ojo
    plot_eye(data_I, os, offset, T)
    plot_eye(data_Q, os, offset, T)

    ### trasa diagrama de constelacion
    plot_constellation(data_I, data_Q, os, beta, offset)
