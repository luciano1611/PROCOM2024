from plot       import *
from functions   import *


### variables globales ###
# parametros del enunciado
beta    = 0.5           # Roll-Off
freq    = 100.0e6       # frecuencia de 100MHz
T       = 1 / freq      # periodo en baudios
n_baud  = 6             # numero de baudios
os      = 4             # oversampling
# parametros elegidos
n_freq  = 256           # numero de freq
n_symb  = 1000          # numero de simbolos
offset  = 4             # offset para diagrama de ojo
Ts      = T / os        # tasa de muestreo
norm    = False         # normalizacion


if __name__ == '__main__':

    ### RESPUESTA AL IMPULSO
    # calculo de respuesta al impulso con caida cosenoidal
    t, rc   = rcosine(beta, T, os, n_baud, norm = False)
    # trasa de respuesta la impulso
    plot_rcosine(t, rc, beta)


    ### RESPUESTA EN FRECUENCIA
    ### calculo de respuesta en frecuencia: devuelve la magnitud M, fase P y vector de frecuncias
    M, P, f = freq_resp(rc, Ts, n_freq)

    ### trasa de la respuesta en frecuencia
    plot_freqresp(f, M, P, beta)


    ### DIAGRAMA DEL OJO
    ### diagrama de ojo
    data_I, data_Q = eye_diagram(rc, offset, n_symb)

    ### trasa de diagrama de ojo
    plot_eye(data_I, os, offset, T)
    plot_eye(data_Q, os, offset, T)


    ### DIAGRAMA DE CONSTELACION
    ### trasa diagrama de constelacion
    offset = 1  # ajuste de offset
    plot_constellation(data_I, data_Q, os, beta, offset)
