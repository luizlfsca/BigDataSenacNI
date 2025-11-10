
def exemplo():
    x = 42               # variável local (só existe dentro da função)
    print("Dentro:", x)  # OK: imprime dentro
    return x             # devolve x para quem chamou

valor = exemplo()        # chama a função
print("Fora:", valor)    # OK: usa o que foi retornado

print(x)
