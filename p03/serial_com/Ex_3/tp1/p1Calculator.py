from .p1Class import Calculator
from .p1Matrix import MatrixDot

#Se usa la variable flag para elegir entre: 
#el menu del ejercicio 1 y el menu del ejercicio 2
def menu(flag):
    
    #Se crea un objeto "obj" de tipo Calculator para realizar las operaciones
    obj = Calculator()

    print("Bienvenido a la aplicación de calculadora")
    while True:
        #Opciones del Menu 1:
        print("Ingrese el número de la operación a realizar:")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Iterativo")

        #Opciones adicionales del Menu 2:
        print("6. Producto punto entre matrices")   if flag == '2' else None                                                                                                                                         
        print("7. Salir del programa")              if flag == '2' else None

        #Validación de la opción ingresada
        while True:
            op = input("Opción: ")
            if op in ['1', '2', '3', '4', '5'] or (flag == '2' and op in ['6', '7']):
                break
            else:
                print("Error, ingrese una opción válida.")


        if op in ['1', '2', '3', '4']:
            # Validación de ingreso de valores
            while True:
                try:
                    Num1 = float(input("Ingrese el primer número: "))
                    Num2 = float(input("Ingrese el segundo número: "))
                    break
                except ValueError:
                    print("Error, ingrese números reales.")

            #Crea un objeto Calculator "C"
            obj.update_values(Num1, Num2)

            # Realiza las operaciones y muestra el resultado
            if op == '1':
                obj.add()
                print(f"Resultado: {Num1} + {Num2} = {obj.result}")
            elif op == '2':
                obj.sub()
                print(f"Resultado: {Num1} - {Num2} = {obj.result}")
            elif op == '3':
                obj.mul()
                print(f"Resultado: {Num1} * {Num2} = {obj.result}")
            elif op == '4':
                obj.div()
                print(f"Resultado: {Num1} / {Num2} = {obj.result}")

        # Operación iterativa
        elif op == '5':
            print("Seleccione una operación iterativa a realizar:")
            print("a) Sumar")
            print("b) Restar")
            print("c) Multiplicación")

            # Evalúa el ingreso correcto de input()
            while True:
                op_iter = input("Ingrese el tipo de operación: ")
                if op_iter in ['a', 'b', 'c']:
                    break
                else:
                    print("Opción no válida.")

            # Ingreso de valores para la operación iterativa
            while True:
                try:
                    step = float(input("Ingrese el valor: "))
                    iterations = int(input("Ingrese el número de iteraciones: "))
                    break
                except ValueError:
                    print("Error: Ingrese números válidos.")

            # Cambia el valor de los atributos del objeto ya creado
            obj.update_values(step, iterations, op_iter)
            # Realiza la operación iterativa
            obj.iter()
            # Imprime en pantalla
            print(f"Resultado de operación iterativa: {obj.result}")

        #Para el menu del ejercicio 2:
        if flag == '2':
            #Para realizar operación de producto punto
            if   op == '6':
                MatrixDot()

            #Para salir del menu o continuar operando
            elif op == '7':
                break #Sale del bucle

        #Si se selecciono el menu 1:
        if flag == '1':
            break #Sale del bucle