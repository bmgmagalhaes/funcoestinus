import os
from juncao_simples import executar_simples
from utilitarios import pegar_data_pagamento_arquivo_retorno
from arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo


def executar_parnamirim(pasta_municipio):
    lista_arquivos = os.listdir(pasta_municipio)

    # VERIFICANDO SE TEM ARQUIVO ZIP
    tem_zip = verificar_arquivo_zip(pasta_municipio, lista_arquivos)

    # DESCOMPACTANDO ARQUIVOS
    while tem_zip:
        descompactar_arquivo(pasta_municipio, lista_arquivos)
        lista_arquivos = os.listdir(pasta_municipio)
        tem_zip = verificar_arquivo_zip(pasta_municipio, lista_arquivos)

    for arquivo in lista_arquivos:
        try:
            caminho_completo = os.path.join(pasta_municipio, arquivo)
            
            with open(caminho_completo, 'r+') as retorno:
                header = retorno.readline()
                detalhe = retorno.readlines()
                if not 'DAF607' in arquivo:
                    data = pegar_data_pagamento_arquivo_retorno(
                        header, detalhe)

        except Exception as e:
            print("Erro na abertura de arquivo:", e)
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        if 'DAF607' in arquivo:
            executar_simples(pasta_municipio)

        try:

            nome_arquivo = rf'{pasta_municipio}\MR{data}'

            if '2008769113600000000FUNDO MUNICIPAL DE SAUDE DE PAC ECON FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.204')

            elif '779460100000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.304')

            elif 'ARRECADACAO PM PARNA001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.001')

            elif 'PM PARNAMIRIM       104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')

        except:
            pass
            # os.remove(rf'{pasta_municipio}\{arquivo}')


if __name__ == '__main__':
    executar_parnamirim(rf"c:\temp")
