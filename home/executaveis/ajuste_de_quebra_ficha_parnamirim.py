import os
from dados_acesso import DIRETORIO

pasta_municipio = DIRETORIO
arquivo_encontrado = os.listdir(pasta_municipio)
nome_original = arquivo_encontrado[0]

with open(rf'{pasta_municipio}\{arquivo_encontrado[0]}', 'r+') as arquivo_304:

    # Carregando o conteúdo completo do arquivo retorno
    registros = arquivo_304.readlines()

# Renomeando arquivo original 
os.rename(rf'{pasta_municipio}\{arquivo_encontrado[0]}', rf'{pasta_municipio}\old {arquivo_encontrado[0]}')
 
# Obtendo a linha que se repete quando há quebra de cabeçalho
linha_de_quebra_do_arquivo = registros[1]

# Isolando o trecho que se repete
parte_1 = linha_de_quebra_do_arquivo.find(" ")
parte_2 = linha_de_quebra_do_arquivo.find(" ", parte_1+1)
linha_de_quebra_do_arquivo = linha_de_quebra_do_arquivo[parte_1:parte_2+1]

# Verificando linhas em duplicidade e adicionando na lista pra remoção
linhas_pra_remover = []
primeiro_registro = True

for indice, linha in enumerate(registros):

    if linha.find(linha_de_quebra_do_arquivo) > 0:

        if primeiro_registro:
            primeiro_registro = False
        else:
            linhas_pra_remover += [indice-1, indice]
    

# Removendo as linhas (cabeçalho) duplicadas
for linha in linhas_pra_remover[::-1]:
    del registros[linha]


# GERANDO O TRAILER (2 últimas linhas)
total_penultima_linha = str(len(registros) - 2).zfill(6)
penultima_linha = registros[-2][:17] + total_penultima_linha + registros[-2][23:]
registros[-2] = penultima_linha


total_ultima_linha = str(len(registros)).zfill(6)
ultima_linha = registros[-1][:23] + total_ultima_linha + registros[-1][29:]
registros[-1] = ultima_linha

with open(rf"{pasta_municipio}\{nome_original}", "w+") as criar_arquivo_304:
    for linha in registros:
        criar_arquivo_304.write(linha)