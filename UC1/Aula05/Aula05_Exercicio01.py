'''1. Cálculo de Média Escolar para Vários Alunos Use o laço for para repetir a lógica de cálculo de média e status
(Aprovado/Reprovado/Recuperação) que você fez na Aula 4, agora para 10 estudantes.'''

print('===Calculadora de Média Escolar===')

for i in range(10):

    try:

        print(f'Tentativa {i+1} de 10')
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
    except ValueError:
        print('Entrada invalida, tente novamente!')
