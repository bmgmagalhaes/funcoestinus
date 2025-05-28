import os, shutil
from juncao_simples import executar_simples
from utilitarios import gerar_nome_arquivo_retorno

def executar_pedro_avelino(pasta_municipio):

    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\PAV\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        

        try:
            if 'ARRECADACAO PM P AVE001BANCO DO BRASIL' in header:
                nome_arquivo += '.001'

            elif 'MUN PEDRO AVELINO   104CAIXA ECON. FEDERAL' in header:
                nome_arquivo += '.104'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)


        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

def executar_galinhos(pasta_municipio):

    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\GAL\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

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

def executar_equador(pasta_municipio):

    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\EQU\ARRECADA'
    # os.system(f'explorer {caminho_destino}')
    

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        

        try:
            if 'EQUADOR - ARRECADACA001BANCO DO BRASIL' in header:
                nome_arquivo += '.001'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)



        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

def executar_caicara_ro_rio_do_vento(pasta_municipio):

    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\CRV\ARRECADA'
    # os.system(f'explorer {caminho_destino}')
    

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)
        

        try:
            if 'PREF CAIC RIO DO VEN001BANCO DO BRASIL' in header:
                nome_arquivo += '.001'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)



        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

def executar_passa_e_fica(pasta_municipio):
    
    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\PEF\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)

        try:
            if 'PASSA E FICA PREFEITURA       C ECON FEDERAL' in header:
                nome_arquivo += '.904'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

def executar_sao_miguel_do_gostoso(pasta_municipio):
    
    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\SMG\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)

        try:

            if 'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A' in header:
                nome_arquivo += '.001'
            if 'PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL' in header:
                nome_arquivo += '.104'
            if 'MUNICIPIO DE SAO MIGUEL DO GOS001BANCO DO BRASIL' in header:
                nome_arquivo += '.002'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

def executar_lajes(pasta_municipio):
    
    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\LAJ\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)

        try:

            if 'PREFEITURA MUNIC DE 001BANCO DO BRASIL  S/A' in header:
                nome_arquivo += '.001'
            if 'PM LAJES            104CAIXA ECON. FEDERAL' in header:
                nome_arquivo += '.104'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)            


def executar_itaja(pasta_municipio):
    
    lista_arquivos = executar_simples(pasta_municipio)

    caminho_destino = rf'D:\Prefeituras\ITJ\ARRECADA'
    # os.system(f'explorer {caminho_destino}')

    for arquivo in lista_arquivos:

        header = ''
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(pasta_municipio, arquivo)

        try:

            if '104CAIXA ECON. FEDERAL' in header:
                nome_arquivo += '.104'

            # Renomeia o retorno conforme a data
            os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{nome_arquivo}', caminho_destino)
        
        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)            



if __name__ == '__main__':

    executar_pedro_avelino(rf"H:\Arqs\PAV\arquivoretorno")
    executar_galinhos(rf"H:\Arqs\GAL\arquivoretorno")
    executar_equador(rf"H:\Arqs\EQU\arquivoretorno")
    executar_caicara_ro_rio_do_vento(rf"H:\Arqs\CRV\arquivoretorno")
    executar_passa_e_fica(rf"H:\Arqs\PEF\arquivoretorno")
    executar_lajes(rf"H:\Arqs\LAJ\arquivoretorno")
    executar_sao_miguel_do_gostoso(rf"H:\Arqs\SMG\arquivoretorno")
    executar_itaja(rf"H:\Arqs\ITJ\arquivoretorno")
    
    
    