"""
Projeto: Sistema de Pedidos - Restaurante Japonês Tanoshimi
Requisitos: variáveis, operações, condicionais, laços, listas/tuplas/conjuntos/dicionários e funções.
Interface: linha de comando (print/input). Sem BD, sem arquivos, sem integrações externas.

Fluxo macro:
1) Cliente vê cardápio
2) Garçom lança pedido no sistema
3) Sistema gera número do pedido (cartão)
4) Cliente paga no caixa informando o número do pedido

Regras principais:
- Pedido aberto pode receber itens; não pode fechar pedido vazio.
- Número do pedido é único e incremental.
- Taxa de serviço fixa em 10% (pode alterar em TAXA_SERVICO).
- Pagamento exibe formas: dinheiro, pix, débito, crédito, vale-refeição (VR).
- Dinheiro calcula troco; PIX/cartões/VR apenas confirmam valor.
- Pagamento dividido permitido até quitar total.
- Relatório simples de vendas do dia.
"""

# =========================
# "Constantes" e dados-base
# =========================

TAXA_SERVICO = 0.10  # 10%

FORMAS_PAGAMENTO = [
    "dinheiro",
    "pix",
    "debito",
    "credito",
    "vale-refeicao"
]

# Cardápio inicial (lista de dicionários)
cardapio = [
    {"id_item": 1, "nome": "Combo Sushi 12 peças", "descricao": "Salmão, atum, kani", "preco": 39.90, "categoria": "sushi", "disponivel": True},
    {"id_item": 2, "nome": "Temaki Salmão", "descricao": "Salmão com cebolinha", "preco": 25.00, "categoria": "temaki", "disponivel": True},
    {"id_item": 3, "nome": "Yakisoba Tradicional", "descricao": "Carne e legumes", "preco": 34.00, "categoria": "quente", "disponivel": True},
    {"id_item": 4, "nome": "Guioza 6 unidades", "descricao": "Recheio de porco", "preco": 22.00, "categoria": "entrada", "disponivel": True},
    {"id_item": 5, "nome": "Refrigerante Lata", "descricao": "350ml", "preco": 7.00, "categoria": "bebida", "disponivel": True},
    {"id_item": 6, "nome": "Água sem gás", "descricao": "500ml", "preco": 5.00, "categoria": "bebida", "disponivel": True},
]

# Garçons (lista de dicionários)
garcons = [
    {"id_garcom": 1, "nome": "Ana", "ativo": True},
    {"id_garcom": 2, "nome": "Bruno", "ativo": True},
    {"id_garcom": 3, "nome": "Carla", "ativo": True},
]

# Mesas (lista de dicionários)
mesas = [
    {"id_mesa": 1, "capacidade": 2, "status": "livre"},
    {"id_mesa": 2, "capacidade": 4, "status": "livre"},
    {"id_mesa": 3, "capacidade": 4, "status": "livre"},
    {"id_mesa": 4, "capacidade": 6, "status": "livre"},
]

# Pedidos (dicionário indexado pelo id_pedido)
pedidos = {}

# Gerador simples de IDs de pedido
proximo_id_pedido = 1


# =========================
# Funções utilitárias (I/O)
# =========================

def pausar():
    input("\nPressione ENTER para continuar... ")


def input_int(msg):
    """Lê um inteiro com tratamento de erro."""
    while True:
        valor = input(msg).strip()
        if valor.isdigit() or (valor.startswith("-") and valor[1:].isdigit()):
            return int(valor)
        print("Entrada inválida. Digite um número inteiro.")


def input_float(msg):
    """Lê um float com tratamento simples."""
    while True:
        valor = input(msg).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite um número (use . ou ,).")


def escolher_opcao(msg, opcoes):
    """
    Exibe opções numeradas e retorna o índice escolhido.
    opcoes: lista de strings
    """
    for i, texto in enumerate(opcoes, start=1):
        print(f"{i}) {texto}")
    while True:
        escolha = input_int(msg)
        if 1 <= escolha <= len(opcoes):
            return escolha - 1
        print("Opção inválida.")


# =========================
# Funções de listagem
# =========================

def listar_cardapio():
    print("\n=== CARDÁPIO ===")
    for item in cardapio:
        status = "DISPONÍVEL" if item["disponivel"] else "INDISPONÍVEL"
        print(f'[{item["id_item"]}] {item["nome"]} - R$ {item["preco"]:.2f} | {item["categoria"]} | {status}')
        print(f'     {item["descricao"]}')
    print("================")


def listar_garcons():
    print("\n=== GARÇONS ===")
    for g in garcons:
        status = "ATIVO" if g["ativo"] else "INATIVO"
        print(f'[{g["id_garcom"]}] {g["nome"]} | {status}')
    print("================")


def listar_mesas():
    print("\n=== MESAS ===")
    for m in mesas:
        print(f'[{m["id_mesa"]}] Capacidade: {m["capacidade"]} | Status: {m["status"]}')
    print("==============")


def listar_pedidos(resumo=False):
    print("\n=== PEDIDOS ===")
    if not pedidos:
        print("Não há pedidos registrados.")
        return
    for pid, p in pedidos.items():
        if resumo:
            print(f'#{pid} | Mesa: {p["id_mesa"]} | Garçom: {p["id_garcom"]} | Status: {p["status"]} | Itens: {len(p["itens"])}')
        else:
            print(f'\nPedido #{pid} | Mesa: {p["id_mesa"]} | Garçom: {p["id_garcom"]} | Status: {p["status"]}')
            if not p["itens"]:
                print("  (sem itens)")
            else:
                for idx, item in enumerate(p["itens"], start=1):
                    print(f'  {idx}. {item["nome"]} x{item["qtd"]} - R$ {item["preco_unit"]:.2f} | Obs: {item["observacao"]}')
            print(f'  Subtotal: R$ {p.get("subtotal", 0.0):.2f}')
            print(f'  Taxa Serv.: R$ {p.get("taxa_servico", 0.0):.2f}')
            print(f'  Desconto: R$ {p.get("desconto", 0.0):.2f}')
            print(f'  TOTAL: R$ {p.get("total", 0.0):.2f}')
    print("================")


# =========================
# Funções de busca simples
# =========================

def buscar_item_cardapio(id_item):
    for i in cardapio:
        if i["id_item"] == id_item:
            return i
    return None


def buscar_garcom(id_garcom):
    for g in garcons:
        if g["id_garcom"] == id_garcom:
            return g
    return None


def buscar_mesa(id_mesa):
    for m in mesas:
        if m["id_mesa"] == id_mesa:
            return m
    return None


# =========================
# Funções de negócio
# =========================

def abrir_pedido():
    """Cria pedido aberto, atribui mesa (ocupa) e garçom."""
    global proximo_id_pedido

    listar_mesas()
    id_mesa = input_int("Informe o ID da mesa (ou 0 para pedido sem mesa/balcão): ")
    if id_mesa == 0:
        mesa = None
    else:
        mesa = buscar_mesa(id_mesa)
        if not mesa:
            print("Mesa inexistente.")
            return
        if mesa["status"] != "livre":
            print("Mesa não está livre.")
            return

    listar_garcons()
    id_garcom = input_int("Informe o ID do garçom: ")
    garcom = buscar_garcom(id_garcom)
    if not garcom or not garcom["ativo"]:
        print("Garçom inválido/inativo.")
        return

    pid = proximo_id_pedido
    proximo_id_pedido += 1

    pedidos[pid] = {
        "id_pedido": pid,
        "id_mesa": id_mesa if mesa else 0,
        "id_garcom": id_garcom,
        "status": "aberto",
        "itens": [],
        "subtotal": 0.0,
        "taxa_servico": 0.0,
        "desconto": 0.0,
        "total": 0.0,
        "pagamentos": []  # lista de dicts: {"forma": str, "valor": float}
    }

    if mesa:
        mesa["status"] = "ocupada"

    print(f"Pedido #{pid} criado com sucesso!")
    pausar()


def adicionar_item():
    """Adiciona item ao pedido aberto."""
    if not pedidos:
        print("Não há pedidos.")
        return

    listar_pedidos(resumo=True)
    pid = input_int("Informe o número do pedido: ")
    pedido = pedidos.get(pid)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if pedido["status"] != "aberto":
        print("Somente pedidos ABERTOS podem receber itens.")
        return

    listar_cardapio()
    id_item = input_int("Informe o ID do item do cardápio: ")
    item = buscar_item_cardapio(id_item)
    if not item or not item["disponivel"]:
        print("Item inexistente ou indisponível.")
        return

    qtd = input_int("Quantidade: ")
    if qtd <= 0:
        print("Quantidade deve ser positiva.")
        return
    obs = input("Observação (opcional): ").strip()

    pedido["itens"].append({
        "id_item": item["id_item"],
        "nome": item["nome"],
        "qtd": qtd,
        "preco_unit": item["preco"],
        "observacao": obs
    })
    print("Item adicionado com sucesso!")
    pausar()


def remover_item():
    """Remove um item do pedido aberto pelo índice mostrado."""
    if not pedidos:
        print("Não há pedidos.")
        return

    listar_pedidos()
    pid = input_int("Informe o número do pedido: ")
    pedido = pedidos.get(pid)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if pedido["status"] != "aberto":
        print("Somente pedidos ABERTOS podem remover itens.")
        return
    if not pedido["itens"]:
        print("Pedido não possui itens.")
        return

    for idx, it in enumerate(pedido["itens"], start=1):
        print(f'{idx}) {it["nome"]} x{it["qtd"]} - R$ {it["preco_unit"]:.2f} | Obs: {it["observacao"]}')
    escolha = input_int("Informe o número do item a remover: ")

    if 1 <= escolha <= len(pedido["itens"]):
        pedido["itens"].pop(escolha - 1)
        print("Item removido.")
    else:
        print("Índice inválido.")
    pausar()


def calcular_totais(pedido):
    """Calcula subtotal, taxa e total do pedido, atualizando o dicionário."""
    subtotal = 0.0
    for it in pedido["itens"]:
        subtotal += it["preco_unit"] * it["qtd"]

    taxa = subtotal * TAXA_SERVICO
    desconto = pedido.get("desconto", 0.0)
    total = max(subtotal + taxa - desconto, 0.0)

    pedido["subtotal"] = round(subtotal, 2)
    pedido["taxa_servico"] = round(taxa, 2)
    pedido["total"] = round(total, 2)


def fechar_pedido():
    """Fecha itens do pedido (prepara para pagamento calculando totais)."""
    if not pedidos:
        print("Não há pedidos.")
        return

    listar_pedidos()
    pid = input_int("Informe o número do pedido: ")
    pedido = pedidos.get(pid)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if pedido["status"] != "aberto":
        print("Somente pedidos ABERTOS podem ser fechados.")
        return
    if not pedido["itens"]:
        print("Não é possível fechar pedido vazio.")
        return

    # Perguntar desconto (opcional)
    usar_desc = input("Aplicar desconto? (s/n): ").strip().lower()
    if usar_desc == "s":
        valor_desc = input_float("Valor do desconto (R$): ")
        if valor_desc < 0:
            print("Desconto não pode ser negativo. Ignorado.")
        else:
            pedido["desconto"] = valor_desc

    calcular_totais(pedido)
    pedido["status"] = "pronto_pagamento"

    print("\nResumo do pedido:")
    print(f"Subtotal: R$ {pedido['subtotal']:.2f}")
    print(f"Taxa serv. (10%): R$ {pedido['taxa_servico']:.2f}")
    print(f"Desconto: R$ {pedido['desconto']:.2f}")
    print(f"TOTAL: R$ {pedido['total']:.2f}")
    pausar()


def pagar_pedido():
    """Realiza o pagamento, permitindo divisão entre formas até quitar o total."""
    if not pedidos:
        print("Não há pedidos.")
        return

    listar_pedidos()
    pid = input_int("Informe o número do pedido: ")
    pedido = pedidos.get(pid)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if pedido["status"] not in ("pronto_pagamento", "aberto"):
        print("Pedido não está pronto para pagamento.")
        return

    # Garante totais atualizados
    calcular_totais(pedido)
    total = pedido["total"]

    if total <= 0:
        print("Total zerado. Pedido será fechado.")
        finalizar_pedido(pedido)
        pausar()
        return

    print("\nFormas de pagamento disponíveis:")
    for f in FORMAS_PAGAMENTO:
        print(f"- {f}")
    print("(Você pode dividir em múltiplas formas. Digite 'fim' para encerrar.)")

    restante = total
    while restante > 0:
        print(f"\nValor restante: R$ {restante:.2f}")
        forma = input("Escolha a forma (dinheiro/pix/debito/credito/vale-refeicao) ou 'fim': ").strip().lower()
        if forma == "fim":
            break
        if forma not in FORMAS_PAGAMENTO:
            print("Forma inválida.")
            continue

        if forma == "dinheiro":
            # No dinheiro, usuário informa quanto recebeu do cliente.
            recebido = input_float("Valor recebido em dinheiro (R$): ")
            if recebido <= 0:
                print("Valor inválido.")
                continue
            if recebido >= restante:
                troco = recebido - restante
                pedido["pagamentos"].append({"forma": forma, "valor": restante})
                restante = 0.0
                print(f"Pagamento concluído. Troco: R$ {troco:.2f}")
            else:
                # Pagou parcialmente com dinheiro
                pedido["pagamentos"].append({"forma": forma, "valor": recebido})
                restante -= recebido
                print("Pagamento parcial registrado.")
        else:
            # Em PIX/Cartões/VR: registrar valor que será cobrado nessa forma
            valor = input_float("Valor a cobrar nessa forma (R$): ")
            if valor <= 0:
                print("Valor inválido.")
                continue
            if valor >= restante:
                pedido["pagamentos"].append({"forma": forma, "valor": restante})
                restante = 0.0
                print("Pagamento concluído.")
            else:
                pedido["pagamentos"].append({"forma": forma, "valor": valor})
                restante -= valor
                print("Pagamento parcial registrado.")

    if restante > 0:
        print("\nPagamento não concluído. Pedido permanece 'pronto_pagamento'.")
    else:
        finalizar_pedido(pedido)
    pausar()


def finalizar_pedido(pedido):
    """Marca pedido como fechado e libera mesa (se houver)."""
    pedido["status"] = "fechado"
    if pedido["id_mesa"] != 0:
        mesa = buscar_mesa(pedido["id_mesa"])
        if mesa:
            mesa["status"] = "livre"
    print("\n*** Pedido fechado com sucesso! ***")
    imprimir_comprovante(pedido)


def imprimir_comprovante(pedido):
    """Imprime um comprovante simples de pagamento/pedido."""
    print("\n======= COMPROVANTE =======")
    print(f'Pedido #{pedido["id_pedido"]} | Mesa: {pedido["id_mesa"]} | Garçom: {pedido["id_garcom"]}')
    print("Itens:")
    if not pedido["itens"]:
        print("  (sem itens)")
    else:
        for it in pedido["itens"]:
            total_item = it["qtd"] * it["preco_unit"]
            print(f'  - {it["nome"]} x{it["qtd"]}  R$ {it["preco_unit"]:.2f}  =  R$ {total_item:.2f}')
            if it["observacao"]:
                print(f'      Obs: {it["observacao"]}')
    print(f"Subtotal: R$ {pedido['subtotal']:.2f}")
    print(f"Taxa serv. (10%): R$ {pedido['taxa_servico']:.2f}")
    print(f"Desconto: R$ {pedido['desconto']:.2f}")
    print(f"TOTAL: R$ {pedido['total']:.2f}")
    if pedido["pagamentos"]:
        print("Pagamentos:")
        for pg in pedido["pagamentos"]:
            print(f'  - {pg["forma"]}: R$ {pg["valor"]:.2f}')
    print("===========================\n")


def gerar_relatorio():
    """Relatório simples: total de vendas e vendas por garçom; item mais vendido."""
    total_geral = 0.0
    vendas_por_garcom = {}  # id_garcom -> soma
    contagem_itens = {}     # nome_item -> quantidade total

    for p in pedidos.values():
        if p["status"] == "fechado":
            total_geral += p["total"]
            # soma por garçom
            g = p["id_garcom"]
            vendas_por_garcom[g] = vendas_por_garcom.get(g, 0.0) + p["total"]
            # contagem de itens
            for it in p["itens"]:
                contagem_itens[it["nome"]] = contagem_itens.get(it["nome"], 0) + it["qtd"]

    print("\n=== RELATÓRIO DE VENDAS ===")
    print(f"Total de vendas (pedidos fechados): R$ {total_geral:.2f}")

    if vendas_por_garcom:
        print("\nVendas por garçom:")
        for g_id, valor in vendas_por_garcom.items():
            g = buscar_garcom(g_id)
            nome = g["nome"] if g else f"Garçom {g_id}"
            print(f"- {nome}: R$ {valor:.2f}")
    else:
        print("\nSem vendas fechadas por garçom.")

    if contagem_itens:
        # descobrir item mais vendido
        mais_vendido = None
        qtd_max = -1
        for nome, qtd in contagem_itens.items():
            if qtd > qtd_max:
                qtd_max = qtd
                mais_vendido = nome
        print(f"\nItem mais vendido: {mais_vendido} (qtd: {qtd_max})")
    else:
        print("\nAinda não há itens vendidos.")
    print("===========================")
    pausar()


def alterar_disponibilidade_item():
    """Marca item do cardápio como disponível/indisponível."""
    listar_cardapio()
    id_item = input_int("Informe o ID do item: ")
    item = buscar_item_cardapio(id_item)
    if not item:
        print("Item não encontrado.")
        return
    novo = input("Marcar como disponível? (s/n): ").strip().lower()
    if novo == "s":
        item["disponivel"] = True
        print("Item marcado como DISPONÍVEL.")
    else:
        item["disponivel"] = False
        print("Item marcado como INDISPONÍVEL.")
    pausar()


# =========================
# Menu principal
# =========================

def menu():
    while True:
        print("\n=== TANOSHIMI - SISTEMA DE PEDIDOS ===")
        print("1) Listar cardápio")
        print("2) Abrir pedido")
        print("3) Adicionar item ao pedido")
        print("4) Remover item do pedido")
        print("5) Fechar pedido (calcular total)")
        print("6) Pagar pedido")
        print("7) Listar pedidos (detalhado)")
        print("8) Listar mesas")
        print("9) Listar garçons")
        print("10) Relatório de vendas")
        print("11) Marcar item disponível/indisponível")
        print("0) Sair")

        opcao = input_int("Escolha uma opção: ")

        if opcao == 1:
            listar_cardapio()
            pausar()
        elif opcao == 2:
            abrir_pedido()
        elif opcao == 3:
            adicionar_item()
        elif opcao == 4:
            remover_item()
        elif opcao == 5:
            fechar_pedido()
        elif opcao == 6:
            pagar_pedido()
        elif opcao == 7:
            listar_pedidos()
            pausar()
        elif opcao == 8:
            listar_mesas()
            pausar()
        elif opcao == 9:
            listar_garcons()
            pausar()
        elif opcao == 10:
            gerar_relatorio()
        elif opcao == 11:
            alterar_disponibilidade_item()
        elif opcao == 0:
            print("Encerrando. Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
