import os
from .utilitarios import verificar_arquivo_zip, descompactar_arquivo
# from juncao_simples import executar_simples

def executar_bodo(pasta_municipio):
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
                data = retorno.readlines()[0][23:29]
        except:
            # Quando arquivo do tesouro for alterado, esse teste ignora parte da lista inconsistente
            continue

        # if 'DAF607' in arquivo:
        #     executar_simples(pasta_municipio)

        try:
            if 'PREFEITURA DE BODO  001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{pasta_municipio}\MR{data}.001')
        except:
            # REMOVE ARQUIVOS DUPLICADOS
            os.remove(rf'{pasta_municipio}\{arquivo}')

if __name__ == '__main__':
    executar_bodo(rf"c:\temp")