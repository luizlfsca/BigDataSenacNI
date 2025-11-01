'''Atividade Assistida:
Vamos desenvolver um programa que leia 5 números e calcule o dobro, o triplo e o
quádruplo de cada um. Faremos isso de três formas, focando nas estruturas:
Usando for (Quando sabemos a contagem: 5 vezes nesse caso)
O for em Python usa a função range() para determinar a contagem.
print("--- Usando FOR (Repetição Contada) ---")'''
# O range(5) gera os números 0, 1, 2, 3, 4 (5 repetições)


for i in range(5):
 try:
 # i representa o número atual da repetição (0, 1, 2...)
    print(f"Número {i + 1} de 5:")
    num = float(input("Digite um número: "))
    
    dobro = num * 2
    triplo = num * 3
    quádruplo = num * 4
    
    print(f" Resultado: Dobro={dobro}, Triplo={triplo}, Quádruplo={quádruplo}\n")
 
 except ValueError:
    print("Entrada inválida. Tente novamente.")




''' Usando while (Repetição baseada em Condição)
O while repete o bloco de código enquanto a condição inicial for True. Precisamos de um
contador manual para controlar o número de repetições:'''


print("--- Usando WHILE (Repetição Condicional) ---")
contador = 0 # Inicializamos o contador
limite = 5 # Definimos o limite
while contador < limite: # A condição de parada: Enquanto o contador for menor que 5
    try:
        print(f"Número {contador + 1} de {limite}:")
        num = float(input("Digite um número: "))
        
        dobro = num * 2
        triplo = num * 3
        quádruplo = num * 4
        
        print(f" Resultado: Dobro={dobro}, Triplo={triplo}, Quádruplo={quádruplo}\n")
        
        contador = contador + 1 # IMPORTANTÍSSIMO! Incrementa o contador para evitar loop infinito
    except ValueError:
        print("Entrada inválida. Tente novamente.") # Não incrementamos o contador para dar nova chance ao usuário




'''Usando do-while (Executar primeiro, checar depois)
Como o Python não tem o do-while nativo, nós o simulamos garantindo que o bloco interno
execute pelo menos uma vez, ou usando um while True com um if para quebrar (comando
break):'''


print("--- Simulação DO-WHILE (Executa 1ª vez, depois checa) ---")
contador = 0
limite = 5
while True: # Loop infinito garantido para executar pelo menos uma vez
    if contador >= limite:
        break # Ponto de DECISÃO: Se o limite for atingido, usamos 'break' para sair
 
    try:
        print(f"Número {contador + 1} de {limite}:")
        num = float(input("Digite um número: "))
        
        dobro = num * 2
        triplo = num * 3
        quádruplo = num * 4
        
        print(f" Resultado: Dobro={dobro}, Triplo={triplo}, Quádruplo={quádruplo}\n")
        
        contador = contador + 1 # Incremento
    except ValueError:
         print("Entrada inválida. Tente novamente.")   