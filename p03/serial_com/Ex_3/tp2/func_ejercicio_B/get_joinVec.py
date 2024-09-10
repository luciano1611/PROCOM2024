from .get_joinVec_aux_func import getMatrix
from .get_joinVec_aux_func import validPos
from .get_joinVec_aux_func import validTuple

# *Funciones de ingreso de 'joinVec' * #

#[1]: función para validar la opción del usuario
def getOption(matrix, count):  

    #Evalúa el ingreso:
    while True:
        # menu de opciones:
        print("\nIngrese: ")
        print(f"1- Para plotear el gráfico {count} en única celda.")
        print(f"2- Para plotear el gráfico {count} en mas de una celda.")
    
        # se lo lee como una string
        op = input("Opción: ")

        # si la opción ingresada es valida
        if op in ['1', '2']:
            # sale del bucle
            break

        # si la opción no es valida, reitera en el bucle
        print("Error, ingrese una opción valida.")
        print("Lugares disponibles de la matriz: \n", matrix)
    
    # fin del while
    # devuelve la opción validada
    return op

#[2]: función para validar el ingreso de una única posición del sub-plot en la figura
def getSinglePos(matrix):
    # bucle para validar la opción ingresada
    while True:
        # valida que el ingreso del usuario sea un entero
        try:
            pos = int(input("Ingrese una posición dentro del rango = "))

        # si no es un entero
        except ValueError:
            # resetea el valor de pos
            pos = 0
            # imprime mensaje de error
            print("Error, ingrese un número valido.")
        
        # si se realizo un ingreso valido (un entero): se evalúa su valor
        if(pos != 0):
            # valida la posición elegida por el usuario
            matrixAux = validPos(pos, matrix)
            
            # si la función devuelve None significa que es un error
            if matrixAux is None:
                # mensaje de error
                print("Error al validar la posición.")

            else:
                # se actualiza la matriz con matrixAux
                matrix = matrixAux
                # sale del bucle
                break

        # si no es valido el ingreso reitera en el bucle 
        print("Lugares disponibles de la matriz: \n", matrix)
     
    # fin del bucle
    # devuelve la matriz actualizada y el valor de 'pos'
    return matrix, pos

#[3]
def getTuplePos(matrix):
    # bucle para validar el ingreso del usuario
    while True:
        # valida que sean valores enteros
        try:
            start   = int(input("Ingrese la posición inicial dentro del rango = "))
            end     = int(input("Ingrese la posición final dentro del rango   = "))
            # se los asigna en pos como una tupla
            pos     = (start, end)
        # si no son valores enteros
        except ValueError:
            # se resetan los valores
            start = 0
            end   = 0
            # se imprime mensaje de error
            print("Error, ingrese un número valido.")
        
        # entra al if solo para valores validos y mayores que 0
        if (start > 0) and (end > 0):
            # valida la posición elegida por el usuario
            matrixAux = validTuple(pos, matrix)

            # si la función devuelve None significa que es un error
            if matrixAux is None:
                print("Error al validar la posición.")
            
            else:
                # se actualiza la matriz con las posiciones disponibles
                matrix = matrixAux
                # sale del bucle
                break

        # si no es valido el ingreso reitera en el bucle 
        print("Lugares disponibles de la matriz: \n", matrix)
    # fin del bucle

    # retorna la matriz actualizada y la posición elegida 
    return matrix, pos



def getJoinVec(row, col):

    # crea la variable 'joinVec' como una lista
    joinVec = []

    #Validación del ingreso del usuario
    print("Ingreso de número de la distribución de las celdas de cada gráfico.")    

    # genera una matriz para enseñar al usuario las posiciones disponibles en la figura 
    matrix  = getMatrix(row, col)
    
    # para indicar el número de cada sub-plot  
    count   = 0

    #Bucle para ingresar cada posición 
    while True:

        # incrementa el contador
        count = count + 1   

        # se muestra al usuario los lugares disponibles del gráfico por medio de la matriz
        print("\nLos lugares representados con '0' ya han sido ocupados")
        print("Lugares disponibles de la matriz: \n", matrix)

        # se ingresa la opción 'op' del usuario validada:
        op = getOption(matrix, count)

        # matriz auxiliar para evaluar la elección del usuario
        matrixAux = None

        # si se quiere ocupar una única celda para el sub-plot en la figura
        if op == '1':
            # llama a la función para obtener una posición valida, y actualizar la matriz de selección
            matrix, pos = getSinglePos  (matrix)
        
        # si se quiere ocupar mas de una celda para el sub-plot en la figura
        elif op == '2':
             # llama a la función para obtener una posición valida, y actualizar la matriz de selección
            matrix, pos = getTuplePos   (matrix)
        
        
        #Una vez validada la posición, se la almacena en joinVec
        joinVec.append(pos) #Append se usa para trabajar a joinVec como una lista dinámica

        #Evalúa el estado de matrix
        flagAllZero = True

        # bucle para recorrer la matriz: si la matriz esta rellena con 0, significa que se finalizo de ingresar las posiciones
        for mRow in matrix:                 # recorre cada fila
            for mElement in mRow:           # recorre cada elemento de la fila
                 
                if mElement != 0:           # si al menos un elemento es distinto de 0
                    flagAllZero = False     # se setea la bandera
                    break                   # sale del 1er for
             
            if flagAllZero == False: 
                break                       # sale del 2do for
        # fin del for

        # si todos los elementos de la matriz son 0
        if flagAllZero == True:             
            print("Se ocuparon todas las celdas del plot. \n")
            # sale del while
            break   

    # devuelve joinVec con todas sus posiciones validadas
    return joinVec
