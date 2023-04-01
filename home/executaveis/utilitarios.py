from datetime import datetime
def converter_string_lista_credito(credito_string):

    credito_temp = []
    credito = []

    if credito_string:

        credito_string = credito_string.replace('[', '').replace(']', '')
        credito_string = credito_string.replace("'", "").replace(" ", "")

        credito_string = credito_string.split(',')

        credito_temp.append(credito_string)

        for item in credito_temp:

            for regitros in range(0, len(item), 3):
                if len(item[regitros]) > 6:
                    item[regitros] = item[regitros].replace("/",'')
                    item[regitros] = datetime.strptime(item[regitros],"%d%m%Y")
                    item[regitros] = datetime.strftime(item[regitros],"%d%m%y")

                credito.append([item[regitros], float(item[regitros + 1]), item[regitros + 2]])

    return credito

def converter_string_dicionario_compensar(texto):
    texto = texto.replace("{", '').replace("}", '').replace("],", ':')
    texto = texto.replace(" ", '').replace("'", '').replace("[", '').replace("]", '')
    texto = texto.split(':')

    dicionario = {}

    for indice in range(0, len(texto), 2):
        parcelas = texto[indice + 1].split(",")
        dicionario[texto[indice]] = parcelas

    return dicionario

def converter_string_dicionario_uf(texto):
    texto = texto.replace("{", '').replace("}", '')
    texto = texto.replace(" ", '').replace("'", '')
    texto = texto.split(',')


    dicionario = {}

    for uf in texto:
        dicionario[uf[0:2]] = float(uf[3:])

    return dicionario

def converter_string_dicionario_extrato(texto):
    texto = texto.replace("{", '').replace("}", '').replace(" ", '')
    texto = texto.replace("[[", '[').replace("]]", ']')
    texto = texto.replace("],'", "]:'").replace("],[", "|").replace("'", '')
    texto = texto.replace("[", '').replace("]", '')

    texto = texto.split(':')

    dicionario = {}

    for indice in range(0, len(texto), 2):

        parcelas = texto[indice + 1].split("|")
        for i in range(0, len(parcelas)):

            parcelas[i] =parcelas[i].split(",")
            parcelas[i][2] = float(parcelas[i][2])
            parcelas[i][3] = float(parcelas[i][3])
            parcelas[i][4] = float(parcelas[i][4])

        dicionario[texto[indice]] = parcelas

    return dicionario

def converter_string_float_valor(texto):
    if not "." in texto and "," in texto:
        texto = texto.replace(",", ".")
    elif "." in texto and "," in texto:
        posicao_virgula = texto.index(",")
        posicao_ponto = texto.index(".")
        if posicao_ponto < posicao_virgula:
            texto = texto.replace(".", "")
            texto = texto.replace(",", ".")
        else:
            texto = texto.replace(",", "")

    return float(texto)

def converter_string_dicionario_globais(texto):

    texto = texto.replace("{", '').replace("}", '')
    texto = texto.replace(" ", '').replace("','",";")
    texto = texto.replace("'", '')
    texto = texto.split(';')

    dicionario = {}

    for reg in texto:
        pagamento = reg.split(":")
        dicionario[pagamento[0]] = pagamento[1]

    return dicionario

def pegar_data_pagamento_arquivo_retorno(header, detalhe):
    
    tamanho = len(header)
    
    if tamanho == 241:
        data = datetime.strptime(header[143:151], '%d%m%Y')
        data = datetime.strftime(data, '%y%m%d')
    elif tamanho == 401:
        data = datetime.strptime(header[94:100],'%d%m%y')
        data = datetime.strftime(data, '%y%m%d')
    elif tamanho == 151:
        data = detalhe[0][23:29]
    
    return data