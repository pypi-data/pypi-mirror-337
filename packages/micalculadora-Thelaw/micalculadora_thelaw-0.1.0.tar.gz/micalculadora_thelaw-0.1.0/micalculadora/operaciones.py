def Suma(a, b):
    return a + b

def Resta(a, b):
    return a - b

def Multiplicacion(a, b):
    return a * b

def Divicion(a, b):
    if b == 0:
        raise ValueError("No se puede dividir por 0")
    return a / b

