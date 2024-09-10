#!/usr/bin/env python
# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

# funciones de archivos
from rcosine        import rcosine
from freq_response  import resp_freq
from eye_diagram    import eyediagram
# funciones agregadas
from quantum        import quantum


'''parametros globales'''
# generales
freq    = 1e9               # frecuencia en baudios
T       = 1.0 / freq        # periodo en baudios
Nsymb   = 1000              # numero de simbolos
os      = 4#8                 # over-sampling

# para rcosine
beta    = [0.0, 0.5, 0.99]  # roll-off
Nbauds  = 8                 # cantidad de baudios

# para freq. response
Nfreqs  = 256               # cantidad de frecuencias 

# funcionales
Ts      = T / os            # periodo de muestro


# codigo de ejecucion
if __name__ == '__main__':
    #########################################################
    #########################################################
    #########################################################
    ### Calculo de tres pusos con diferente roll-off
    (t,rc0) = rcosine(beta[0], T,os,Nbauds,Norm=False)
    (t,rc1) = rcosine(beta[1], T,os,Nbauds,Norm=False)
    (t,rc2) = rcosine(beta[2], T,os,Nbauds,Norm=False)

    print (np.sum(rc0**2),np.sum(rc1**2),np.sum(rc2**2))

    rc0     = quantum(rc0, s=(8, 6), op='trunc')
    rc1     = quantum(rc1, s=(8, 6), op='trunc')
    rc2     = quantum(rc2, s=(8, 6), op='trunc')

    ### Generacion de las graficas
    plt.figure(figsize=[14,7])
    plt.plot(t,rc0,'ro-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.plot(t,rc1,'gs-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.plot(t,rc2,'k^-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,len(rc0)-1)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    symb00    = np.zeros(int(os)*3+1);symb00[os:len(symb00)-1:int(os)] = 1.0
    rc0Symb00 = np.convolve(rc0,symb00);
    rc1Symb00 = np.convolve(rc1,symb00);
    rc2Symb00 = np.convolve(rc2,symb00);

    offsetPot = os*((Nbauds//2)-1) + int(os/2)*(Nbauds%2) + 0.5*(os%2 and Nbauds%2)

    plt.figure(figsize=[14,7])
    plt.subplot(3,1,1)
    plt.plot(np.arange(0,len(rc0)),rc0,'r.-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.plot(np.arange(os,len(rc0)+os),rc0,'k.-',linewidth=2.0,label=r'$\beta=0.0$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')#,use_line_collection=True)
    plt.plot(rc0Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    plt.title('Rcosine - OS: %d'%int(os))

    #plt.figure()
    plt.subplot(3,1,2)
    plt.plot(np.arange(0,len(rc1)),rc1,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.plot(np.arange(os,len(rc1)+os),rc1,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')#,use_line_collection=True)
    plt.plot(rc1Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    #plt.title('Rcosine - OS: %d'%int(os))

    #plt.figure()
    plt.subplot(3,1,3)
    plt.plot(np.arange(0,len(rc2)),rc2,'r.-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.plot(np.arange(os,len(rc2)+os),rc2,'k.-',linewidth=2.0,label=r'$\beta=1.0$')
    plt.stem(np.arange(offsetPot,len(symb00)+offsetPot),symb00,label='Bits')#,use_line_collection=True)
    plt.plot(rc2Symb00[os::],'--',linewidth=3.0,label='Convolution')
    plt.legend()
    plt.grid(True)
    #plt.xlim(0,35)
    plt.ylim(-0.2,1.4)
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')
    #plt.title('Rcosine - OS: %d'%int(os))

    plt.show()


    

    #########################################################
    #########################################################
    #########################################################

    ### Calculo respuesta en frec para los tres pulsos
    [H0,A0,F0] = resp_freq(rc0, Ts, Nfreqs)
    [H1,A1,F1] = resp_freq(rc1, Ts, Nfreqs)
    [H2,A2,F2] = resp_freq(rc2, Ts, Nfreqs)

    ### Generacion de los graficos
    plt.figure(figsize=[14,6])
    plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.0$')
    plt.semilogx(F1, 20*np.log10(H1),'g', linewidth=2.0, label=r'$\beta=0.5$')
    plt.semilogx(F2, 20*np.log10(H2),'k', linewidth=2.0, label=r'$\beta=1.0$')

    plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
    plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
    plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
    plt.legend(loc=3)
    plt.grid(True)
    plt.xlim(F2[1],F2[len(F2)-1])
    plt.xlabel('Frequencia [Hz]')
    plt.ylabel('Magnitud [dB]')
    plt.show()


    # In[6]:


    symbolsI = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;
    symbolsQ = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1;

    label = 'Simbolos: %d' % Nsymb
    plt.figure(figsize=[14,6])
    plt.subplot(1,2,1)
    plt.hist(symbolsI,label=label)
    plt.legend()
    plt.xlabel('Simbolos')
    plt.ylabel('Repeticiones')
    plt.subplot(1,2,2)
    plt.hist(symbolsQ,label=label)
    plt.legend()
    plt.xlabel('Simbolos')
    plt.ylabel('Repeticiones')

    plt.show()


    # In[7]:


    zsymbI = np.zeros(os*Nsymb); zsymbI[1:len(zsymbI):int(os)]=symbolsI
    zsymbQ = np.zeros(os*Nsymb); zsymbQ[1:len(zsymbQ):int(os)]=symbolsQ

    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.plot(zsymbI,'o')
    plt.xlim(0,20)
    plt.grid(True)
    plt.subplot(2,1,2)
    plt.plot(zsymbQ,'o')
    plt.xlim(0,20)
    plt.grid(True)

    plt.show()


    symb_out0I = np.convolve(rc0,zsymbI,'same'); symb_out0Q = np.convolve(rc0,zsymbQ,'same')
    symb_out1I = np.convolve(rc1,zsymbI,'same'); symb_out1Q = np.convolve(rc1,zsymbQ,'same')
    symb_out2I = np.convolve(rc2,zsymbI,'same'); symb_out2Q = np.convolve(rc2,zsymbQ,'same')

    plt.figure(figsize=[10,6])
    plt.subplot(2,1,1)
    plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(symb_out1I,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(symb_out2I,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    plt.subplot(2,1,2)
    plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[0])
    plt.plot(symb_out1Q,'g-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[1])
    plt.plot(symb_out2Q,'k-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta[2])
    plt.xlim(1000,1250)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Muestras')
    plt.ylabel('Magnitud')

    #plt.figure(figsize=[10,6])
    #plt.plot(np.correlate(symbolsI,2*(symb_out0I[3:len(symb_out0I):int(os)]>0.0)-1,'same'))

    plt.show()


    #########################################################
    #########################################################
    #########################################################





    eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds)
    eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)

    eyediagram(symb_out1I[100:len(symb_out1I)-100],os,5,Nbauds)
    eyediagram(symb_out1Q[100:len(symb_out1Q)-100],os,5,Nbauds)

    eyediagram(symb_out2I[100:len(symb_out2I)-100],os,5,Nbauds)
    eyediagram(symb_out2Q[100:len(symb_out2Q)-100],os,5,Nbauds)

    plt.show()

    #########################################################
    #########################################################
    #########################################################

    offset = int(os / 2)
    plt.figure(figsize=[6,6])
    plt.plot(symb_out0I[100+offset:len(symb_out0I)-(100-offset):int(os)],
            symb_out0Q[100+offset:len(symb_out0Q)-(100-offset):int(os)],
                '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')

    plt.figure(figsize=[6,6])
    plt.plot(symb_out1I[100+offset:len(symb_out1I)-(100-offset):int(os)],
            symb_out1Q[100+offset:len(symb_out1Q)-(100-offset):int(os)],
                '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')

    plt.figure(figsize=[6,6])
    plt.plot(symb_out2I[100+offset:len(symb_out2I)-(100-offset):int(os)],
            symb_out2Q[100+offset:len(symb_out2Q)-(100-offset):int(os)],
                '.',linewidth=2.0)
    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.grid(True)
    plt.xlabel('Real')
    plt.ylabel('Imag')

    plt.show()


# In[ ]:


