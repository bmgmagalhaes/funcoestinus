import os
from utilitarios import descompactar_arquivo, pegar_data_pagamento_arquivo_retorno
from juncao_simples import executar_simples

def executar_sao_bento_do_norte(pasta_municipio):
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

        # nome_arquivo = rf'{pasta_municipio}\MR{data}'

        try:
            if 'SAO BENTO DO NORTE PREFEITURA C ECON FEDERAL' in header:
                #TESTAR T e U
                for linha_pagamento in detalhe:
                    if 'U 06' in linha_pagamento:
                        registro_de_pagamento = True
                        break
                if registro_de_pagamento:
                    os.rename(caminho_completo, f'{nome_arquivo}.104')
                else:
                    #REMOVE SE NÃO HOUVER PAGAMENTO
                    os.remove(caminho_completo)
                registro_de_pagamento = False
            else:
                #REMOVE SE NÃO FOR ARQUIVO RETORNO DE PRODUÇÃO
                os.remove(caminho_completo)

        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_sao_bento_do_norte(rf"c:\temp")