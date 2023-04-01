import csv
import os


def converte_brasil_inter(numero):
    numero = numero.replace(".", "")
    numero = numero.replace(",", ".")
    return numero


def converte_inter_brasil(numero):
    numero = numero.replace(",", "_")
    numero = numero.replace(".", ",")
    numero = numero.replace("_", ".")
    return numero


diretorio = rf"c:\temp"
encontrar_arquivo = os.listdir(diretorio)
competencia = input("Informe a competência: ")

with open(rf'{diretorio}\{encontrar_arquivo[0]}', 'r+') as relatorio_original:
    dados = list(csv.reader(relatorio_original, delimiter=';'))
    header = dados[0]
    detalhe = dados[1:]

header.insert(17, "IPTU")
header.insert(18, "Taxas")

with open(rf"{diretorio}\RelatorioDividaAtivaPagamento {competencia}.csv", "w+") as relatorio_ajustado:
    # REFORMULANDO HEADER
    for i in header:
        relatorio_ajustado.write(f"{i};")
    relatorio_ajustado.write(f"\n")

    # REFORMULANDO DETALHES (calculando IPTU e Taxas)
    for i in detalhe:
        i.insert(17, 0)
        i.insert(18, 0)
        if i[9] == "IPTU + Taxas":
            pagamento_convertido = float(converte_brasil_inter(i[16]))
            i[17] = converte_inter_brasil(f"{pagamento_convertido * 0.815:,.2f}")
            i[18] = converte_inter_brasil(f"{pagamento_convertido * 0.185:,.2f}")

    for pagamentos in detalhe:
        pagamentos.pop()
        for pagamento in pagamentos:
            try:
                relatorio_ajustado.write(f"{pagamento};")
            except:
                pagamento = str(pagamento)
                relatorio_ajustado.write(pagamento)
        relatorio_ajustado.write(f"\n")
