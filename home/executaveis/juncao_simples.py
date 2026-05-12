import os
from datetime import timedelta, datetime
# from time import sleep
import shutil

def salvar_original(diretorio, item, data):
    # Cria a pasta com o nome da data, se não existir
    pasta_data = os.path.join(diretorio, data)
    os.makedirs(pasta_data, exist_ok=True)

    # Move o arquivo original para dentro dessa pasta
    origem = os.path.join(diretorio, item)
    destino = os.path.join(pasta_data, item)
    shutil.move(origem, destino)

# VERIFICANDO SE JÁ FOI LIDO UM ARQUIVO COM A MESMA DATA PR ADICIONAR NO MESMO MN___.999
def data_existe(data, lista):
    for i in lista:
        if data == i[0]:
            return lista.index(i)


# VERIFICAR SE A DATA DE GERACAO É UM FIM DE SEMANA E PASSAR PRA O DIA ANTERIOR
def verificar_dia_util(data):
    """
    Retorna o dia útil anterior à data do regime de caixa. São considerados sábado, domingo e feriados nacionais.
    Feriados municipais não são considerados, pois podem ter pagamentos do Simples Nacional.
    """

    # LISTA COM FERIADOS NACIONAIS 2025
    feriados = [
        '250101','250303','250304','250418','250421','250501','250619','250907','251012','251102','251115','251120','251225',
        '260101','260216','260217','260403','260421','260501','260604','260907','261012','261102','261115','261120','261225',
        '270101','270208','270209','270326','270421','270501','270527','270907','271012','271102','271115','271120','271225',
        '280101','280228','280229','280414','280421','280501','280615','280907','281012','281102','281115','281120','281225',
        '290101','290212','290213','290330','290421','290501','290607','290907','291012','291102','291115','291120','291225',
        '300101','300304','300305','300419','300421','300501','300620','300907','301012','301102','301115','301120','301225']     


    dia_semana = datetime.strptime(data,"%y%m%d")
    
    # RETORNANDO AO DIA ANTERIOR DA DISPONIBILIZACAO DO REGIME DE CAIXA
    dia_semana += timedelta(days=-1)
    
    while (True):
        #Se for sábado
        if dia_semana.weekday() == 5:
            dia_semana += timedelta(days=-1)
        #Senão, se for 
        elif dia_semana.weekday() == 6:
            dia_semana += timedelta(days=-2)

        #Se estiver entre a lista de feriados nacionais
        if dia_semana.strftime('%y%m%d') in feriados:
            dia_semana += timedelta(days=-1)
        else:
            break

    return dia_semana.strftime("%y%m%d")


def executar_simples(diretorio):
    """
    Verifica se tem DAF607 e executa Junção do Simples e Tesouro Nacional
    Retorna lista de arquivos atualizadas após remoção dos DAFs
    """

    log_de_arquivos_com_problema = ''

    # print("Diretório (executar_simples)= ", diretorio)

    lista_arquivos = os.listdir(diretorio)

    # print("lista_arquivos (executar_simples)= ", lista_arquivos)
    novo_arquivo = []
    lista_remessa_serpro = []

    for item in lista_arquivos:
        # print('Lendo arquivo', item)
        if 'DAF607' not in item:
            # print("Não é DAF")
            continue
        with open(rf'{diretorio}\{item}', 'r+') as arquivo:
            # print('Trando Simples no arquivo', item)

            # SEPARANDO HEADER, DETALHE E TRAILER
            header = arquivo.readline()
    
            # ALERTA PRA ARQUIVO COM ERRO NO HEADER
            if 'DAF607' not in header or 'Ocorreu um problema' in header:
                log_de_arquivos_com_problema += f'{item} com erro. É recomendável refazer o download. | HEADER: {header}\n'
                # sleep(5)
                continue
            
            # if '!DOCTYPE HTML PUBLIC' in header or 'Ocorreu um problema' in header:
            #     print(f'Arquivo {item} com erro. É recomendável refazer o download.')
            #     print(f'header do arquivo = {header}')
            #     sleep(5)
            #     continue
            # if 'Not found' in header or 'Ocorreu um problema' in header:
            #     print(f'Arquivo {item} com erro. É recomendável refazer o download.')
            #     print(f'header do arquivo = {header}')
            #     sleep(5)
            #     continue

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
                    salvar_original(diretorio, item, data_tesouro)
                    # os.remove(rf'{diretorio}\{item}')
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
            salvar_original(diretorio, item, data_retorno_simples)
            # os.remove(rf'{diretorio}\{item}')

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
    lista_arquivos = os.listdir(diretorio)
    # print("lista_arquivos FINAL EXEC SN = ", lista_arquivos)
    return lista_arquivos, log_de_arquivos_com_problema