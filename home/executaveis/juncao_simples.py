import os
from datetime import timedelta, datetime

# VERIFICANDO SE JÁ FOI LIDO UM ARQUIVO COM A MESMA DATA PR ADICIONAR NO MESMO MN___.999

def data_existe(data, lista):
    for i in lista:
        if data == i[0]:
            return lista.index(i)


# VERIFICAR SE A DATA DE GERACAO É UM FIM DE SEMANA E PASSAR PRA O DIA ANTERIOR
def verificar_dia_util(data):

    dia_semana = datetime.strptime(data,"%y%m%d")

    # RETORNANDO AO DIA ANTERIOR DA DISPONIBILIZACAO DO ARQUIVO(REGIME DE CAIXA)
    dia_semana += timedelta(days=-1)

    if dia_semana.weekday() == 5:
        dia_semana += timedelta(days=-1)
    elif dia_semana.weekday() == 6:
        dia_semana += timedelta(days=-2)

    return dia_semana.strftime("%y%m%d")


def executar_simples(diretorio):
    lista_arquivos = os.listdir(diretorio)
    novo_arquivo = []
    lista_remessa_serpro = []

    for item in lista_arquivos:
        if 'DAF607' not in item:
            continue
        with open(rf'{diretorio}\{item}', 'r+') as arquivo:

            # SEPARANDO HEADER, DETALHE E TRAILER
            header = arquivo.readline()
    
            # ALERTA PRA ARQUIVO COM ERRO NO HEADER
            if '!DOCTYPE HTML PUBLIC' in header or 'Ocorreu um problema' in header:
                print(f'Arquivo {item} com erro. É recomendável refazer o download.')
                continue

            detalhe = arquivo.readlines()

        trailer = detalhe[-1]
        detalhe.pop()
        valor_total = int(trailer[15:32])
        remessa_serpro = header[37:43]

        # VERIFICANDO DUPLICIDADE DE ARQUIVOS PELO NÚMERO DA REMESSA
        if remessa_serpro in lista_remessa_serpro:
            os.remove(rf'{diretorio}\{item}')
        else:
            # VERIFICANDO SE É DO TESOURO NACIONAL E RENOMEANDO
            if 'DAF607              ' in header:
                data_regime_caixa_tesouro = header[80:86]
                data_tesouro = verificar_dia_util(data_regime_caixa_tesouro)
                try:
                    lista_remessa_serpro.append(remessa_serpro)
                    os.rename(rf'{diretorio}\{item}', rf'{diretorio}\MS{data_tesouro}.991')
                except:
                    os.remove(rf'{diretorio}\{item}')
                continue

            data_regime_caixa_simples = header[80:86]
            data_retorno_simples = verificar_dia_util(data_regime_caixa_simples)
            buscarData = data_existe(data_retorno_simples, novo_arquivo)

            # SE JÁ TEM A DATA EM UMA JUNÇÃO, FAZ A ADIÇÃO NESSE ARQUIVO.
            # SE FOR UMA NOVA DATA, CRIA UM NOVO ARQUIVO MN___.999
            if buscarData is not None:
                for linha_detalhe in detalhe:
                    novo_arquivo[buscarData].insert(2, linha_detalhe)
                novo_arquivo[buscarData][-1] = novo_arquivo[buscarData][-1] + valor_total
            else:
                novo_arquivo.append([data_retorno_simples, header, *detalhe, data_regime_caixa_simples, valor_total])
            lista_remessa_serpro.append(remessa_serpro)

            os.remove(rf'{diretorio}\{item}')

    # MONTANDO ARQUIVOS DO SIMPLES NO DIRETÓRIO
    for linha_detalhe in novo_arquivo:
        with open(rf"{diretorio}\MN" + (linha_detalhe[0]) + ".999", "w+") as criar_arquivo_simples:
            for posicao in range(1, len(linha_detalhe) - 2):
                # ADICIONANDO LINHA AOS ARQUIVOS COM O REGISTRO DO REGIME DE CAIXA
                if posicao > 1 and posicao < (len(linha_detalhe) - 2):
                    # RETIRANDO QUEBRA DE LINHA
                    linha_detalhe[posicao] = linha_detalhe[posicao][0:(len(linha_detalhe[posicao]) - 1)]
                    # ADICIONANDO REGIME DE CAIXA E QUEBRA DE LINHA
                    criar_arquivo_simples.write(
                        f'{str(linha_detalhe[posicao])}' + f'#20{linha_detalhe[len(linha_detalhe) - 2]}\n')
                else:
                    criar_arquivo_simples.write(str(linha_detalhe[posicao]))

            # GERANDO O TRAILER DO ARQUIVO FINAL DE CADA DATA
            registros = str((len(linha_detalhe) - 2)).zfill(6)
            total_pago = str(linha_detalhe[-1]).zfill(17)
            trailer_final = '999999999' + registros + total_pago
            criar_arquivo_simples.write(trailer_final)