import numpy as np
from tool._fixedInt import *

### [3]: funcion de calculo de respuesta en frecuencia al filtro FIR
def freq_resp(filter, Ts, n_freq):

    M = []  # lista de salida de la magnitud
    P = []  # lista de salida de la fase

    # vector de frecuencias
    freq_vec    = np.matrix(np.linspace(0, 1.0 / (2.0 * Ts), n_freq))

    # calculo de la frecuencia minima: necesaria para 20 cilcos
    low_seq     = 20.0 / (freq_vec[0, 1]*Ts)

    # vector de muestras de tiempo de 2pi f Tn
    t_vec       = np.matrix(np.arange(0, low_seq))*Ts

    # matriz de 2pi f Tn
    omega       = 2.0j*np.pi*(t_vec.transpose()*freq_vec)

    # valuacion de la exp. cmplx. en todo el rango de freq
    fin         = np.exp(omega)

    # suma de convolucion con cada una de las exp. cmplx. 
    for i in range(0, np.size(fin, 1)):

        col_i   = np.squeeze(np.array(fin[:,i].transpose()))                #         
        f_out   = np.convolve(col_i, filter)                                # 
        m_out   = abs       (f_out[len(filter) : len(f_out) - len(filter)]) # 
        p_out   = np.angle  (f_out[len(filter) : len(f_out) - len(filter)]) # 

        M.append(m_out.sum() / len(m_out))                                  # 
        P.append(p_out.sum() / len(p_out))                                  # 

    F    = list(np.squeeze(np.array(freq_vec)))

    # retorna modulo, fase y frecuencia
    return M, P, F
