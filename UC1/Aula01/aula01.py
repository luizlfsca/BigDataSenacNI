# AULA 01 - Variáveis em Python (22/10/2025)

## Categorias:

idade=30 #int
nome='maria' #string
preco=19.99 #float 
estoque=False #boolean
print(idade)
print(type(idade))
print(nome)
print(type(nome))
print(preco)
print(type(preco))
print(estoque)
print(type(estoque))
cadastro=input('Digite seu nome:')
print(cadastro)
print(type(cadastro))

''' BOLETIM: criem um algoritmo que associe duas notas de estudantes a duas variáveis criadas e calculem a média desse estudante e guardem em uma terceira variável.'''

nota01=float(input('Informe a nota da primeira avaliação:'))
nota02=float(input('Informe a nota da segunda avaliação:'))
media=((nota01+nota02)/2)
print('A média é ',media)

''' CALCULADORA: construa um algoritmo no qual o usuário digitará 2 números e o programa exibirá o resultado das quatro operações básicas da matemática (soma, subtração, divisão, multiplicação) e módulo'''

numero01=float(input('Digite um número:'))
numero02=float(input('Digite o segundo número:'))
soma=(numero01+numero02)
subtracao=(numero01-numero02)
divisao=(numero01/numero02)
multiplicacao=(numero01*numero02)
modulo=(numero01%numero02)
print('Soma:',soma)
print('Subtração:',subtracao)
print('Divisão:',divisao)
print('Multiplicação',multiplicacao)
print('Módulo:',modulo)
