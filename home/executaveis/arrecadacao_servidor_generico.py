import os
import shutil
from datetime import datetime

from juncao_simples import executar_simples
from utilitarios import gerar_nome_arquivo_retorno, obter_dia_util_anterior

"""
Orientações gerais antes de gerar o executável:

"""

### Lista dos municípios com atualização "automática" e seus headers com respectivos códigos bancários
LISTA_MUNICIPIOS = {
    # A barra invertida antes da sigla é necessária, pois a string será usada pra integrar o caminho dos diretórios do servidor
    r"\ANG": {
        "IMPOSTOS MUNICIPAIS 001BANCO DO BRASIL  S/A": ".001",
    },
    r"\CAI": {
        "CAICO ARRECADACAO TR001BANCO DO BRASIL": ".001",
        "MUNICIPIO DE CAICO            BANCO DO BRASIL": ".002",
    },
    r"\CEA": {
        "PMCM - ARRECADACAO  001BANCO DO BRASIL  S/A": ".001",
        "PMCEARAMIRIM        104CAIXA ECON. FEDERAL": ".104",
    },
    r"\CEC": {
        "P M C CORA TRIBUTOS 001BANCO DO BRASIL": ".001",
        "MUNICIPIO CERRO CORA104CAIXA ECON": ".104",
    },
    r"\CRE": {
        "PM CAMPO REDONDO RN 104CAIXA ECON. FEDERAL": ".104",
    },
    r"\CRV": {
        "PREF CAIC RIO DO VEN001BANCO DO BRASIL": ".001",
    },
    r"\EQU": {
        "EQUADOR - ARRECADACA001BANCO DO BRASIL": ".001",
    },
    r"\EXT": {
        "PM EXTREMOZ - TRIBUT001BANCO DO BRASIL  S/A": ".001",
        "PM EXTREMOZ         104CAIXA ECON. FEDERAL": ".104",
    },
    r"\GAL": {
        "PMGALINHOS          104CAIXA ECON. FEDERAL": ".104",
        "PREF MUN DE GALINHOS001BANCO DO BRASIL": ".001",
    },
    r"\GAV": {
        "PM S G AVELINO TRIBU001BANCO DO BRASIL": ".001",
        "PMSGA               104CAIXA ECON. FEDERAL": ".104",
    },
    r"\GOH": {
        "00000307963 MUNICIPIO DE GOIANINHA": ".901",
        "PMG-ARREC IMPOSTOS/T001BANCO DO BRASIL": ".001",
        "PM GOIANINHA        104CAIXA ECON. FEDERAL": ".104",
    },
    r"\GON": {
        "PMSGA ARRECADACAO   001BANCO DO BRASIL": ".001",
        "MUNICIPIO DE SAO GONCALO DO AMBANCO DO BRASIL": ".901",
        "PMSGAMARANTERN      104CAIXA ECON. FEDERAL": ".104",
    },
    r"\ITJ": {
        "104CAIXA ECON. FEDERAL": ".104",
    },
    r"\JDS": {
        "3512214  2807793": ".001",
        "MUN JARDIM DO SERIDO001BANCO DO BRASIL  S/A": ".901",  # agz
        "3512214  3178850": ".902",
    },
    r"\LAJ": {
        "PREFEITURA MUNIC DE 001BANCO DO BRASIL  S/A": ".001",
        "PM LAJES            104CAIXA ECON. FEDERAL": ".104",
    },
    r"\LDA": {
        "PM DE LAGOA DANTA   104CAIXA ECON. FEDERAL": ".104",
        "ARRECADACAO LAGOA DA001BANCO DO BRASIL": ".001",
    },
    r"\MAC": {
        "PREF MACAIBA TRIB DI001BANCO DO BRASIL": ".001",
        "MUNICIPIO DE MACAIBA          001BANCO DO BRASIL": ".902",
        "PM MACAIBA          104CAIXA ECON. FEDERAL": ".104",
    },
    r"\MAM": {
        "PMM - Tributos Munic001BANCO DO BRASIL": ".001",
    },
    r"\MON": {
        "P M MONTE ALEGRE IPT001BANCO DO BRASIL": ".001",
    },
    r"\NIS": {
        "PREF MUN NISIA FLORE001BANCO DO BRASIL": ".001",
        "PMDENISIAFLORESTA   104CAIXA": ".104",
        "NISIA FLORESTA 756SICOOB": ".756",
    },
    r"\NCR": {
        "PMNC ARRECADACAO    001BANCO DO BRASIL": ".001",
        "PM DE NOVA CRUZ/RN  104CAIXA ECON. FEDERAL": ".904",
        "PM DE NOVA CRUZ - RN237BANCO BRADESCO": ".237",
    },
    r"\OUB": {
        "PREF MUN DE OURO BRA001BANCO DO BRASIL": ".001",
    },
    r"\PAH": {
        "PM DE PARELHAS      104CAIXA ECON. FEDERAL": ".204",
        "PM PARELHAS - ARRECA001BANCO DO BRASIL": ".904",
    },
    r"\PAR": {
        "2008769113600000000FUNDO MUNICIPAL DE SAUDE DE PAC ECON FEDERAL": ".204",
        "779460100000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL": ".304",
        "ARRECADACAO PM PARNA001BANCO DO BRASIL": ".001",
        "PM PARNAMIRIM       104CAIXA ECON. FEDERAL": ".104",
        "2008798913700000000MUNICIPIO DE PARNAMIRIM       C ECON FEDERAL": ".404",
    },
    r"\PAV": {
        "PM PEDRO AVELINO    104CAIXA ECON. FEDERAL": ".104",
        "ARRECADACAO PM P AVE001BANCO DO BRASIL": ".001",
    },
    r"\PEF": {
        "PASSA E FICA PREFEITURA       C ECON FEDERAL": ".904",
    },
    r"\PEN": {
        "MUN DE PENDENCIAS RN001BANCO DO BRASIL": ".001",
        "PM DE PENDENCIAS    104CAIXA ECON. FEDERAL": ".104",
    },
    r"\PUR": {
        "ARRECADACAO PUREZA  001BANCO DO BRASIL": ".001",
        "PMPUREZA            104CAIXA ECON. FEDERAL": ".104",
    },
    r"\PVE": {
        "MUN. PEDRO VELHO    104CAIXA ECON. FEDERAL": ".104",
        "PEDRO VELHO ARRECADA001BANCO DO BRASIL ": ".001",
    },
    r"\RDF": {
        "PREF MUN RIO DO FOGO001BANCO DO BRASIL": ".001",
        "PMRIODOFOGO         104CAIXA ECON. FEDERAL": ".104",
    },
    r"\SBN": {
        "SAO BENTO DO NORTE PREFEITURA C ECON FEDERAL": ".104",
    },
    r"\SJM": {
        "PREF MUN S J MIPIBU 001BANCO DO BRASIL": ".901",
        "PM SAO JOSE MIPIBU  104CAIXA ECON. FEDERAL": ".104",
    },
    r"\SMG": {
        "P M SAO MIGUEL DO GO001BANCO DO BRASIL  S/A": ".001",
        "PM S M DO GOSTOSO RN104CAIXA ECON. FEDERAL": ".104",
        "MUNICIPIO DE SAO MIGUEL DO GOS001BANCO DO BRASIL": ".002",
    },
    r"\SNN": {
        # 'MUNICIPIO DE SERRA NEGRA DO NOBANCO DO BRASIL': '.001',
        # '272639000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL': '.002',
        "PM S NEGRA DO NORTE 104CAIXA": ".104",
        # '570168000000MUNICIPIO DE SERRA NEGRA DO NO001BANCO DO BRASIL': '.004',
        "SERRA NEGRA NORTE TR001BANCO DO BRASIL  S/A": ".005",
    },
    r"\STM": {
        "ARRECADACAO SAO TOME001BANCO DO BRASIL": ".001",
        "PM DE SAO TOME      104CAIXA ECON. FEDERAL": ".104",
    },
    r"\TDB": {
        "MUNICIPIO DE TIMBAUBA DOS BATI001BANCO DO BRASIL": ".002",
        "PM TIMBAUBA DOS BATI104CAIXA ECON. FEDERAL": ".104",
    },
    # MUNICÍPIOS QUE AINDA DEPENDEM DA CONCLUSÃO DA CONFIGURAÇÃO PARA O DOWNLOAD AUTOMÁTICO
    # '\CUR':{
    #     'PM CURRAIS NOVOS RN 001BANCO DO BRASIL':'.001',
    #     '33251 MUNICIPIO DE CURRAIS NOVOS    BANCO DO BRASIL':'.002',
    #     'PPM CURRAIS NOVOS   104CAIXA ECON. FEDERAL':'.104',
    # },
}
ORIGEM_PREFIXO = r"H:\Arqs"
ORIGEM_SUFIXO = r"\arquivoretorno"

DESTINO_PREFIXO = r"D:\Prefeituras"
DESTINO_SUFIXO = r"\ARRECADA"

DIRETORIO_DO_LOG = r"D:\Prefeituras\Tratar Retornos\log"

# PARA TESTES LOCAIS (COMENTAR LINHAS PRA PRODUÇÃO)
# ORIGEM_PREFIXO = r"C:\temp"
# ORIGEM_SUFIXO = r""

# DESTINO_PREFIXO = r"C:\temp\D"
# DESTINO_SUFIXO = r""

# DIRETORIO_DO_LOG = r"C:\temp\log"


def renomear_retorno_generico(sigla, retorno_config):

    # Armazena a data esperada pra atualização da arrecadação (dia útil anterior) para controle do log
    data_esperada_da_atualizacao = obter_dia_util_anterior()

    # Variável para apurar quais retornos ficaram ausente no movimento diário
    retornos_bancarios_esperados = list(retorno_config.values())
    # Remove exceções dos retornos para alguns municípios

    # Adicionando Simples Nacional como padrão geral
    retornos_bancarios_esperados.append(".999")

    diretorio_origem = ORIGEM_PREFIXO + sigla + ORIGEM_SUFIXO
    diretorio_destino = DESTINO_PREFIXO + sigla + DESTINO_SUFIXO

    lista_arquivos, log_do_simples = executar_simples(diretorio_origem)

    registros_do_arquivo_de_log = f"\n{sigla[1:]}: "
    registros_do_arquivo_de_log += log_do_simples

    # Remover da lista as pastas com os originais do DAF607 e copia para a pasta destino
    for item in lista_arquivos:

        caminho_item = os.path.join(diretorio_origem, item)
        destino_item = os.path.join(diretorio_destino, item)

        if len(item) == 6:
            shutil.copytree(caminho_item, destino_item, dirs_exist_ok=True)
            lista_arquivos.remove(item)

    for arquivo in lista_arquivos:

        # SE ARQUIVO FOR SIMPLES NACIONAL OU TESOURO NACIONAL, PASSA PRA O ARQUIVO SEGUINTE SEM TENTAR RENOMEAR

        if "MN" in arquivo:
            # Move o arquivo para o diretório de destino
            shutil.copy2(rf"{diretorio_origem}\{arquivo}", diretorio_destino)

            data_retorno_simples_nacional = arquivo[2:8]

            if data_retorno_simples_nacional == data_esperada_da_atualizacao:
                # Remove o Simples Nacional da lista de retornos aguardados se for retorno do dia
                retornos_bancarios_esperados.remove(".999")
            continue

        if "MS" in arquivo:
            # Move o arquivo para o diretório de destino
            shutil.copy2(rf"{diretorio_origem}\{arquivo}", rf"{diretorio_destino}\STN")
            continue

        if "RCB200" in arquivo:
            # Ignora retornos temporários e passa pra o próximo arquivo
            continue

        header = ""

        caminho_origem, nome_arquivo, header = gerar_nome_arquivo_retorno(
            diretorio_origem, arquivo
        )

        try:

            for nome_do_banco, codigo_banco in retorno_config.items():

                if nome_do_banco in header:

                    nome_arquivo += codigo_banco

                    # Renomeia o retorno conforme a data
                    os.rename(rf"{caminho_origem}", rf"{nome_arquivo}")

                    # Controle de datas para gestão do arquivo de log
                    data_do_arquivo_retorno = nome_arquivo[-10:-4]

                    if data_do_arquivo_retorno == data_esperada_da_atualizacao:
                        # Remove da lista de retornos aguardados o código do banco encontrado se for do dia da atualização
                        retornos_bancarios_esperados.remove(codigo_banco)

                    # Move o arquivo para o diretório de destino
                    shutil.copy2(rf"{nome_arquivo}", diretorio_destino)
                    continue

                elif "Not Found" in header and "DAF607" not in arquivo:
                    # Grava nome do arquivo e conteúdo parcial do arquivo com problema no arquivo de log
                    registros_do_arquivo_de_log += (
                        f"Arquivo corrompido: {arquivo}\nHeader: {header}\n"
                    )

        except Exception as e:
            print(f"Erro ao tratar o arquivo retorno {arquivo}")
            print(e)

    if retornos_bancarios_esperados:
        # registros_do_arquivo_de_log += "Retornos ausentes: "
        for codigo in retornos_bancarios_esperados:
            registros_do_arquivo_de_log += f"{codigo} "

    return registros_do_arquivo_de_log


def gerar_arquivo_de_log(log_de_arquivos_com_problema):

    # Data e hora atual
    agora = datetime.now()
    data_e_hora = agora.strftime("%y%m%d%H%M%S")

    with open(
        rf"{DIRETORIO_DO_LOG}\log_retorno_{data_e_hora}.txt", "w+"
    ) as criar_arquivo:

        criar_arquivo.write("Arquivo retorno ausente: \n")
        criar_arquivo.writelines(log_de_arquivos_com_problema)

    # print(log_de_arquivos_com_problema)


if __name__ == "__main__":

    registros_de_log = ""

    for sigla in LISTA_MUNICIPIOS:
        try:

            registros_de_log += renomear_retorno_generico(
                sigla, LISTA_MUNICIPIOS[sigla]
            )

        except FileNotFoundError:
            print(f"Pasta do município {sigla} não encontrada")

    gerar_arquivo_de_log(registros_de_log)
