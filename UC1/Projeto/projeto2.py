"""
Projeto: Sistema de Pedidos - Restaurante Japonês Tanoshimi (Opção B)
Requisitos: variáveis, operações, condicionais, laços, listas/tuplas/conjuntos/dicionários e funções.
Interface: linha de comando (print/input). Sem BD, sem arquivos, sem integrações externas.

Fluxo macro:
1) Cliente vê cardápio
2) Garçom lança pedido no sistema
3) Sistema gera número do pedido (cartão)
4) Cliente paga no caixa informando o número do pedido

Regras principais:
- Pedido aberto pode receber itens; não pode pagar pedido vazio.
- Número do pedido é único e incremental.
- Formas de pagamento: dinheiro, pix, débito, crédito, vale-refeição (VR).
- Apenas UMA forma de pagamento por pedido.
- Dinheiro: pedir valor recebido, calcular troco, imprimir comprovante e confirmar pagamento.
- Relatório simples de vendas do dia.
"""

# =========================
# "Constantes" e dados-base
# =========================

FORMAS_PAGAMENTO = ["dinheiro", "pix", "debito", "credito", "vale-refeicao"]

# Cardápio (sem 'disponivel')
cardapio = [
    {"id_item": 1, "nome": "Combo Sushi 12 peças", "descricao": "Salmão, atum, kani", "preco": 39.90, "categoria": "sushi"},
    {"id_item": 2, "nome": "Temaki Salmão",       "descricao": "Salmão com cebolinha", "preco": 25.00, "categoria": "temaki"},
    {"id_item": 3, "nome": "Yakisoba Tradicional", "descricao": "Carne e legumes",      "preco": 34.00, "categoria": "quente"},
    {"id_item": 4, "nome": "Guioza 6 unidades",    "descricao": "Recheio de porco",     "preco": 22.00, "categoria": "entrada"},
    {"id_item": 5, "nome": "Refrigerante Lata",    "descricao": "350ml",                "preco": 7.00,  "categoria": "bebida"},
    {"id_item": 6, "nome": "Água sem gás",         "descricao": "500ml",                "preco": 5.00,  "categoria": "bebida"},
]

# Garçons (sem 'ativo')
garcons = [
    {"id_garcom": 1, "nome": "Ana"},
    {"id_garcom": 2, "nome": "Bruno"},
    {"id_garcom": 3, "nome": "Carla"},
]

# Mesas (sem 'status')
mesas = [
    {"id_mesa": 1, "capacidade": 2},
    {"id_mesa": 2, "capacidade": 4},
    {"id_mesa": 3, "capacidade": 4},
    {"id_mesa": 4, "capacidade": 6},
]

# Pedidos (id_pedido -> dict)
pedidos = {}

# Gerador simples de IDs
proximo_id_pedido = 1


# =========================
# Utilitários I/O
# =========================

def pausar():
    input("\nPressione ENTER para continuar... ")

def input_int(msg):
    while True:
        valor = input(msg).strip()
        if valor.isdigit() or (valor.startswith("-") and valor[1:].isdigit()):
            return int(valor)
        print("Entrada inválida. Digite um número inteiro.")

def input_float(msg):
    while True:
        valor = input(msg).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Entrada inválida. Digite um número (use . ou ,).")


# =========================
# Listagens
# =========================

def listar_cardapio():
    print("\n=== CARDÁPIO ===")
    for item in cardapio:
        print(f'[{item["id_item"]}] {item["nome"]} - R$ {item["preco"]:.2f} | {item["categoria"]}')
        print(f'     {item["descricao"]}')
    print("================")

def listar_mesas():
    print("\n=== MESAS ===")
    for m in mesas:
        print(f'[{m["id_mesa"]}] Capacidade: {m["capacidade"]}')
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
            print(f'  TOTAL: R$ {p.get("total", 0.0):.2f}')
    print("================")


# =========================
# Buscas simples
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
# Regras de negócio
# =========================

def abrir_pedido():
    """Cria pedido ABERTO e atribui mesa e garçom (sem checar status/ativo)."""
    global proximo_id_pedido

    listar_mesas()
    id_mesa = input_int("Informe o ID da mesa (ou 0 para pedido sem mesa/balcão): ")
    mesa = buscar_mesa(id_mesa) if id_mesa != 0 else None
    if id_mesa != 0 and not mesa:
        print("Mesa inexistente.")
        return

    print("\n=== GARÇONS ===")
    for g in garcons:
        print(f'[{g["id_garcom"]}] {g["nome"]}')
    print("================")
    id_garcom = input_int("Informe o ID do garçom: ")
    garcom = buscar_garcom(id_garcom)
    if not garcom:
        print("Garçom inválido.")
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
        "total": 0.0,
        "pagamento": None  # {"forma": str, "valor": float, "troco": float (se dinheiro)}
    }

    print(f"Pedido #{pid} criado com sucesso!")
    pausar()

def adicionar_item():
    """Adiciona item ao pedido ABERTO."""
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
    if not item:
        print("Item inexistente.")
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
    """Remove um item do pedido ABERTO pelo índice mostrado."""
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
    """Calcula subtotal e total (total == subtotal)."""
    subtotal = 0.0
    for it in pedido["itens"]:
        subtotal += it["preco_unit"] * it["qtd"]
    pedido["subtotal"] = round(subtotal, 2)
    pedido["total"] = round(subtotal, 2)

def pagar_pedido():
    """
    Cobra o pedido diretamente (sem 'fechar' antes).
    - Exige pedido com itens.
    - Calcula total e realiza pagamento com APENAS UMA forma.
    - Dinheiro: pede valor recebido, calcula troco e confirma.
    """
    if not pedidos:
        print("Não há pedidos.")
        return

    listar_pedidos()
    pid = input_int("Informe o número do pedido: ")
    pedido = pedidos.get(pid)
    if not pedido:
        print("Pedido não encontrado.")
        return
    if pedido["status"] == "fechado":
        print("Este pedido já está fechado.")
        return

    if not pedido["itens"]:
        print("Não é possível pagar um pedido vazio.")
        return

    calcular_totais(pedido)
    total = pedido["total"]

    print("\nResumo do pedido:")
    print(f"Subtotal: R$ {pedido['subtotal']:.2f}")
    print(f"TOTAL: R$ {pedido['total']:.2f}")

    print("\nFormas de pagamento:")
    for f in FORMAS_PAGAMENTO:
        print("-", f)
    forma = input("Escolha a forma: ").strip().lower()
    if forma not in FORMAS_PAGAMENTO:
        print("Forma inválida.")
        return

    pagamento_registrado = {"forma": forma, "valor": total, "troco": 0.0}

    if forma == "dinheiro":
        recebido = input_float("Valor recebido (R$): ")
        if recebido < total:
            print("Valor insuficiente. Pagamento cancelado.")
            return
        troco = round(recebido - total, 2)
        pagamento_registrado["troco"] = troco
        print(f"Pagamento OK. Troco: R$ {troco:.2f}")
    else:
        print("Pagamento confirmado (simulação).")

    pedido["pagamento"] = pagamento_registrado
    finalizar_pedido(pedido)
    pausar()

def finalizar_pedido(pedido):
    """Marca pedido como FECHADO e imprime comprovante."""
    pedido["status"] = "fechado"
    imprimir_comprovante(pedido)

def imprimir_comprovante(pedido):
    """Comprovante simples do pedido."""
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
    print(f"TOTAL: R$ {pedido['total']:.2f}")
    if pedido["pagamento"]:
        pg = pedido["pagamento"]
        print("Pagamento:")
        print(f'  - Forma: {pg["forma"]} | Valor: R$ {pg["valor"]:.2f}')
        if pg["forma"] == "dinheiro":
            print(f'  - Troco: R$ {pg["troco"]:.2f}')
    print("===========================\n")

def gerar_relatorio():
    """Relatório simples: total de vendas, vendas por garçom e item mais vendido."""
    total_geral = 0.0
    vendas_por_garcom = {}  # id_garcom -> soma
    contagem_itens = {}     # nome_item -> quantidade total

    for p in pedidos.values():
        if p["status"] == "fechado":
            total_geral += p["total"]
            g = p["id_garcom"]
            vendas_por_garcom[g] = vendas_por_garcom.get(g, 0.0) + p["total"]
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


# =========================
# Menu principal (sem "Fechar pedido")
# =========================

def menu():
    while True:
        print("\n=== TANOSHIMI - SISTEMA DE PEDIDOS ===")
        print("1) Listar cardápio")
        print("2) Abrir pedido")
        print("3) Adicionar item ao pedido")
        print("4) Remover item do pedido")
        print("5) Pagar pedido (uma forma)")
        print("6) Listar pedidos (detalhado)")
        print("7) Listar mesas")
        print("8) Relatório de vendas")
        print("0) Sair")

        opcao = input_int("Escolha uma opção: ")

        if opcao == 1:
            listar_cardapio(); pausar()
        elif opcao == 2:
            abrir_pedido()
        elif opcao == 3:
            adicionar_item()
        elif opcao == 4:
            remover_item()
        elif opcao == 5:
            pagar_pedido()
        elif opcao == 6:
            listar_pedidos(); pausar()
        elif opcao == 7:
            listar_mesas(); pausar()
        elif opcao == 8:
            gerar_relatorio()
        elif opcao == 0:
            print("Encerrando. Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()

