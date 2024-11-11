from plot           import *
from functions      import *
from functions2     import *


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


    ### GENERACION DE SIMBOLOS
    ### generacion de los simbolos en I y Q con la PRBS9
    symb_I      = prbs9(seed=0b110101010, length=n_symb, QPSK=True)
    symb_Q      = prbs9(seed=0b111111110, length=n_symb, QPSK=True)

    # zeros para muestreo: upsampling
    zsymb_I     = upsample(symb_I, os, n_symb)
    zsymb_Q     = upsample(symb_Q, os, n_symb)

    # convolucion de los simbolos con la funcion de transferencia del filtro
    conv_I      = np.convolve(rc, zsymb_I, 'same')
    conv_Q      = np.convolve(rc, zsymb_Q, 'same')

    # datos para trasa de diagrama de ojo
    data_I      = conv_I[100:len(conv_I)-100]
    data_Q      = conv_Q[100:len(conv_I)-100]

    # extrae los simbolos de la salida del filtro: downsampling
    o_symb_I    = downsample(conv_I, os)
    o_symb_Q    = downsample(conv_Q, os)


    ### DIAGRAMA DEL OJO

    ### trasa de diagrama de ojo
    plot_eye(data_I, os, offset, T)
    plot_eye(data_Q, os, offset, T)


    ### DIAGRAMA DE CONSTELACION
    ### trasa diagrama de constelacion
    offset = 1  # ajuste de offset
    plot_constellation(data_I, data_Q, os, beta, offset)


    ### SIBOLOS TRANSMITIDOS
    plot_symb(zsymb_I, zsymb_Q)
    plot_symb_out(symb_I, symb_Q, beta)

    ### BIT ERROR RATE:
    ### calculo de ber

    out_I   = downsample(zsymb_I, os)
    out_Q   = downsample(zsymb_Q, os)

    ber_I   = bit_error_rate(symb_I, out_I)
    ber_Q   = bit_error_rate(symb_Q, out_Q)

    print("Bit Error Rate en I: ", ber_I)
    print("Bit Error Rate en Q: ", ber_Q)