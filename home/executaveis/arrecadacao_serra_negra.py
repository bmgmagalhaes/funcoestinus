import os
from datetime import datetime
from arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo
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
                tamanho = len(header)

                if tamanho == 241:
                    data_ficha = datetime.strptime(header[143:151], '%d%m%Y')
                    data_ficha = datetime.strftime(data_ficha, '%y%m%d')
                elif tamanho == 401:
                    data_cobranca = datetime.strptime(header[94:100],'%d%m%y')
                    data_cobranca = datetime.strftime(data_cobranca, '%y%m%d')
                elif tamanho == 151:
                    data_convenio = detalhe[0][23:29]

        except Exception as e:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            print('ERRO',e)
            continue

        # if 'DAF607' in arquivo:
        #     executar_simples(pasta_municipio)


        try:
            if 'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL' in header:
                # TESTAR T e U - VERIFICAR SE TEM PAGAMENTO
                for linha_pagamento in detalhe:
                    if 'U 06' in linha_pagamento:
                        registro_de_pagamento = True
                        break
                if registro_de_pagamento:
                    os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_ficha}.001')
                else:
                    # REMOVE SE NÃO HOUVER PAGAMENTO
                    os.remove(caminho_completo)
                registro_de_pagamento = False
            elif '272639000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_cobranca}.002')

            # elif '237493000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL' in header:
            #     os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_cobranca}.003')

            elif '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_cobranca}.004')

            elif 'SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_convenio}.005')

            else:
                # REMOVE SE NÃO HOUVER PAGAMENTO
                os.remove(caminho_completo)
                registro_de_pagamento = False

        except Exception as e:
            # REMOVE SE FOR ARQUIVO DUPLICADO
            os.remove(caminho_completo)

if __name__ == '__main__':
    executar_serra_negra(rf"c:\temp")