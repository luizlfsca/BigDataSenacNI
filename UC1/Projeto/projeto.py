"""
Sistema simples de restaurante japonês Tanoshimi
Autor: Luiz Felipe Almeida
Recursos usados:
- Variáveis
- Operadores
- Estruturas condicionais (if / else)
- Estruturas de repetição (while / for)
- Listas
- Funções
"""

# ==============================
# 1. CARDÁPIO
# ==============================

# Lista com os nomes dos pratos
menu_pratos = ["Sushi Salmão 8un", "Hot Roll 8un", "Temaki Salmão", "Yakissoba", "Refrigerante", "Água"]

# Lista com os preços correspondentes de cada prato
menu_precos = [24.90, 22.90, 29.90, 32.00, 6.00, 4.00]


# ==============================
# 2. LISTAS PARA GUARDAR PEDIDOS
# ==============================

# Cada posição representa um pedido
pedidos_numeros = []   # guarda o número do pedido
pedidos_mesas = []     # guarda o número da mesa
pedidos_garcons = []   # guarda o nome do garçom
pedidos_itens = []     # guarda a lista de itens escolhidos
pedidos_qtds = []      # guarda as quantidades

# variável para gerar novos números de pedido automaticamente
proximo_pedido = 1


# ==============================
# 3. FUNÇÃO: mostrar o cardápio
# ==============================

def mostrar_cardapio():
    """Mostra o cardápio com os números e preços."""
    print("\n=== CARDÁPIO DIGITAL ===")
    # percorre a lista e mostra cada prato e preço
    for i in range(len(menu_pratos)):
        print(f"{i + 1} - {menu_pratos[i]} - R$ {menu_precos[i]:.2f}")
    print("0 - Finalizar seleção de itens")


# ==============================
# 4. FUNÇÃO: criar um novo pedido
# ==============================

def criar_pedido():
    """Cria um pedido novo e guarda nas listas."""
    global proximo_pedido  # permite alterar a variável global

    print("\n=== NOVO PEDIDO ===")
    mesa = int(input("Digite o número da mesa: "))      # pede número da mesa
    garcom = input("Digite o nome do garçom: ")          # pede nome do garçom

    # cria listas vazias para guardar itens e quantidades deste pedido
    itens = []
    qtds = []

    # loop para adicionar itens até o usuário digitar 0
    while True:
        mostrar_cardapio()                               # mostra o cardápio
        codigo = int(input("Escolha o código do item (0 para finalizar): "))

        if codigo == 0:                                  # 0 encerra o pedido
            break

        # verifica se o código é válido
        if codigo < 1 or codigo > len(menu_pratos):
            print("Código inválido, tente novamente.")
        else:
            quantidade = int(input("Quantidade: "))
            if quantidade > 0:                           # adiciona item válido
                itens.append(codigo - 1)                 # salva o índice do prato
                qtds.append(quantidade)                  # salva a quantidade
            else:
                print("Quantidade inválida.")

    # se o cliente não escolheu nada, cancela
    if len(itens) == 0:
        print("Nenhum item escolhido. Pedido cancelado.")
        return

    # grava o pedido completo nas listas principais
    numero = proximo_pedido
    proximo_pedido += 1  # prepara o próximo número

    pedidos_numeros.append(numero)
    pedidos_mesas.append(mesa)
    pedidos_garcons.append(garcom)
    pedidos_itens.append(itens)
    pedidos_qtds.append(qtds)

    print(f"\nPedido criado com sucesso! Número do pedido: {numero}")
    print("Entregue esse número ao cliente.")


# ==============================
# 5. FUNÇÃO: listar pedidos abertos
# ==============================

def listar_pedidos():
    """Mostra todos os pedidos que ainda não foram pagos."""
    print("\n=== PEDIDOS EM ABERTO ===")
    if len(pedidos_numeros) == 0:
        print("Nenhum pedido em aberto.")
    else:
        for i in range(len(pedidos_numeros)):
            print(f"Pedido {pedidos_numeros[i]} | Mesa {pedidos_mesas[i]} | Garçom: {pedidos_garcons[i]}")


# ==============================
# 6. FUNÇÃO: calcular o total do pedido
# ==============================

def calcular_total(indice):
    """Soma o valor total de um pedido específico."""
    total = 0
    itens = pedidos_itens[indice]
    qtds = pedidos_qtds[indice]

    # percorre cada item do pedido e soma ao total
    for i in range(len(itens)):
        indice_item = itens[i]
        quantidade = qtds[i]
        preco = menu_precos[indice_item]
        total = total + (preco * quantidade)
    return total


# ==============================
# 7. FUNÇÃO: fechar pedido (pagamento)
# ==============================

def fechar_pedido():
    """Fecha o pedido e remove das listas."""
    if len(pedidos_numeros) == 0:
        print("\nNenhum pedido em aberto.")
        return

    numero = int(input("\nDigite o número do pedido: "))

    indice_encontrado = -1
    # procura o pedido com o número informado
    for i in range(len(pedidos_numeros)):
        if pedidos_numeros[i] == numero:
            indice_encontrado = i

    if indice_encontrado == -1:
        print("Pedido não encontrado.")
        return

    # mostra resumo do pedido
    print(f"\nPedido {pedidos_numeros[indice_encontrado]}")
    print(f"Mesa: {pedidos_mesas[indice_encontrado]}")
    print(f"Garçom: {pedidos_garcons[indice_encontrado]}")
    print("Itens:")

    itens = pedidos_itens[indice_encontrado]
    qtds = pedidos_qtds[indice_encontrado]

    for j in range(len(itens)):
        nome = menu_pratos[itens[j]]
        quantidade = qtds[j]
        print(f"- {nome} x{quantidade}")

    total = calcular_total(indice_encontrado)
    print(f"Total a pagar: R$ {total:.2f}")

    pago = input("Pagamento recebido? (s/n): ")

    # se foi pago, remove o pedido das listas
    if pago.lower() == "s":
        pedidos_numeros.pop(indice_encontrado)
        pedidos_mesas.pop(indice_encontrado)
        pedidos_garcons.pop(indice_encontrado)
        pedidos_itens.pop(indice_encontrado)
        pedidos_qtds.pop(indice_encontrado)
        print("Pedido fechado com sucesso!")
    else:
        print("Pagamento não confirmado.")


# ==============================
# 8. MENU PRINCIPAL
# ==============================

def menu_principal():
    """Mostra as opções principais do sistema."""
    while True:
        print("\n=== SISTEMA TANOSHIMI ===")
        print("1 - Novo pedido")
        print("2 - Listar pedidos")
        print("3 - Fechar pedido")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        # usa condicionais para chamar a função certa
        if opcao == "1":
            criar_pedido()
        elif opcao == "2":
            listar_pedidos()
        elif opcao == "3":
            fechar_pedido()
        elif opcao == "4":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# ==============================
# 9. INÍCIO DO PROGRAMA
# ==============================

# chama o menu principal para começar
<<<<<<< HEAD
menu_principal()
=======
menu_principal()
>>>>>>> a45a733 (Inclusão do Projeto)
