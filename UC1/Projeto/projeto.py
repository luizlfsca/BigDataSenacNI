# =========================
# Dados-base
# =========================
FORMAS_PAGAMENTO = ["dinheiro", "pix", "debito", "credito", "vale-refeicao"]

cardapio = [
    {"id_item": 1, "nome": "Combo Sushi 12 peças", "descricao": "Salmão, atum, kani", "preco": 39.90},
    {"id_item": 2, "nome": "Temaki Salmão",       "descricao": "Salmão com cebolinha", "preco": 25.00},
    {"id_item": 3, "nome": "Yakisoba Tradicional", "descricao": "Carne e legumes",      "preco": 34.00},
    {"id_item": 4, "nome": "Guioza 6 unidades",    "descricao": "Recheio de porco",     "preco": 22.00},
    {"id_item": 5, "nome": "Refrigerante Lata",    "descricao": "350ml",                "preco": 7.00},
    {"id_item": 6, "nome": "Água sem gás",         "descricao": "500ml",                "preco": 5.00},
]

garcons = [
    {"id_garcom": 1, "nome": "Ana"},
    {"id_garcom": 2, "nome": "Bruno"},
    {"id_garcom": 3, "nome": "Carla"},
]

mesas = [{"id_mesa": 1}, {"id_mesa": 2}, {"id_mesa": 3}, {"id_mesa": 4}]

pedidos = {}
proximo_id_pedido = 1


# =========================
# Utilitários I/O (com try/except)
# =========================

def pausar():
    input("\nENTER para continuar... ")

def input_int(msg):
    while True:
        try:
            return int(input(msg).strip())
        except ValueError:
            print("Digite um número inteiro válido.")

def input_float(msg):
    while True:
        try:
            return float(input(msg).strip().replace(",", "."))
        except ValueError:
            print("Digite um número válido (use . ou ,).")


# =========================
# Listagens
# =========================

def listar_cardapio():
    print("\n=== CARDÁPIO ===")
    for it in cardapio:
        print(f'[{it["id_item"]}] {it["nome"]} - R$ {it["preco"]:.2f}')
        print(f'     {it["descricao"]}')
    print("================")

def listar_mesas():
    print("\n=== MESAS ===")
    for m in mesas:
        print(f'Mesa {m["id_mesa"]}')
    print("==============")

def listar_pedidos(resumo=False):
    print("\n=== PEDIDOS ===")
    if not pedidos:
        print("Não há pedidos.")
        return
    for pid, p in pedidos.items():
        if resumo:
            print(f'#{pid} | Mesa: {p["id_mesa"]} | Garçom: {p["id_garcom"]} | Status: {p["status"]} | Itens: {len(p["itens"])}')
        else:
            print(f'\nPedido #{pid} | Mesa: {p["id_mesa"]} | Garçom: {p["id_garcom"]} | Status: {p["status"]}')
            if not p["itens"]:
                print("  (sem itens)")
            else:
                for idx, it in enumerate(p["itens"], start=1):
                    print(f'  {idx}. {it["nome"]} x{it["qtd"]} - R$ {it["preco_unit"]:.2f} | Obs: {it["observacao"]}')
            print(f'  Total: R$ {p.get("total", 0.0):.2f}')
    print("================")

def mostrar_resumo_pedido(pedido):
    """Mostra itens e total do pedido (sem alterar status)."""
    print(f'\n--- Pedido #{pedido["id_pedido"]} | Mesa: {pedido["id_mesa"]} | Garçom: {pedido["id_garcom"]} ---')
    if not pedido["itens"]:
        print("(sem itens)")
    else:
        subtotal = 0.0
        for it in pedido["itens"]:
            tot_it = it["qtd"] * it["preco_unit"]
            subtotal += tot_it
            print(f'- {it["nome"]} x{it["qtd"]} = R$ {tot_it:.2f} (R$ {it["preco_unit"]:.2f} cada)')
        print(f"TOTAL: R$ {subtotal:.2f}")


# =========================
# Buscas simples
# =========================

def buscar_item_cardapio(id_item):
    return next((i for i in cardapio if i["id_item"] == id_item), None)

def buscar_garcom(id_garcom):
    return next((g for g in garcons if g["id_garcom"] == id_garcom), None)

def buscar_mesa(id_mesa):
    return next((m for m in mesas if m["id_mesa"] == id_mesa), None)

def pedidos_abertos_da_mesa(id_mesa):
    """Retorna pedidos com status != 'fechado' daquela mesa."""
    return [p for p in pedidos.values() if p["id_mesa"] == id_mesa and p["status"] != "fechado"]


# =========================
# Core de pedidos
# =========================

def calcular_total(pedido):
    """Atualiza o campo 'total' (soma dos itens)."""
    pedido["total"] = round(sum(it["qtd"] * it["preco_unit"] for it in pedido["itens"]), 2)

def abrir_pedido():
    """Cria um pedido 'aberto', imprime cardápio e já oferece adicionar itens."""
    global proximo_id_pedido

    listar_mesas()
    id_mesa = input_int("Mesa (0 para balcão): ")
    mesa = buscar_mesa(id_mesa) if id_mesa != 0 else None
    if id_mesa != 0 and not mesa:
        print("Mesa inexistente.")
        return

    print("\n=== GARÇONS ===")
    for g in garcons:
        print(f'[{g["id_garcom"]}] {g["nome"]}')
    print("================")
    id_garcom = input_int("Garçom: ")
    if not buscar_garcom(id_garcom):
        print("Garçom inexistente.")
        return

    pid = proximo_id_pedido
    proximo_id_pedido += 1
    pedidos[pid] = {
        "id_pedido": pid,
        "id_mesa": id_mesa if mesa else 0,
        "id_garcom": id_garcom,
        "status": "aberto",
        "itens": [],
        "total": 0.0,
        "pagamento": None
    }
    print(f"\nPedido #{pid} criado!")

    # Já imprime cardápio e oferece adicionar itens
    while True:
        listar_cardapio()
        print("Opções: 1) Adicionar item  |  0) Concluir abertura (voltar)")
        op = input_int("Escolha: ")
        if op == 0:
            break
        if op == 1:
            _adicionar_item_no_pedido(pid)
        else:
            print("Opção inválida.")

def _adicionar_item_no_pedido(pid):
    """Auxiliar: adiciona item ao pedido especificado (sem perguntar mesa)."""
    pedido = pedidos.get(pid)
    if not pedido or pedido["status"] == "fechado":
        print("Pedido inválido.")
        return
    id_item = input_int("ID do item do cardápio: ")
    item = buscar_item_cardapio(id_item)
    if not item:
        print("Item inexistente.")
        return
    qtd = input_int("Quantidade: ")
    if qtd <= 0:
        print("Qtd inválida.")
        return
    obs = input("Observação (opcional): ").strip()
    pedido["itens"].append({
        "id_item": item["id_item"],
        "nome": item["nome"],
        "qtd": qtd,
        "preco_unit": item["preco"],
        "observacao": obs
    })
    calcular_total(pedido)
    print("Item adicionado.")

def manutencao_pedido():
    """
    Navega: mesas -> pedidos abertos -> mostra itens/total -> [adicionar | remover | voltar]
    Adicionar: imprime cardápio
    Remover: imprime itens do pedido
    """
    listar_mesas()
    id_mesa = input_int("Informe o ID da mesa: ")
    if id_mesa != 0 and not buscar_mesa(id_mesa):
        print("Mesa inexistente.")
        return

    abertos = pedidos_abertos_da_mesa(id_mesa)
    if not abertos:
        print("Não há pedidos ABERTOS nessa mesa.")
        return

    print("\nPedidos abertos nessa mesa:")
    for p in abertos:
        calcular_total(p)
        print(f'- #{p["id_pedido"]} | Itens: {len(p["itens"])} | Total atual: R$ {p["total"]:.2f}')
    pid = input_int("Selecione o número do pedido: ")

    pedido = pedidos.get(pid)
    if not pedido or pedido["status"] == "fechado" or pedido["id_mesa"] != id_mesa:
        print("Pedido inválido para esta mesa.")
        return

    while True:
        calcular_total(pedido)
        mostrar_resumo_pedido(pedido)
        print("\nOpções:")
        print("1) Adicionar itens")
        print("2) Remover itens")
        print("0) Voltar ao menu 'Pedidos'")
        op = input_int("Escolha: ")

        if op == 0:
            break

        elif op == 1:
            listar_cardapio()
            _adicionar_item_no_pedido(pid)

        elif op == 2:
            if not pedido["itens"]:
                print("Pedido sem itens para remover.")
                continue
            for idx, it in enumerate(pedido["itens"], start=1):
                print(f'{idx}) {it["nome"]} x{it["qtd"]} - R$ {it["preco_unit"]:.2f}')
            idx_rem = input_int("Número do item para remover: ")
            if 1 <= idx_rem <= len(pedido["itens"]):
                pedido["itens"].pop(idx_rem - 1)
                calcular_total(pedido)
                print("Item removido.")
            else:
                print("Índice inválido.")
        else:
            print("Opção inválida.")


# =========================
# Pagamento (seleção numérica)
# =========================

def pagar_pedido():
    """
    Pagar pedido:
    - Navegar por mesa OU digitar nº do pedido.
    - Mostrar itens e total.
    - Escolher UMA forma de pagamento (via número). Se dinheiro, pedir recebido e imprimir troco.
    """
    if not pedidos:
        print("Não há pedidos.")
        return

    print("\n=== PAGAR PEDIDO ===")
    print("1) Navegar por mesa")
    print("2) Digitar número do pedido")
    print("0) Voltar")
    modo = input_int("Escolha: ")

    pedido = None

    if modo == 1:
        listar_mesas()
        id_mesa = input_int("Mesa: ")
        if id_mesa != 0 and not buscar_mesa(id_mesa):
            print("Mesa inexistente.")
            return

        abertos = pedidos_abertos_da_mesa(id_mesa)
        if not abertos:
            print("Não há pedidos ABERTOS nessa mesa.")
            return

        print("\nPedidos abertos nessa mesa:")
        for p in abertos:
            calcular_total(p)
            print(f'- #{p["id_pedido"]} | Itens: {len(p["itens"])} | Total: R$ {p["total"]:.2f}')
        pid = input_int("Selecione o número do pedido: ")
        p = pedidos.get(pid)
        if not p or p["status"] == "fechado" or p["id_mesa"] != id_mesa:
            print("Pedido inválido para esta mesa.")
            return
        pedido = p

    elif modo == 2:
        pid = input_int("Número do pedido: ")
        p = pedidos.get(pid)
        if not p:
            print("Pedido não encontrado.")
            return
        if p["status"] == "fechado":
            print("Esse pedido já está fechado.")
            return
        pedido = p

    elif modo == 0:
        return
    else:
        print("Opção inválida.")
        return

    # Exibe itens e total
    calcular_total(pedido)
    mostrar_resumo_pedido(pedido)

    total = pedido["total"]
    if total <= 0:
        print("Não é possível pagar um pedido vazio.")
        return

    print("\nFormas de pagamento:")
    for i, f in enumerate(FORMAS_PAGAMENTO, start=1):
        print(f"{i}) {f.capitalize()}")

    while True:
        escolha = input_int("Escolha a forma (número): ")
        if 1 <= escolha <= len(FORMAS_PAGAMENTO):
            forma = FORMAS_PAGAMENTO[escolha - 1]
            break
        print("Opção inválida.")

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
        print(f"Pagamento confirmado via {forma.capitalize()} (simulação).")

    pedido["pagamento"] = pagamento_registrado
    pedido["status"] = "fechado"
    imprimir_comprovante(pedido)
    pausar()


def imprimir_comprovante(pedido):
    print("\n======= COMPROVANTE =======")
    print(f'Pedido #{pedido["id_pedido"]} | Mesa: {pedido["id_mesa"]} | Garçom: {pedido["id_garcom"]}')
    print("Itens:")
    if not pedido["itens"]:
        print("  (sem itens)")
    else:
        for it in pedido["itens"]:
            total_it = it["qtd"] * it["preco_unit"]
            print(f'  - {it["nome"]} x{it["qtd"]}  R$ {it["preco_unit"]:.2f}  =  R$ {total_it:.2f}')
            if it["observacao"]:
                print(f'      Obs: {it["observacao"]}')
    print(f"TOTAL: R$ {pedido['total']:.2f}")
    if pedido.get("pagamento"):
        pg = pedido["pagamento"]
        print("Pagamento:")
        print(f'  - Forma: {pg["forma"]} | Valor: R$ {pg["valor"]:.2f}')
        if pg["forma"] == "dinheiro":
            print(f'  - Troco: R$ {pg["troco"]:.2f}')
    print("===========================\n")


# =========================
# Relatório
# =========================

def gerar_relatorio():
    """Total de vendas, vendas por garçom e item mais vendido (somente pedidos FECHADOS)."""
    total_geral = 0.0
    vendas_por_garcom = {}
    contagem_itens = {}

    for p in pedidos.values():
        if p["status"] == "fechado":
            total_geral += p["total"]
            g = p["id_garcom"]
            vendas_por_garcom[g] = vendas_por_garcom.get(g, 0.0) + p["total"]
            for it in p["itens"]:
                contagem_itens[it["nome"]] = contagem_itens.get(it["nome"], 0) + it["qtd"]

    print("\n=== RELATÓRIO DE VENDAS ===")
    print(f"Total de vendas (fechados): R$ {total_geral:.2f}")

    if vendas_por_garcom:
        print("\nVendas por garçom:")
        for g_id, valor in vendas_por_garcom.items():
            g = buscar_garcom(g_id)
            nome = g["nome"] if g else f"Garçom {g_id}"
            print(f"- {nome}: R$ {valor:.2f}")
    else:
        print("\nSem vendas fechadas por garçom.")

    if contagem_itens:
        mais_vendido, qtd_max = None, -1
        for nome, qtd in contagem_itens.items():
            if qtd > qtd_max:
                mais_vendido, qtd_max = nome, qtd
        print(f"\nItem mais vendido: {mais_vendido} (qtd: {qtd_max})")
    else:
        print("\nAinda não há itens vendidos.")
    print("===========================")
    pausar()


# =========================
# Menus
# =========================

def submenu_pedidos():
    while True:
        print("\n=== PEDIDOS ===")
        print("1) Abrir pedido")
        print("2) Manutenção de pedido")
        print("0) Voltar")
        op = input_int("Escolha: ")

        if op == 1:
            abrir_pedido()
        elif op == 2:
            manutencao_pedido()
        elif op == 0:
            break
        else:
            print("Opção inválida.")

def menu():
    while True:
        print("\n=== TANOSHIMI - SISTEMA DE PEDIDOS ===")
        print("1) Cardápio")
        print("2) Pedidos")
        print("3) Pagar pedido")
        print("4) Relatório de vendas")
        print("0) Sair")

        op = input_int("Escolha: ")

        if op == 1:
            listar_cardapio(); pausar()
        elif op == 2:
            submenu_pedidos()
        elif op == 3:
            pagar_pedido()
        elif op == 4:
            gerar_relatorio()
        elif op == 0:
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()