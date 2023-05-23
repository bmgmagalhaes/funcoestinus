import os
from .utilitarios import pegar_data_pagamento_arquivo_retorno, descompactar_arquivo
from .utilitarios import descompactar_arquivo, gerar_nome_arquivo_retorno
from .juncao_simples import executar_simples
from .retorno_config import selecionar_municipio

def renomear_retorno(pasta_municipio, municipio):

    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    orgaos_retornos = selecionar_municipio(municipio)
       
    nome_arquivo = ''

    for arquivo in lista_arquivos:
        try:
            caminho_completo = os.path.join(pasta_municipio, arquivo)
            with open(caminho_completo, 'r+') as retorno:
                header = retorno.readline()
                detalhe = retorno.readlines()

                if not'DAF607' in arquivo:
                    data = pegar_data_pagamento_arquivo_retorno(header, detalhe)
                    nome_arquivo = rf'{pasta_municipio}\MR{data}'
                    
        except:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        for arquivo in lista_arquivos:

            header = ''
            caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
            
            try:
                # extensao = ''
                for retorno, extensao in orgaos_retornos.items():
                    if retorno in header:
                        os.rename(caminho_completo, f'{nome_arquivo}{extensao}')
                        break

            except Exception as e:
                print(f"Erro ao tratar o arquivo retorno {arquivo}")
                print(e)

if __name__ == '__main__':
    municipio = input("Informe o município: ")
    pasta_municipio = rf"c:\temp" + rf"\{municipio}"
    renomear_retorno(pasta_municipio, municipio)
    # renomear_retorno(rf"c:\temp", municipio)