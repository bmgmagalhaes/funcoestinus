import os
from utilitarios import pegar_data_pagamento_arquivo_retorno, descompactar_arquivo
from juncao_simples import executar_simples

def executar_serra_negra(pasta_municipio):
    registro_de_pagamento = False
    
    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)

    
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

        if 'DAF607' in arquivo:
            executar_simples(pasta_municipio)

        try:

            if 'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL' in header:
                # TESTAR T e U - VERIFICAR SE TEM PAGAMENTO
                for linha_pagamento in detalhe:
                    if 'U 06' in linha_pagamento:
                        registro_de_pagamento = True
                        print("Achei pagamento em ", nome_arquivo)
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
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_serra_negra(rf"c:\temp")