import os
# from datetime import datetime
from arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo
from utilitarios import pegar_data_pagamento_arquivo_retorno
# from juncao_simples import executar_simples

def executar_serra_negra(pasta_municipio):
    registro_de_pagamento = False
    lista_arquivos = os.listdir(pasta_municipio)

    # VERIFICANDO SE TEM ARQUIVO ZIP
    tem_zip = verificar_arquivo_zip(pasta_municipio, lista_arquivos)

    # DESCOMPACTANDO ARQUIVOS

    while tem_zip:
        descompactar_arquivo(pasta_municipio, lista_arquivos)
        lista_arquivos = os.listdir(pasta_municipio)
        tem_zip = verificar_arquivo_zip(pasta_municipio, lista_arquivos)

    # RENOMEANDO ARQUIVOS
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
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            print('ERRO',e)
            continue
        
        # if 'DAF607' in arquivo:
        #     executar_simples(pasta_municipio)


        try:
            nome_arquivo = rf'{pasta_municipio}\MR{data}'
            if 'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL' in header:
                # TESTAR T e U - VERIFICAR SE TEM PAGAMENTO
                for linha_pagamento in detalhe:
                    if 'U 06' in linha_pagamento:
                        registro_de_pagamento = True
                        break
                if registro_de_pagamento:
                    os.rename(caminho_completo, rf'{nome_arquivo}.001')
                else:
                    # REMOVE SE NÃO HOUVER PAGAMENTO
                    os.remove(caminho_completo)
                registro_de_pagamento = False

            elif '272639000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.002')

            elif 'PM S NEGRA DO NORTE 104CAIXA' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.104')

            elif '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.004')

            elif 'SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.005')

            else:
                # REMOVE SE NÃO HOUVER PAGAMENTO
                os.remove(caminho_completo)
                registro_de_pagamento = False

        except Exception as e:
            # REMOVE SE FOR ARQUIVO DUPLICADO
            os.remove(caminho_completo)

if __name__ == '__main__':
    executar_serra_negra(rf"c:\temp")