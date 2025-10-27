valor_analisado = 15
limite_inferior = 10
if valor_analisado > limite_inferior: # Este bloco só será executado se a condição for True
    print("O valor está acima do limite. Sinalize o dado.")
# Ação 2: Decisão com múltiplos caminhos 
tipo_transacao = "Compra"
if tipo_transacao == "Venda":
    print("Processamento de receita.")
elif tipo_transacao == "Compra":
    print("Processamento de despesa e inventário.")
else:
    print("Tipo de transação desconhecido. Requer auditoria.")
# Verificando se um registro é "novo" e tem um ID válido
registro_id = 95
status_registro = "Novo"
# Teste 1: Comparação de Igualdade (==)
if status_registro == "Novo":
 print("O registro é novo.")
# Teste 2: Comparação de Maior/Menor
if registro_id < 100 and registro_id > 0:
 print("ID válido no intervalo 1 a 99.")

#Um risco é alto se o Volume for maior que 10.000 E a Probabilidade for maior que 0.8.
volume = 12500
probabilidade = 0.90
if volume > 10000 and probabilidade > 0.8:
 print("ALERTA: Risco Alto! Requer intervenção imediata.")
else:
 print("Risco Controlado.")

# Uma amostra de dados é considerada "Importante" se o valor for menor que 1000 OU se o status for 'Crítico':
valor_dado = 500
status_dado = "Normal"
# Usando 'or': se o valor for muito baixo (mesmo que o status seja Normal) OU se o status for Crítico (mesmo que o valor não seja baixo)
if valor_dado < 1000 or status_dado == "Crítico":
 print("Amostra Importante para Análise.")
else:
 print("Amostra Padrão.")
# Testando a negação (not)
if not (valor_dado > 1000 and status_dado == "Normal"):
 print("A amostra não é um 'dado padrão alto'.")

'''Desafio 1: Ordenação de Três Números
Recebidos 3 números inteiros, crie um programa que os mostre ordenados em ordem crescente.
● Dica: Este desafio exige que você use estruturas if aninhadas ou uma série de testes usando operadores de comparação para determinar qual número é o menor, o do meio e o maior.'''

numero01 = float(input('digite um número:'))
numero02 = float(input('digite outro número:'))
numero03 = float(input('digite mais um número:'))

if numero01<numero02 and numero01<numero03:
    print(numero01)
elif numero02<numero03 and numero02<numero01:
    print(numero02)
else: 
    print(numero03)

if (numero01>numero02 and numero01<numero03) or (numero01>numero03 and numero01<numero02):
    print(numero01)
elif (numero02>numero01 and numero02<numero03) or (numero02>numero03 and numero02<numero01):
    print (numero02)
else:
    print(numero03)
if numero01>numero02 and numero01>numero03:
    print(numero01)
elif numero02>numero01 and numero02>numero03:
    print(numero02)
else:
    print(numero03)
'''Desafio 2: Cálculo de Média e Status do Estudante
Dadas as 4 notas de um estudante, calcule sua média e, com base nela, emita a mensagem de status correspondente:
1. Aprovado: Média estritamente maior que 7.
2. Recuperação: Média entre 5 (inclusive) e 7 (inclusive).
3. Reprovação: Média estritamente abaixo de 5'''
nota1=float(input('Informe a nota da 1ª Avaliação:'))
nota2=float(input('Informe a nota da 2ª Avaliação:'))
nota3=float(input('Informe a nota da 3ª Avaliação:'))
nota4=float(input('Informe a nota da 4ª Avaliação:'))
media=(nota1+nota2+nota3+nota4)/4
if media>7:
    print('Média ',media,', Aprovado!')
elif media>=5 and media<=7:
    print('Média ',media,', Recuperação!')
else:
    print('Média ',media,', Reprovado!')