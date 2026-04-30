import os

def parse_cnab240(file_path):
    pagamentos = []
    with open(file_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    for i in range(len(linhas)):
        linha = linhas[i]

        if linha[13:17] == "U 06":  # Registro U com código 06
            valor_str = linha[84:92]  # valor pago (centavos)
            valor = int(valor_str) / 100.0

            data_pagamento_str = linha[137:145]
            data_credito_str = linha[145:153]

            data_pagamento = f"{data_pagamento_str[0:2]}/{data_pagamento_str[2:4]}/{data_pagamento_str[4:8]}"
            data_credito = f"{data_credito_str[0:2]}/{data_credito_str[2:4]}/{data_credito_str[4:8]}"

            pagamentos.append({
                "valor": valor,
                "data_pagamento": data_pagamento,
                "data_credito": data_credito
            })

    return pagamentos


if __name__ == "__main__":
    pasta = "C:/temp"
    arquivos = os.listdir(pasta)

    if not arquivos:
        print("Nenhum arquivo encontrado em C:/temp")
    else:
        arquivo_retorno = os.path.join(pasta, arquivos[0])
        pagamentos = parse_cnab240(arquivo_retorno)

        # Consolidar totais por data
        totais_pagamento = {}
        totais_credito = {}

        for p in pagamentos:
            totais_pagamento[p["data_pagamento"]] = totais_pagamento.get(p["data_pagamento"], 0) + p["valor"]
            totais_credito[p["data_credito"]] = totais_credito.get(p["data_credito"], 0) + p["valor"]

        print("\n=== RESULTADO FINAL ===")
        for data, total in totais_pagamento.items():
            print(f"Valor total = R$ {total:.2f}")
            print(f"Data do pagamento: {data}")

        print("\n")
        for data, total in totais_credito.items():
            print(f"Valor total = R$ {total:.2f}")
            print(f"Regime de Caixa: {data}")

        print("\n")
