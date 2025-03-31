# classe calculadora
class Calc:
    def __init__(self):
        pass

    def somar(self, a, b):
        return a + b

    def subtrair(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b == 0:
            return "Erro divisão por zero."
        else:
            return a / b

# helper function
def help():
    print("Digite calculadora (ponto) e o método passando as duas variáveis (a, b)")