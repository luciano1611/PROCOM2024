"""
Función de ingreso de row y col, busca verificar 
el tipo de dato y que sean validas (mayores que 0)

No se define un limite en numero de filas y columnas
"""
def getRowCol():

    # validación del ingreso del usuario
    print("Ingreso de número de filas y columnas del plot.")

    # bucle de validación
    while True:
        
        # por excepción verifica el tipo de dato
        try:
            row = int(input("Número de filas: "))
            col = int(input("Número de filas: "))
            
            # verifica que los valores sean mayores que 0
            if (row > 0) and (col > 0):
                # sale del bucle
                break    
            
            else:
                # mensaje de error
                print("\nError, debe ingresar valores mayores que 0\n")

        # si los valores ingresados no son cantidades enteras
        except ValueError:
            # mensaje de error
            print("\nError, debe ingresar valores enteros.\n")

    # devuelve los valores de cantidad de filas y columnas validadas
    return row, col