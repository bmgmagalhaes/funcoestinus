import os
from juncao_simples import executar_simples
from utilitarios import descompactar_arquivo, gerar_nome_arquivo_retorno

def executar_serra_do_mel(pasta_municipio):
    
    descompactar_arquivo(pasta_municipio, os.listdir(pasta_municipio))
    lista_arquivos = executar_simples(pasta_municipio)
    
    for arquivo in lista_arquivos:

        header = ''
        caminho_completo, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        
        try:
            if 'PREF MUNICIPAL S MEL001BANCO DO BRASIL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.001')
            elif 'PM SERRA DO MEL     104CAIXA ECON. FEDERAL' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.104')
            elif '056847000000071867X' in header:
                os.rename(caminho_completo, f'{nome_arquivo}.002')
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':
    executar_serra_do_mel(rf'c:\temp')