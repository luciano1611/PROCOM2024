def recepcion(sig_in):
    # size_sigin=len(sig_in)
    # sig_outrx = np.zeros(size_sigin//os)
    # offset_rx=(int)(0.5NbaudsTbaud) #Cantidad de muestras de offset
    # #offset_rx=10

    # for i in range(len(sig_in/os)):
    #     if((osi+offset_rx)<len(sig_in)):
    #         sig_outrx[i]=sig_in[osi+offset_rx]
    #         #if(sig_outrx[i]>0):
    #         #    sig_outrx[i]=1
    #         #else: sig_outrx[i]=-1

    size_sigin  =   len(sig_in)
    size_outrx  =   (int)(size_sigin/os)
    sig_outrx   =   np.zeros(size_outrx)  # Inicializar con el tamaño reducido (saltando cada os)
    offset_rx   =   (int)(0.5NbaudsTbaud)+2 #Cantidad de muestras de offset

    for i in range(len(sig_outrx)):
        # Asegurarse de que no se exceda el tamaño de sig_in
        idx = os * i + offset_rx
        if idx < len(sig_in):
            sig_outrx[i] = sig_in[idx]
            if(sig_outrx[i]>0):
                    sig_outrx[i]    =   1
            else:   sig_outrx[i]    =   -1
        else:
            break  # Detener si el índice excede el tamaño de sig_in

    return sig_outrx