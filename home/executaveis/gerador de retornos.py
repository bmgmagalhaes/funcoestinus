# -*- coding: utf-8 -*-
# Separa C:\temp\total.txt por data (AAAAMMDD -> AAMMDD),
# gera arquivos MRAAMMDD.104 com cabeçalho, registros e trailer:
# Z{qtd_total_linhas:06d}{soma_centavos:018d}

import re

arquivo_origem = r"C:\temp\total.txt"
ANCORA_POS_VALOR = "0000264000000071903"  # bloco fixo que aparece logo após o valor

with open(arquivo_origem, "r", encoding="utf-8") as f:
    linhas = [ln.rstrip("\n") for ln in f]

cabecalho = linhas[0]
registros = [ln for ln in linhas[1:] if ln.strip()]

# Agrupa por data (AAAAMMDD começa em posição 21)
grupos = {}
for linha in registros:
    data_aaaa_mm_dd = linha[21:29]  # AAAAMMDD
    data_aammdd = data_aaaa_mm_dd[2:]  # AAMMDD
    grupos.setdefault(data_aammdd, []).append(linha)

def extrair_valor_centavos(linha: str) -> int:
    """
    Extrai o valor em centavos imediatamente antes da âncora fixa.
    - Encontra a âncora '0000264000000071903'
    - Pega a última sequência de dígitos antes dela
    - Usa apenas os 18 dígitos à direita dessa sequência (campo do valor),
      converte para inteiro (centavos)
    """
    idx = linha.find(ANCORA_POS_VALOR)
    if idx == -1:
        raise ValueError("Âncora pós-valor não encontrada na linha.")
    bloco_pre_ancora = linha[:idx]

    m = re.search(r"(\d+)\s*$", bloco_pre_ancora)  # última sequência de dígitos
    if not m:
        raise ValueError("Sequência numérica do valor não encontrada antes da âncora.")

    seq = m.group(1)
    # Mantém no máximo os 18 dígitos mais à direita (campo do valor)
    valor_18 = seq[-18:]
    return int(valor_18)

for data, conteudo in grupos.items():
    nome_arquivo = f"C:\\temp\\MR{data}.001"

    qtd_total_linhas = 1 + len(conteudo) + 1  # cabeçalho + registros + trailer
    soma_centavos = sum(extrair_valor_centavos(l) for l in conteudo)

    trailer = f"Z{qtd_total_linhas:06d}{soma_centavos:017d}"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(cabecalho + "\n")
        for ln in conteudo:
            f.write(ln + "\n")
        f.write(trailer + "\n")

    print(f"Gerado: {nome_arquivo} | Linhas: {qtd_total_linhas} | Soma: {soma_centavos} | Trailer: {trailer}")
