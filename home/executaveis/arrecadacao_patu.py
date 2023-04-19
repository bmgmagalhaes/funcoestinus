import os
from .arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo
# from juncao_simples import executar_simples

def executar_patu(pasta_municipio):
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
                linha1 = retorno.readline()
                data = retorno.readlines()[0][23:29]
        except:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        # if 'DAF607' in i and contador_simples==0:
        #     executar_simples(diretorio)

        try:
            if 'MUNICIPIO DE PATU TR001BANCO DO BRASIL' in linha1:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.001')
        except:
            os.remove(caminho_completo)

if __name__ == '__main__':
    executar_patu(rf'c:\Temp')