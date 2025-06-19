import os
from .juncao_simples import executar_simples
from .utilitarios import gerar_nome_arquivo_retorno, descompactar_arquivo

def executar_sousa(pasta_municipio):

    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    
    for arquivo in lista_arquivos:

        header = ''
        caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        
        try:
            
            if 'PREF. MUN. SOUSA IPT001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.001')
            elif 'ARREC PM SOUSA      104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')
            elif 'PREF DE SOUSA       004BANCO DO NORDESTE' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.004')
    
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_sousa(rf'c:\temp')