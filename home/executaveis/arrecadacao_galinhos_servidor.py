import os, shutil
from juncao_simples import executar_simples
from utilitarios import gerar_nome_arquivo_retorno

def executar_galinhos(pasta_municipio):

    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\GAL\ARRECADA'
    os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        

        try:
            if 'PREF MUN DE GALINHOS001BANCO DO BRASIL' in header:
                nome_arquivo += '.001'

            elif 'PMGALINHOS          104CAIXA ECON. FEDERAL' in header:
                nome_arquivo += '.104'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)


        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

if __name__ == '__main__':

    executar_galinhos(rf"H:\Arqs\GAL\arquivoretorno")