import os
from .arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo
from .utilitarios import pegar_data_pagamento_arquivo_retorno
# from juncao_simples import executar_simples

def executar_passa_e_fica(pasta_municipio):
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

                if not'DAF607' in arquivo:
                    data = pegar_data_pagamento_arquivo_retorno(header, detalhe)

        except Exception as e:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            print(e)
            continue

        # if 'DAF607' in arquivo:
        #     executar_simples(pasta_municipio)

        nome_arquivo = rf'{pasta_municipio}\MR{data}'

        try:
            if 'PASSA E FICA PREFEITURA       C ECON FEDERAL' in header:
                # TESTAR T e U - VERIFICAR SE TEM PAGAMENTO
                for linha_pagamento in detalhe:
                    if 'U 06' in linha_pagamento:
                        registro_de_pagamento = True
                        break
                if registro_de_pagamento:
                    os.rename(caminho_completo, f'{nome_arquivo}.904')
                else:
                    # REMOVE SE NÃO HOUVER PAGAMENTO
                    os.remove(caminho_completo)
                registro_de_pagamento = False

            elif 'PM PASSA E FICA RN  104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')

            else:
                # REMOVE SE NÃO FOR ARQUIVO RETORNO DE PRODUÇÃO
                os.remove(caminho_completo)

        except Exception as e:
            # REMOVE SE FOR ARQUIVO DUPLICADO
            os.remove(caminho_completo)

if __name__ == '__main__':
    executar_passa_e_fica(rf"c:\temp")