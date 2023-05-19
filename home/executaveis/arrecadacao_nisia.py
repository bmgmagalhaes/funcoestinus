import os
from .juncao_simples import executar_simples
from .utilitarios import descompactar_arquivo, gerar_nome_arquivo_retorno


def executar_nisia(pasta_municipio):

    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    
    for arquivo in lista_arquivos:

        header = ''
        caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        
        try:
            if 'PREF MUN NISIA FLORE001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.001')
            if 'PMDENISIAFLORESTA   104CAIXA' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.104')
            if 'NISIA FLORESTA 756SICOOB' in header:
                os.rename(caminho_completo, rf'{nome_arquivo}.756')
                
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)


if __name__ == '__main__':
    executar_nisia(rf"c:\temp")
