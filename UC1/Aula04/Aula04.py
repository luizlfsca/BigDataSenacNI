semana = 3
if semana == 1:
 print("Domingo")
elif semana == 2:
 print("Segunda-feira")
elif semana == 3:
 print("Terça-feira")
elif semana == 4:
 print("Quarta-feira")
elif semana == 5:
 print("Quinta-feira")
elif semana == 6:
 print("Sexta-feira")
elif semana == 7:
 print("Sábado")
else: # O 'else' funciona como o 'default'
 print("Dia inválido")

mes = 6
match mes:
    case 1:
        print("Janeiro")
    case 2:
        print("Fevereiro")
    case 3:
        print("Março")
    case 6:
        print("Junho")
    case _ :
        print("Mês inválido")

'''Atividade Assistida
Vamos desenvolver o programa dos meses do ano juntos:
● Objetivo: Peça ao usuário para digitar um número entre 1 e 12 e imprima o nome do mês.
● Entrada de Dados: Use int(input("Digite um número de 1 a 12: "))
● Implementação (Exemplo com Match/Case):'''

try:
    numero_mes=int(input('Digite um número de 1 a 12'))
    match numero_mes: 
        case 1:
            print("Janeiro")
        case 2:
            print("Fevereiro")
        case 3:
            print("Março")
        case 4:
            print("Abril")
        case 5:
            print("Maio")
        case 6:
            print("Junho")
        case 7:
            print("Julho")
        case 8:
            print("Agosto")
        case 9:
            print("Setembro")
        case 10:
            print("Outubro")
        case 11:
            print("Novembro")
        case 12:
            print("Dezembro")
        case _ :
            print(f"Número {numero_mes} invalido. Digite um número entre 1 e 12")
except ValueError:
    print("Entrada inválida. Por favor, digite um número inteiro")

'''1. Cálculo de Lâmpadas:
Escreva um programa para calcular e imprimir o número de lâmpadas necessárias para
iluminar um determinado cômodo de uma residência. Dados de entrada: a potência da
lâmpada utilizada (em watts), as dimensões (largura e comprimento, em metros) do
cômodo. Considere que a potência necessária é de 3 watts por metro quadrado e a cada
3m² existe um bocal para uma lâmpada'''

potenciaLampada= float(input("Informe a Potencia da Lâmpada:"))
largura= float(input("Informe a largura do comodo:"))
cumprimento= float(input("Informe cumprimento do comodo:"))
area=largura*cumprimento
potencia_necessaria=area * 3
num_lampadas=potencia_necessaria/potenciaLampada
bocais=area/3
if num_lampadas <= bocais:
    lampadasInstaladas=num_lampadas
else:
    lampadasInstaladas=bocais
if lampadasInstaladas % 1 > 0:
    lampadasInstaladas=int(lampadasInstaladas)+1
else:
    lampadasInstaladas=int(lampadasInstaladas)
print(f"Número de lâmpadas necessárias: {lampadasInstaladas}")

'''2. Quantidade de Caixas de Azulejos:
Escreva um programa para ler as dimensões de uma cozinha retangular (comprimento,
largura e altura), calcular e escrever a quantidade de caixas de azulejos para se colocar em
todas as suas paredes (considere que não será descontada a área ocupada por portas e
janelas). Cada caixa de azulejos possui 1,5 m²'''

larguracozinha=float(input("Digite a largura da cozinha (m):"))
comprimentocozinha=float(input("Digite o comprimento da cozinha (m):"))
alturacozinha=float(input("Digite a autura da cozinha (m):"))
Metrosquadradoscozinha=((2*larguracozinha*alturacozinha)+(2*comprimentocozinha*alturacozinha))
caixas=Metrosquadradoscozinha/1.4
if caixas % 1 > 0:
    caixas=int(caixas+1)
else:
    caixas=int(caixas)
print(f"Quantidade de caixas necessárias:{caixas}")

'''3. Rendimento do Taxista:
Um motorista de táxi deseja calcular o rendimento de seu carro na praça. Sabendo-se que o
preço do combustível é de R$ 6,15, escreva um programa para ler: a marcação do
odômetro (km) no início do dia, a marcação (km) no final do dia, o número de litros de
combustível gasto e o valor total (R$) recebido dos passageiros. Calcular e escrever: a
média do consumo em km/L e o lucro (líquido) do dia.
'''

odometroinicio=float(input("Informe a quilometragem no inicio do dia"))
odometrofinal=float(input("Informe a quilometragem no final do dia"))
litrosgastos=float(input("Informe quantos litros de combustivel foram gastos"))
valorrecebido=float(input("Informe o valor recebido do passageiro"))
kmrodado=odometrofinal-odometroinicio
kmlitro=litrosgastos/kmrodado
gastocomb=litrosgastos*6.15
lucro=valorrecebido-gastocomb
if lucro > 0:
    print(f"Motorista teve R${lucro} de lucro")
elif lucro<0:
    print(f"Motorista teve R${lucro*(-1)} de prejuizo")
else:
    print("Motorista não teve lucro")
'''4. Código de Origem do Produto:
Escreva um programa que leia o código de origem de um produto e imprima na tela a região
de sua procedência, conforme a tabela abaixo:
Observação: caso o código não seja nenhum dos especificados, o produto deve ser
encarado como “Importado”.
'''
codigoorigem=int(input("Informe o código de origem do produto:"))
match codigoorigem:
    case 1:
        print("Sul")
    case 2:
        print("Norte")
    case 3:
        print("Leste")
    case 4:
        print("Oeste")
    case 5 | 6:
        print("Nordeste")
    case 7| 8| 9:
        print("Sudeste")
    case 10:
        print("Centro-Oeste")
    case 11:
        print("Noroeste")
    case _ :
        print("Importado")
'''5. Média do Aluno com Optativa:
Escreva um programa que leia as notas das duas avaliações normais e a nota da avaliação
optativa dos estudantes de uma turma. Caso o estudante não tenha feito a optativa, deve
ser fornecido o valor -1. Calcular a média do semestre considerando que a prova optativa
substitui a nota mais baixa entre as duas primeiras avaliações. Escrever a média e
mensagens que indiquem se o estudante foi aprovado, reprovado ou se está em
recuperação, de acordo com as informações abaixo:
Aprovado: média >= 6.0
Reprovado: média < 3.0
Recuperação: média >= 3.0 e < 6.0
'''
nota1=float(input("Informe a nota da primeira avaliação:"))
nota2=float(input("Informe a nota da segunda avaliação:"))
notaoptativa=float(input("Informe a nota da avaliação optativa:"))
if notaoptativa>nota1 or notaoptativa>nota2:
    if nota1>nota2:
        media=(nota1+notaoptativa)/2
    else:
        media=(nota2+notaoptativa)/2
else:
    media=(nota1+nota2)/2

if media>=6:
    print(f"Média {media}, Aprovado")
elif media<3:
    print(f"Média {media}, Reprovado")
else:
    print(f"Média {media}, Recuperação")

'''6. Positivo ou Negativo:
Escreva um programa para ler um valor e escrever se é positivo ou negativo. Considere o
valor zero como positivo.'''

valor=float(input("Insira um número"))
if valor>0 :
    print("O valor é positivo")
elif valor<0 :
    print("O valor é negativo")
else:
    print("o valor é nulo:")