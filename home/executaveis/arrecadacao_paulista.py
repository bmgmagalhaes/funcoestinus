import os
from .juncao_simples import executar_simples
from .arrecadacao_descompactar import verificar_arquivo_zip, descompactar_arquivo

def executar_paulista(pasta_municipio):
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
                data = retorno.readlines()[0][23:29]
        except:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        if 'DAF607' in arquivo:
            executar_simples(pasta_municipio)

        try:
            if 'IPTU PAULISTA-PE    001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.001')
            elif 'PM DE PAULISTA      104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.104')
            elif 'PM PAULISTA         033BANCO SANTANDER' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.033')
            elif 'PREF.MUN.DE PAULISTA237BANCO BRADESCO' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.237')
            elif 'PREF MUN PAULISTA  P341BANCO ITAU S.A.' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.341')
        except:
            #REMOVE ARQUIVOS DUPLICADOS
            os.remove(rf'{pasta_municipio}\{arquivo}')
if __name__ == '__main__':
    executar_paulista(rf'c:\temp')