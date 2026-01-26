from datetime import datetime
import os

def unir_agz(diretorio):
    """
    Une retornos do tipo AGZ em um único arquivo, independente da data de pagamento
    """
    lista_arquivos = os.listdir(diretorio)
    valor_total = 0
    pagamento_por_dia = {}
    pagamento_por_dia_regime_de_caixa = {}
    novo_detalhe = []
    for item in lista_arquivos:

        with open(rf'{diretorio}\{item}', 'r+') as arquivo:

            # SEPARANDO HEADER, DETALHE E TRAILER
            header = arquivo.readline()
            detalhe = arquivo.readlines()
            data_competencia = detalhe[0][23:29]

        trailer = detalhe[-1]
        detalhe.pop()
        novo_detalhe.extend(detalhe)
        valor_total += int(trailer[16:24])
        for linhas in detalhe:
            
            valor_detalhe = linhas[84:93]
            data_regime_de_caixa = linhas[31:37]
            
            if pagamento_por_dia.get(data_competencia):
                pagamento_por_dia[data_competencia] += int(valor_detalhe)
            else:
                pagamento_por_dia[data_competencia] = int(valor_detalhe)


            if pagamento_por_dia_regime_de_caixa.get(data_regime_de_caixa):
                pagamento_por_dia_regime_de_caixa[data_regime_de_caixa] += int(valor_detalhe)
            else:
                pagamento_por_dia_regime_de_caixa[data_regime_de_caixa] = int(valor_detalhe)

        
    
            

    novo_arquivo = [header]
    novo_arquivo.extend(novo_detalhe)

    # GERANDO O TRAILER DO ARQUIVO FINAL DE CADA DATA
    registros = str((len(novo_detalhe) + 2)).zfill(6)
    total_pago = str(valor_total).zfill(17)
    trailer_final = 'Z' + registros + total_pago
    novo_arquivo.append(trailer_final)

    print("GERANDO NOVO AGZ")
    # MONTANDO ARQUIVO AGZ NO DIRETÓRIO
    with open(rf"{diretorio}\novo_agz.ret", "w+") as criar_arquivo:
        for posicao in novo_arquivo:
            criar_arquivo.write(posicao)
    
    print("AGZ GERADO - GERAR REL COMP")
    # MONTANDO RELATÓRIO EM DICIONÁRIO COM PAGAMENTOS TOTAIS POR DIA
    with open(rf"{diretorio}\pagamentos_por_competencia.csv", "w+") as criar_arquivo:

        criar_arquivo.write(f'DATA_PAGAMENTO;VALOR\n')
        
        for dia, valor in pagamento_por_dia.items():
            
            dia = datetime.strptime(dia, '%d%m%y')
            dia = datetime.strftime(dia, '%y/%m/%d')  

            criar_arquivo.write(f'{dia};{int(valor)/100}\n')

    print(" REL COMP GERADO - GERAR RG")

    # MONTANDO RELATÓRIO EM DICIONÁRIO COM PAGAMENTOS TOTAIS POR DIA (REGIME DE CAIXA)
    with open(rf"{diretorio}\pagamentos_por_regime_de_caixa.csv", "w+") as criar_arquivo:

        criar_arquivo.write(f'DATA_REGIME_DE_CAIXA;VALOR\n')
        
        for dia, valor in pagamento_por_dia_regime_de_caixa.items():
            
            dia = datetime.strptime(dia, '%d%m%y')
            dia = datetime.strftime(dia, '%y/%m/%d')  

            criar_arquivo.write(f'{dia};{int(valor)/100}\n')

if __name__ == '__main__':
    unir_agz(rf"c:\temp")
