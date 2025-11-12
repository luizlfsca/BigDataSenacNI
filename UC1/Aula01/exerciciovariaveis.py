# Nível 1 — Fundamentos (10 exercícios)

#Crie uma variável chamada nome e atribua o seu nome. Em seguida, exiba o valor com print().

nome="Luiz Felipe Santos da Costa Almeida"
print(nome)

#Crie variáveis idade e altura e mostre uma frase como:
#"Meu nome é Luiz, tenho 27 anos e 1.78m de altura."

idade=27
altura=1.78
print(f"Meu nome é {nome}, tenho {idade} anos e {altura}m de altura.")

#Crie três variáveis (a, b, soma) e exiba a soma dos dois primeiros.
a=1
b=2
soma=a+b
print(f'O resultado da soma de a e b é {soma}')

#Crie uma variável cidade e depois altere o valor dela, mostrando ambos os valores.
cidade = 'Mesquita'
print("Cidade (antes):", cidade)
cidade = 'Nilópolis'
print("Cidade (depois):", cidade)
#Crie variáveis produto e preco, e mostre uma frase: "O produto X custa R$ Y".
produto='sabão'
preco=float(10)
print(f'O produto {produto} custa R${preco:.2f}')
#Descubra o tipo de cada variável usando type().
print(f'\n{type(nome)},\n{type(idade)},\n{type(altura)},\n{type(a)},\n{type(b)},\n{type(soma)},\n{type(cidade)},\n{type(produto)},\n{type(preco)}')
#Crie variáveis nota1 e nota2, some e calcule a média.
nota1=10
nota2=5
media=(nota1+nota2)/2
print(media)

#Crie uma variável booleana tem_carteira = True e exiba: "Possui carteira? True".
tem_carteira=True
print(f'Possui carteira? {tem_carteira}')

#Faça um programa que leia seu nome com input() e exiba "Olá, <nome>".
nome=input('Escreva seu nome:')
print(f'Olá, {nome}')

#Faça um programa que leia dois números inteiros com input() e mostre a soma deles.
numero1=int(input('Digite um número:'))
numero2=int(input('Digite outro número:'))
print(f'A soma é {numero1+numero2}')
# Nível 2 — Aplicação (5 exercícios)

#Peça ao usuário o nome de um produto, a quantidade e o preço unitário, e mostre o total da compra.
nomeproduto=input("Digite o nome do produto:")
quantidade=int(input("Digite a quantidade do produto:"))
precounit=float(input("Digite o Preço unitário:"))
print(f"O total da compra é {(quantidade*precounit):.2f}")

#Peça o nome e o ano de nascimento do usuário, calcule a idade e mostre uma frase com f-string.
nome=input("Digite seu nome:")
anonascimento=int(input("Digite seu ano de nascimento:"))
print(f"Sua idade é {2025-anonascimento}")
#Crie um programa que leia o nome e o peso de uma pessoa e exiba: "Fulano pesa X kg".
nome=input("Digite seu nome:")
peso=float(input("Digite seu peso:"))
print(f"{nome} pesa {peso}kg")
#Leia dois números e troque os valores entre as variáveis (sem usar listas).
num1 = int(input('Digite um número: '))
num2 = int(input('Digite outro número: '))
print("Antes da troca:", num1, num2)
tmp = num1
num1 = num2
num2 = tmp
print("Depois da troca:", num1, num2)
#Crie um programa que leia uma temperatura em Celsius e exiba em Fahrenheit.
celsius = float(input('Digite a temperatura em graus Celsius: '))
fahrenheit = (celsius * 1.8) + 32
print(f'{celsius:.2f} °C equivalem a {fahrenheit:.2f} °F')
