import os
from .juncao_simples import executar_simples
from .utilitarios import gerar_nome_arquivo_retorno, descompactar_arquivo

def executar_paulista(pasta_municipio):

    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    
    for arquivo in lista_arquivos:

        header = ''
        caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        
        try:
            if 'IPTU PAULISTA-PE    001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.001')
            elif 'PM DE PAULISTA      104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')
            elif 'PM PAULISTA         033BANCO SANTANDER' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.033')
            elif 'PREF.MUN.DE PAULISTA237BANCO BRADESCO' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.237')
            elif 'PREF MUN PAULISTA  P341BANCO ITAU S.A.' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.341')
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_paulista(rf'c:\temp')