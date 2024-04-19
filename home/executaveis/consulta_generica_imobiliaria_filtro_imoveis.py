import csv
import os

diretorio = rf"c:\temp"
encontrar_arquivo = os.listdir(diretorio)
lista_sequenciais = [
'10248390',
'10250115',
]

with open(rf'{diretorio}\{encontrar_arquivo[0]}', 'r+') as consulta_original:
    
    dados = list(csv.reader(consulta_original, delimiter=';'))
    header = dados[0]
    detalhe = dados[1:]

with open(rf"{diretorio}\consulta_generica_filtrada.csv", "w+") as consulta_filtrada:
    
    # ESCREVENNDO HEADER
    for item in header:
        consulta_filtrada.write(f"{item};")
    consulta_filtrada.write(f"\n")

    # REFORMULANDO DETALHES (filtrando os sequenciais dentro da lista)

    for imovel in detalhe:
        
        # CONFERE SE O SEQUENIAL DO IMÓVEL ESTÁ NA LISTA INFORMADA
        if imovel[1] in lista_sequenciais:

            for dados_do_imovel in imovel:
                    
                    consulta_filtrada.write(f"{dados_do_imovel};")

            consulta_filtrada.write(f"\n")
