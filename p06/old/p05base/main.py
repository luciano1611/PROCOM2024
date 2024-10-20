import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

### FUNCIONES
from rcosine        import rcosine
from freq_response  import freq_resp
from eye_diagram    import eyediagram
from quantum        import quantum


### PARAMETROS GLOBALES ###
# parametros generales: 
freq    = 100e6                   # frecuencia de 1GBaud
T       = 1 / freq              # periodo en baudios
n_symb  = 1000                  # numero de simbolos
os      = 8                     # oversampling

# parametros del filtro 
beta    = [0.0, 0.5, 0.99]      # roll-off
n_baud  = 8                    # numero de baudios

# parametros de la respuesta en frecuencia
n_freq  = 256                   # cantidad de frecuencias

# parametros funcionales:
Ts      = T / os                # periodo de muestreo


if __name__ == '__main__':

    # definciones
    idx     = 0
    rc      = [0,0,0]
    rc_symb = [0,0,0]
    A       = [0,0,0]
    P       = [0,0,0]
    F       = [0,0,0]
    conv_I  = [0,0,0]
    conv_Q  = [0,0,0]

    ### RESPUESTA AL IMPULSO ###
    # calculo de 3 pulsos con distinto roll-off
    t, rc0  = rcosine(beta[0], T, os, n_baud, norm = False)  # 0.0
    t, rc1  = rcosine(beta[1], T, os, n_baud, norm = False)  # 0.5
    t, rc2  = rcosine(beta[2], T, os, n_baud, norm = False)  # 0.99

    s       = (3, 2)
    op      = 'trunc'
    Norm    = True

    ### CUANTIFICACION ###
    rc0     = quantum(rc0, s, op)
    if Norm is True:
        rc0 = rc0/sum(rc0)

    rc1     = quantum(rc1, s, op)
    if Norm is True:
        rc1 = rc1/sum(rc1)
    
    rc2     = quantum(rc2, s, op)
    if Norm is True:
        rc2 = rc2/sum(rc2)

    rc      = (rc0, rc1, rc2)

    idx     = 0
    for i in rc:
        print(f'Roll-Off = {beta[idx]} : {np.sum(rc[idx]**2)}')
        idx = idx + 1

    # graficas: de rcosine:
    plt.figure(figsize=[14,7])
    plt.plot(t,rc[0],'ro-',linewidth=2.0,label=f'$beta={beta[0]}$')
    plt.plot(t,rc[1],'gs-',linewidth=2.0,label=f'$beta={beta[1]}$')
    plt.plot(t,rc[2],'k^-',linewidth=2.0,label=f'$beta={beta[2]}$')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,len(rc0)-1)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.show()

    # simbolos para convolucion:
    symb        = np.zeros(int(os)*3 + 1)
    symb[os:len(symb)-1:int(os)]   = 1.0

    # convoluciona cada filtro con los simbolos
    rc_symb[0]  = np.convolve(rc[0], symb)
    rc_symb[1]  = np.convolve(rc[1], symb)
    rc_symb[2]  = np.convolve(rc[2], symb)
    # calculo de offset

    offset_pot  = os*(n_baud//2 -1) + int(os/2)*(n_baud%2) + 0.5*(os%2 and n_baud%2)
    
    # graficas de convolucion de los 3 filtros 
    for i in range(3):
        plt.subplot(3, 1, i + 1)
        plt.plot(np.arange(0, len(rc[i])), rc[i], 'r.-', linewidth=2.0, label=f'beta={beta[i]}')
        plt.plot(np.arange(os, len(rc[i]) + os), rc[i], 'k.-', linewidth=2.0, label=f'beta={beta[i]}')
        plt.stem(np.arange(offset_pot, len(symb) + offset_pot), symb, label='Bits')  #,use_line_collection=True
        plt.plot(rc_symb[i][os::], '--', linewidth=3.0, label='Convolution')
        plt.legend()
        plt.grid(True)
        #plt.xlim(0,35)
        #plt.ylim(-0.2, 1.4)    # recortaba el grafico
        plt.xlabel('Muestras')
        plt.ylabel('Magnitud')
        if i == 0:  # Solo poner el título en la primera gráfica
            plt.title('Rcosine - OS: %d' % int(os))

    plt.show()

    ### RESPUESTA EN FRECUENCIA ###
    A[0], P[0], F[0] = freq_resp(rc[0], Ts, n_freq)
    A[1], P[1], F[1] = freq_resp(rc[1], Ts, n_freq)
    A[2], P[2], F[2] = freq_resp(rc[2], Ts, n_freq)

    plt.figure(figsize=[14,6])
    plt.semilogx(F[0], 20*np.log10(A[0]),'r', linewidth=2.0, label=f'beta={beta[0]}')
    plt.semilogx(F[1], 20*np.log10(A[1]),'g', linewidth=2.0, label=f'beta={beta[1]}')
    plt.semilogx(F[2], 20*np.log10(A[2]),'k', linewidth=2.0, label=f'beta={beta[2]}')

    #plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
    #plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
    #plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
    plt.legend(loc=3)
    plt.grid(True)
    plt.ylim(-100, 50)
    plt.xlim(F[2][1],F[2][len(F[2])-1])
    plt.xlabel('Frequencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.title('Respuesta en Frecuencia')
    plt.show()

    ### COMPONENTES I Y Q ###
    symb_I  = 2*(np.random.uniform(-1, 1, n_symb) > 0.0) -1
    symb_Q  = 2*(np.random.uniform(-1, 1, n_symb) > 0.0) -1

    label   = 'Simbolos: %d' %n_symb
    print(label)
    plt.figure(figsize=[14,6])
    plt.subplot(1,2,1)
    plt.hist(symb_I,label=label)
    plt.legend()
    plt.xlabel('Simbolos')
    plt.ylabel('Repeticiones')
    plt.title('In-phase')
    plt.subplot(1,2,2)
    plt.hist(symb_Q,label=label)
    plt.legend()
    plt.xlabel('Simbolos')
    plt.ylabel('Repeticiones')
    plt.title('Quadrature')
    plt.show()

    ### SIMBOLOS ###
    zsymb_I = np.zeros(os*n_symb)
    zsymb_I[1:len(zsymb_I):int(os)] = symb_I
    
    zsymb_Q = np.zeros(os*n_symb)
    zsymb_Q[1:len(zsymb_Q):int(os)] = symb_Q

    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.plot(zsymb_I,'o')
    plt.xlim(0,20)
    plt.grid(True)
    plt.title('Secuencia de Símbolos de I')
    plt.subplot(2,1,2)
    plt.plot(zsymb_Q,'o')
    plt.xlim(0,20)
    plt.grid(True)
    plt.title('Secuencia de Símbolos de Q')
    plt.show()

    ### CONVOLUCION DE LOS FILTROS CON SIMBOLOS I & Q
    conv_I[0] = np.convolve(rc[0], zsymb_I, 'same')
    conv_Q[0] = np.convolve(rc[0], zsymb_Q, 'same')
    
    conv_I[1] = np.convolve(rc[1], zsymb_I, 'same')
    conv_Q[1] = np.convolve(rc[1], zsymb_Q, 'same')
    
    conv_I[2] = np.convolve(rc[2], zsymb_I, 'same')
    conv_Q[2] = np.convolve(rc[2], zsymb_Q, 'same')

    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.plot(conv_I[0],'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(conv_I[1],'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(conv_I[2],'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.title('Convolucion de los filtros con los simbolos I & Q')

    plt.subplot(2,1,2)
    plt.plot(conv_Q[0],'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(conv_Q[1],'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(conv_Q[2],'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    
    plt.show()

    ### DIAGRAMA DE OJO ###

    eyediagram(conv_I[0][100:len(conv_I[0])-100],os,5,n_baud)
    eyediagram(conv_Q[0][100:len(conv_Q[0])-100],os,5,n_baud)
    
    eyediagram(conv_I[1][100:len(conv_I[1])-100],os,5,n_baud)
    eyediagram(conv_Q[1][100:len(conv_Q[1])-100],os,5,n_baud)
    
    eyediagram(conv_I[2][100:len(conv_I[2])-100],os,5,n_baud)
    eyediagram(conv_Q[2][100:len(conv_Q[2])-100],os,5,n_baud)

    plt.show()

    ### DIAGRAMA DE CONSTELACION ###
    offset = 6

    for i in range(3):
        plt.figure(figsize=[6,6])
        plt.plot(conv_I[i][100+offset:len(conv_I[i])-(100-offset):int(os)],
                 conv_Q[i][100+offset:len(conv_Q[i])-(100-offset):int(os)],
                 '.', linewidth=2.0)
        plt.xlim((-2, 2))
        plt.ylim((-2, 2))
        plt.grid(True)
        plt.xlabel('Real')
        plt.ylabel('Imag')
        plt.title(f'Diagrama de Constelación - Roll-Off {beta[i]}')
    plt.show()


