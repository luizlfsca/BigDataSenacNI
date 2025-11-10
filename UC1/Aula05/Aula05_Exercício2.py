'''2. Cadastro de Candidatos
Desenvolva um programa que colete dados de 12 pessoas, usando a decisão para filtrar candidatos menores de 18 anos.
● O programa deve pedir o Ano de Nascimento do candidato.
● Se for menor de 18, o programa deve informar que ele não pode participar e pular a coleta dos demais dados (telefone, email etc) para esse candidato.
● Se for maior de 18, o programa prossegue com o input() para os demais dados.'''

from datetime import date #Importa a função data da biblioteca datetime
TOTAL_CANDIDATOS = 12 #Define a quantidade de candidatos
ANO_ATUAL = date.today().year #tras o ano atual
IDADE_MINIMA = 18 #define a idade de corte
aprovados = []
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