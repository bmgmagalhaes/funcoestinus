from datetime import datetime
import os

def unir_agz(diretorio):
    """
    Une retornos do tipo AGZ em um único arquivo, independente da data de pagamento
    """
    lista_arquivos = os.listdir(diretorio)
    valor_total = 0
    pagamento_por_dia = {}
    novo_detalhe = []
    for item in lista_arquivos:

        with open(rf'{diretorio}\{item}', 'r+') as arquivo:

            # SEPARANDO HEADER, DETALHE E TRAILER
            header = arquivo.readline()
            detalhe = arquivo.readlines()
            data_arquivo = detalhe[0][23:29]

        trailer = detalhe[-1]
        detalhe.pop()
        novo_detalhe.extend(detalhe)
        valor_total += int(trailer[16:24])
        for linhas in detalhe:
            if pagamento_por_dia.get(data_arquivo):
                pagamento_por_dia[data_arquivo] += int(linhas[84:93])
            else:
                pagamento_por_dia[data_arquivo] = int(linhas[84:93])

    novo_arquivo = [header]
    novo_arquivo.extend(novo_detalhe)

    # GERANDO O TRAILER DO ARQUIVO FINAL DE CADA DATA
    registros = str((len(novo_detalhe) + 2)).zfill(6)
    total_pago = str(valor_total).zfill(17)
    trailer_final = 'Z' + registros + total_pago
    novo_arquivo.append(trailer_final)

    # MONTANDO ARQUIVO AGZ NO DIRETÓRIO
    with open(rf"{diretorio}\novo_agz.ret", "w+") as criar_arquivo:
        for posicao in novo_arquivo:
            criar_arquivo.write(posicao)
    
    # MONTANDO RELATÓRIO EM DICIONÁRIO COM PAGAMENTOS TOTAIS POR DIA
    with open(rf"{diretorio}\pagamentos_detalhados.csv", "w+") as criar_arquivo:

        criar_arquivo.write(f'DATA_PAGAMENTO;VALOR\n')
        
        for dia, valor in pagamento_por_dia.items():
            
            dia = datetime.strptime(dia, '%d%m%y')
            dia = datetime.strftime(dia, '%y/%m/%d')    
            criar_arquivo.write(f'{dia};{int(valor)/100}\n')

if __name__ == '__main__':
    unir_agz(rf"c:\temp")
