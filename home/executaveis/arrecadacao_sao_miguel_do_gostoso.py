import os
from .arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo
from datetime import datetime
# from juncao_simples import executar_simples

def executar_sao_miguel_do_gostoso(pasta_municipio):
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

                # if tamanho == 241:
                #     data_ficha = datetime.strptime(header[143:151], '%d%m%Y')
                #     data_ficha = datetime.strftime(data_ficha, '%y%m%d')
                if tamanho == 401:
                    data_cobranca = datetime.strptime(header[94:100], '%d%m%y')
                    data_cobranca = datetime.strftime(data_cobranca, '%y%m%d')
                elif tamanho == 151:
                    data_convenio = detalhe[0][23:29]
        except:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        # if 'DAF607' in i and contador_simples==0:
        #     executar_simples(diretorio)

        try:
            if 'PREFEITURA MUNICIPAL DE SAO MI237BRADESCO' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_cobranca}.237')
            if 'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data_convenio}.001')
        except:
            os.remove(caminho_completo)

if __name__ == '__main__':
    executar_sao_miguel_do_gostoso(rf'c:\Temp')