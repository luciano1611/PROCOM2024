import numpy as np
#################################
#Funciones para producto punto:
#Entre vectores de dimensión "n" 
#y matrices de dimensión "nxn"
#################################

#Sub-menu para operación con matrices:
def SubMenu():
    print("* Elija una opción.")
    print("Desea realizar el producto punto entre: ")
    print("1) Vectores.")
    print("2) Matrices.")

    #Bucle infinito
    while True:
        Sel = input("Opción: ")

        #Evalúa el ingreso del usuario
        if Sel in ['1', '2']:
            return Sel  #Sale del bucle y de la función
        
        #Si no es valido
        else:           #Repite el bucle
            print("Error, elija una opción valida.")

#Función para ingresar el contenido del vector o matriz.
def InputMatrix(n = 1, Sel = '0'):
    #Por defecto
    if Sel == 'Error, especifique el tamaño del array':
        return 0
    
    #Para vector
    elif Sel == '1': 

        Matrix = np.zeros(n)
        
        #Itera en i de 0 a n, donde n es el tamaño del vector
        for i in range(n): 
            
            #Evalúa si las entradas del usuario
            while True:    
                try:
                    Matrix[i] = float(input(f"Elemento {i+1}: "))
                    break   #Sale del while
                except ValueError:
                    print("Error, ingrese un número real.")
    
    #Para matriz
    elif Sel == '2':

        Matrix = np.zeros((n,n))

        #Itera en "i" de "0" a "n"
        for i in range(n):
            #Itera en "j" de "0" a "n"
            for j in range(n):

                #Evalúa si las entradas del usuario
                while True:    
                    try:
                        Matrix[i,j] = float(input(f"Elemento {i+1}, {j+1}: "))
                        break   #Sale del while
                    except ValueError:
                        print("Error, ingrese un número real.")
    
    #Devuelve la matriz
    return Matrix

#Función que realiza el producto punto
def MatrixDot():

    Sel = SubMenu()

    if Sel == '1':
        Array = 'el vector'
    elif Sel == '2':
        Array = 'la matriz'

    #Evalúa el tamaño ingresado del array 
    while True:
        try:
            n = int(input(f"Ingrese el tamaño de {Array}: "))
            break
        except ValueError:
            print("Error, ingrese un número valido.")
    
    #Crea los arrays:
    if Sel == '1':
        Arr1 = np.zeros(n)
        Arr2 = np.zeros(n)  
    
    elif Sel == '2':
        Arr1 = np.zeros((n,n))
        Arr2 = np.zeros((n,n))


    #Ingresa el array 1:
    print(f"Ingrese {Array} 1")
    Arr1 = InputMatrix(n, Sel)
    print(f"{Array} 2 ingresado es: \n", Arr1)

    #Ingresa el array 1:
    print(f"Ingrese {Array} 2")
    Arr2 = InputMatrix(n, Sel)
    print(f"{Array} 2 ingresado es: \n", Arr2)

    #Realiza el producto punto y lo muestra en pantalla:
    Result = np.dot(Arr1, Arr2)
    print("El producto punto es: \n", Result)
    