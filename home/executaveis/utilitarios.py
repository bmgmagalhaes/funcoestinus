import os
from datetime import datetime
from zipfile import ZipFile, is_zipfile

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
    data = ''

    if tamanho == 241:
        data = datetime.strptime(header[143:151], '%d%m%Y')
        data = datetime.strftime(data, '%y%m%d')
    elif tamanho == 401:
        data = datetime.strptime(header[94:100],'%d%m%y')
        data = datetime.strftime(data, '%y%m%d')
    elif tamanho == 151:
        data = detalhe[0][23:29]
    
    return data

# Verificando se há .zip nos arquivos retornos baixados do e-mail
def verificar_arquivo_zip(diretorio, lista_arquivos):

    for arquivo in lista_arquivos:
        caminho_completo = os.path.join(diretorio, arquivo)
        if is_zipfile(caminho_completo):
            return True
    return False

# Descompactando os arquivos .zip
def descompactar_arquivo(diretorio, lista_arquivos):
    """
    Verifica se tem arquivo ZIP e descompacta tudo
    """
    tem_zip = verificar_arquivo_zip(diretorio, lista_arquivos)
    while tem_zip:

        for arquivo in lista_arquivos:

            caminho_completo = os.path.join(diretorio, arquivo)

            if is_zipfile(caminho_completo):

                with ZipFile(caminho_completo, 'r') as retornos:
                    retornos.extractall(diretorio)

                os.remove(caminho_completo)

        lista_arquivos = os.listdir(diretorio)
        tem_zip = verificar_arquivo_zip(diretorio, lista_arquivos)

# Gera o nome do correto pra cada arquivo retorno recebido
def gerar_nome_arquivo_retorno(pasta_municipio, arquivo):
    """
    A partir do arquivo informado, determina o nome com base na data.
    Retorna o caminho completo, o nome (sem extensão) e o header, para definir a extensão no executável do município
    """

    nome_arquivo = ''
    try:
        caminho_completo = os.path.join(pasta_municipio, arquivo)

        with open(caminho_completo, 'r+') as retorno:
            header = retorno.readline()
            detalhe = retorno.readlines()
            # if not'DAF607' in arquivo:
            data = pegar_data_pagamento_arquivo_retorno(header, detalhe)
            nome_arquivo = rf'{pasta_municipio}\MR{data}'
                
    except Exception as e:
        print(f"Erro ao tratar o arquivo retorno {arquivo}")
        print(e)

    return caminho_completo, nome_arquivo, header