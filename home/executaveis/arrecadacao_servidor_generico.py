import os, shutil
from juncao_simples import executar_simples
from utilitarios import gerar_nome_arquivo_retorno
import time
"""
Orientações gerais antes de gerar o executável:

"""

### Lista dos municípios com atualização "automática" e seus headers com respectivos códigos bancários
LISTA_MUNICIPIOS = {

        # A barra invertida antes da sigla é necessária, pois a string será usada pra integrar o caminho dos diretórios do servidor
        '\ANG': {
            'IMPOSTOS MUNICIPAIS 001BANCO DO BRASIL  S/A': '.001',
        },
        '\CAI': {
            'CAICO ARRECADACAO TR001BANCO DO BRASIL': '.001',
            'MUNICIPIO DE CAICO            BANCO DO BRASIL': '.002',
        },
        '\CEA': {
            'PMCM - ARRECADACAO  001BANCO DO BRASIL  S/A': '.001',
            'PMCEARAMIRIM        104CAIXA ECON. FEDERAL': '.104',
        },
        '\CRE': {
            'PM CAMPO REDONDO RN 104CAIXA ECON. FEDERAL': '.104',
        },
        '\CRV': {
            'PREF CAIC RIO DO VEN001BANCO DO BRASIL': '.001',
        },
        '\EQU': {
            'EQUADOR - ARRECADACA001BANCO DO BRASIL': '.001',
        },
        '\EXT': {
            'PM EXTREMOZ - TRIBUT001BANCO DO BRASIL  S/A': '.001',
            'PM EXTREMOZ         104CAIXA ECON. FEDERAL': '.104',
        },
        '\GAL': {
            'PMGALINHOS          104CAIXA ECON. FEDERAL': '.104',
            'PREF MUN DE GALINHOS001BANCO DO BRASIL': '.001',
        },
        '\GAV': {
            'PM S G AVELINO TRIBU001BANCO DO BRASIL': '.001',
            'PMSGA               104CAIXA ECON. FEDERAL': '.104',
        },
        '\GOH': {
            '00000307963 MUNICIPIO DE GOIANINHA': '.901',
            'PMG-ARREC IMPOSTOS/T001BANCO DO BRASIL': '.001',
            'PM GOIANINHA        104CAIXA ECON. FEDERAL': '.104',
        },
        '\GON':{
            'PMSGA ARRECADACAO   001BANCO DO BRASIL':'.001', 
            'MUNICIPIO DE SAO GONCALO DO AMBANCO DO BRASIL':'.901', 
            'PMSGAMARANTERN      104CAIXA ECON. FEDERAL':'.104',
        },  
        '\ITJ': {
            '104CAIXA ECON. FEDERAL': '.104',
        },
        '\JDS': {
            '3512214  2807793': '.001',
            'MUN JARDIM DO SERIDO001BANCO DO BRASIL  S/A': '.901',  # agz
            '3512214  3178850': '.902',
        },
        '\LAJ': {
            'PREFEITURA MUNIC DE 001BANCO DO BRASIL  S/A': '.001',
            'PM LAJES            104CAIXA ECON. FEDERAL': '.104',
        },
        '\LDA': {
            'PM DE LAGOA DANTA   104CAIXA ECON. FEDERAL': '.104',
            'ARRECADACAO LAGOA DA001BANCO DO BRASIL': '.001',
        },
        '\MAC':{
            'PREF MACAIBA TRIB DI001BANCO DO BRASIL':'.001', 
            'MUNICIPIO DE MACAIBA          001BANCO DO BRASIL':'.902', 
            'PM MACAIBA          104CAIXA ECON. FEDERAL':'.104',
        },
        '\MON': {
            'P M MONTE ALEGRE IPT001BANCO DO BRASIL': '.001',
        },
        rf'\NIS': {
            'PREF MUN NISIA FLORE001BANCO DO BRASIL': '.001',
            'PMDENISIAFLORESTA   104CAIXA': '.104',
            'NISIA FLORESTA 756SICOOB': '.756',
        },
        '\OUB': {
            'PREF MUN DE OURO BRA001BANCO DO BRASIL': '.001',
        },
        '\PAR': {
            '2008769113600000000FUNDO MUNICIPAL DE SAUDE DE PAC ECON FEDERAL': '.204',
            '779460100000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL': '.304',
            'ARRECADACAO PM PARNA001BANCO DO BRASIL': '.001',
            'PM PARNAMIRIM       104CAIXA ECON. FEDERAL': '.104',
            '2008798913700000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL': '.404',
        },
        '\PAV': {
            'PM PEDRO AVELINO    104CAIXA ECON. FEDERAL': '.104',
            'ARRECADACAO PM P AVE001BANCO DO BRASIL': '.001',
        },
        '\PEF': {
            'PASSA E FICA PREFEITURA       C ECON FEDERAL': '.904',
        },
        '\PUR': {
            'ARRECADACAO PUREZA  001BANCO DO BRASIL': '.001',
            'PMPUREZA            104CAIXA ECON. FEDERAL': '.104',
        },
        '\PVE': {
            'MUN. PEDRO VELHO    104CAIXA ECON. FEDERAL': '.104',
            'PEDRO VELHO ARRECADA001BANCO DO BRASIL ': '.001',
        },
        '\RDF': {
            'PREF MUN RIO DO FOGO001BANCO DO BRASIL': '.001',
            'PMRIODOFOGO         104CAIXA ECON. FEDERAL': '.104',
        },
        '\SBN': {
            'SAO BENTO DO NORTE PREFEITURA C ECON FEDERAL': '.104',
        },
        '\SJM': {
            'PREF MUN S J MIPIBU 001BANCO DO BRASIL': '.901',
            'PM SAO JOSE MIPIBU  104CAIXA ECON. FEDERAL': '.104',
        },
        '\SMG': {
            'P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A': '.001',
            'PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL': '.104',
            'MUNICIPIO DE SAO MIGUEL DO GOS001BANCO DO BRASIL': '.002',
        },
        '\SNN': {
            'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL': '.001',
            '272639000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL': '.002',
            'PM S NEGRA DO NORTE 104CAIXA': '.104',
            '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL': '.004',
            'SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A': '.005',
        },
        '\STM': {
            'ARRECADACAO SAO TOME001BANCO DO BRASIL': '.001',
            'PM DE SAO TOME      104CAIXA ECON. FEDERAL': '.104',
        },
        '\TDB': {
            'MUNICIPIO DE TIMBAUBA DOS BATI001BANCO DO BRASIL': '.002',
            'PM TIMBAUBA DOS BATI104CAIXA ECON. FEDERAL': '.104',
        },
    
        # MUNICÍPIOS QUE AINDA DEPENDEM DA CONCLUSÃO DA CONFIGURAÇÃO PARA O DOWNLOAD AUTOMÁTICO

        # '\CUR':{
        #     'PM CURRAIS NOVOS RN 001BANCO DO BRASIL':'.001', 
        #     '33251 MUNICIPIO DE CURRAIS NOVOS    BANCO DO BRASIL':'.002',
        #     'PPM CURRAIS NOVOS   104CAIXA ECON. FEDERAL':'.104',
        # },

}
ORIGEM_PREFIXO = rf'H:\Arqs'
ORIGEM_SUFIXO = rf'\arquivoretorno'

DESTINO_PREFIXO = rf'D:\Prefeituras'
DESTINO_SUFIXO = rf'\ARRECADA'

DIRETORIO_DO_LOG = rf"D:\Prefeituras\Tratar Retornos"

# PARA TESTES LOCAIS (COMENTAR LINHAS PRA PRODUÇÃO)
# ORIGEM_PREFIXO = rf'C:\temp'
# ORIGEM_SUFIXO = rf''

# DESTINO_PREFIXO = rf'C:\temp\D'
# DESTINO_SUFIXO = rf''

# DIRETORIO_DO_LOG = rf'C:\temp'


def renomear_retorno_generico(sigla, retorno_config):

    diretorio_origem = ORIGEM_PREFIXO+sigla+ORIGEM_SUFIXO
    diretorio_destino = DESTINO_PREFIXO+sigla+DESTINO_SUFIXO
    

    lista_arquivos, log_simples = executar_simples(diretorio_origem)

    log_de_arquivos_com_problema = f'\nMunicípio {sigla}\n' 
    log_de_arquivos_com_problema += log_simples
    
    # Remover da lista as pastas com os originais do DAF607 e copia para a pasta destino
    for item in lista_arquivos:
        
        caminho_item = os.path.join(diretorio_origem, item)
        destino_item = os.path.join(diretorio_destino, item)
        
        if len(item)==6 :
            shutil.copytree(caminho_item, destino_item, dirs_exist_ok=True)
            lista_arquivos.remove(item)
        

    for arquivo in lista_arquivos:
   
        #SE ARQUIVO FOR SIMPLES NACIONAL OU TESOURO NACIONAL, PASSA PRA O ARQUIVO SEGUINTE SEM TENTAR RENOMEAR
            
        if 'MN' in arquivo:
            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{diretorio_origem}\{arquivo}', diretorio_destino)
            continue

        if 'MS' in arquivo:
            # Move o arquivo para o diretório de destino
            shutil.copy2(rf'{diretorio_origem}\{arquivo}', rf'{diretorio_destino}\STN')
            continue

        if 'RCB200' in arquivo:
            # Ignora retornos temporários e passa pra o próximo arquivo 
            continue

        header = ''
        
        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(diretorio_origem, arquivo)
        
        try:
            for nome_do_banco, codigo_banco in retorno_config.items():
                
                if nome_do_banco in header:

                    nome_arquivo += codigo_banco

                    # Renomeia o retorno conforme a data
                    os.rename(rf'{caminho_origem}', rf'{nome_arquivo}')

                    # Move o arquivo para o diretório de destino
                    shutil.copy2(rf'{nome_arquivo}', diretorio_destino)
                

                    continue
                

                elif 'Not Found' in header and "DAF607" not in arquivo:
                    # Grava nome do arquivo e conteúdo parcial do arquivo com problema no arquivo de log
                    log_de_arquivos_com_problema += f"Arquivo corrompido: {arquivo}\nHeader: {header}\n"
                

        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

    return log_de_arquivos_com_problema


if __name__ == '__main__':

    log_de_arquivos_com_problema = ''
    for sigla in LISTA_MUNICIPIOS:

        try:
           
           log_de_arquivos_com_problema += renomear_retorno_generico(sigla, LISTA_MUNICIPIOS[sigla])
        except FileNotFoundError as f:
            print(f"Pasta do município {sigla} não encontrada")
    
    if log_de_arquivos_com_problema:

        with open(rf"{DIRETORIO_DO_LOG}\log_de_arquivos_com_problema.txt", "w+") as criar_arquivo:
            criar_arquivo.write("LOG de arquivo retorno: \n")
            for linha in log_de_arquivos_com_problema:
                criar_arquivo.write(linha)


    # time.sleep(10)