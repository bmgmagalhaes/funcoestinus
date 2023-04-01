import os

diretorio = rf"c:\temp"
#ARQUIVO COM NOTAS EMITIDAS EM DETERMINADO PERÍODO (RESUMID0)
#RENOMEAR PARA: notas.csv
arquivo_notas_geradas = "notas.csv"

#LISTA DE USUÁRIOS MASTER AUTORIZADOS A EMITIR NOTAS
#RENOMEAR PARA: empresas.csv
arquivo_empresas_autorizadas = "empresas.csv"

lista_arquivos = os.listdir(diretorio)
posicao_inscricao_notas = 2
posicao_inscricao_empresas = 1
emitiu_nota = False

##################################################################################
lista_notas = open(rf'{diretorio}\{arquivo_notas_geradas}', 'r+')
header_notas = lista_notas.readline()
header_notas = header_notas.split(";")
detalhe_notas = lista_notas.readlines()

for posicao, item in enumerate(detalhe_notas):
    detalhe_notas[posicao] = item.split(";")
lista_notas.close()
##################################################################################
lista_empresas = open(rf'{diretorio}\{arquivo_empresas_autorizadas}', 'r+')
header_empresas = lista_empresas.readline()
header_empresas = header_empresas.split(";")
detalhe_empresas = lista_empresas.readlines()

for posicao, item in enumerate(detalhe_empresas):
    detalhe_empresas[posicao] = item.split(";")
lista_empresas.close()
##################################################################################

inscricoes_sem_emissao = open(rf"{diretorio}\inscricoes_sem_emissao.csv", "w+")
inscricoes_sem_emissao.write(f"{header_empresas[posicao_inscricao_empresas]};"
                             f"{header_empresas[0]};"
                             f"{header_empresas[2]};"
                             f"{header_empresas[3]};"
                             f"{header_empresas[6]};"
                             f"\n")

for empresa in detalhe_empresas:
    for notas in detalhe_notas:
        if notas[posicao_inscricao_notas] in empresa[posicao_inscricao_empresas]:
            emitiu_nota = True

    if not emitiu_nota:
        inscricoes_sem_emissao.write(f"{empresa[posicao_inscricao_empresas]};"
                                     f"{empresa[0]};"
                                     f"{empresa[2]};"
                                     f"{empresa[3]};"
                                     f"{empresa[6]};"
                                     f"\n")
    emitiu_nota = False

inscricoes_sem_emissao.close()