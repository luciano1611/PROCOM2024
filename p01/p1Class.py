class Calculator:
    # Constructor de la clase:
    def __init__(self, Num1 = 1.0, Num2 = 1.0, Sel = ' '):
        self.a = Num1
        self.b = Num2
        self.op = Sel 
        self.result = None

    #Actualización de los atributos
    def update_values(self, Num1 = 1.0, Num2 = 1.0, Sel = ' '):
        self.a = Num1
        self.b = Num2
        self.op = Sel 
        self.result = None

    # Funciones básicas:
    def add(self):
        self.result = self.a + self.b
    
    def sub(self):
        self.result = self.a - self.b
    
    def mul(self):
        self.result = self.a * self.b

    def div(self):
        if self.b == 0:
            print("No se puede dividir por cero")
            self.result = 'Math. Error'
        else:
            self.result = self.a / self.b
    
    # Función iterativa:
    def iter(self):
        if self.op == 'c':
            self.result = 1 
        else: 
            self.result = 0
            
    # Función iterativa:
    def iter(self):
        if self.op == 'c':
            self.result = 1 
        else: 
            self.result = 0

        for i in range(self.b):
            if  self.op == 'a':
                self.result += self.a
            
            elif self.op == 'b':
                self.result -= self.a
            
            elif self.op == 'c':
                self.result *= self.a

