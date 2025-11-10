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


'''2. Cadastro de Candidatos
Desenvolva um programa que colete dados de 12 pessoas, usando a decisão para filtrar candidatos menores de 18 anos.
● O programa deve pedir o Ano de Nascimento do candidato.
● Se for menor de 18, o programa deve informar que ele não pode participar e pular a coleta dos demais dados (telefone, email etc) para esse candidato.
● Se for maior de 18, o programa prossegue com o input() para os demais dados.'''

from datetime import date #Importa a função data da biblioteca datetime
TOTAL_CANDIDATOS = 12 #Define a quantidade de candidatos
ANO_ATUAL = date.today().year #tras o ano atual
IDADE_MINIMA = 18 #define a idade de corte

print('===Cadastro de Candidatos===')

for i in range(1, TOTAL_CANDIDATOS + 1): #a cada loop numa amostra de 1 até a quantidade de candidatos + 1 (nesse exemplo ficaria 13) isso traria um range(1,13), definindo o total de tentativas.
    print(f'\n Candidato {i} de {TOTAL_CANDIDATOS}.')  #Imprime na tela uma especie de contador, {i} apresenta a sequancia atual do loop.
    while True: #Quer dizer que ele vai repetir o código enquanto a condição for verdadeira
        entrada=input('Digite o ano de nascimento (AAAA):').strip() #Vai receber o ano de nascimento, o .strip() remove espaços e quebras de linhas antes e depois da string
        try: 
            ano_nascimento = int(entrada) #Essa variavel recebe o valor da variavel entrada e transforma em um número inteiro
        except ValueError:
            print('Valor inserido inválido. Digite apenas números, ex: 2007.') #Caso o valor inserido não seja um número inteiro, ocorrerá um erro de valor; o try/except exibe uma mensagem personalizada.
            continue #volta a pedir o ano, sem avançar o for
        
        min_ano=ANO_ATUAL-120 #nesse caso estamos definindo que o usuário não consegue inserir uma idade maior que 120 anos
        max_ano=ANO_ATUAL #nesse caso impede que o usuário coloque uma data futura
        if not (min_ano <= ano_nascimento <= max_ano): #Essa condição informa se o ano informado é plausível
            print(f'Ano fora do intervalo plausível ({min_ano} a {max_ano}). Tente Novamente.') #caso o usuário informe um ano fora do intervalo, ele apresenta uma mensagem de erro e permite o usuário colocar uma nova data plausível.
            continue 
        break
    idade = ANO_ATUAL-ano_nascimento
    if (idade<IDADE_MINIMA):
        print('Idade não permitida!Prosseguindo para o proximo candidato.')
        continue
    nome = input('Informe seu nome: ').strip().title()
    telefone = input('Informe seu telefone: ').strip()
    email = input('Informe seu e-mail: ').strip()

    
    aprovados.append({
        'nome': nome,
        'idade': idade,
        'telefone': telefone,
        'email': email
    })

    print(f'Usuário {nome}, tem {idade} anos: pode prosseguir!')

# 7) Resumo final
print('\n=== Resumo dos aprovados ===')
if not aprovados:
    print('Nenhum candidato aprovado.')
else:
    for idx, c in enumerate(aprovados, start=1):
        print(f"{idx}. {c['nome']} - {c['idade']} anos - Tel: {c['telefone']} - E-mail: {c['email']}")
    print(f'\nTotal de aprovados: {len(aprovados)} de {TOTAL_CANDIDATOS}')
    


'''3. Tentativa de Login e Senha
Simule um sistema de login simples onde o usuário tem um número limitado de tentativas
para digitar a senha correta.
● Defina um nome de usuário e uma senha corretos (ex: admin e 123456).
● Dê ao usuário 3 tentativas para acertar a combinação.
● Se a senha estiver correta, imprima uma mensagem de sucesso e use o comando break para sair do loop.
● Se a senha estiver errada, informe o erro e diminua o número de tentativas restantes.
● Se as tentativas acabarem, imprima uma mensagem de bloqueio'''