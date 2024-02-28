import os
from juncao_simples import executar_simples
from utilitarios import descompactar_arquivo, gerar_nome_arquivo_retorno

def executar_sao_miguel_do_gostoso(pasta_municipio):

    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    
    for arquivo in lista_arquivos:

        header = ''
        caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        
        try:
            if 'PREFEITURA MUNICIPAL DE SAO MI237BRADESCO' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.237')
            if 'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.001')

            if 'PREFEITURA MUNICIPAL DE SAO MI001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.002')

            if 'PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')
            

        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_sao_miguel_do_gostoso(rf'c:\Temp')