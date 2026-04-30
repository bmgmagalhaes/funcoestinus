import os

diretorio = rf"c:\temp"
#ARQUIVO A BASE DE DADOS A SER ANALISADA
#RENOMEAR PARA: total.csv
arquivo_inicial = "total.csv"

#ARQUIVO COM OS DADOS A SEREM COMPARADOS
#RENOMEAR PARA: excluir.csv
arquivo_excluir = "excluir.csv"

lista_arquivos = os.listdir(diretorio)
# DEFINIR POSIÇAO DAS COLUNAS A SEREM COMPARADAS
indice_arquivo_inicial = 1
indice_arquivo_excluir = 0
indice_encontrado = False

##################################################################################
lista_total = open(rf'{diretorio}\{arquivo_inicial}', 'r+')
header_inicial = lista_total.readline()
header_inicial = header_inicial.split(";")
# print("header_tota formatado = ",header_total)
detalhe_inicial = lista_total.readlines()

for posicao, item in enumerate(detalhe_inicial):
    detalhe_inicial[posicao] = item.split(";")
# print("detalhe_inicial = ",detalhe_inicial)
lista_total.close()
##################################################################################
lista_excluir = open(rf'{diretorio}\{arquivo_excluir}', 'r+')
header_excluir = lista_excluir.readline()
header_excluir = header_excluir.split(";")
# print("header_excluir formatado = ",header_excluir)

detalhe_excluir = lista_excluir.readlines()

# for posicao, item in enumerate(detalhe_excluir):
#     detalhe_excluir[posicao] = item.split(";")
# print("detalhe_excluir = ",detalhe_excluir)

lista_excluir.close()
##################################################################################

resultado = open(rf"{diretorio}\resultado.csv", "w+")
header_final = ";".join(header_inicial)
resultado.write(f"{header_final}")


for registro_excluir in detalhe_excluir:

    # print("registro a excluir = ", registro_excluir)
    for registro_incial in detalhe_inicial:
        # print("registro da vez = ", registro_incial)

        # print("Comparando" , {registro_incial[indice_arquivo_inicial]}," = ",{ registro_excluir})
        if registro_incial[indice_arquivo_inicial] in registro_excluir:
            # print("Entrei no IF, removi linha e registro_encontrado = True BREAK. Vai pra fim do for 2")
            # print("vou remover = " , registro_incial)
            # print("vou remover [indice_arquivo_inicial] = " , registro_incial[indice_arquivo_inicial])
            # print("Está em  " , registro_excluir)
            # print("validado? = " , registro_incial[indice_arquivo_inicial] in registro_excluir)
            detalhe_inicial.remove(registro_incial)
            # registro_encontrado = True
            # print("registro_excluir[indice_arquivo_excluir] = " , registro_excluir[indice_arquivo_excluir])
            # indice_encontrado = True
            break


    # print("fim do for 2 e registro_encontrado = ", registro_encontrado)
    # if registro_encontrado:
    #     print(" registro_encontrado agora = false")
    #     registro_encontrado = False
    # else:
    #     print("GRAVEI LINHA NO RESULTADO")


        




# lista_final = [imovel for imovel in detalhe_inicial if imovel[2] not in detalhe_excluir]
# print("lista_final = ",lista_final)
# Saída: [[1, 'a', 100], [3, 'c', 300]]

for linha in detalhe_inicial:
    resultado.write(";".join(linha))

resultado.close()