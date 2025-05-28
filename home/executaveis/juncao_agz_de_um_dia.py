import os

def unir_agz_de_um_dia(diretorio):
    """
    Une em um único arquivo retorno no modelo AGZ quando há geração de arquivo complementar com novos pagamentos 
    enviado pelos bancos, verificando se há pagamento em duplicidade
    """

    # LISTANDO ARQUIVOS EXISTENTE NO DIRETÓRIO PADRÃO
    lista_arquivos = os.listdir(diretorio)

    retornos = {}

    # CONJUNTO DE DATAS EXSTENTE EM TODOS OS ARQUIVOS DA PASTA
    datas_de_retornos = set([])

    for item in lista_arquivos:

        with open(rf'{diretorio}\{item}', 'r+') as arquivo:

            # SEPARANDO HEADER, DETALHE E TRAILER
            header = arquivo.readline()
            detalhe = arquivo.readlines()
        
        data_arquivo = detalhe[0][23:29]
        valor = int(detalhe[-1][16:24])
        # REMOVE O TRAILER (QUE SERÁ RECALCULADO NO FINAL)
        detalhe.pop()

        # SE É O UM NOVO HEADER, ADICIONA OS VALORES NO DICIONÁRIO DE RETORNOS.
        # SE JÁ EXISTE O MESMO HEADER, O ARQUIVO É DESPREZADO
        if not retornos.get(header):
        
            retornos[header]={
                'data': data_arquivo,
                'detalhe': detalhe,
                'total': valor,
            }
            datas_de_retornos.add(data_arquivo)
            
        else:
            print(f"Arquivo duplicado e desprezado: {item}")
        

    # Inicializando o dicionário base pra geração dos arquivos finais
    base_final = {}

    for data in datas_de_retornos:

        #CONFIGURANDO O NOME DO RETORNO PRA USAR COMO CHAVE NA BASE FINAL
        nome_arquivo_retorno = 'MR'+data+'.ret'
        base_final[nome_arquivo_retorno] = {}

        #LAÇO PRA PERCORRER CADA RETORNO DIFERENTE, VERIFICANDO A QUAL DATA PERTENCE
        for cabecalho, conteudo in retornos.items():

            if data == conteudo.get('data'):
                
                # JÁ HAVENDO INFORMAÇÃO NESSA DATA, APENAS SOMA O VALOR AO TOTAL E ADICIONA OS REGISTROS DE PAGAMENTO
                if base_final[nome_arquivo_retorno].get('header'):
                    
                    base_final[nome_arquivo_retorno]['total'] += conteudo.get('total')
                    base_final[nome_arquivo_retorno]['detalhe'] += conteudo.get('detalhe')

                # JÁ HAVENDO INFORMAÇÃO NESSA DATA, CRIA UM NOVO HEADER
                else:
                    base_final[nome_arquivo_retorno] = {
                        'header' : cabecalho,
                        'detalhe' : conteudo.get('detalhe'),
                        'total' : conteudo.get('total'),
                    }


    # LAÇO PRA CRIAR TODOS OS RETORNOS COM OS DADOS DA BASE FINAL POR DATA
    for nome, conteudo in base_final.items():

        novo_arquivo = {}
        novo_arquivo = [conteudo['header']]
        novo_arquivo.extend(conteudo['detalhe'])
        
        # GERANDO O TRAILER DO ARQUIVO FINAL DE CADA DATA
        registros = str((len(conteudo['detalhe']) + 2)).zfill(6)
        total_pago = str(conteudo['total']).zfill(17)
        trailer_final = 'Z' + registros + total_pago
        novo_arquivo.append(trailer_final)

        # MONTANDO ARQUIVO AGZ NO DIRETÓRIO
        with open(rf"{diretorio}\{nome}", "w+") as criar_arquivo:
            for posicao in novo_arquivo:
                criar_arquivo.write(posicao)
    

if __name__ == '__main__':
    unir_agz_de_um_dia(rf"c:\temp")
