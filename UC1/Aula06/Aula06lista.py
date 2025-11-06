''' lista01=[100,20,43,23,675,23,12,55]
#Uma lista em Python é uma estrutura de dados que armazena uma coleção ordenada e mutável de elementos, que podem ser de diferentes tipos.
for i in lista01:
    print(i,':',type(i))
print(lista01[2])

'''
'''listas

lista02 = [
    'Lavar Louça',
    'Ir ao Mercado',
    'Lavar banheiro',
    'Tirar poeira',
    'Lavar quintal']

lista02.append('Dar banho no doguinho') #O comando .append serve para incluir um elemento na lista
lista02.pop(5) #O comando .pop remove um elemento através da sua ordem (indice), se não for informado o indice - parenteses em branco() será removido o ultimo elemento da lista
print(lista02[1]) #Para chamar o elemento de uma lista, deve escrever o nome da lista e entre chaves [] colocar o indice do elemento
print(lista02[1][6:12]) #Nesse comando ele vai até o elemento de indice 1 da lista02 e tras os elementos do índice 6 ao 12
print(lista02[1][6:]) #Nesse comando ele vai até o elemento de indice 1 da lista02 e tras os elementos a partir do índice 6
print(lista02[1][:6]) #Nesse comando ele vai até o elemento de indice 1 da lista02 e tras os elementos antes do índice 6 
print(lista02[1][6:], lista02[4][6:]) #Nesse comando ele vai até os elementos de indice 1 e 4 da lista02 e tras os elementos depois do índice 6
lista02_pets=lista02.copy() #Esse comando cria uma nova lista, que copia os elementos de uma lista que está antes do ponto
lista02_pets.append('Dar banho no Doguinho')
lista02_pets.append('Limpar areia dos gatos')

lista02_pets.insert(5,'Ir ao veterinário')#O comando insert, insere o elemento no índice informado
lista02_pets.remove('Lavar quintal')#O comando remove, remove o elemento da lista, esse comando não aceita o número do indice, deve se escrever o elemento da forma que ele está escrito na lista

print(lista02)
print(lista02_pets)'''

''' TUPLAS '''
'''
pares=(40,20,2,18,14,34,96,30,20,58)
print(pares)
print(type(pares))
print(type(pares[3]))



lista_pares=list(pares) #cria uma lista, com os elementos da tupla "pares", isso é feito para acrescentar elementos ao conjunto
lista_pares.append(102) #acrescenta o elemento entre parenteses na lista
lista_pares.sort() #ordena os elementos da lista
lista_pares=tuple(lista_pares)'''

'''Sets'''
'''
impares={33,5,17,11,27,11,71,79,99,15}
print(impares)
print(type(impares))

impares_02={11,3,23,83,15,73}

uniao=impares.union(impares_02)

print(uniao)

intercessao=impares.intersection(impares_02)

print(intercessao)'''

'''Dicionários'''

filme={
    'nome':'V for Vendetta',
    'ano':2005, 
    'genero':"Ação",
    'faixa etaria':16}
print(filme)
print(type(filme))
print(filme['genero'])
print(filme.keys())
print(filme.values())
print(len(filme))
filme['duracao']=130
print(filme)
print(type(filme))
print(filme['genero'])
print(filme.keys())
print(filme.values())
print(len(filme))
filme.pop()