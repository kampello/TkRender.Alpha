from engine.solid import Objecto

objects = []
air = []


def resetar_mapa():
    global objects, air
    objects.clear()
    air.clear()


def ini_mapa(ficheiro):
    resetar_mapa()
    global objects, air
    objects.clear()
    air.clear()

    blocos = {}
    linhas_mapa = []
    lendo_mapa = False

    with open(ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()

            # Ignorar comentários e linhas vazias
            if not linha or linha.startswith("#"):
                continue

            # Processar definições de blocos
            if "=" in linha and not linha.startswith("map"):
                id_str, resto = linha.split("=", 1)
                bloco_id = int(id_str.strip())
                partes = [parte.strip() for parte in resto.split(",")]

                imagem = partes[0]
                layer = int(partes[1].split("=")[-1])
                tipo = partes[2]  # "air" ou "object"

                blocos[bloco_id] = {
                    "imagem": imagem,
                    "layer": layer,
                    "tipo": tipo
                }

            # Começou o mapa
            elif linha.startswith("map"):
                lendo_mapa = True
                linha = linha.split("=", 1)[1].strip()
                if linha:
                    linhas_mapa.append(linha)
                continue

            elif lendo_mapa:
                linhas_mapa.append(linha)
                if "]" in linha:
                    lendo_mapa = False
                continue

    # Unir todas as linhas e avaliar a lista
    mapa_str = "".join(linhas_mapa)
    mapa_valores = eval(mapa_str)

    # Agora vamos calcular o número de colunas automaticamente com base no tamanho do mapa
    total_blocos = len(mapa_valores)

    # Ajustar o número de colunas automaticamente com base no tamanho do mapa
    colunas = 70  # O número de colunas pode ser ajustado automaticamente ou calculado
    if total_blocos > colunas:  # Se o número de blocos exceder as colunas, recalculamos
        colunas = int(total_blocos ** 0.5)  # Por exemplo, uma raiz quadrada para balancear as dimensões

    # Ajuste para garantir que colunas e linhas se ajustem perfeitamente ao mapa
    while total_blocos % colunas != 0:
        colunas += 1

    # Calcular as posições (x, y) dos blocos no mapa
    for i, bloco_id in enumerate(mapa_valores):
        x = (i % colunas) * 30  # A posição X é calculada com base na coluna
        y = (i // colunas) * 30  # A posição Y é calculada com base na linha

        if bloco_id not in blocos:
            continue

        bloco = blocos[bloco_id]
        obj = Objecto(x, y, 30, 30, bloco["imagem"], bloco["layer"])

        if bloco["tipo"] == "object":
            objects.append(obj)
        else:
            air.append(obj)
