from .p1Calculator import menu

def menuCalculator():
    flag = 0
    
    print("Ingrese el menu a utilizar.")
    print("1. Menu del ejercicio 1")
    print("2. Menu del ejercicio 2")
    
    #Evalúa la entrada del usuario
    while True:
        flag = input("Opción: ")
        if flag in ['1', '2']: 
            break
        print("Ingrese una opción valida")
        
    menu(flag)

if __name__ == '__main__':
    menuCalculator()